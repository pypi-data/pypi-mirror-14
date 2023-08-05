import logging
import os
from hashlib import md5
from pathlib import Path

from youtube_dl import YoutubeDL
from yurl import URL

from tumdlr.downloader import sanitize_filename, download
from tumdlr.errors import TumdlrDownloadError, TumdlrParserError


class TumblrPost:
    """
    This is the base container class for all Tumblr post types. It contains data that is always available with any
    type of post.

    Additional supported post types may extend this class to provide additional metadata parsing
    """
    def __init__(self, post, blog):
        """
        Args:
            post(dict): API response
            blog(tumdlr.api.TumblrBlog): Parent blog
        """
        self._post = post
        self.blog = blog
        self.log = logging.getLogger('tumdlr.containers.post')

        self.id         = None  # type: int
        self.type       = None  # type: str
        self.url        = None  # type: URL
        self.tags       = set()
        self.post_date  = None  # type: str
        self.note_count = None  # type: int

        self.files = []

        try:
            self._parse_post()
        except Exception as e:
            self.log.warn('Failed to parse post data: %r', self, exc_info=e)
            raise TumdlrParserError(post_data=post)

    @property
    def is_text(self):
        """
        Returns:
            bool
        """
        return self.type == 'text'

    @property
    def is_photo(self):
        """
        Returns:
            bool
        """
        return self.type in ['photo', 'link']

    @property
    def is_video(self):
        """
        Returns:
            bool
        """
        return self.type == 'video'

    def _parse_post(self):
        self.id         = self._post['id']
        self.type       = self._post['type']
        self.url        = URL(self._post['post_url']) if 'post_url' in self._post else None
        self.tags       = set(self._post.get('tags', []))
        self.note_count = self._post.get('note_count')
        self.post_date  = self._post['date']

    def __repr__(self):
        return "<TumblrPost id='{id}' type='{type}' url='{url}'>"\
            .format(id=self.id, type=self.type, url=self.url)

    def __str__(self):
        return self.url.as_string() if self.url else ''


class TumblrPhotoSet(TumblrPost):
    """
    Container class for Photo and Photo Link post types
    """
    def __init__(self, post, blog):
        """
        Args:
            post(dict): API response
            blog(tumdlr.api.blog.TumblrBlog): Parent blog
        """
        self.log = logging.getLogger('tumdlr.containers.post')
        super().__init__(post, blog)

    def _parse_post(self):
        """
        Parse all available photos using the best image sizes available
        """
        super()._parse_post()
        self.title  = self._post.get('caption', self._post.get('title'))

        photos = self._post.get('photos', [])
        is_photoset = (len(photos) > 1)

        for page_no, photo in enumerate(photos, 1):
            best_size = photo.get('original_size') or max(photo['alt_sizes'], key='width')
            best_size['page_no'] = page_no if is_photoset else False
            self.files.append(TumblrPhoto(best_size, self))

    def __repr__(self):
        return "<TumblrPhotoSet title='{title}' id='{id}' photos='{count}'>"\
            .format(title=self.title.split("\n")[0].strip(), id=self.id, count=len(self.files))


class TumblrVideoPost(TumblrPost):
    """
    Container class for Video post types
    """
    def __init__(self, post, blog):
        """
        Args:
            post(dict): API response
            blog(tumdlr.api.blog.TumblrBlog): Parent blog
        """
        self.log = logging.getLogger('tumdlr.containers.post')

        self.title          = None
        self.description    = None
        self.duration       = None
        self.format         = None

        super().__init__(post, blog)

    def _parse_post(self):
        """
        Parse all available photos using the best image sizes available
        """
        super()._parse_post()

        video_info = YoutubeDL().extract_info(self.url.as_string(), False)

        self.title = video_info.get('title')

        self.description    = video_info.get('description')
        self.duration       = int(video_info.get('duration', 0))
        self.format         = video_info.get('format', 'Unknown')

        self.files.append(TumblrVideo(video_info, self))

    def __repr__(self):
        return "<TumblrVideoPost id='{id}'>".format(id=self.id)


class TumblrFile:
    """
    This is the base container class for all downloadable resources associated with Tumblr posts.
    """

    CATEGORY = 'misc'

    def __init__(self, data, container):
        """
        Args:
            data(dict): API response data
            container(TumblrPost): Parent container
        """
        self.log = logging.getLogger('tumdlr.containers.file')

        self._data      = data
        self.container  = container
        self.url        = URL(self._data.get('url', self._data.get('post_url')))

    def download(self, context, **kwargs):
        """
        Args:
            context(tumdlr.main.Context): CLI request context
            kwargs(dict): Additional arguments to send with the download request

        Returns:
            str: Path to the saved file
        """
        try:
            download(self.url.as_string(), str(self.filepath(context, kwargs)), **kwargs)
        except Exception as e:
            self.log.warn('Post download failed: %r', self, exc_info=e)
            raise TumdlrDownloadError(error_message=str(e), download_url=self.url.as_string())

    def filepath(self, context, request_data):
        """
        Args:
            context(tumdlr.main.Context): CLI request context
            request_data(Optional[dict]): Additional arguments to send with the download request

        Returns:
            Path
        """
        # Construct the save basedir
        basedir = Path(context.config['Tumdlr']['SavePath'])

        # Are we categorizing by user?
        if context.config['Categorization']['User']:
            self.log.debug('Categorizing by user: %s', self.container.blog.name)
            basedir = basedir.joinpath(sanitize_filename(self.container.blog.name))

        # Are we categorizing by post type?
        if context.config['Categorization']['PostType']:
            self.log.debug('Categorizing by type: %s', self.CATEGORY)
            basedir = basedir.joinpath(self.CATEGORY)

        self.log.debug('Basedir constructed: %s', basedir)

        return basedir


class TumblrPhoto(TumblrFile):

    CATEGORY = 'photos'

    def __init__(self, photo, photoset):
        """
        Args:
            photo(dict): Photo API data
            photoset(TumblrPhotoSet): Parent container
        """
        super().__init__(photo, photoset)

        self.width   = self._data.get('width')
        self.height  = self._data.get('height')
        self.page_no = self._data.get('page_no', False)

    def filepath(self, context, request_data):
        """
        Get the full file path to save the downloaded file to

        Args:
            context(tumdlr.main.Context): CLI request context
            request_data(Optional[dict]): Additional arguments to send with the download request

        Returns:
            Path
        """
        assert isinstance(self.container, TumblrPhotoSet)
        filepath = super().filepath(context, request_data)

        request_data['progress_data']['Caption'] = self.container.title

        # Are we categorizing by photosets?
        if self.page_no and context.config['Categorization']['Photosets']:
            self.log.debug('Categorizing by photoset: %s', self.container.id)
            filepath = filepath.joinpath(sanitize_filename(str(self.container.id)))

        # Prepend the page number for photosets
        if self.page_no:
            filepath = filepath.joinpath(sanitize_filename('p{pn}_{pt}'.format(pn=self.page_no,
                                                                               pt=self.container.title)))
            request_data['progress_data']['Photoset Page'] = '{cur} / {tot}'\
                .format(cur=self.page_no, tot=len(self.container.files))
        else:
            filepath = filepath.joinpath(sanitize_filename(self.container.title))

        # Work out the file extension and return
        return str(filepath) + os.path.splitext(self.url.as_string())[1]

    def __repr__(self):
        return "<TumblrPhoto url='{url}' width='{w}' height='{h}'>".format(url=self.url, w=self.width, h=self.height)

    def __str__(self):
        return self.url.as_string()


class TumblrVideo(TumblrFile):

    CATEGORY = 'videos'

    def __init__(self, video, vpost):
        """
        Args:
            video(dict): Video API data
            vpost(TumblrVideoPost): Parent container
        """
        super().__init__(video, vpost)

    def filepath(self, context, request_data):
        """
        Get the full file path to save the video to

        Args:
            context(tumdlr.main.Context): CLI request context
            request_data(Optional[dict]): Additional arguments to send with the download request

        Returns:
            Path
        """
        assert isinstance(self.container, TumblrVideoPost)
        filepath = super().filepath(context, request_data)

        minutes  = int(self.container.duration / 60)
        seconds  = self.container.duration % 60
        duration = '{} minutes {} seconds'.format(minutes, seconds) if minutes else '{} seconds'.format(seconds)

        if self.container.title:
            request_data['progress_data']['Title'] = self.container.title

        request_data['progress_data']['Description'] = self.container.description
        request_data['progress_data']['Duration'] = duration
        request_data['progress_data']['Format'] = self.container.format

        filepath = filepath.joinpath(sanitize_filename(
            self.container.description or
            md5(self.url.as_string().encode('utf-8')).hexdigest())
        )

        # Work out the file extension and return
        return '{}.{}'.format(str(filepath), self._data.get('ext', 'mp4'))

    def __repr__(self):
        return "<TumblrVideo id='{i}'>".format(i=self.container.id)

    def __str__(self):
        return self.url.as_string()
