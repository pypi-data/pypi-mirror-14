import urllib

from requests import Session, Response
from yurl import URL

from tumdlr import __version__
from tumdlr.containers import TumblrPost, TumblrPhotoSet


class TumblrBlog:

    def __init__(self, url, session=None):
        """
        Tumblr blog

        Args:
            url(URL|str): Tumblr profile URL
            session(Optional[Session]): An optional custom Requests session
        """
        self._url = url if isinstance(url, URL) else URL(url)
        self._api_url = URL(scheme='https', host='api.tumblr.com', path='/v2/')
        self._api_response = None  # type: Response

        if not session:
            session = Session()
            session.headers.update({
                'Referer': urllib.parse.quote(self._url.as_string()),
                'User-Agent': 'tumdlr/{v}'.format(v=__version__)
            })

        self.session = session

        self.title          = None  # type: str
        self.url            = None  # type: URL
        self.name           = None  # type: str
        self.description    = None  # type: str
        self.is_nsfw        = None  # type: bool
        self.likes          = None  # type: int|False
        self.post_count     = None  # type: int
        self.updated        = None  # type: int

        self._posts = []
        self.offset = 0

        self._api_url = self._api_url.replace(
            path=self._api_url.path + 'blog/{host}/posts'.format(host=self._url.host)
        )
        self._api_get()

    def _api_get(self, query=None, parse=True):
        """
        Execute an API query

        Args:
            query(Optional[str]): Extra query parameters
            parse(Optional[bool]): Parse the API response immediately
        """
        endpoint = self._api_url.replace(
            query='api_key=fuiKNFp9vQFvjLNvx4sUwti4Yb5yGutBN4Xh10LXZhhRKjWlV4&filter=text&offset={}'.format(self.offset)
        )

        response = self.session.get(endpoint.as_string())  # type: Response
        response.raise_for_status()

        self._api_response = response
        if parse:
            self._api_parse_response()

    def _api_parse_response(self):
        """
        Parse an API response

        """
        blog = self._api_response.json()['response']['blog']

        self.title          = blog['title']
        self.url            = URL(blog['url'])
        self.name           = blog['name']
        self.description    = blog['description']
        self.is_nsfw        = blog['is_nsfw']
        self.likes          = blog.get('likes', False)  # Returned only if sharing of likes is enabled
        self.post_count     = blog['posts']
        self.updated        = blog['updated']

        posts = self._api_response.json()['response']['posts']

        for post in posts:
            if post['type'] in ['photo', 'link']:
                self._posts.append(TumblrPhotoSet(post, self))
                continue

            self._posts.append(TumblrPost(post, self))

    def posts(self):
        """
        Yields:
            TumblrPost
        """
        while True:
            # Out of posts?
            if not self._posts:
                # Do we have any more to query?
                self._api_get()

                if not self._posts:
                    # Nope, we've queried everything, break now
                    break

            # Pop our next post and increment the offset
            post = self._posts.pop(0)
            self.offset += 1

            yield post
