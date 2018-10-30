import PlotDataHolder as Holder


class DataReader(object):

    def __init__(self):
        self.data_holders = []

    def read_p0f_data(self):  # Reads the p0f data and creates P0fDataHolder from the data
        # Read two lines at a time from p0f as each IP has two lines of data

        fd = open("p0f.txt", "r")
        while True:
            line1 = fd.readline()
            line2 = fd.readline()
            if not line2:
                break  # EOF
            self.data_holders.append(Holder.PlotDataHolder(line1, line2))

    def read_asn_data(self):
        pass
