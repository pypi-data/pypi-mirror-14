# coding: utf-8;
"""
Configuration file handling.
"""
import os

try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser


def get_path():
    return "config.cfg"
#    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "eagle.conf")
#    if not os.path.exists(path):
#        path = os.getenv('EAGLE_CONFIG')
#    if path is None:
#        XDG_CONFIG_HOME = os.environ.get("XDG_CONFIG_HOME",
#            os.path.join(os.path.expanduser("~"), ".config"))
#        path = os.path.join(XDG_CONFIG_HOME, "eagle.conf")
#    if not os.path.exists(path):
#        raise IOError("No configuration file found at {0}".format(path))
#    return path


def parse(path=None):
    """
    Read the configuration and return a populated ConfigParser object.

    Places to look for the configuration file, in order:
    * configuration file specified by the EAGLE_CONFIG
      environment variable.
    * $XDG_CONFIG_HOME/eagle.conf
    * ~/.config/eagle.conf

    The first file that is encountered is used.
    """
    if not path:
        path = get_path()
    config = ConfigParser()
    config.read(path)
    return config
