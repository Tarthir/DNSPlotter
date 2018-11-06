import re
import sys


class PlotDataHolder(object):
    # These are all strings which correspond with data that p0f r
    # eturns

    def __init__(self, line1, line2, line3):
        self.mod = ""
        self.client = ""
        self.srv = ""
        self.subj = ""
        self.link = ""
        self.raw_mtu = ""
        self.os = ""
        self.dist = ""
        self.params = ""
        self.raw_sig = ""
        # reason that we had a did not find 'link' attr
        # mod will equal 'host change' for second p0f line in this case
        self.reason = ""

        # parse the lines and hold the data
        self.parseline1(line1)
        self.parseline2(line2)
        if line3 is not None:
            sys.stderr.write("IP with three p0f lines found: {}\n".format(self.client))
            self.parseline2(line3)

    def parseline1(self, line1):
        try:
            self.mod = re.search(r'mod=([^|]+)', line1).group(1)
            self.client = re.search("cli=([^|]+)", line1, re.DOTALL).group(1)
            self.srv = re.search("srv=([^|]+)", line1, re.DOTALL).group(1)
            self.subj = re.search("subj=([^|]+)", line1, re.DOTALL).group(1)
            self.os = re.search("os=([^|]+)", line1, re.DOTALL).group(1)
            self.dist = re.search("dist=([^|]+)", line1, re.DOTALL).group(1)
            self.params = re.search("params=([^|]+)", line1, re.DOTALL).group(1)
            self.raw_sig = re.search("raw_sig=([^|]+)", line1, re.DOTALL).group(1).rstrip()
        except AttributeError as err:
            sys.stderr.write('ERROR: %sn' % str(err))

    def parseline2(self, line2):
        try:
            if re.search(r'mod=([^|]+)', line2).group(1) != "host change":
                self.link = re.search("link=([^|]+)", line2, re.DOTALL).group(1)
                self.raw_mtu = re.search("raw_mtu=([^|]+)", line2, re.DOTALL).group(1).rstrip()
            else:
                self.reason = re.search("reason=([^|]+)", line2, re.DOTALL).group(1)
        except AttributeError as err:
            sys.stderr.write('ERROR: %sn' % str(err))
