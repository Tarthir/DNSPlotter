import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple
from numpy import array


class Plotter(object):

    # Ths method handles the making of categorical bar graphs
    # you pass in two lists, one of your x_values and one of your y values in respective order
    def bar_graph(self, title, x_name, y_name, cat_x_values, num_y_values):
        max_name_len = 20
        # convert NoneType to a string
        for i in range(0, len(cat_x_values)):
            if cat_x_values[i] is None:
                cat_x_values[i] = "None"
            elif isinstance(cat_x_values[i], str) and len(cat_x_values[i]) > max_name_len:
                # All we are doing here is cutting off everything but the first 10 characters
                cat_x_values[i] = (cat_x_values[i])[:-(len(cat_x_values[i]) - max_name_len)]
                cat_x_values[i] = (cat_x_values[i]) + "..."

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
        # fig.tight_layout()
        plt.show()

    # This method creates pie charts from given data
    # title: the title you want for the chart
    # labels: An array where each element is the name of a slice of the pie
    # sizes: An array numbers, each representing how big each slice will be
    # explode: An array of zeroes, anything non zero, like 0.1 will cause
    # the respective slice to be more pronounced
    def pie_chart(self, title, labels, sizes, explode):
        # Pie chart, where the slices will be ordered and plotted counter-clockwise:

        fig1, ax = plt.subplots()
        ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.set_title(title)

        plt.show()

    def hist(self, title, x_label, y_label, values, num_of_bins):
        self.__check_dict(values)

        # mean of distribution
        mu = self.__get_mean(values)
        # standard deviation of distribution
        sigma, new_arr = self.__get_std_dev(values)

        num_bins = num_of_bins

        fig, ax = plt.subplots()

        # the histogram of the datae
        n, bins, patches = ax.hist(new_arr, num_bins, density=1)

        # add a 'best fit' line
        y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
             np.exp(-0.5 * (1 / sigma * (bins - mu)) ** 2))
        ax.plot(bins, y, '--')
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)

        # Tweak spacing to prevent clipping of ylabel
        fig.tight_layout()
        plt.show()

    # Computes/returns the mean from a set of values. They should all be numbers of course
    def __get_mean(self, values):
        mu = 0
        num = 0
        for distance in values.keys():
            try:
                mu += int(distance) * values[distance]
            except ValueError:
                continue
            num += values[distance]
        return mu // num  # mean of distribution

    # This function gets the standard dev from a list of values from a dictionary
    # It computes that std dev and also returns the np array it made from the values
    # to make the std dev. The np array is needed to complete the histogram
    def __get_std_dev(self, values):
        # expand the dictionary keys/values into a list of lists
        arr = [[int(dist)] * int(values[dist]) for dist in values.keys()]
        new_arr = []
        for i in range(len(arr)):
            new_arr.extend(arr[i])
        new_arr = array(new_arr)
        std = np.sqrt(np.mean(abs(new_arr - new_arr.mean()) ** 2))
        return std, new_arr

    # This function simply checks to see if there are ONLY numbers being passed in
    # as values, if there are any non numbers passed in we remove it from the list
    def __check_dict(self, values):
        to_be_removed = []
        for key in values.keys():
            try:
                int(key)
            except ValueError:
                to_be_removed.append(key)
        for remove in to_be_removed:
            values.pop(remove, None)
            # Can log this error if we want

    # def rand(self):
    #     np.random.seed(19680801)
    #
    #     # example data
    #     mu = 100  # mean of distribution
    #     sigma = 15  # standard deviation of distribution
    #     x = mu + sigma * np.random.randn(437)
    #
    #     num_bins = 50
    #
    #     fig, ax = plt.subplots()
    #
    #     # the histogram of the data
    #     n, bins, patches = ax.hist(x, num_bins, density=1)
    #
    #     # add a 'best fit' line
    #     y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
    #          np.exp(-0.5 * (1 / sigma * (bins - mu)) ** 2))
    #     ax.plot(bins, y, '--')
    #     ax.set_xlabel('Smarts')
    #     ax.set_ylabel('Probability density')
    #     ax.set_title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')
    #
    #     # Tweak spacing to prevent clipping of ylabel
    #     fig.tight_layout()
    #     plt.show()
