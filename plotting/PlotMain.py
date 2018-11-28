from readers import DataReader as Data_Obj, FileReader as File_Reader
from model import DataHolderMethods as Methods
import sys
import json

# TODO see if there are different ASNs for both the one we queried and the one who queries our servers
# example of how to call: python PlotMain.py C:\Users\tyler\PycharmProjects\PlottingPractice\

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

dataReader = Data_Obj.DataReader()
fileReader = File_Reader.FileReader(sys.argv[1], dataReader)

# All files we are reading should be in one directory given as an argument
# Read in all the files
print("Reading all files...\n")
fileReader.read_all_files()


######################################################################################################
# BEGIN PROCESSING THE DATA
print("Compiling Data...\n")
key = "client"
variable_dict = dataReader.add_up_all_attrs()
special_dict = dataReader.add_up_all_attrs(Methods.get_var_of_one_type, Methods.make_dict_of_one_type, key)
print("Compilation complete!")
######################################################################################################
# Write data out to files
print("Creating JSON Files...")
with open("datalib/variable_dict.json", "w") as fp:
    json.dump(variable_dict, fp)
with open("datalib/special_dict.json", "w") as fp:
    json.dump(special_dict, fp)
print("JSON files complete!")

