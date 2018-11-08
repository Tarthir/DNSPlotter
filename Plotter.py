import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple


class Plotter(object):

    # Ths method handles the making of categorical bar graphs
    # you pass in two lists, one of your x_values and one of your y values in respective order
    def categorical_bar_graph(self, title, x_name, y_name, cat_x_values, cat_y_values):
        plt.style.use('ggplot')
        fig, ax = plt.subplots()
        x_pos = [i for i, _ in enumerate(cat_x_values)]

        plt.bar(x_pos, cat_y_values, color='green')
        ax.set_xlabel(x_name)
        ax.set_ylabel(y_name)
        ax.set_title(title)
        plt.xticks(x_pos, cat_x_values)

        plt.show()

