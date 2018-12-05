#############################################################################################################
#############################################################################################################
# ################################## METHODS FOR GETTING VARIABLES FROM CLASSES #############################

# returns a list of just the variable that var_str equals
def get_var_of_one_type(var_str=None, data_holder=None):
    return [var_str]

##############################################################################################################
##############################################################################################################
# ################################## METHODS FOR THE MAKING OF VALUE DICTIONARIES ############################


# Makes a dictionary that looks like this:
# {value -> {variable -> value_of_variable}}
# This set of dictionaries is then added as a value to variable_dict in DataReader.py
# So it ends up looking like {attr - > {value_of_attr -> {variable -> value_of_variable}}}
def make_dict_of_one_type(attribute_dict, variables, data_holders, key):
    for holder in data_holders:
        value = holder.var_dict[key]# getattr(holder, key)
        # prepare a dict if value has not been seen before now
        if value not in attribute_dict:
            attribute_dict[value] = {}
        # for each variable in the DataHolder class put its type as key and value as the value
        for v in variables:
            # do all but the main key
            if v != key:
                # If this attribute isnt found, add it and make it None
                if v not in holder.var_dict.keys():
                    (attribute_dict[value])[v] = None
                else:
                    (attribute_dict[value])[v] = holder.var_dict[v]


