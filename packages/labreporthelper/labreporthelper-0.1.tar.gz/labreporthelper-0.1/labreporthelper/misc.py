"""
Misc Functions
"""
import numpy as np


def get_default_format(val):
    """
    Get default format

    Args:
        val: String/Scalar
            if np.isscalar(val) is true, returns "{:.3e}" else "{}"
    """
    if np.isscalar(val):
        default_format = "{:.3e}"
    else:
        default_format = "{}"
    return default_format
