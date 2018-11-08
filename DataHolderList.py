import sys
class DataHolderList(object):
    def __init__(self):
        self.ip_to_holder = {}
        self.holder_list = []
        self.all_possible_keys = set()

    def append(self, holder):
        self.holder_list.append(holder)
        if holder.var_dict["client"] in self.ip_to_holder.keys():
            try:
                holder.ports_found_on.append(holder.var_dict["clientport"])
            except KeyError as err:
                sys.stderr.write('KeyError in DataHolderList: %s\n' % str(err))
        else:
            self.ip_to_holder[holder.var_dict["client"]] = holder
        self.all_possible_keys.update((list(holder.var_dict.keys())))
