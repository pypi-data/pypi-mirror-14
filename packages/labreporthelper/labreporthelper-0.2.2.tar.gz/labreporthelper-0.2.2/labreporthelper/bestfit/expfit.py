"""
Exponential Fit
"""
import numpy as np

from .bestfit import BestFit


class ExpFit(BestFit):
    """
    Exponential Fitting class
    """
    def __init__(self, **kwargs):
        """
        Constructor
        """
        BestFit.__init__(self, **kwargs)
        # set defaults
        self.set_defaults(resolution=1000)
        self.fit_args_log = None

    def do_bestfit(self):
        """
        Method to get fit_args after getting necessary variables
        """
        self.check_important_variables()
        logx = np.log(self.args["x"])
        logy = np.log(self.args["y"])
        self.fit_args_log = np.polyfit(logx, logy, 1)
        self.fit_args = self.fit_args_log[:]
        self.fit_args[1] = np.exp(self.fit_args[1])
        self.done_bestfit = True
        return self.fit_args

    def bestfit_func(self, bestfit_x):
        """
        Returns bestfit_function

        args:
            bestfit_x: scalar, array_like
                x value
        return: scalar, array_like
            bestfit y value
        """
        if not self.done_bestfit:
            raise KeyError("Do do_bestfit first")
        bestfit_y = self.fit_args[1] * (bestfit_x ** self.fit_args[0])
        return bestfit_y
