import logging
import os
import urllib
from pathlib import Path

import click
from requests import Session

from tumdlr.main import pass_context
from tumdlr.api import TumblrBlog, TumblrPhotoSet
from tumdlr.containers import TumblrPost
from tumdlr.downloader import download, sanitize_filename


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

    # Construct the save basedir
    basedir = Path(ctx.config['Tumdlr']['SavePath'])

    if ctx.config['Categorization']['User']:
        log.debug('Categorizing by user: %s', tumblr.name)
        basedir = basedir.joinpath(sanitize_filename(tumblr.name))

    log.debug('Basedir constructed: %s', basedir)

    for post in tumblr.posts():  # type: TumblrPost
        # Generic data
        progress_data = {
            'Progress': '{cur} / {total} posts processed'.format(cur=progress, total=tumblr.post_count),
            'Type': post.type.title(),
            'Post Date': post.post_date,
            'Tags': post.tags
        }

        # Are we downloading a photo post?
        if post.is_photo:
            assert isinstance(post, TumblrPhotoSet)

            # Construct our filepath
            post_basedir = Path(basedir)
            if ctx.config['Categorization']['PostType']:
                log.debug('Categorizing by type: photos')
                post_basedir = post_basedir.joinpath(post_basedir, 'photos')

            total_photos = len(post.photos)
            is_photoset = (total_photos > 1)
            if is_photoset and ctx.config['Categorization']['Photosets']:
                log.debug('Categorizing by photoset: %s', post.id)
                post_basedir = post_basedir.joinpath(sanitize_filename(post.id))

            progress_data['Caption'] = post.title

            session = Session()
            session.headers.update({'referer': urllib.parse.quote(post.url.as_string())})

            for page_no, photo in enumerate(post.photos, 1):
                filepath = Path(post_basedir)

                # Prepend the page number for photosets
                if is_photoset:
                    filepath = filepath.joinpath(sanitize_filename('p{pn}_{pt}'.format(pn=page_no, pt=post.title)))
                    progress_data['Photoset Page'] = '{cur} / {tot}'.format(cur=page_no, tot=total_photos)
                else:
                    filepath = filepath.joinpath(sanitize_filename(post.title))

                # Work out the file extension
                filepath = str(filepath) + os.path.splitext(photo.url.as_string())[1]

                download(photo.url.as_string(), filepath, progress_data, session)

        progress += 1
