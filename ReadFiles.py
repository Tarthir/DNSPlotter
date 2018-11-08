import os


# This class holds all methods for reading in the different types of files
# This is
class FileReader(object):

    def __init__(self, directory, data_reader):
        self.dir = directory
        self.data_reader = data_reader
    # TODO can be simplified to only go though the files once, grabbing/reading correctly each time
    # This function calls the methods which read in all the data into our DataReader
    def read_all_files(self):
        self.__readfiles(".log", self.data_reader.read_p0f_data)
        self.__readfiles(".data", self.data_reader.read_asn_data)

    # Read the p0f files
    def __readfiles(self, extension, reader_method):
        # Go through every p0f file
        for file in os.listdir(self.dir):
            # TODO make sure this is only reading the files we want
            if file.endswith(extension):
                myfile = self.dir + file
                # read that files contents into our DataReader
                reader_method(myfile)
