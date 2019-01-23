import os
import sys
import states.AsnReader as ASN
import states.P0fReader as P0F
import states.UdpSizeReader as UDPSIZE
import states.IpvReader as IPV
from graphmodel import DataHolderList as Holder_List


# FilerReader holds DataHolder list and other requisute data. And a state object, tracks what kinda file we are reading
# Reading and parsing of files is handled by various DataReader Types
# This class holds all methods for reading in the different types of files
# Each subclass of the state has a read and parse function(perhaps parse is private)
class FileReader(object):

    def __init__(self, directory):
        # The List of DataHolder classes we will be pulling data from
        self.dir = directory
        # Add to this if you want to read additional file types!
        self.readers = {'.p0f': P0F.P0fReader(), '.asn': ASN.AsnReader(), '.udpsize': UDPSIZE.UdpSizeReader(), '.ipv': IPV.IpvReader()}

    # This function calls the methods which read in all the data into our DataReader
    def read_all_files(self):
        data_holders = Holder_List.DataHolderList()
        # Go through every file
        for file in os.listdir(self.dir):
            filename, file_extension = os.path.splitext(file)
            try:
                reader = self.readers[file_extension]
                my_file = self.dir + file
                # read that files contents into our DataReader
                reader.read(my_file, data_holders)
                print("{} has been read\n".format(file))
            except KeyError as err:
                sys.stderr.write('KeyError in ReadFiles: %s\n' % str(err))
        print("All Files read\nIPs Found in total: ", len(data_holders.ip_to_holder))
        return data_holders

