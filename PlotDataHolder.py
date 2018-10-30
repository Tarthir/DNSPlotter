import re


class PlotDataHolder(object):

    def __init__(self, line1, line2):
        # parse the lines and hold the data
        self.mod = ""
        self.client = ""
        self.srv = ""
        self.subj = ""
        self.link = ""
        self.raw_mtu = ""
        self.os = ""
        self.dist = ""
        self.params = ""
        self.tos = ""
        self.raw_sig = ""
        self.parseline1(line1)
        self.parseline2(line2)

    def parseline1(self, line1):
        self.mod = re.search("mod=(.*?)|", line1, re.DOTALL).group(1)
        self.client = re.search("cli=(.*?)|", line1, re.DOTALL).group(1)
        self.srv = re.search("srv=(.*?)|", line1, re.DOTALL).group(1)
        self.subj = re.search("subj=(.*?)|", line1, re.DOTALL).group(1)
        self.os = re.search("os=(.*?)|", line1, re.DOTALL).group(1)
        self.dist = re.search("dist=(.*?)|", line1, re.DOTALL).group(1)
        self.params = re.search("params=(.*?)|", line1, re.DOTALL).group(1)
        self.tos = re.search("tos=(.*?)|", line1, re.DOTALL).group(1)
        self.raw_sig = re.search("raw_sig=(.*?)|", line1, re.DOTALL).group(1)

    def parseline2(self, line2):
        self.link = re.search("link=(.*?)|", line2, re.DOTALL).group(1)
        self.raw_mtu = re.search("raw_mtu=(.*?)|", line2, re.DOTALL).group(1)
