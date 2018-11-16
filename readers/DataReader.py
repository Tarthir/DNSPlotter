class DataReader(object):

    def __init__(self):
        # The Variables of those DataHolder Classes
        self.__vars = None
        self.__data_holders = None

    def set_vars(self, var_list):
        self.__vars = var_list

    def set_holders(self, data_holders):
        self.__data_holders = data_holders

    # Goes through every PlotDataHolder Object and adds every value for a given attribute
    # to a dictionary and adds 1 to the that key's value. So the os attribute may contribute zero or more entries
    # into the dictionary depending on what OSs were detected by p0f and held in these PlotDataHolder objects
    def __add_up_attr(self, attr, attribute_dict, data_holders):
        # For each attribute, add 1 to its value
        for holder in data_holders:
            # make the value the key
            if attr not in holder.var_dict.keys():
                attribute_dict[attr] = 0
            else:
                key = holder.var_dict[attr]# getattr(holder, attr)
                if key not in attribute_dict:
                    attribute_dict[key] = 1.0
                else:
                    # add value of attribute into the dictionary
                    attribute_dict[key] += 1.0

    # This is the default way to get variables from DataHolder, it grabs them all
    # Key is None in this case as we are going to get all the variables in this method
    def __get_variables(key, data_holder):
        return list(data_holder.all_possible_keys)

    # Returns a dictionary of dictionaries which holds every piece of data in PlotDataHolder objects as well as
    # how many times each piece of data was found. Also returns the number of IPs which are in our data
    # Optional parameters determine what variables are used for the variable dict and
    # how the dictionary is constructed
    def add_up_all_attrs(self, get_vars=__get_variables, make_vals=__add_up_attr, key=None):
        # This dictionary will hold a value for every variable attribute in the PlotDataHolder class
        # gets only the variables from the given DataHolder class
        variables = get_vars(key, self.__data_holders)
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
                make_vals(attribute_dict, self.__data_holders.all_possible_keys, self.__data_holders.holder_list, key)
            else:
                make_vals(self, attribute, attribute_dict, self.__data_holders.holder_list)
            # if the dictionary we passed into make_values came back with keys and values in it
            if attribute_dict:
                # the variable name
                # noinspection PyTypeChecker
                variable_dict[attribute] = attribute_dict
        return variable_dict