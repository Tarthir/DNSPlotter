import DataReader as data_obj
import Plotter as plot
import sys
import os
import DataHolderMethods as methods

# example of how to call: python PlotMain.py C:\Users\tyler\PycharmProjects\PlottingPractice\
#                                         C:\Users\tyler\PycharmProjects\PlottingPractice\ client

reader = data_obj.DataReader()
p0fLogFilePath = ""
asnLogFilePath = ""


# Read the p0f files
def readp0files():
    # Go through every p0f file
    for file in os.listdir(p0fLogFilePath):
        if file.endswith(".log"):
            p0file = p0fLogFilePath + file
            # read that files contents into our DataReader
            reader.read_p0f_data(p0file)


if len(sys.argv) < 3 or len(sys.argv) > 4:
    print("Invalid, Usage: python PlotMain.py {} {} {}\n".format("p0fLogDirPath", "asnLogFile","[Main attribute]"))
    exit(1)

# p0f files are held in a directory, there is a p0f file for every tcpdump .pcap file that was created
p0fLogFilePath = sys.argv[1]
# All the asn data is held within on file
asnLogFilePath = sys.argv[2]
# Read in all the p0f files
readp0files()
variable_dict, numIPs = reader.add_up_all_attrs()
special_dict = None
# If we were told to create a more specific set of data
if len(sys.argv) == 4:
    key = sys.argv[3]
    special_dict = reader.add_up_all_attrs(methods.get_var_of_one_type, methods.make_dict_of_one_type, key)

plotter = plot.Plotter(variable_dict, special_dict, numIPs)




