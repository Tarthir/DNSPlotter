import sys
class DataHolderList(object):
    def __init__(self):
        self.ip_to_holder = {}
        self.holder_list = []
        self.all_possible_keys = set()

    def append(self, holder):

        # See if ip address is already been found, if so add new ports it was found on
        # also update the already existing holder
        if holder.var_dict["client"] in self.ip_to_holder.keys():
            try:
                old_holder = self.ip_to_holder[holder.var_dict["client"]]
                # old_holder.ports_found_on.append(holder.var_dict["clientport"])
                old_holder.update(holder)
                holder = old_holder

            except KeyError as err:
                sys.stderr.write('KeyError in DataHolderList: %s\n' % str(err))
                return
        else:
            # this ip and its associated data has not been found before
            self.ip_to_holder[holder.var_dict["client"]] = holder
            self.holder_list.append(holder)
        self.all_possible_keys.update((list(holder.var_dict.keys())))
