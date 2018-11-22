from abc import ABC, abstractmethod


class ReaderState(ABC):

    def __init__(self):
        super().__init__()

    # Created and Held in the FileReader class
    # Reads a given file and extracts a set of data "A" from the file it needs.
    # Then creates an empty PlotDataHolder
    # Then passes "A" into the a subclass defined parse function which adds populates the PlotDataHolder obj with data
    # The PlotDataHolder is then returned tp the FilerReader where it is stored
    # data_holders is the list of all data_holders made so far. It is needed for updating purposes for all files read
    @abstractmethod
    def read(self, filename, data_holders):
        pass

