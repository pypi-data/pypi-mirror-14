"""Wrapper for the Hacker News API

Supports requests for:
  -Stories
  -Comments
  -Users
  -Polls
  -Updates
  -Top
  -New

Author: Rylan Santinon
"""

try:
    # pylint: disable= no-name-in-module, import-error
    import urllib.request as urllib2
except ImportError:
    import urllib2
import time
import json
import logging

from .hnitem import HnItem


class NetworkError(RuntimeError):
    """Runtime errors for http calls and json parsing

    >>> raise NetworkError('foo')
    Traceback (most recent call last):
    NetworkError: foo
    """

    def __init__(self, e):
        super(NetworkError, self).__init__(e)


class HnApi(object):
    '''Connects to HackerNews API and provides the schema'''

    def __init__(self,
                 timeout=35,
                 max_retries=5,
                 backoff_multiplier=0.9):
        self.logger = logging.getLogger(__name__)
        self.backoff_multiplier = backoff_multiplier

        # stop warnings that these are defined outside of __init__
        self.timeout, self.max_retries = 1, 1

        self.set_timeout(timeout)
        self.set_max_retries(max_retries)

    def set_max_retries(self, retries):
        """
        Set the number of retries before failing the HTTP request

        >>> HnApi().set_max_retries(2).max_retries == 2
        True

        >>> HnApi().set_max_retries(0)
        Traceback (most recent call last):
        RuntimeError: Max retries must be 1 or more
        """
        if retries < 1:
            raise RuntimeError("Max retries must be 1 or more")
        self.max_retries = retries
        return self

    def set_timeout(self, timeout):
        """Set the timeout in seconds for the urllib2.urlopen call

        >>> HnApi().set_timeout(3.551).timeout == 3.551
        True

        >>> HnApi().set_timeout(-2)
        Traceback (most recent call last):
        RuntimeError: Timeout must be non-negative
        """
        if timeout < 0:
            raise RuntimeError("Timeout must be non-negative")
        self.timeout = timeout
        return self

    # pylint: disable=line-too-long, invalid-name
    def request(self, url):
        """Request json data from the URL

        >>> j = HnApi().request('https://hacker-news.firebaseio.com/v0/item/1.json')
        >>> j['by'] == 'pg'
        True

        >>> HnApi().request('https://hacker-news.firebaseio.com/v0/foobar/1.json')
        Traceback (most recent call last):
        NetworkError: HTTP Error 401: Unauthorized

        >>> HnApi().request('http://www.yahoo.co.jp') # doctest: +ELLIPSIS
        Traceback (most recent call last):
        NetworkError: ...
        """
        this_try = 0
        ex = RuntimeError()
        while this_try < self.max_retries:
            try:
                sleep_time = self.backoff_multiplier * ((2 ** this_try) - 1)
                self.logger.debug("Sleeping for %s seconds", str(sleep_time))
                time.sleep(sleep_time)
                return self.__request(url)
            except NetworkError as e:
                ex = e
                if "HTTP Error 401" not in str(e):
                    raise e
                else:
                    this_try += 1
        raise ex

    def __request(self, url):
        """Request json data from url without retries"""
        try:
            resp = urllib2.urlopen(url, timeout=self.timeout)
            jsondata = json.loads(resp.read().decode('utf-8'))
            if not jsondata:
                raise NetworkError('When requesting [%s] got nothing' % url)
            return jsondata
        except (urllib2.URLError, ValueError, Exception) as e:
            self.logger.exception(e)
            raise NetworkError(e)
        finally:
            self.logger.debug("Requested %s", url)

    def get_top(self):
        """Request the top stories
        >>> top = HnApi().get_top()
        >>> len(top) > 100
        True
        """
        return self.request('https://hacker-news.firebaseio.com/v0/topstories.json')

    def get_new(self):
        """Request new stories

        >>> HnApi().get_new()[0] > 11448677
        True

        >>> len(HnApi().get_new()) > 100
        True
        """
        return self.request('https://hacker-news.firebaseio.com/v0/newstories.json')

    # pylint: disable=no-self-use, unused-variable
    def _make_item_endpoint(self, item_id):
        """Return the API URL for the given item_id

        >>> HnApi()._make_item_endpoint(1)
        'https://hacker-news.firebaseio.com/v0/item/1.json'

        >>> HnApi()._make_item_endpoint(None)
        Traceback (most recent call last):
        RuntimeError: Parameter None must be an integer

        >>> HnApi()._make_item_endpoint('baz')
        Traceback (most recent call last):
        RuntimeError: Parameter baz must be an integer
        """
        try:
            int(item_id)
        except (TypeError, ValueError) as e:
            raise RuntimeError("Parameter %s must be an integer" % item_id)
        return "https://hacker-news.firebaseio.com/v0/item/" + str(item_id) + ".json"

    def _make_user_endpoint(self, username):
        """Return the API URL for the given username

        >>> HnApi()._make_user_endpoint('pg')
        'https://hacker-news.firebaseio.com/v0/user/pg.json'
        """
        return "https://hacker-news.firebaseio.com/v0/user/" + username + ".json"

    def _build_hnitem(self, item_json):
        """Build an instance of hnitem depending on the type"""
        if not item_json:
            self.logger.debug("Item_json should not be none. Skipping")
            return None
        return HnItem(item_json)

    def get(self, id_or_username):
        """Get an item or user

        >>> HnApi().get('pg').type
        'user'

        >>> HnApi().get('x-name-doesnot-exist').type
        Traceback (most recent call last):
        NetworkError: When requesting [https://hacker-news.firebaseio.com/v0/user/x-name-doesnot-exist.json] got nothing

        >>> HnApi().get(11436228).type
        u'story'

        >>> HnApi().get(0).type
        Traceback (most recent call last):
        NetworkError: When requesting [https://hacker-news.firebaseio.com/v0/item/0.json] got nothing

        >>> HnApi().get({}).type
        Traceback (most recent call last):
        RuntimeError: get should be called with a string or number
        """
        try:
            return self.get_item(int(id_or_username))
        except ValueError:
            return self.get_user(id_or_username)
        except TypeError as e:
            raise RuntimeError('get should be called with a string or number')

    def get_item(self, item_id):
        """Get a particular item by item's id

        >>> it = HnApi().get_item(1)
        >>> it.get_field_by_name('by') == 'pg'
        True
        """
        url = self._make_item_endpoint(item_id)
        story = self.request(url)
        if story != None and story.get("by"):
            by = str(story["by"])
        return self._build_hnitem(story)

    def get_user(self, username):
        """Get a user by username

        >>> u = HnApi().get_user('pg')
        >>> u.get('id') == 'pg'
        True
        """
        url = self._make_user_endpoint(username)
        user = self.request(url)
        return self._build_hnitem(user)

    def get_updates(self):
        """Get recent updates

        See UpdatesItem and UpdatesSchema

        >>> u = HnApi().get_updates()
        >>> len(u.get('profiles')) > 3
        True

        >>> len(u.get('items')) > 3
        True

        >>> n = u.get('items')[0]
        >>> int(n) == n
        True
        """
        url = "https://hacker-news.firebaseio.com/v0/updates.json"
        updates = self.request(url)
        return self._build_hnitem(updates)

    def get_max_item(self):
        """Get max item's id

        Examples
        --------

        >>> itemid = HnApi().get_max_item()
        >>> itemid > 8669130
        True
        """
        url = "https://hacker-news.firebaseio.com/v0/maxitem.json"
        itemid = self.request(url)
        return itemid

    def is_api_item(self, obj):
        '''Returns true iff obj is an HN item

        >>> HnApi().is_api_item({'id':321})
        True

        >>> HnApi().is_api_item(None)
        False

        >>> HnApi().is_api_item({'id':123, 'deleted':'True'})
        True
        '''
        if obj == None:
            return False
        return bool(obj.get('id'))

    def is_valid_item(self, obj):
        '''Returns true iff obj is an undeleted HN item

        >>> HnApi().is_valid_item({'id':123})
        True

        >>> HnApi().is_valid_item(None)
        False

        >>> HnApi().is_valid_item({'id':123, 'deleted':'True'})
        False
        '''
        try:
            return self.is_api_item(obj) and not obj.is_deleted()
        except AttributeError:
            return self.is_api_item(obj) and not obj.get('deleted')

    def is_dead_item(self, obj):
        '''
        Return True iff obj is a dead HN item

        >>> HnApi().is_dead_item({'id':101})
        False

        >>> HnApi().is_dead_item({'id':101, 'dead':'true'})
        True

        >>> HnApi().is_dead_item(None)
        False
        '''
        return bool(self.is_api_item(obj) and obj.get('dead'))

if __name__ == '__main__':
    import doctest
    logging.disable(logging.CRITICAL)
    doctest.testmod()
    logging.disable(logging.NOTSET)
