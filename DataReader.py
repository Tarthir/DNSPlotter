import PlotDataHolder as Holder
import re


class DataReader(object):

    def __init__(self):
        # The List of DataHolder classes we will be pulling data from
        self.__data_holders = []
        # The Variables of those DataHolder Classes
        self.__vars = None

    def set_holders(self, holders):
        self.__data_holders = holders

    def set_vars(self, var_list):
        self.__vars = var_list

    @staticmethod
    def __check_host_change(line):
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
            if self.__check_host_change(line2):
                line3 = fd.readline()
            self.__data_holders.append(Holder.PlotDataHolder(line1, line2, line3))

    def read_asn_data(self):
        pass

    # Goes through every PlotDataHolder Object and adds every value for a given attribute
    # to a dictionary and adds 1 to the that key's value. So the os attribute may contribute zero or more entries
    # into the dictionary depending on what OSs were detected by p0f and held in these PlotDataHolder objects
    def __add_up_attr(self, attr, attribute_dict, data_holders):
        # For each attribute, add 1 to its value
        for holder in data_holders:
            # make the value the key
            key = getattr(holder, attr)
            if key not in attribute_dict:
                attribute_dict[key] = 1.0
            else:
                # add value of attribute into the dictionary
                attribute_dict[key] += 1.0

    # Get the variable names in the DataHolder class passed in
    # Key is None in this case as we are going to get all the variables in this method
    def __get_variables(key, data_holder):
        return [a for a in dir(data_holder) if not a.startswith('__') and not callable(getattr(data_holder, a))]

    # Returns a dictionary of dictionaries which holds every piece of data in PlotDataHolder
    # and how many times each piece of data was found
    # Also returns the number of IPs which are in our data
    # Optional parameters determine what variables are used for the variable dict and
    # how the dictionary is constructed
    def add_up_all_attrs(self, get_vars=__get_variables, make_vals=__add_up_attr, key=None):
        # This dictionary will hold a value for every variable attribute in the PlotDataHolder class
        # gets only the variables from the given DataHolder class
        variables = get_vars(key, self.__data_holders[0])
        self.set_vars(variables)

        # add the variable names to a dictionary
        variable_dict = dict.fromkeys(self.__vars, None)
        # go through each variable
        # each value in the variables will become its own key whose value will be incremented each time it is found
        for attribute in self.__vars:
            attribute_dict = {}

            if len(variable_dict) == 1:
                # If you are passing in only one variable I assume you want all the other DataHolder Vars as
                # keys in attribute_dict and value of variable_dict
                make_vals(attribute_dict, self.__get_variables(self.__data_holders[0]), self.__data_holders, key)
            else:
                make_vals(self, attribute, attribute_dict, self.__data_holders)
            # if the dictionary we passed into make_values came back with keys and values in it
            if attribute_dict:
                # the variable name
                # noinspection PyTypeChecker
                variable_dict[attribute] = attribute_dict
        return variable_dict, len(self.__data_holders)
