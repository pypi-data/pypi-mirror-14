"""
PolyFit
"""
import numpy as np

from .bestfit import BestFit


class PolyFit(BestFit):
    """
    Polyfit class
    """
    def __init__(self, **kwargs):
        """
        Constructor
        args:
            **kwargs:
                degree: int, default=1
                    degree of polynomial fitting
                resolution: int, default=1000
        """
        BestFit.__init__(self, **kwargs)
        # set defaults
        self.set_defaults(degree=1, resolution=1000)

    def do_bestfit(self):
        """
        Method to get fit_args after getting necessary variables
        """
        self.check_important_variables()
        self.fit_args = np.polyfit(
            self.args["x"], self.args["y"], self.args.get("degree", 1))
        self.done_bestfit = True
        return self.fit_args

    def bestfit_func(self, bestfit_x):
        """
        Returns bestfit_y value

        args:
            bestfit_x: scalar, array_like
                x value
        return: scalar, array_like
            bestfit y value
        """
        bestfit_x = np.array(bestfit_x)
        if not self.done_bestfit:
            raise KeyError("Do do_bestfit first")
        bestfit_y = 0
        for idx, val in enumerate(self.fit_args):
            bestfit_y += val * (bestfit_x **
                                (self.args.get("degree", 1) - idx))
        return bestfit_y
