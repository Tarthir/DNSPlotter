import states.ReaderState as State
import re
from model import PlotDataHolder as Holder
import sys


class UdpSizeReader(State.ReaderState):

    def read(self, filename, data_holders):

        udp_size_parsed = open(filename, "r")

        for line in udp_size_parsed:
            holder = Holder.PlotDataHolder()
            line_array = line.split()
            holder.var_dict["client"] = line_array[0]
            if line_array[1] != "0":
                holder.var_dict["512"] = line_array[1]
            if line_array[2] != "0":
                holder.var_dict["1024"] = line_array[2]
            if line_array[3] != "0":
                holder.var_dict["2048"] = line_array[3]
            if line_array[4] != "0":
                holder.var_dict["5120"] = line_array[4]
            if line_array[5] != "0":
                holder.var_dict["10240"] = line_array[5]
            if line_array[6] != "0":
                holder.var_dict["20480"] = line_array[6]
            data_holders.append(holder)
