# -*- coding: utf-8 -*-
from collections import namedtuple
import os
import re
import shutil
import tempfile

try:
    home_dir = os.environ["HOME"]
except KeyError:
    home_dir = "."

class ClientConfig():
    def __init__(self, file="/".join([home_dir, ".ssh", "config"])):
        self.file = file
        # print("File -> {0}".format(self.file))
        self.configs = []
        self.file_bkps = []

    def read(self):
        configs = []
        with open(self.file) as fh:
            c = []
            for line in fh.readlines():
                if not line.strip():
                    c.append({"comment": None, "flag": None, "value": None})
                elif re.search("^#[ ]*", line):
                    if c:
                        configs.append(c)
                    c = []
                    c.append({"comment": line.strip(), "flag": None, "value": None})
                elif re.search("[ ]*#[ ]*", line):
                    c.append({"comment": line.strip(), "flag": None, "value": None})
                elif "host " in line.strip().lower():
                    if c:
                        configs.append(c)
                    c = []
                    c.append({"comment": None, "flag": "Host", "value": " ".join(line.split()[1:])})
                else:
                    line_ = line.split()
                    c.append({"comment": None, "flag": line_[0], "value": " ".join(line_[1:])})
            if c:
                configs.append(c)
        self.configs = configs[:]
        # print("configs -> {0}".format(self.configs))

    def append(self):
        self.read()
        # Do the appending here
        self.write()

    def remove(self):
        self.read()
        # Do the removing here
        self.write()

    def disable(self):
        self.read()
        # Do the disabling here
        self.write()

    def enable(self):
        self.read()
        # Do the enabling here
        self.write()

    def write(self):
        out = []
        for line in self.configs:
            new_host = None
            for config in line:
                if config["flag"] == "Host" and not config["comment"]:
                    new_host = " ".join([line[0]["flag"], line[0]["value"]])
                    out.append(new_host)
                elif new_host and config["comment"]:
                    comment = config["comment"]
                    out.append("    {0}".format(comment))
                elif new_host and not config["comment"] and not config["flag"] and not config["value"]:
                    out.append("")
                elif new_host:
                    config_ = " ".join([config["flag"], config["value"]])
                    out.append("    {0}".format(config_))
                elif not new_host and not config["comment"] and not config["flag"] and not config["value"]:
                    out.append("")
                elif not new_host and config["comment"]:
                    comment = config["comment"]
                    out.append(comment)

        # print("Out -> {0}".format(out))

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as fh_out:
            orig_copy = fh_out.name
            # print("Original copy -> {0}".format(orig_copy))

        shutil.copy2(src=self.file, dst=orig_copy, follow_symlinks=True)

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as fh_out:
            new_file = fh_out.name
            # print("New file -> {0}".format(new_file))
            for line in out:
                # print("Line to write -> {0}".format(line))
                fh_out.write("{0}\n".format(line))

        os.replace(src=new_file, dst=self.file)

        self.file_bkps.append(orig_copy)

        return orig_copy
