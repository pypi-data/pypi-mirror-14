import logging

from yurl import URL


class TumblrPost:

    def __init__(self, post, blog):
        """
        Args:
            post(dict): API response
            blog(tumdlr.api.blog.TumblrBlog): Parent blog
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

        self._classes = []
        self._parse_post()

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

    def __init__(self, post, blog):
        """
        Args:
            post(dict): API response
            blog(tumdlr.api.blog.TumblrBlog): Parent blog
        """
        self.log = logging.getLogger('tumdlr.containers.post')

        self.title  = None
        self.photos = []

        super().__init__(post, blog)

    def _parse_post(self):
        super()._parse_post()
        self.title  = self._post.get('caption', self._post.get('title'))  # title else summary else id

        for photo in self._post.get('photos', ()):
            best_size = photo.get('original_size') or max(photo['alt_sizes'], key='width')
            self.photos.append(TumblrPhoto(best_size, self))

    def __repr__(self):
        return "<TumblrPhotoSet title='{title}' id='{id}' photos='{count}'>"\
            .format(title=self.title.split("\n")[0].strip(), id=self.id, count=len(self.photos))

    def __str__(self):
        return self.url.as_string()

    @property
    def first(self):
        """
        Fetch the first photo in a photoset (or the only photo in a single)

        Returns:
            TumblrPhoto or None
        """
        return self.photos[-1] if self.photos else None


class TumblrPhoto:

    def __init__(self, photo, photoset):
        """
        Args:
            photo(dict): Photo API data
            photoset(TumblrPhotoSet): Parent container
        """
        self._photo = photo
        self.photoset = photoset

        self.width  = photo.get('width')
        self.height = photo.get('height')
        self.url    = URL(photo['url'])

    def __repr__(self):
        return "<TumblrPhoto url='{url}' width='{w}' height='{h}'>".format(url=self.url, w=self.width, h=self.height)

    def __str__(self):
        return self.url.as_string()
