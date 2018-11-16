import os
import sys
import states.AsnReader as ASN
import states.P0fReader as P0F
from model import DataHolderList as Holder_List


#TODO use state pattern
# FilerReader holds DataHolder list and other requisute data. And a state object, tracks what kinda file we are reading
# Reading and parsing of files is handled by various DataReader Types
# This class holds all methods for reading in the different types of files
# Each subclass of the state has a read and parse function(perhaps parse is private)
class FileReader(object):

    def __init__(self, directory, data_reader):
        # The List of DataHolder classes we will be pulling data from
        self.__data_holders = Holder_List.DataHolderList()
        self.dir = directory
        self.data_reader = data_reader
        # Add to this if you want to read additional file types!
        self.readers = {'.log': P0F.P0fReader(), '.data': ASN.AsnReader()}

    # This function calls the methods which read in all the data into our DataReader
    def read_all_files(self):
        # Go through every p0f file
        for file in os.listdir(self.dir):
            filename, file_extension = os.path.splitext(file)
            try:
                reader = self.readers[file_extension]
                my_file = self.dir + file
                # read that files contents into our DataReader
                reader.read(my_file, self.__data_holders)
            except KeyError as err:
                sys.stderr.write('KeyError in ReadFiles: %s\n' % str(err))
        self.data_reader.set_holders(self.__data_holders)

