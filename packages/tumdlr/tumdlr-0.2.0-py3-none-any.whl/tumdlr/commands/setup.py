import os

import click

from tumdlr.config import write_user_config
from tumdlr.main import pass_context


# noinspection PyIncorrectDocstring,PyUnusedLocal
@click.command('setup', short_help='(Re-)run the setup and configuration for Tumdlr')
@click.option('-p', '--path', help='Path to save Tumdlr downloads to', default=os.path.expanduser('~/tumblr'),
              prompt='Where would you like your downloads to be saved? ',
              type=click.Path(file_okay=False, writable=True, resolve_path=True))
@click.option('--images/--skip-images', help='Toggles the downloading of image posts', default=True,
              prompt='Do you want to save photo posts?')
@click.option('--videos/--skip-videos', help='Toggles the downloading of video posts', default=True,
              prompt='Do you want to save video posts?')
@click.option('--pause/--no-pause', default=True,
              help='Toggles the brief pause between downloads to prevent traffic flooding, which may be detected as '
                   'abuse by Tumblr and result in blocked connections')
@pass_context
def cli(ctx, path, images, videos, pause):
    """
    Sets Tumdlr up for use after a fresh installation or reconfigures the settings of an existing installation.
    """
    config = {
        'Tumdlr': {
            'SavePath': path,
            'SavePhotos': images,
            'SaveVideos': videos
        },
        'Development': {
            'AgreedToTerms': True
        }
    }

    click.echo('Writing user configuration...')
    path = write_user_config('tumdlr', None, **config)
    click.echo('Configuration written to {}'.format(path))

    return path
