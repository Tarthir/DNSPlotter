import PlotDataHolder as Holder
import re


class DataReader(object):

    def __init__(self):
        self.data_holders = []

    def check_host_change(self, line):
        return re.search(r'mod=([^|]+)', line).group(1) == "host change"

    def read_p0f_data(self, filename):  # Reads the p0f data and creates P0fDataHolder from the data
        # Read two lines at a time from p0f as each IP has two lines of data

        fd = open(filename, "r")
        while True:
            line1 = fd.readline()
            line2 = fd.readline()
            line3 = None
            if not line1 or not line2:
                break  # EOF
            if self.check_host_change(line2):
                line3 = fd.readline()
            self.data_holders.append(Holder.PlotDataHolder(line1, line2, line3))

    def read_asn_data(self):
        pass

    # Goes through every PlotDataHolder Object and adds every value for a given attribute
    # to a dictionary and adds 1 to the that key's value. So the os attribute may contribute zero or more entries
    # into the dictionary depending on what OSs were detected by p0f and held in these PlotDataHolder objects
    def add_up_attr(self, attr, attribute_dict):
        for item in self.data_holders:
            # add value of attribute into the dictionary
            attribute_dict[getattr(item, attr)] += 1.0

    # Returns a dictionary of dictionaries which holds every piece of data in PlotDataHolder
    # and how many times each piece of data was found
    # Also returns the number of IPs which are in our data set
    def add_up_all_attrs(self):
        # This dictionary will hold a value for every variable attribute in the PlotDataHolder class
        variable_dict = {}
        for data_holder in self.data_holders:
            # gets only the variables from the PlotDataHolder class
            variables = [a for a in dir(data_holder) if not a.startswith('__') and not callable(getattr(data_holder, a))]
            # add the variable names to a dictionary
            if not variable_dict:
                variable_dict = dict.fromkeys(variables, None)
            # go through each variable
            # each value in the variables will become its own key whose value will be incremented each time it is found
            for attribute in variables:
                attribute_dict = {}
                self.add_up_attr(attribute, attribute_dict)
                # the variable name
                variable_dict[attribute] = attribute_dict
        return variable_dict, len(self.data_holders)
