import operator
import DataReader as data_obj
import Plotter as plot
import sys
import ReadFiles as file_reader
import DataHolderMethods as methods


# example of how to call: python PlotMain.py C:\Users\tyler\PycharmProjects\PlottingPractice\ client

######################################################################################################
# READ IN THE DATA FROM OUR FILES

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Invalid, Usage: python PlotMain.py {} {}\n".format("<DataFilesPath>", "[Main attribute]"))
    exit(1)

dataReader = data_obj.DataReader()
fileReader = file_reader.FileReader(sys.argv[1], dataReader)

# All files we are reading should be in one directory given as an argument
# Read in all the files
fileReader.read_all_files()


######################################################################################################
# BEGIN PROCESSING THE DATA

variable_dict = dataReader.add_up_all_attrs()
special_dict = None
# If we were told to create a more specific set of data
if len(sys.argv) == 3:
    key = sys.argv[2]
    special_dict = dataReader.add_up_all_attrs(methods.get_var_of_one_type, methods.make_dict_of_one_type, key)

plotter = plot.Plotter()


######################################################################################################
# AT THIS POINT YOU CAN CALL/USE WHAT FUNCTIONS LOGIC YOU WANT TO CREATE THE NEEDED GRAPHS
# TODO take out long names for OS's (take out unneeded info in parens)

# DO OS's
# Grab The inner dicts
all_ips = (list(special_dict.values()))[0]
num_of_os = {}
for ip_dict in all_ips.values():

    if ip_dict["os"] not in num_of_os.keys():
        num_of_os[ip_dict["os"]] = 1
    else:
        num_of_os[ip_dict["os"]] += 1
plotter.categorical_bar_graph("Type Of OS's Found", "OS Types", "Number Found", list(num_of_os.keys()), list(num_of_os.values()))

# DO by country
all_countries = (variable_dict["country"])
# get the top 20 countries
countries = dict(sorted(all_countries.items(), key=operator.itemgetter(1), reverse=True)[:25])
plotter.categorical_bar_graph("Countries of Origin", "Countries", "Number Found",
                              list(countries.keys()), list(countries.values()))
