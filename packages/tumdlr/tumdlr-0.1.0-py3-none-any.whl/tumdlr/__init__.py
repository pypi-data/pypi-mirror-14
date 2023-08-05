import os

import appdirs


# Application metadata
__author__      = "FujiMakoto"
__copyright__   = "Copyright 2016, FujiMakoto"
__license__     = "MIT"
__version__     = "0.1.0"
__maintainer__  = "FujiMakoto"
__email__       = "makoto@makoto.io"
__status__      = "Prototype"


# Global paths
APP_DIR     = os.path.dirname(__file__)
PLUGIN_DIR  = os.path.join(APP_DIR, 'commands')
DATA_DIR    = os.path.join(APP_DIR, 'data')

USER_CONFIG_DIR = appdirs.user_config_dir('tumdlr')
SITE_CONFIG_DIR = appdirs.site_config_dir('tumdlr')

USER_DATA_DIR   = appdirs.user_data_dir('tumdlr')
SITE_DATA_DIR   = appdirs.site_config_dir('tumdlr')

USER_LOG_DIR    = appdirs.user_log_dir('tumdlr')
