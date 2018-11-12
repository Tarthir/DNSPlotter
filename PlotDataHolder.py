import re
import sys


# This class is responsible for parsing and holding the data for one "unit" of a given data type,
#  whether that be p0f/asn/etc
class PlotDataHolder(object):
    # These are all strings which correspond with data that p0f returns

    def __init__(self):
        # THe dictionary holding all the data
        self.var_dict = {}
        # The IP address associated with this data
        self.holder_ip = None
        # The number of times this IP has been found between all data sets
       # self.ports_found_on = []
        self.SIZE_OF_COUNTRY_CODES = 2

    def parse_p0f(self, line1, line2, line3):
        # parse the lines and hold the data
        self.__parseline1(line1)
        self.__parseline2(line2)
        if line3 is not None:
            sys.stderr.write("IP with host change found: {}\n".format(self.var_dict["client"]))
            self.__parseline2(line3)
        self.holder_ip = self.var_dict["client"]

    # This method parses ASN lines
    # Basically these lines are laid out thusly: ASN | IP | SHORT_NAME - LONGNAME, COUNTRY CODE
    # However there are exceptions which complicate the logic
    # line_arr will usually look like this: [ASN,IP,REST] with REST = 'SHORT_NAME - LONGNAME, COUNTRY CODE'
    def parse_asn(self, line_arr):
        self.var_dict["asn"] = line_arr[0]
        self.var_dict["client"] = line_arr[1]

        # Will split: MIT-GATEWAYS - Massachusetts Institute of Technology, US
        # to: [MIT-GATEWAYS, Massachusetts Institute of Technology, US ]
        # and GNW-ASN39211, EE
        # to: [GNW-ASN39211, EE]
        name = line_arr[2].split(" - ", 1) if " - " in line_arr[2] else line_arr[2].split(", ", 1)
        # This first part will be the 'short name'
        self.var_dict["shortname"] = name[0]
        if name[0] != "NA":
            idx = 1
            # if we are given a very small result we may not have a " - " to split on
            if len(name) == 1:
                idx = 0
            # split the name array into longname and country attributes
            longname_country_arr = name[idx].rsplit(', ', 1)
            if len(longname_country_arr) == 1:
                self.__check_small_len(longname_country_arr,name)
            else:
                self.var_dict["longname"] = longname_country_arr[0].strip()
                self.var_dict["country"] = longname_country_arr[1].strip()

    # Helper function which deals with the complicated logic of parsing asn lines
    # In this function what comes in is longname_country_arr of length 1
    # It may contain the country code, if it does we grab it
    # If it does not then we see if it was parsed out in an earlier step from 'name'
    def __check_small_len(self, longname_country_arr, name):
        self.var_dict["longname"] = name[0]
        # If there is no country code that was parsed, return
        if len(longname_country_arr[0].strip()) > self.SIZE_OF_COUNTRY_CODES:
            # If 'name' has the country code
            if len(name) == 3:
                self.var_dict['country'] = name[2]
                return
            # If there is no country code given to us
            self.var_dict["country"] = None
            return
        self.var_dict["country"] = longname_country_arr[0].strip()

    def __parseline1(self, line1):
        try:
            self.var_dict["mod"] = re.search(r'mod=([^|]+)', line1).group(1)
            ip = (re.search("cli=([^|]+)", line1, re.DOTALL).group(1)).split("/")
            self.var_dict["client"] = ip[0]
            #self.ports_found_on.append(ip[1])
            self.var_dict["srv"] = re.search("srv=([^|]+)", line1, re.DOTALL).group(1)
            self.var_dict["subj"] = re.search("subj=([^|]+)", line1, re.DOTALL).group(1)
            self.var_dict["os"] = re.search("os=([^|]+)", line1, re.DOTALL).group(1)
            self.var_dict["dist"] = re.search("dist=([^|]+)", line1, re.DOTALL).group(1)
            self.var_dict["params"] = re.search("params=([^|]+)", line1, re.DOTALL).group(1)
            self.var_dict["raw_sig"] = re.search("raw_sig=([^|]+)", line1, re.DOTALL).group(1).rstrip()
        except AttributeError as err:
            sys.stderr.write('ERROR: %sn' % str(err))

    def __parseline2(self, line2):
        try:
            if re.search(r'mod=([^|]+)', line2).group(1) != "host change":
                self.var_dict["link"] = re.search("link=([^|]+)", line2, re.DOTALL).group(1)
                self.var_dict["raw_mtu"] = re.search("raw_mtu=([^|]+)", line2, re.DOTALL).group(1).rstrip()
            else:
                self.var_dict["reason"] = re.search("reason=([^|]+)", line2, re.DOTALL).group(1)
        except AttributeError as err:
            sys.stderr.write('ERROR: %sn' % str(err))

    # This method updates a PlotDataHolder object
    # Given another PlotDataHolder object you can update the fields of a current Holder with the one passed in
    def update(self, new_holder):
        for key in new_holder.var_dict.keys():
            # if this key doesnt exist in our current holder or it's value is of NoneType
            if key not in self.var_dict.keys() or self.var_dict[key] is None:
                self.var_dict[key] = new_holder.var_dict[key]