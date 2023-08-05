import html
import os
import re

import click
import unicodedata
from requests import Session, Response
from humanize import naturalsize


def download(url, filename, progress_data=None, session=None, silent=False):
    """
    Initiate a file download and display the progress

    Args:
        url(str):               Download URL
        filename(str):          Path to save the file to
        progress_data(dict):    Static information to display above the progress bar
        session(Session):       An optional download session to use
        silent(bool):           Download the file, but don't print any output

    Returns:

    """
    # Set up our requests session and make sure the filepath exists
    session = session or Session()
    os.makedirs(os.path.dirname(filename), 0o755, True)

    # Test the connection
    response = session.head(url, allow_redirects=True)  # type: Response
    response.raise_for_status()

    # Get some information about the file we are downloading
    filesize    = naturalsize(response.headers.get('content-length', 0))
    filetype    = response.headers.get('content-type', 'Unknown')

    # Perform a few quick sanity checks
    if not filename:
        raise ValueError('Failed to parse a filename for the download request')

    # Format the information output
    info_lines = [
        click.style('Saving to: ', bold=True) + filename,
        click.style('File type: ', bold=True) + filetype,
        click.style('File size: ', bold=True) + filesize
    ]

    if progress_data:
        for key, value in progress_data.items():
            info_lines.append('{key} {value}'.format(key=click.style(key + ':', bold=True), value=value))

    # Print the static information now
    click.echo()
    for line in info_lines:
        click.echo(line)

    # Now let's make the real download request
    response = session.get(url, allow_redirects=True)  # type: Response

    # Process the download
    with open(filename, 'wb') as file:
        length = int(response.headers.get('content-length'))

        with click.progressbar(response.iter_content(1024), length) as progress:
            for chunk in progress:
                if chunk:
                    file.write(chunk)
                    file.flush()


def sanitize_filename(name):
    """
    Replace reserved characters/names with underscores (windows)

    Args:
        name(str)

    Returns:
        str
    """
    if isinstance(name, int):
        return str(name)

    if os.sep == '/':
        bad_chars = re.compile(r'^\.|\.$|^ | $|^$|\?|:|<|>|\||\*|\"|/')
    else:
        bad_chars = re.compile(r'^\.|\.$|^ | $|^$|\?|:|<|>|/|\||\*|\"|\\')

    bad_names = re.compile(r'(aux|com[1-9]|con|lpt[1-9]|prn)(\.|$)')

    # Unescape '&amp;', '&lt;', and '&gt;'
    name = html.unescape(name)

    # Replace bad characters with an underscore
    name = bad_chars.sub('_', name)
    if bad_names.match(name):
        name = '_' + name

    # Replace newlines with spaces
    name = name.replace("\r", '')
    name = name.replace("\n", ' ')

    # Yavos (?)
    while name.find('.\\') != -1:
        name = name.replace('.\\', '\\')

    name = name.replace('\\', os.sep)

    # Replace tab characters with spaces
    name = name.replace('\t', ' ')

    # Cut to 125 characters
    if len(name) > 125:
        name = name[:125]

    # Remove unicode control characters
    name = ''.join(char for char in name if unicodedata.category(char)[0] != "C")

    return name.strip()
