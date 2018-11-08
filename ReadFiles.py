import os


# This class holds all methods for reading in the different types of files
class FileReader(object):

    def __init__(self, directory,data_reader):
        self.dir = directory
        self.data_reader = data_reader

    # This function calls the methods which read in all the data into our DataReader
    def read_all_files(self):
        self.__readp0files()

    # Read the p0f files
    def __readp0files(self):
        # Go through every p0f file
        for file in os.listdir(self.dir):
            # TODO make sure this is only reading the files we want
            if file.endswith(".log"):
                p0file = self.dir + file
                # read that files contents into our DataReader
                self.data_reader.read_p0f_data(p0file)
