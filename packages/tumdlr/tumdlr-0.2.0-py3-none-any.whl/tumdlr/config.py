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
    filename = _config_path(name, container)

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

    filename = _config_path(name, container)
    log.debug('Rendering user configuration file: %s', filename)

    # Make sure the user config directory exists
    os.makedirs(USER_CONFIG_DIR, 0o755, True)
    user_config_path = os.path.join(USER_CONFIG_DIR, filename)

    # Generate regular expressions for section tags and key=value assignments
    sect_regexps = _compile_setting_comment_regexps(**kwargs)

    # Read the example configuration
    eg_cfg_path = os.path.join(DATA_DIR, 'config', filename + '.example')
    with open(eg_cfg_path, 'r') as eg_cfg:
        logging.debug('Example configuration opened: %s', eg_cfg.name)

        # Save the configuration
        with open(user_config_path, 'w') as user_cfg:
            logging.debug('User configuration opened: %s', user_cfg.name)

            for line in _parse_example_configuration(eg_cfg, sect_regexps):
                user_cfg.write(line)

    return user_config_path


def _compile_setting_comment_regexps(**kwargs):
    """
    Compile regex substitutions for removing comments and updating setting values from example configuration files

    Args:
        **kwargs(dict[str, dict]): Setting key=values pairs

    Returns:
        dict[str, list[tuple[re.__Regex, str]]]
    """
    log = logging.getLogger('tumdlr.config')
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

    return sect_regexps


def _parse_example_configuration(config, regexps):
    """
    Parse configuration lines against a set of comment regexps

    Args:
        config(_io.TextIOWrapper): Example configuration file to parse
        regexps(dict[str, list[tuple[re.__Regex, str]]]):

    Yields:
        str: Parsed configuration lines
    """
    # What section are we currently in?
    in_section = None

    def iter_regexps(_line):
        nonlocal regexps
        nonlocal in_section

        for section, sect_cfg in regexps.items():
            sect_regex = sect_cfg[0][0]  # type: re.__Regex

            if sect_regex.match(line):
                in_section = section
                return line.lstrip('#')

        raise RuntimeError('No section opening regexps matched')

    def iter_section_regexps(_line):
        nonlocal regexps
        nonlocal in_section

        for key_regex, kv in regexps[in_section]:
            # Skip the section regex
            if kv is None:
                continue

            # Does the key match?
            if key_regex.match(_line):
                return "{key} = {value}\n".format(key=kv[0], value=kv[1])

        raise RuntimeError('No key=value regexps matched')

    for line in config:
        # Are we in a section yet?
        if in_section:
            try:
                yield iter_section_regexps(line)
            except RuntimeError:
                # No key=value match? Are we venturing into a new section?
                try:
                    yield iter_regexps(line)
                except RuntimeError:
                    # Still nothing? Return the unprocessed line then
                    yield line
        # Not in a section yet? Are we venturing into our first one then?
        else:
            try:
                yield iter_regexps(line)
            except RuntimeError:
                # Not yet? Return the unprocessed line then
                yield line


def _config_path(name, container=None):
    """
    Convert a config name to a safe format for file/dir names

    Args:
        name(str): Configuration filename without the .cfg extension
        container(Optional[str]): Configuration container

    Returns:
        str
    """
    def slugify(string):
        string = string.lower().strip()
        string = re.sub('[^\w\s]', '', string)  # Strip non-word characters
        return re.sub('\s+', '_', string)  # Replace space characters with underscores

    filename = slugify(name) + '.cfg'

    return os.path.join(slugify(container), filename) if container else filename
