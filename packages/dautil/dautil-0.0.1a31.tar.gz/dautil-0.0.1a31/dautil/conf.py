""" This module contains configuration utilities. """
import json
import os


FJSON = 'dautil.json'


def file_exists(tocheck):
    """ Checks whether a file exists.

    :param tocheck: The path of the file.

    :returns: True if the file exists.
    """
    return os.path.isfile(tocheck)


def read_rc():
    """ Reads a configuration file in the JSON format.

    :returns: A dictionary representing the contents \
        of the configuration file.
    """
    old = None

    if file_exists(FJSON):
        with open(FJSON) as json_file:
            old = json.load(json_file)

    return old


def update_rc(key, updates):
    """ Updates the JSON configuration file.

    :param key: The key of the record to update.
    :param updates: Values with which to update the relevant record.
    """
    config = {key: updates}
    old = read_rc()

    if old:
        old.update(config)
        config = old

    with open(FJSON, 'w') as json_file:
        json.dump(config, json_file, indent=4, sort_keys=True)
