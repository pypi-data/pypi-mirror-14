import logging
import os
import sys
from os.path import expanduser, expandvars, join, sep, exists
from shutil import copyfile

from configobj import ConfigObj, interpolation_engines, flatten_errors
from validate import Validator


def _file_exists_or_die(path):
    """
    Check if the file exists or exit with error

    :param path: The file path
    :return: The file path
    """
    path = expandvars(expanduser(path))
    if path is not None:
        if not exists(path):
            logging.error("File '{}' not found".format(path))
            sys.exit(-1)
    return path


def _file_none_exists_or_die(path):
    """
    Check if the file exists or it's None

    :param path: The file path
    :return: The file path
    """
    if path is None:
        return None
    return _file_exists_or_die(path)


def _file_name(file):
    """
    Return the base filename of a path without the extensions.

    :param file: The file path
    :return: The base name without extensions
    """

    if file is None:
        return None
    return os.path.basename(file).split('.')[0]


def _get_home_folder(config_namespace):
        """
        Returns the home config folder. You can define this folder using the
        system variable [NAMESPACE]_HOME or it defaults to ~/.[namespace]

        :return: The BBGLAB config folder.
        """
        home_folder = expandvars(expanduser(os.getenv("{}_HOME".format(config_namespace.upper()), "~/.{}/".format(config_namespace.lower()))))
        home_folder = home_folder.rstrip(os.path.sep)

        return join(sep, home_folder)


def _get_config_file(config_namespace, config_name, config_template):
        """
        Returns default config location.

        First check if it exists in the running folder, second if exists in the home
        config folder and if it's not there create it using the template.

        :return: The path to the config file
        """

        file_name = "{}.conf".format(config_name)
        home_folder = _get_home_folder(config_namespace)
        file_path = file_name

        # Check if the configuration file exists in current folder
        if exists(file_path):
            return file_path

        # Check if exists in the default configuration folder
        file_path = join(home_folder, file_name)
        if exists(file_path):
            return file_path

        # Otherwise, create the configuration file from the template
        if not exists(home_folder):
            os.makedirs(home_folder)

        copyfile(config_template, file_path)

        return file_path


class BGConfig(ConfigObj):

    def __init__(self, config_template, config_name=None, config_file=None, config_spec=None, config_namespace="bbglab", strict=True, use_bgdata=True):

        if use_bgdata:
            from bgdata.configobj import BgDataInterpolation
            interpolation_engines['bgdata'] = BgDataInterpolation

        if config_name is None:
            config_name = _file_name(config_template)

        if config_file is None:
            config_file = _get_config_file(config_namespace, config_name, config_template)

        if not exists(config_file):
            raise FileExistsError("Config file {} not found".format(config_file))

        if config_spec is None:
            config_spec = config_template + ".spec"

            if not os.path.exists(config_spec):
                raise ValueError("You need to create a spec file here: {}".format(config_spec))

        super().__init__(config_file, configspec=config_spec, interpolation="bgdata")

        res = self.validate(Validator(), preserve_errors=True)
        for section_list, key, error in flatten_errors(self, res):

            if key is not None:
                section_list.append(key)
            else:
                section_list.append('[missing section]')
            section_string = ' > '.join(section_list)

            if not error:
                error = 'Missing value or section.'

            logging.error("Config error at {} = {}".format(section_string, error))

        if strict and res != True:
            raise ValueError("The config file '{}' has errors.".format(config_file))
