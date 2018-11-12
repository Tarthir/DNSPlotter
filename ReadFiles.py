import os
import sys


# This class holds all methods for reading in the different types of files
class FileReader(object):

    def __init__(self, directory, data_reader):
        self.dir = directory
        self.data_reader = data_reader
        # Add to this if you want to read additional file types!
        self.reader_methods = {'.log': self.data_reader.read_p0f_data,
                               '.data': self.data_reader.read_asn_data}

    # This function calls the methods which read in all the data into our DataReader
    def read_all_files(self):
        # Go through every p0f file
        for file in os.listdir(self.dir):
            filename, file_extension = os.path.splitext(file)
            try:
                reader_method = self.reader_methods[file_extension]
                my_file = self.dir + file
                # read that files contents into our DataReader
                reader_method(my_file)
            except KeyError as err:
                sys.stderr.write('KeyError in ReadFiles: %s\n' % str(err))
        # Consolidate all the data now
       # self.data_reader.consolidate_data()


