import logging
import os
import re
from configparser import ConfigParser

from tumdlr import DATA_DIR, USER_CONFIG_DIR, SITE_CONFIG_DIR


def load_config(name, container=None, default=True):
    """
    Load a configuration file and optionally merge it with another default configuration file

    Args:
        name(str): Name of the configuration file to load without any file extensions
        container(Optional[str]): An optional container for the configuration file
        default(Optional[bool or str]): Merge with a default configuration file. Valid values are False for
            no default, True to use an installed default configuration file, or a path to a config file to use as the
            default configuration

    Returns:
        ConfigParser
    """
    paths = []

    filename = _slugify(name) + '.cfg'
    if container:
        filename = os.path.join(_slugify(container), filename)

    # Load the default configuration (if enabled)
    if default:
        paths.append(os.path.join(DATA_DIR, 'config', filename) if default is True else default)

    # Load the site configuration first, then the user configuration
    paths.append(os.path.join(SITE_CONFIG_DIR, filename))
    paths.append(os.path.join(USER_CONFIG_DIR, filename))

    config = ConfigParser()
    config.read(paths)

    return config


def write_user_config(name, container=None, **kwargs):
    """
    Save a users configuration without losing comments / documentation in the example configuration file

    Args:
        name(str): Name of the configuration file to use
        container(Optional[str]): An optional container for the configuration file
        **kwargs(dict[str, dict]): Configuration parameters

    Returns:
        str: Path to the user configuration file
    """
    log = logging.getLogger('tumdlr.config')

    filename = _slugify(name) + '.cfg'
    if container:
        filename = os.path.join(_slugify(container), filename)
    log.debug('Rendering user configuration file: %s', filename)

    # Generate regular expressions for section tags and key=value assignments
    sect_regexps = {}

    for section, settings in kwargs.items():
        log.debug('Generating regular expression for section `%s`', section)
        sect_regexps[section] = [
            (
                re.compile('^#\s*\[{sect}\]\s*$'.format(sect=re.escape(section)), re.IGNORECASE),
                None
            )
        ]

        for key, value in settings.items():
            log.debug('Generating regular expression for setting `%s` with the value `%s`', key, value)
            sect_regexps[section].append(
                (
                    re.compile('^#\s*{key}\s+=\s+'.format(key=re.escape(key)), re.IGNORECASE),
                    (key, value)
                )
            )

        log.debug('Done generating regular expressions for section `%s`', section)

    # Read the example configuration
    eg_cfg_path = os.path.join(DATA_DIR, 'config', filename + '.example')
    with open(eg_cfg_path, 'r') as file:
        logging.debug('Reading sample configuration file: %s', eg_cfg_path)
        config = file.readlines()

    # Assign the appropriate setting values in the example configuration template
    in_section = None

    for line_no, line in enumerate(config):
        # Are we already in a section, and can we match a setting assignment?
        if in_section:
            for key_regex, kv in sect_regexps[in_section]:
                # Skip the section regex
                if kv is None:
                    continue

                # Does the key match?
                if key_regex.match(line):
                    config[line_no] = "{key} = {value}\n".format(key=kv[0], value=kv[1])

        for section, sect_cfg in sect_regexps.items():
            sect_regex = sect_cfg[0][0]  # type: re.__Regex

            if sect_regex.match(line):
                in_section = section
                config[line_no] = line.lstrip('#')
                break

    os.makedirs(USER_CONFIG_DIR, 0o755, True)
    user_config_path = os.path.join(USER_CONFIG_DIR, filename)

    # Save the configuration
    with open(user_config_path, 'w') as file:
        for line in config:
            file.write(line)

    return user_config_path


def _slugify(string):
    """
    Convert a string to a safe format for file/dir names

    Args:
        string(str)

    Returns:
        str
    """
    string = string.lower().strip()
    string = re.sub('[^\w\s]', '', string)  # Strip non-word characters
    string = re.sub('\s+', '_', string)  # Replace space characters with underscores

    return string
