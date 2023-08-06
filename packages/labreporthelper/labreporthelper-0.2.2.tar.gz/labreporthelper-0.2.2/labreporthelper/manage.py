"""
Processes commands from user
"""
import os
import sys
import json
import importlib


ENV_VAR_SETTINGS = "LAB_SETTINGS"
ENV_VAR_ROOT_DIR = "LAB_ROOT_DIR"
FILEPATHSTR = "{root_dir}{os_sep}{folder}{os_sep}{name}{os_extsep}{ext}"


def generate_datasets_list(settings, argv):
    """
    generate datasets list to activate

    args:
        settings: dictionary
            from settings file
        argv: list
            from sys.argv
    """
    datasets_string_list = settings["DATASETS_LIST"]
    datasets_list = []
    if len(argv) == 2:
        try:
            datasets_items = datasets_string_list.iteritems()
        except AttributeError:
            datasets_items = datasets_string_list.items()
        for key, val in datasets_items:
            key_module = importlib.import_module(
                settings["PYTHON_MODULE"] + "." + key
            )
            for element in val:
                datasets_list.append(
                    (key, element, getattr(key_module, element)())
                )
    elif len(argv) > 2:
        arguments = argv[2:]
        for argument in arguments:
            argument_list = argument.split(".")
            key = ".".join(argument_list[:-1])
            key_module = importlib.import_module(
                settings["PYTHON_MODULE"] + "." + key
            )
            datasets_list.append(
                (key, argument_list[-1],
                 getattr(key_module, argument_list[-1])())
            )
    else:
        print_help()
    return datasets_list

def make_data_file(datasets_list, argv):
    """
    generate the data file
    """
    for datasets in datasets_list:
        datasets[2].create_dat_file()

def parse_data(datasets_list, argv):
    """
    parse data to pickle/hickle
    """
    for datasets in datasets_list:
        datasets[2].parse_data_to_internal()

def do_operations(datasets_list, argv):
    """
    do operations
    """
    for datasets in datasets_list:
        datasets[2].operations()

def print_help():
    """
    Usage: python [options] [arguments] ...
    options:
        make-data-file: make data file for all
        datasets-list in the arguments, or all datasets_list
        in settings.json file if no arguments given

        parse-data: parse data to pickle/hickle folder

        do-operations: do operations method on the datasets

    arguments:
        filename.classname ... -- loop through all selected
    """
    print print_help.__doc__
    sys.exit(0)

def manage(settingspath, root_dir, argv):
    """
    Manage all processes
    """
    # add settings.json to environment variables
    os.environ[ENV_VAR_SETTINGS] = settingspath
    # add root_dir
    os.environ[ENV_VAR_ROOT_DIR] = root_dir
    # get datasets list
    with open(settingspath) as settings_file:
        settings = json.load(settings_file)
    # manage args
    datasets_list = generate_datasets_list(settings, argv)
    if "make-data-file" == argv[1]:
        make_data_file(datasets_list, argv)
    elif "parse-data" == argv[1]:
        parse_data(datasets_list, argv)
    elif "do-operations" == argv[1]:
        do_operations(datasets_list, argv)
    else:
        print_help()
