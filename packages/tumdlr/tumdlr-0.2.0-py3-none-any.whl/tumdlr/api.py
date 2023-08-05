import urllib

from requests import Session
from yurl import URL

from tumdlr import __version__
from tumdlr.containers import TumblrPost, TumblrPhotoSet, TumblrVideoPost
from tumdlr.errors import TumdlrParserError


class TumblrBlog:

    def __init__(self, url, session=None, **kwargs):
        """
        Tumblr blog

        Args:
            url(URL|str): Tumblr profile URL
            session(Optional[Session]): An optional custom Requests session

        Keyword Args:
            api_key(str): Tumblr API key
            uagent(str): Custom User-Agent header
        """
        self._url = url if isinstance(url, URL) else URL(url)
        self._api_url = URL(scheme='https', host='api.tumblr.com', path='/v2/')
        self._api_response = None  # type: Response
        self._api_key = kwargs.get('api_key', 'fuiKNFp9vQFvjLNvx4sUwti4Yb5yGutBN4Xh10LXZhhRKjWlV4')
        self._uagent = kwargs.get('user_agent', 'tumdlr/{version}')

        if not session:
            session = Session()
            session.headers.update({
                'Referer': urllib.parse.quote(self._url.as_string()),
                'User-Agent': self._uagent.format(version=__version__)
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
            query(Optional[dict]): Extra query parameters
            parse(Optional[bool]): Parse the API response immediately
        """
        # Parse extra query parameters
        query_extra = []

        if query:
            for key, value in query.items():
                query_extra.append(
                    '{key}={value}'.format(
                        key=urllib.parse.quote(key),
                        value=urllib.parse.quote(value)
                    )
                )

        # Only prepend an ampersand if we have extra attributes, otherwise default to an empty string
        if query_extra:
            query_extra = '&' + '&'.join(query_extra)
        else:
            query_extra = ''

        endpoint = self._api_url.replace(
            query='api_key={api_key}&filter=text&offset={offset}{extra}'.format(
                api_key=self._api_key, offset=self.offset, extra=query_extra
            )
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
            try:
                if post['type'] in ['photo', 'link']:
                    self._posts.append(TumblrPhotoSet(post, self))
                    continue
                elif post['type'] == 'video':
                    self._posts.append(TumblrVideoPost(post, self))
                    continue

                self._posts.append(TumblrPost(post, self))
            except TumdlrParserError:
                continue

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
