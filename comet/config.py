# -*- coding: utf-8 -*-
"""
Module containing the logic associated with passing configuration
between the different functions of comet as well as loading and
saving it.
"""

import click
import os
import configparser

APP_NAME = 'comet'

class Config(object):
    """
    Holds configuration and is passed between functions of comet.
    """
    def __init__(self):
        self.data_folder = os.path.join(click.get_app_dir(APP_NAME), 'data')
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
        self.conf_file = os.path.join(click.get_app_dir(APP_NAME), 'comet.ini')


    def read_conf(self, path):
        if path is not None:
            self.conf_file = path;
        parser = configparser.RawConfigParser()
        parser.read(self.conf_file)
        for section in parser.sections():
            for key, value in parser.items(section):
                if section == APP_NAME:
                    setattr(self, key, value)
                else:
                    if getattr(self, section) is None:
                        setattr(self, section, {})
                    setattr(self.section, key, value)


    def write_conf(self, path):
        print(path)
        if path is None:
            path = self.conf_file
        config = configparser.ConfigParser()
        config[APP_NAME] = {}
        for state in [a for a in dir(self) if not a.startswith('__')
                      and not callable(getattr(self, a)) and a != 'conf_file']:
            config[APP_NAME][state] = str(getattr(self, state))
        folder = os.path.dirname(path)
        if folder == '':
            folder = './'
        if not os.path.exists(folder):
            os.makedirs(os.path.dirname(path))
        with open(path, 'w') as file:
            config.write(file)


pass_config = click.make_pass_decorator(Config, ensure=True)
