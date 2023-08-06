"""
Input data file class
"""
import os
import glob
import cPickle as pickle
import json
import numpy as np

from . import parse
from .manage import FILEPATHSTR, ENV_VAR_SETTINGS, ENV_VAR_ROOT_DIR


class CustomDataFile(object):
    """
    Input data file class
    """
    def __init__(self, name, ext=None, argnum=2, filetype="pickle", **kwargs):
        """
        Constructor

        args:
            name: string
                invalid filename will be changed to valid filename in files
            argnum: int, default=2
                number of columns
            **kwargs: string
                keyword is the variable
                arguments is either 'f' (float) or 'l' (list)
        """
        self.name = str(name)
        keepcharacters = (" ", ".", "_")
        self.valid_filename = "".join(
            c for c in self.name if c.isalnum() or c in keepcharacters
        ).rstrip()
        self.argnum = int(argnum)
        self.kwargs = kwargs
        with open(os.environ[ENV_VAR_SETTINGS], 'rb') as settings_file:
            settings = json.load(settings_file)
        root_dir = os.environ[ENV_VAR_ROOT_DIR]
        purpose = settings.get("PURPOSE", {})
        self.filetype = filetype if filetype is "pickle" or "hickle"\
            else "pickle"
        self.location_dat = FILEPATHSTR.format(
            root_dir=root_dir, os_sep=os.sep, os_extsep=os.extsep,
            name=self.valid_filename,
            folder=purpose.get("data", {}).get("folder", "data"),
            ext=ext if ext is not None else purpose.get(
                "data", {}).get("extension", "dat"),
        )
        self.location_internal = FILEPATHSTR.format(
            root_dir=root_dir, os_sep=os.sep, os_extsep=os.extsep,
            name=self.valid_filename,
            folder=purpose.get("pickle", {}).get("folder", "pickle"),
            ext=purpose.get("pickle", {}).get("extension", "pickle")
        )

    def create_dat_file(self):
        """
        Create and write empty data file in the data directory
        """
        output = "## {}\n".format(self.name)
        try:
            kwargs_items = self.kwargs.iteritems()
        except AttributeError:
            kwargs_items = self.kwargs.items()
        for key, val in kwargs_items:
            if val is "l":
                output += "#l {}=\n".format(str(key))
            elif val is "f" or True:
                output += "#f {}=\n".format(str(key))
        comment = "## " + "\t".join(["col{" + str(i) + ":d}"
                                     for i in range(self.argnum)])
        comment += "\n"
        rangeargnum = range(self.argnum)
        output += comment.format(*rangeargnum)
        if os.path.isfile(self.location_dat):
            files = glob.glob(self.location_dat + "*")
            count = 2
            while ((self.location_dat + str(count) in files)
                  ) and (count <= 10):
                count += 1
            os.rename(self.location_dat, self.location_dat + str(count))
        dat_file = open(self.location_dat, "wb")
        dat_file.write(output)
        dat_file.close()

    def parse_data_to_internal(self, data=None):
        """
        Parse data and save to pickle/hickle
        """
        if data is None:
            data = parse.getdata(open(self.location_dat, "rb"),
                                 argnum=self.argnum, close=True)
        if self.filetype is "pickle":
            pickle.dump(data, open(self.location_internal, "wb"))
        elif self.filetype is "hickle":
            import hickle
            hickle.dump(data, open(self.location_internal, "wb"))
        else:
            raise ValueError(
                "Invalid filetype {} (must be {} or {})".format(
                    self.filetype, "pickle", "hickle"
                )
            )

    def get_internal_data(self):
        """
        Get data that is saved in pickle/hickle
        """
        if self.filetype is "pickle":
            return pickle.load(open(self.location_internal, "rb"))
        elif self.filetype is "hickle":
            import hickle
            return hickle.load(open(self.location_internal, "rb"))
        else:
            raise ValueError(
                "Invalue filetype {} (must be {} or {})".format(
                    self.filetype, "pickle", "hickle"
                )
            )


class MCADataFile(CustomDataFile):
    """
    Data Table in the MCA
    """
    def create_dat_file(self):
        """Pass
        """
        pass
    def save_to_internal(self, data):
        """save
        """
        if self.filetype is "pickle":
            pickle.dump(data, open(self.location_internal, "wb"))
        elif self.filetype is "hickle":
            import hickle
            hickle.dump(data, open(self.location_internal, "wb"))
        else:
            raise ValueError(
                "Invalid filetype {} (must be {} or {})".format(
                    self.filetype, "pickle", "hickle"
                )
            )
    def parse_data_to_internal(self, data=None):
        """parse to internal
        """
        if data is None:
            f = open(self.location_dat, "rb")
            data = {
                "PMCA SPECTRUM": {},
                "DATA": [],
                "DP5 CONFIGURATION": {},
                "DPP STATUS": {}
            }
            delimiter = {
                "PMCA SPECTRUM": " - ",
                "DP5 CONFIGURATION": "=",
                "DPP STATUS": ":"
            }
            comments = {
                "PMCA SPECTRUM": None,
                "DP5 CONFIGURATION": ";",
                "DPP STATUS": None
            }
            for e in f:
                if "<<" in e:
                    if "<<END>>" in e:
                        current = None
                    elif "<<PMCA SPECTRUM>>" in e:
                        current = "PMCA SPECTRUM"
                    elif "<<DATA>>" in e:
                        current = "DATA"
                    elif "<<DP5 CONFIGURATION>>" in e:
                        current = "DP5 CONFIGURATION"
                    elif "<<DPP STATUS>>" in e:
                        current = "DPP STATUS"
                else:
                    if current == "DATA":
                        data["DATA"].append(float(e))
                    elif current is not None:
                        e = e.split("\r\n")[0]
                        if comments[current] is not None:
                            e = e.split(comments[current], 1)[0]
                        e_list = e.split(delimiter[current], 1)
                        data[current][e_list[0]] = e_list[1]
            f.close()
        self.save_to_internal(data)


class DataFile(CustomDataFile):
    """
    Standard Data Table using numpy to parse
    """
    def create_dat_file(self):
        """Pass
        """
        pass
    def parse_data_to_internal(self, data=None):
        """Use numpy loadtxt
        """
        if data is None:
            kwargs = self.kwargs
            data = np.loadtxt(
                open(self.location_dat, "rb"), **kwargs
            )
        if self.filetype is "pickle":
            pickle.dump(data, open(self.location_internal, "wb"))
        elif self.filetype is "hickle":
            import hickle
            hickle.dump(data, open(self.location_internal, "wb"))
        else:
            raise ValueError(
                "Invalid filetype {} (must be {} or {})".format(
                    self.filetype, "pickle", "hickle"
                )
            )
