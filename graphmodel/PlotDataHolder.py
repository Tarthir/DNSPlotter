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

    # This method updates a PlotDataHolder object
    # Given another PlotDataHolder object you can update the fields of a current Holder with the one passed in
    def update(self, new_holder):
        for key in new_holder.var_dict.keys():
            # if this key doesnt exist in our current holder or it's value is of NoneType
            if key not in self.var_dict.keys() or self.var_dict[key] is None:
                self.var_dict[key] = new_holder.var_dict[key]
