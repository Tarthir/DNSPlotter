import operator
from readers import DataReader as data_obj, FileReader as file_reader
from model import Plotter as plot, DataHolderMethods as methods
import sys

# TODO see if there are different ASNs for both the one we queried and the one who queries our servers
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
# TODO package up and do json dumps of these dictionaries so they can be put into peoples own graphs
#
# # DO OS's
# # Grab The inner dicts
all_ips = (list(special_dict.values()))[0]
num_of_os = {}
for ip_dict in all_ips.values():

    if ip_dict["os"] not in num_of_os.keys():
        num_of_os[ip_dict["os"]] = 1
    else:
        num_of_os[ip_dict["os"]] += 1
plotter.bar_graph("Type Of OS's Found", "OS Types", "Number Found", list(num_of_os.keys()), list(num_of_os.values()))

# DO by country
all_countries = (variable_dict["country"])
# get the top 15 countries
sorted_countries = sorted(all_countries.items(), key=operator.itemgetter(1), reverse=True)
top_countries = dict(sorted_countries[:15])
plotter.bar_graph("Top 15 Countries", "Countries", "Number Found",
                               list(top_countries.keys()), list(top_countries.values()))

# Do by country and include 'Other'
top_countries['Other'] = 0
for i in range(15, len(sorted_countries)):
    top_countries['Other'] += sorted_countries[i][1]

plotter.bar_graph("Top 15 Countries", "Countries", "Number Found",
                  list(top_countries.keys()), list(top_countries.values()))

# Do by company name
all_companies = variable_dict["shortname"]
# get top 10 companies
sorted_companies = sorted(all_companies.items(), key=operator.itemgetter(1), reverse=True)
top_companies = dict(sorted_companies[:10])
plotter.bar_graph("Top 10 Companies", "Companies", "Number Found",
                  list(top_companies.keys()), list(top_companies.values()))

# Do by Country pie chart
explode = [0] * len(top_countries.keys())
explode[0] = 0.1
plotter.pie_chart("Top 15 Countries", list(top_countries.keys()), list(top_countries.values()), explode)


# Do a bar graph on mtu
all_mtu = variable_dict["raw_mtu"]
sorted_mtus = sorted(all_mtu.items(), key=operator.itemgetter(1), reverse=True)
top_mtus = dict(sorted_mtus[:15])
explode = [0] * len(top_mtus.keys())
explode[0] = 0.1
plotter.bar_graph("Top MTU", "a", "a", list(top_mtus.keys()), list(top_mtus.values()))

#plotter.rand()
# Do Hist for dist
dist = variable_dict["dist"]
plotter.hist("a", "a", "a", dist, 10)
