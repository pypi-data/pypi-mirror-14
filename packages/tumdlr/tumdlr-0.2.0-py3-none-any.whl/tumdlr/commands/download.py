import logging
import urllib
from collections import OrderedDict

import click
from requests import Session

from tumdlr.api import TumblrBlog
from tumdlr.errors import TumdlrDownloadError
from tumdlr.main import pass_context


# noinspection PyIncorrectDocstring,PyUnusedLocal
@click.command('download', short_help='Download posts from a Tumblr account')
@click.argument('URL')
@click.option('--images/--skip-images', help='Toggles the downloading of image posts', default=True, envvar='IMAGES')
@click.option('--videos/--skip-videos', help='Toggles the downloading of video posts', default=True, envvar='VIDEOS')
@pass_context
def cli(ctx, url, images, videos):
    """
    Download posts from a Tumblr account.
    """
    log = logging.getLogger('tumdlr.commands.downloader')
    log.info('Starting a new download session for %s', url)

    # Get our post information
    tumblr = TumblrBlog(url)
    progress = 0

    for post in tumblr.posts():  # type: TumblrPost
        # Generic data
        progress_data = OrderedDict([
            ('Progress', '{cur} / {total} posts processed'.format(cur=progress, total=tumblr.post_count)),
            ('Type', post.type.title()),
            ('Post Date', post.post_date),
            ('Tags', post.tags)
        ])

        session = Session()
        session.headers.update({'referer': urllib.parse.quote(post.url.as_string())})

        for file in post.files:
            try:
                file.download(ctx, session=session, progress_data=progress_data)
            except TumdlrDownloadError:
                click.echo('File download failed, skipping', err=True)

        progress += 1
