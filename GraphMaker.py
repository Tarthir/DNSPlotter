import json
import operator
from model import Plotter as Plot
import sys

#####################################################################################################
# Do setup, grab the json files
plotter = Plot.Plotter()
variable_dict = None
special_dict = None
try:
    with open("variable_dict.json") as file_var:
        variable_dict = json.load(file_var)
    with open("special_dict.json") as file_var:
        special_dict = json.load(file_var)
except IOError as err:
    sys.stderr.write('ERROR: %sn' % str(err))
    exit(1)

######################################################################################################
# AT THIS POINT YOU CAN CALL/USE WHAT FUNCTIONS LOGIC YOU WANT TO CREATE THE NEEDED GRAPHS
# TODO take out long names for OS's (take out unneeded info in parens)
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

# Do Hist for dist
dist = variable_dict["dist"]
plotter.hist("a", "a", "a", dist, 10)
sizes = []
# Comparison of how many ips responded to a given udp size
s = [variable_dict["512"], variable_dict["1024"], variable_dict["2048"], variable_dict["5120"],
     variable_dict["10240"], variable_dict["20480"]]
for dic in s:
    c = (list(dic.values()))[1]
    sizes.append(c)
sizes_names = ["512", "1024", "2048", "5120", "10240", "20480"]
plotter.bar_graph("Number of Responders to certain sizes", "Size of Message", "Responses", sizes_names, sizes)

# How many ips had responded to multiple sizes
numbers = [0, 0, 0, 0, 0, 0, 0]
for ips in (special_dict["client"]).values():
    cnt = 0
    for i in range(0, len(sizes_names)):
        did_respond = ips[sizes_names[i]]
        if did_respond:
            cnt += 1
    numbers[cnt] += 1
plotter.bar_graph("IP Response Number Comparison", "Number of sizes IPs responded to",
                  "Number of IPS that responded", [0, 1, 2, 3, 4, 5, 6], numbers)
# How many ips responded only to larger sizes
numbers = [0, 0, 0, 0, 0]
sizes_names.pop(0)
for ips in (special_dict["client"]).values():
    cnt = 0
    for i in range(0, len(sizes_names)):
        did_respond = ips[sizes_names[i]]
        if did_respond:
            numbers[i] += 1


plotter.bar_graph("How many IPs only responded to > 512 bytes?", "Response sizes",
                  "Number", ["> 512", "> 1024", "> 2048", "> 5120", "> 10240"], numbers)
