#############################################################################################################
#############################################################################################################
# ################################## METHODS FOR GETTING VARIABLES FROM CLASSES #############################

# returns a list of just the variable that var_str equals
def get_var_of_one_type(var_str=None, data_holder=None):
    return [a for a in dir(data_holder) if not a.startswith('__') and not callable(getattr(data_holder, a))
            and a == var_str]

##############################################################################################################
##############################################################################################################
# ################################## METHODS FOR THE MAKING OF VALUE DICTIONARIES ############################


# Makes a dictionary that looks like this:
# {value -> {variable -> value_of_variable}}
# This set of dictionaries is then added as a value to variable_dict in DataReader.py
# So it ends up looking like {attr - > {value_of_attr -> {variable -> value_of_variable}}}
def make_dict_of_one_type(attribute_dict, variables, data_holders, key):
    for holder in data_holders:
        value = getattr(holder, key)
        # TODO handle repeat values, list of dicts perhaps?
        if value not in attribute_dict:
            attribute_dict[value] = {}
            # for each variable in the DataHolder class put its type as key and value as the value
            for v in variables:
                if v != key:
                    (attribute_dict[value])[v] = getattr(holder, v)


