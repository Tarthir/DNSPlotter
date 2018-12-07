import states.ReaderState as Reader
from model import PlotDataHolder as Holder


class IpvReader(Reader.ReaderState):

    # Read through the ipv data files. See who responded to ipv4 or ipv6 on mult_ipv4.py and mult_ipv6.py
    def read(self, filename, data_holders):
        fd = open(filename, "r")
        for line in fd:
            holder = Holder.PlotDataHolder()
            arr = line.split(" | ")
            holder.var_dict["client"] = arr[0].strip()
            holder.var_dict["respondedIpv4"] = False
            holder.var_dict["respondedIpv6"] = False
            # One of two files come in, one with ipv4 responses and the other ipv6
            if "ipv4" in filename:
                holder.var_dict["respondedIpv4"] = True
            else:
                holder.var_dict["respondedIpv6"] = True
            holder.var_dict["timestamp"] = arr[1].strip()
            data_holders.append(holder)
