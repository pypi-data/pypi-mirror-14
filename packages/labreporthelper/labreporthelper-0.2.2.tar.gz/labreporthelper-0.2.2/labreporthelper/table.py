"""
Helper module for make_tex_table
"""
import numpy as np


def make_tex_table(inputlist, outputfile, close=False, fmt=None,
                   **kwargs):
    """
    Parse table from inputlist

    Args:
        inputlist: list
            List to parse
        outputfile: file
            .tex file to write
        fmt: dictionary
            key: integer
                column index starting with 0
            values: string
                format string. eg "{:g}"
        **kwargs:
            nonestring: string
                string when objecttype is None
   Returns:
        None
    """
    output_str = ""
    if fmt is None:
        fmt = {}
    for row in inputlist:
        for key, val in enumerate(row):
            if val is None:
                output_str += r'\text{{{}}}'.format(
                    str(kwargs.get("nonestring", "None"))
                )
            else:
                # get default
                if np.isscalar(val):
                    temp_str_fmt = "$\\num{{" + fmt.get(
                        key, "{:g}") + "}}$"
                else:
                    temp_str_fmt = fmt.get(key, "{}")
                temp_str = temp_str_fmt.format(val).replace("+", "")
            output_str += temp_str + "&"
        output_str = output_str[:-1]
        output_str += "\\\\\n"
    outputfile.write(output_str)
    if close:
        outputfile.close()
