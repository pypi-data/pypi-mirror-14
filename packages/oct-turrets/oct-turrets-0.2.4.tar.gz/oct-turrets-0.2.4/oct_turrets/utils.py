import os
import imp
import inspect
import json
import tempfile

from oct_turrets.config import REQUIRED_CONFIG_KEYS
from oct_turrets.exceptions import InvalidConfiguration


def is_test_valid(test_module):
    """Test if the test_module file is valid

    We only check for the transaction class, since the generic transaction
    parent will raise a NotImplemented exception if the run method is not present
    :return: True if the test is valid, else False
    :rtype: bool
    :raises: InvalidTestError
    """
    if not hasattr(test_module, "Transaction"):
        raise Exception("No transaction class found in test script")
    getattr(test_module, "Transaction")
    return True


def load_module(path):
    """Load a single module based on a path on the system

    :param str path: the full path of the file to load as a module
    :return: the module imported
    :rtype: mixed
    :raises: ImportError, InvalidTestError
    """
    if not os.path.exists(path):
        raise ImportError("File does not exists: {}".format(path))
    try:
        module_name = inspect.getmodulename(os.path.basename(path))
        module = imp.load_source(module_name, path)
        if is_test_valid(module):
            return module
        raise Exception("Module not valid")
    except ImportError as e:
        raise Exception("Error importing the tests script {}\nError: {}".format(module_name, e))


def load_file(file_name):
    """Load a single file based on its full path as a module

    :param str filename: the full path of the file
    :return: the module loaded
    :rtype: mixed
    :raises: ImportError, InvalidTestError
    """
    if not os.path.exists(file_name):
        raise ImportError("File does not exists: {}".format(file_name))
    realpath = os.path.realpath(os.path.abspath(file_name))
    return load_module(realpath)


def validate_conf(config_file):
    """Check a configuration file in json format and return the loaded json.
    If a required key is not present in the file or if the file does not exists a InvalidConfiguration exception
    will be raised

    :param str config_file: the full config.json path
    :param str tar: the full tar file path
    :return: the loaded config object
    :rtype: dict
    :raise: InvalidConfig
    """

    # check if the file exists
    if not os.path.isfile(config_file):
        raise InvalidConfiguration("The given configuration file does not exist")

    with open(config_file) as f:
        data = json.load(f)

    for key in REQUIRED_CONFIG_KEYS:
        if key not in data:
            raise InvalidConfiguration("Missing required configuration key %s" % key)

    return data


def extract_tarfile(tar, filename):
    """Extract the needed file from the tar archive in the temp folder and return the file path

    :param tar: the opened tar object
    :param filename str: the name of the file to extract
    """
    path = os.path.join(tempfile.gettempdir(), filename)
    tar.extract(filename, tempfile.gettempdir())
    return path


def clean_tar_tmp(config=None):
    """This method will try to remove temp files from extracted tar
    """

    try:
        os.remove(os.path.join(tempfile.gettempdir(), 'config.json'))
        if config:
            os.remove(os.path.join(tempfile.gettempdir(), config['script']))
    except OSError:
        pass  # files already removed
