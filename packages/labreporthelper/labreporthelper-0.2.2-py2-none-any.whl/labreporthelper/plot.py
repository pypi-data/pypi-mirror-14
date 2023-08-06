"""
2D single plot module
"""
import matplotlib.pyplot as plt
import collections
import numpy as np

class PlotSingle2D(object):
    """
    make plots using pyplot,
    can be used as a parent class to manage pyplots
    """
    def __init__(self, x, y, filepath, **kwargs):
        """
        args:
            x: array_like
                xdata
            y: array_like
                ydata
            filepath: string
                filepath of pdf to save
            **kwargs:
                figure_options: passed to matplotlib.pyplot.figure
                xlabel_options: dict
                    kwargs passed in set_xlabel
                ylabel_options: dict
                    kwargs passed in set_ylabel
                suptitle_options: dict
                    kwargs passed in figure.suptitle
                title_options: dict
                    kwargs passed in set_title
                scilimits: tuple
                    if number outside this limits, will use scientific notation
                errors: dictionary, array_like, scalar
                    dictionary: {"xerr": xerr, "yerr": yerr}
                    array_like, scalar: yerr
                fmt: string, default="k."
                    line format
                bestfitfmt: string, default="k-"
                    bestfit line format
                bestfit: BestFit child class
                    eg. bestfit.polyfit.PolyFit, bestfit.logfit.LogFit
                bestfitlim: tuple, default=None
                    xlim for bestfit line
                suptitle: string, default=xlim
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
                xlim: tuple, default=None
                    xlim
                ylim: tuple, default=None
                    ylim
                outputdict: dictionary, default=None
                    pass keys and arguments for formatting and
                    to output
        """
        figure_options = kwargs.get("figure_options", {})
        self.figure = plt.figure(**figure_options)
        self.y = y
        self.x = x if x is not None else np.array(range(len(y)))
        self.filepath = filepath
        self.kwargs = kwargs
        self.subplot = None
        self.outputdict = kwargs.get("strformatdict", {})
        self.create_subplot()
    def get_subplot(self):
        """Get subplot
        """
        return self.subplot

    def create_subplot(self):
        """
        Create subplot,
        Method to be overriden in more complex child classes.
        self.subplot can be a subplot, a list of subplot,
        or a dictionary of subplot
        """
        self.subplot = self.figure.add_subplot(1, 1, 1)
        return self

    def before_plot(self):
        """
        Method to be overriden in more complex child classes.
        Done before plot
        """
        return self

    def after_plot(self):
        """
        Method to be overriden in more complex child classes.
        Done after plot
        """
        return self

    def after_label(self):
        """
        Method to be overriden in more complex child classes
        Done after label
        """
        return self

    def do_plot_and_bestfit(self):
        """
        Create plot
        """
        # Plot
        fmt = str(self.kwargs.get("fmt", "k."))
        if "errors" in self.kwargs:
            errors = self.kwargs["errors"]
            if isinstance(errors, dict):
                self.subplot.errorbar(self.x, self.y, fmt=fmt,
                                      xerr=errors.get("xerr", None),
                                      yerr=errors.get("yerr", None))
            elif isinstance(errors, (collections.Sequence, np.ndarray, float)):
                self.subplot.errorbar(self.x, self.y, fmt=fmt, yerr=errors)
            else:
                self.subplot.plot(self.x, self.y, fmt)
        else:
            self.subplot.plot(self.x, self.y, fmt)

        # bestfit
        bestfit = self.kwargs.get("bestfit", None)
        if bestfit is not None:
            bestfitlim = self.kwargs.get("bestfitlim", None)
            if bestfitlim is None:
                bestfitlim = self.kwargs.get("xlim", None)
            if bestfitlim is None:
                bestfitlim = (min(self.x), max(self.x))
            fit_args = bestfit.do_bestfit()
            bestfit_line = bestfit.get_bestfit_line(
                x_min=bestfitlim[0], x_max=bestfitlim[1])
            self.subplot.plot(
                bestfit_line[0], bestfit_line[1],
                self.kwargs.get("bestfitfmt", "k-")
            )
            self.outputdict["fit_args"] = fit_args
            self.outputdict["rmse"] = bestfit.get_rmse()
        return self

    def do_label(self):
        """
        Create label for x and y axis, title and suptitle
        """
        outputdict = self.outputdict
        xlabel_options = self.kwargs.get("xlabel_options", {})
        self.subplot.set_xlabel(
            self.kwargs.get("xlabel", "").format(**outputdict),
            **xlabel_options)
        ylabel_options = self.kwargs.get("ylabel_options", {})
        self.subplot.set_ylabel(
            self.kwargs.get("ylabel", "").format(**outputdict),
            **ylabel_options)
        suptitle = self.kwargs.get("suptitle", None)
        if suptitle is not None:
            suptitle_options = self.kwargs.get("suptitle_options", {})
            self.figure.suptitle(
                suptitle.format(**outputdict),
                fontsize=int(self.kwargs.get("suptitle_fontsize", 15)),
                **suptitle_options)
        title = self.kwargs.get("title", None)
        if title is not None:
            title_options = self.kwargs.get("title_options", {})
            self.subplot.set_title(
                title.format(**outputdict),
                fontsize=int(self.kwargs.get("title_fontsize", 12)),
                **title_options)
        xlim = self.kwargs.get("xlim", None)
        ylim = self.kwargs.get("ylim", None)
        if xlim is not None:
            self.subplot.set_xlim(xlim)
        if ylim is not None:
            self.subplot.set_ylim(ylim)
        # axis format
        self.subplot.ticklabel_format(
            style="sci", useOffset=False,
            scilimits=self.kwargs.get("scilimits", (-4, 4))
        )
        return self

    def save(self):
        """
        save plot to pdf
        """
        self.figure.savefig(self.filepath)
        return self

    def close(self):
        """
        close figure
        """
        self.figure.clf()
        return self

    def get_outputdict(self):
        """
        Get outpudict
        """
        return self.outputdict

    def plot(self):
        """
        Plot
        """
        self.before_plot()
        self.do_plot_and_bestfit()
        self.after_plot()
        self.do_label()
        self.after_label()
        self.save()
        self.close()
        return self.outputdict
