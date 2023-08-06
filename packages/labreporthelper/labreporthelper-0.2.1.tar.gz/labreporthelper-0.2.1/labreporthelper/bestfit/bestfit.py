"""
Module containing BestFit abstract class
"""
import numpy as np
from abc import ABCMeta, abstractmethod


class BestFit(object):
    """
    Base class for bestfit
    """
    __metaclass__ = ABCMeta
    # variables needed to do bestfit
    important_variables = set(['x', 'y'])

    def __init__(self, **kwargs):
        """
        Constructor
        """
        self.args = kwargs
        self.done_bestfit = False
        self.fit_args = None


    def set_defaults(self, **defaults):
        """
        Add all keyword arguments to self.args

        args:
            **defaults:
                key and value represents dictionary key and value
        """
        try:
            defaults_items = defaults.iteritems()
        except AttributeError:
            defaults_items = defaults.items()
        for key, val in defaults_items:
            if key not in self.args.keys():
                self.args[key] = val


    def set_args(self, **kwargs):
        """
        Set more arguments to self.args

        args:
            **kwargs:
                key and value represents dictionary key and value
        """
        try:
            kwargs_items = kwargs.iteritems()
        except AttributeError:
            kwargs_items = kwargs.items()
        for key, val in kwargs_items:
            self.args[key] = val

    def check_important_variables(self):
        """
        Check all the variables needed are defined
        """
        if len(self.important_variables - set(self.args.keys())):
            raise TypeError("Some important variables are not set")

    @abstractmethod
    def do_bestfit(self):
        """
        Method to get fit_args after getting necessary variables
        """
        pass

    @abstractmethod
    def bestfit_func(self, bestfit_x):
        """
        Returns bestfit_function
        args:
            bestfit_x: scalar, array_like
                x value
        return: scalar, array_like
            bestfit y value
        """
        pass

    def get_bestfit_line(self, x_min=None, x_max=None, resolution=None):
        """
        Method to get bestfit line using the defined
        self.bestfit_func method

        args:
            x_min: scalar, default=min(x)
                minimum x value of the line
            x_max: scalar, default=max(x)
                maximum x value of the line
            resolution: int, default=1000
                how many steps between x_min and x_max
        returns:
            [bestfit_x, bestfit_y]
        """
        x = self.args["x"]
        if x_min is None:
            x_min = min(x)
        if x_max is None:
            x_max = max(x)
        if resolution is None:
            resolution = self.args.get("resolution", 1000)
        bestfit_x = np.linspace(x_min, x_max, resolution)
        return [bestfit_x, self.bestfit_func(bestfit_x)]

    def get_rmse(self, data_x=None, data_y=None):
        """
        Get Root Mean Square Error using
        self.bestfit_func

        args:
            x_min: scalar, default=min(x)
                minimum x value of the line
            x_max: scalar, default=max(x)
                maximum x value of the line
            resolution: int, default=1000
                how many steps between x_min and x_max
        """
        if data_x is None:
            data_x = np.array(self.args["x"])
        if data_y is None:
            data_y = np.array(self.args["y"])
        if len(data_x) != len(data_y):
            raise ValueError("Lengths of data_x and data_y are different")
        rmse_y = self.bestfit_func(data_x)
        return np.sqrt(np.mean((rmse_y - data_y) ** 2))

    def get_mae(self, data_x=None, data_y=None):
        """
        Get Mean Absolute Error using
        self.bestfit_func

        args:
            data_x: array_like, default=x
                x value used to determine rmse, used if only a section
                of x is to be calculated
            data_y: array_like, default=y
                y value used to determine rmse, used if only a section
                of y is to be calculated
        """
        if data_x is None:
            data_x = np.array(self.args["x"])
        if data_y is None:
            data_y = np.array(self.args["y"])
        if len(data_x) != len(data_y):
            raise ValueError("Lengths of data_x and data_y are different")
        mae_y = self.bestfit_func(data_x)
        return np.mean(abs(mae_y - data_y))

    def get_fit_args(self):
        """
        return fit_args
        """
        return self.fit_args
