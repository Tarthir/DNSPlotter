import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple


class Plotter(object):

    # Ths method handles the making of categorical bar graphs
    # you pass in two lists, one of your x_values and one of your y values in respective order
    def categorical_bar_graph(self, title, x_name, y_name, cat_x_values, num_y_values):
        # convert NoneType to a string
        for i in range(0, len(cat_x_values)):
            if cat_x_values[i] is None:
                cat_x_values[i] = "None"

        plt.style.use('ggplot')
        fig, ax = plt.subplots()
        # Grab the indexes of each x val
        x_pos = [i for i, _ in enumerate(cat_x_values)]

        plt.bar(x_pos, num_y_values, color='green')
        ax.set_xlabel(x_name)
        ax.set_ylabel(y_name)
        ax.set_title(title)
        plt.xticks(x_pos, cat_x_values)
        plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

        plt.show()

    def pie_chart(self, title, labels, sizes, explode):
        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        #labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
        #sizes = [15, 30, 45, 10]

        fig1, ax = plt.subplots()
        ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.set_title(title)

        plt.show()

