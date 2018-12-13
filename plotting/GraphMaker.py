import operator
from model import Plotter as Plot
import sys
import pickle
#####################################################################################################
# This file shows examples of how to make graphs using Plotter.py
#####################################################################################################
# Do setup, grab the json files
plotter = Plot.Plotter()
data = None
directory = sys.argv[1]
try:
    data = pickle.load(open(directory + 'my_pickeled_data.bin', 'rb'))
except IOError as err:
    sys.stderr.write('ERROR: %sn' % str(err))
    exit(1)


######################################################################################################
# AT THIS POINT YOU CAN CALL/USE WHAT FUNCTIONS LOGIC YOU WANT TO CREATE THE NEEDED GRAPHS
# TODO take out long names for OS's (take out unneeded info in parens)
#
# # DO OS's
# # Grab The inner dicts
num_of_os = data.get_value_dict("os")
plotter.bar_graph("Type Of OS's Found", "OS Types", "Number Found", list(num_of_os.keys()), list(num_of_os.values()))

# DO by country
all_countries = data.get_value_dict("country")
del all_countries[None]
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
all_companies = data.get_value_dict("shortname")
# get top 10 companies
sorted_companies = sorted(all_companies.items(), key=operator.itemgetter(1), reverse=True)
top_companies = dict(sorted_companies[:10])
plotter.bar_graph("Top 10 Companies", "Companies", "Number Found",
                  list(top_companies.keys()), list(top_companies.values()))

# Do by Country pie chart
explode = [0] * len(top_countries.keys())
explode[0] = 0.1
plotter.pie_chart("Top 10 Countries", list(top_countries.keys()), list(top_countries.values()), explode)


# Do a bar graph on mtu
all_mtu = data.get_value_dict("raw_mtu")
sorted_mtus = sorted(all_mtu.items(), key=operator.itemgetter(1), reverse=True)
top_mtus = dict(sorted_mtus[:15])
explode = [0] * len(top_mtus.keys())
explode[0] = 0.1
plotter.bar_graph("Top MTU", "a", "a", list(top_mtus.keys()), list(top_mtus.values()))

# Do Hist for dist
dist = data.get_value_dict("dist")
plotter.hist("a", "a", "a", dist, 10)
sizes = []
# Comparison of how many ips responded to a given udp size
s = [data.get_value_dict("512"), data.get_value_dict("1024"), data.get_value_dict("2048"), data.get_value_dict("5120"),
     data.get_value_dict("10240"), data.get_value_dict("20480")]
for dic in s:
    c = (list(dic.values()))[0]
    sizes.append(c)
sizes_names = ["512", "1024", "2048", "5120", "10240", "20480"]
plotter.bar_graph("Number of Responders to certain sizes", "Size of Message", "Responses", sizes_names, sizes)

# How many ips had responded to multiple sizes
numbers = [0, 0, 0, 0, 0, 0, 0]
for ip in (data.get_value_dict("client")):
    cnt = 0
    for i in range(0, len(sizes_names)):
        did_respond = data.get_var_dict_value(ip, sizes_names[i])
        if did_respond:
            cnt += 1
    numbers[cnt] += 1
plotter.bar_graph("IP Response Number Comparison", "Number of sizes IPs responded to",
                  "Number of IPS that responded", [0, 1, 2, 3, 4, 5, 6], numbers)
# TODO Make a comparison btwn size returned(Kwans data) and MTU. MTU is how many bytes can be sent at time
