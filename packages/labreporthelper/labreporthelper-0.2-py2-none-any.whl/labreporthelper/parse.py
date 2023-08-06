"""
Helper module to parse data
"""
import numpy as np


def getdata(inputfile, argnum=None, close=False):
    """
    Get data from the .dat files

    args:
        inputfile: file
            Input File
        close: bool, default=False
            Closes inputfile if True
        inputfile (File): Input file
        close (boolean): Closes inputfile if True (default: False)
    returns:
        dictionary:
            data: list of parsed data
            variables: dictionary of errors and other additional variables
    """
    # get data and converts them to list
    # outputtype - list, dict, all
    output = []
    add_data = {}
    line_num = 0
    for line in inputfile:
        line_num += 1
        if ("#" not in line) and (line != ""):
            linesplit = line.split()
            if argnum is not None and len(linesplit) != int(argnum):
                raise ValueError(
                    "Line {:d} has {:d} arguments (need {:d})".format(
                        line_num, len(linesplit), argnum))
            output.append(linesplit)
        # additional float variable
        if "#f" in line:
            data = line.split()[1].split("=")
            add_data[data[0]] = float(data[1])
        # additional list float variable
        if "#l" in line:
            data = line.split()[1].split("=")
            add_data[data[0]] = [float(e) for e in data[1].split(",")]
    if close:
        inputfile.close()
    output = cleandata(output)
    return {
        "data": np.array(output),
        "variables": add_data,
    }


def cleandata(inputlist):
    """
    Helper function for parse.getdata.
    Remove empty variables, convert strings to float

    args:
        inputlist: list
            List of Variables
    Returns:
        ouput:
            Cleaned list
    """
    output = []
    for e in inputlist:
        new = []
        for f in e:
            if f == "--":
                new.append(None)
            else:
                new.append(float(f))
        output.append(new)
    return output
