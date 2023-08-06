"""
DataSets -- Main Operation Class
"""
import os
import json
from abc import ABCMeta, abstractmethod

from . import table
from .plot import PlotSingle2D
from .manage import FILEPATHSTR, ENV_VAR_SETTINGS, ENV_VAR_ROOT_DIR
from .misc import get_default_format


with open(os.environ[ENV_VAR_SETTINGS], 'rb') as settings_file:
    SETTINGS = json.load(settings_file)
ROOT_DIR = os.environ[ENV_VAR_ROOT_DIR]
PURPOSE = SETTINGS.get("PURPOSE", {})


class DataSets(object):
    """
    Main Operation Class

    data: dictionary
        "name": DataFile
    custom_data: dictionary
        "name": DataFile
    """
    __metaclass__ = ABCMeta
    data = {}
    custom_data = {}

    def __init__(self):
        self.vardict = {}
        self.vardictformat = {}
        self.variables = {}

    @abstractmethod
    def operations(self):
        """
        Abstract Method
        Main Operations
        """
        pass

    def parse_data_to_internal(self, include_custom=False):
        """
        Invoke parse_data_to_internal() for every element
        in self.data
        """
        for element in self.data:
            self.data[element].parse_data_to_internal()
        if include_custom:
            for element in self.custom_data:
                self.custom_data[element].parse_data_to_internal()

    def create_dat_file(self, include_custom=False):
        """
        Invoke create_dat_file() for every element
        in self.data
        """
        for element in self.data:
            self.data[element].create_dat_file()
        if include_custom:
            for element in self.custom_data:
                self.custom_data[element].parse_data_to_internal()

    # built-in functions
    @staticmethod
    def plot_2d_single(x, y, pdffilename, **kwargs):
        """
        Do make_2d_single_plot and pass all arguments

        args:
            x: array_like
                xdata
            y: array_like
                ydata
            filepath: string
                filepath of pdf to save
            **kwargs:
                errors: dictionary, array_like, scalar
                    dictionary: {"xerr": xerr, "yerr": yerr}
                    array_like, scalar: yerr
                fmt: string, default="k."
                bestfitfmt: string, default="k-"
                bestfit: BestFit child class
                    eg. bestfit.polyfit.PolyFit, bestfit.logfit.LogFit
                suptitle: string, default=None
                    suptitle of pdf plot, formatted with outputdict
                suptitle_fontsize: int, default=15
                    font size of suptitle
                title: string, default=None
                    title of the pdf plot
                title_fontsize: int, default=12
                    font size of title, formatted with outputdict
                xlabel: string, default=None
                    label of string xlabel, formatted with outputdict
                ylabel: string, default=None
                    label of string ylabel, formatted with outputdict
                outputdict: dictionary, default=None
                    pass keys and arguments for formatting and
                    to output
        return: dictionary
            outputdict: passed from outputdict
                fit_args: list
                    fitting arguments
                rmse: list
                    rmse
        """
        pdffilepath = DataSets.get_pdffilepath(pdffilename)
        plotsingle2d = PlotSingle2D(x, y, pdffilepath, **kwargs)
        return plotsingle2d.plot()

    @staticmethod
    def get_pdffilepath(pdffilename):
        """
        Returns the path for the pdf file

        args:
            pdffilename: string
                returns path for the plots folder / pdffilename.pdf
        """
        return FILEPATHSTR.format(
            root_dir=ROOT_DIR, os_sep=os.sep, os_extsep=os.extsep,
            name=pdffilename,
            folder=PURPOSE.get("plots").get("folder", "plots"),
            ext=PURPOSE.get("plots").get("extension", "pdf")
        )


    @staticmethod
    def make_tex_table(inputlist, outputfilename, fmt=None, **kwargs):
        """
        Do make_tex_table and pass all arguments

        args:
            inputlist: list
            outputfilename: string
            fmt: dictionary
                key: integer
                    column index starting with 0
                values: string
                    format string. eg "{:g}"
            **kwargs:
                nonestring: string
                    string when objecttype is None
        """
        outputfilepath = FILEPATHSTR.format(
            root_dir=ROOT_DIR, os_sep=os.sep, os_extsep=os.extsep,
            name=outputfilename,
            folder=PURPOSE.get("tables").get("folder", "tables"),
            ext=PURPOSE.get("tables").get("extension", "tex")
        )
        table.make_tex_table(inputlist, open(outputfilepath, 'wb'),
                             fmt=fmt, close=kwargs.get("close", True), **kwargs)

    def make_compute_file(self):
        """
        Make the compute file from the self.vardict and self.vardictformat
        """
        string = ""
        try:
            vardict_items = self.vardict.iteritems()
        except AttributeError:
            vardict_items = self.vardict.items()
        for key, val in vardict_items:
            # get default
            default_format = get_default_format(val)
            string_format = "\\newcommand{{\\{}}}{{" + self.vardictformat.get(
                key, default_format) + "}}\n"
            string += string_format.format(key, val).replace("+", "")
        # get settings
        compute_file = open(
            "{root_dir}{os_sep}{name}{os_extsep}{ext}".format(
                root_dir=ROOT_DIR, os_sep=os.sep, os_extsep=os.extsep,
                name=SETTINGS["COMPUTE"]["name"],
                ext=SETTINGS["COMPUTE"]["extension"]
            ), "wb")
        compute_file.write(string)
        compute_file.close()
