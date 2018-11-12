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

    def parse_p0f(self, line1, line2, line3):
        # parse the lines and hold the data
        self.__parseline1(line1)
        self.__parseline2(line2)
        if line3 is not None:
            sys.stderr.write("IP with host change found: {}\n".format(self.var_dict["client"]))
            self.__parseline2(line3)
        self.holder_ip = self.var_dict["client"]

    def parse_asn(self, line_arr):
        self.var_dict["asn"] = line_arr[0]
        self.var_dict["client"] = line_arr[1]
        name = line_arr[2].split(" - ")
        self.var_dict["shortname"] = name[0]
        if name[0] != "NA":
            idx = 1
            # if we are given a very small result we may not have split on " - "
            if len(name) == 1:
                idx = 0
            lst = name[idx].rsplit(',', 1)
            self.var_dict["longname"] = lst[0]
            if len(lst) == 2:
                self.var_dict["country"] = lst[1]

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

    def update(self,new_holder):
        for key in new_holder.var_dict.keys():
            # if this key doesnt exist in our current holder or it's value is of NoneType
            if key not in self.var_dict.keys() or self.var_dict[key] is None:
                self.var_dict[key] = new_holder.var_dict[key]