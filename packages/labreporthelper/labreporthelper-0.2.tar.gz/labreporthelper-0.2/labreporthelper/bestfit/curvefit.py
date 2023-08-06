"""
Curve Fit with scipy optimize and ODR
"""
from .bestfit import BestFit

import scipy.optimize as opt
import numpy as np
from scipy.odr import ODR, RealData, Model, Data


class CurveFit(BestFit):
    """
    Curve Fit

    Important Variables: x, y, func, num_vars
    """
    important_variables = set(["x", "y", "func", "num_vars"])
    def __init__(self, **kwargs):
        """
        Constructor
        """
        BestFit.__init__(self, **kwargs)
        self.cov = None

    def bestfit_func(self, bestfit_x):
        """
        Returns bestfit_func
        """
        if not self.bestfit_func:
            raise KeyError("Do do_bestfit first")
        return self.args["func"](bestfit_x, *self.fit_args)

    def do_bestfit(self):
        """
        Do bestfit
        """
        self.check_important_variables()
        x = np.array(self.args["x"])
        y = np.array(self.args["y"])
        p = self.args.get("params", np.ones(self.args["num_vars"]))
        self.fit_args, self.cov = opt.curve_fit(self.args["func"], x, y, p)
        return self.fit_args


class ODRFit(BestFit):
    """
    BestFit with ODR
    """
    important_variables = set(["x", "y", "func"])
    def __init__(self, **kwargs):
        """
        Constructor
        """
        BestFit.__init__(self, **kwargs)
        self.output = None

    def bestfit_func(self, bestfit_x):
        """
        Returns y value
        """
        if not self.bestfit_func:
            raise KeyError("Do do_bestfit first")
        return self.args["func"](self.fit_args, bestfit_x)

    def do_bestfit(self):
        """
        do bestfit using scipy.odr
        """
        self.check_important_variables()
        x = np.array(self.args["x"])
        y = np.array(self.args["y"])
        if self.args.get("use_RealData", True):
            realdata_kwargs = self.args.get("RealData", {})
            data = RealData(x, y, **realdata_kwargs)
        else:
            data_kwargs = self.args.get("Data", {})
            data = Data(x, y, **data_kwargs)
        model_kwargs = self.args.get("Model", {})
        model = Model(self.args["func"], **model_kwargs)
        odr_kwargs = self.args.get("ODR", {})
        odr = ODR(data, model, **odr_kwargs)
        self.output = odr.run()
        if self.args.get("pprint", False):
            self.output.pprint()
        self.fit_args = self.output.beta
        return self.fit_args
