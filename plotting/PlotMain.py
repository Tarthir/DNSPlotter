from readers import FileReader as File_Reader
import sys
import pickle

# TODO see if there are different ASNs for both the one we queried and the one who queries our servers
# example of how to call: python PlotMain.py C:/Users/tyler/PycharmProjects/PlottingPractice/datalib

################################################################################################################
# This program reads all data files that are created from the data gathered by running a fullscan of ipv4 space
# This includes maxudp data, p0f, ASN, and geolocation. In essence this program gathers all the data into one
# point for ease of use. All data is put into two dictionaries. One, variable_dict, has each possible variable
# as a key for
################################################################################################################
# READ IN THE DATA FROM OUR FILES

if len(sys.argv) != 2:
    print("Invalid, Usage: python PlotMain.py {}\n".format("<DataFilesPath>"))
    exit(1)
directory = sys.argv[1]
fileReader = File_Reader.FileReader(directory)

# All files we are reading should be in one directory given as an argument
# Read in all the files
print("Reading all files...\n")
data_holders = fileReader.read_all_files()
d = data_holders.get_value_dict("country")

######################################################################################################
# BEGIN PROCESSING THE DATA
print("All possible keys are as follows: ")
for key in data_holders.all_possible_keys:
    print("%s " % key)

######################################################################################################
# Write data out to files
print("Creating Binary Files...")
binary_file = open(directory + 'my_pickeled_data.bin', mode='wb')
my_pickled_data = pickle.dump(data_holders, binary_file)
binary_file.close()
print("Binary files completed!")

