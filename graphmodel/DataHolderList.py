import sys


class DataHolderList(object):
    def __init__(self):
        self.ip_to_holder = {}
        self.holder_list = []
        self.all_possible_keys = set()

    # TODO this all may not be needed if we do what ASNreader is doing in  and grabbing the old holder to update it
    def append(self, holder):

        # See if ip address is already been found, if so update the already existing holder
        if holder.var_dict["client"] in self.ip_to_holder.keys():
            try:
                old_holder = self.ip_to_holder[holder.var_dict["client"]]
                # old_holder.ports_found_on.append(holder.var_dict["clientport"])
                # Don't bother with duplicates
                if old_holder.var_dict == holder.var_dict:
                    return
                # update keys of old holder with data from new holder
                old_holder.update(holder)
                #self.update_all_keys(old_holder.var_dict, holder.var_dict)
                holder = old_holder

            except KeyError as err:
                sys.stderr.write('KeyError in DataHolderList: %s\n' % str(err))
                return
        else:
            # this ip and its associated data has not been found before
            self.ip_to_holder[holder.var_dict["client"]] = holder
            self.holder_list.append(holder)
        self.all_possible_keys.update((list(holder.var_dict.keys())))

    # This method takes the data held in DataHolderList and creates dicts
    # These dicts contain the keys and values associated with a given set of data.
    # For example passing in "country": keys are the country codes, values the number of times they appear in the data
    # params: key - the key stating what data you want to get
    # return: dictionary
    def get_value_dict(self, key):
        my_dict = {}
        for holder in self.holder_list:
            try:
                val = holder.var_dict[key]
                if val not in my_dict:
                    my_dict[val] = 1
                else:
                    my_dict[val] += 1
            # this key was never found for this IP, just make it None
            except KeyError:
                holder.var_dict[key] = None
        return my_dict

    def get_var_dict_value(self, ip, key):
        return self.ip_to_holder[ip].var_dict[key]
