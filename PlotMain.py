import DataReader as data_obj
import Plotter
import sys
import os


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


if len(sys.argv) != 3:
    print("Invalid, Usage: python PlotMain.py {} {} \n".format("p0fLogDirPath", "asnLogFile"))
    exit(1)

# p0f files are held in a directory, there is a p0f file for every tcpdump .pcap file that was created
p0fLogFilePath = sys.argv[1]
# All the asn data is held within on file
asnLogFilePath = sys.argv[2]

readp0files()
variable_dict, numIPs = reader.add_up_all_attrs()




