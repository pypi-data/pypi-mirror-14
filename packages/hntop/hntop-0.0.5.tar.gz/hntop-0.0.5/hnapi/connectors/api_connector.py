"""
Wrapper for the Hacker News API
Supports requests for:
  -Story items
  -Users

Author: Rylan Santinon
"""

try:
    #pylint: disable= no-name-in-module, import-error
    import urllib.request as urllib2
except ImportError:
    import urllib2
import time
import json
import logging
from ..items.storyitem import StoryItem
from ..items.useritem import UserItem
from ..items.updatesitem import UpdatesItem
from ..items.commentitem import CommentItem
from ..items.pollitem import PollItem

class NetworkError(RuntimeError):
    """Runtime errors for http calls and json parsing

    >>> raise NetworkError('foo')
    Traceback (most recent call last):
    NetworkError: foo
    """
    def __init__(self, e):
        super(NetworkError, self).__init__(e)

class ApiConnector(object):
    '''Connects to HackerNews API and provides the schema'''
    def __init__(self):
        self.user_dict = {}
        self.logger = logging.getLogger(__name__)
        self.timeout = 35
        self.max_retries = 5
        self.backoff_multiplier = 0.9

    def set_max_retries(self, retries):
        """
        Set the number of retries before failing the HTTP request

        >>> ApiConnector().set_max_retries(2).max_retries == 2
        True

        >>> ApiConnector().set_max_retries(0)
        Traceback (most recent call last):
        RuntimeError: Max retries must be 1 or more
        """
        if retries < 1:
            raise RuntimeError("Max retries must be 1 or more")
        self.max_retries = retries
        return self

    def set_timeout(self, timeout):
        """Set the timeout in seconds for the urllib2.urlopen call

        >>> ApiConnector().set_timeout(3.551).timeout == 3.551
        True

        >>> ApiConnector().set_timeout(-2)
        Traceback (most recent call last):
        RuntimeError: Timeout must be non-negative
        """
        if timeout < 0:
            raise RuntimeError("Timeout must be non-negative")
        self.timeout = timeout
        return self

    #pylint: disable=line-too-long, invalid-name
    def request(self, url):
        """Request json data from the URL

        >>> j = ApiConnector().request('https://hacker-news.firebaseio.com/v0/item/1.json')
        >>> j['by'] == 'pg'
        True

        >>> ApiConnector().request('https://hacker-news.firebaseio.com/v0/foobar/1.json')
        Traceback (most recent call last):
        NetworkError: HTTP Error 401: Unauthorized

        >>> ApiConnector().request('http://www.yahoo.co.jp') # doctest: +ELLIPSIS
        Traceback (most recent call last):
        NetworkError: ...
        """
        this_try = 0
        ex = RuntimeError()
        while this_try < self.max_retries:
            try:
                sleep_time = self.backoff_multiplier * ((2**this_try) - 1)
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
            return jsondata
        except (urllib2.URLError, ValueError, Exception) as e:
            self.logger.exception(e)
            raise NetworkError(e)
        finally:
            self.logger.debug("Requested %s", url)

    def get_top(self):
        """Request the top 100 stories
        >>> top = ApiConnector().get_top()
        >>> len(top) == 500
        True
        """
        endpoint_top100 = "https://hacker-news.firebaseio.com/v0/topstories.json"
        try:
            return self.request(endpoint_top100)
        except NetworkError:
            return []

    #pylint: disable=no-self-use, unused-variable
    def make_item_endpoint(self, item_id):
        """Return the API URL for the given item_id

        >>> ApiConnector().make_item_endpoint(1)
        'https://hacker-news.firebaseio.com/v0/item/1.json'

        >>> ApiConnector().make_item_endpoint(None)
        Traceback (most recent call last):
        RuntimeError: Parameter None must be an integer

        >>> ApiConnector().make_item_endpoint('baz')
        Traceback (most recent call last):
        RuntimeError: Parameter baz must be an integer
        """
        try:
            int(item_id)
        except (TypeError, ValueError) as e:
            raise RuntimeError("Parameter %s must be an integer" % item_id)
        return "https://hacker-news.firebaseio.com/v0/item/" + str(item_id) + ".json"

    def make_user_endpoint(self, username):
        """Return the API URL for the given username

        >>> ApiConnector().make_user_endpoint('pg')
        'https://hacker-news.firebaseio.com/v0/user/pg.json'
        """
        return "https://hacker-news.firebaseio.com/v0/user/" + username + ".json"

    def build_hnitem(self, item_json):
        """Build an instance of hnitem depending on the type"""
        if not item_json:
            self.logger.debug("Item_json should not be none. Skipping")
            return None

        if item_json.get('type') == "story" or item_json.get('type') == 'job':
            return StoryItem(item_json)
        elif item_json.get('type') == "comment":
            return CommentItem(item_json)
        elif item_json.get('type') == "poll":
            return PollItem(item_json)
        elif item_json.get('created'):
            return UserItem(item_json)
        elif item_json.get('profiles'):
            return UpdatesItem(item_json)

        raise RuntimeError("Item type unsupported: %r" % item_json)

    def get_item(self, item_id):
        """Get a particular item by item's id

        >>> it = ApiConnector().get_item(1)
        >>> it.get_field_by_name('by') == 'pg'
        True
        """
        url = self.make_item_endpoint(item_id)
        story = self.request(url)
        if story != None and story.get("by"):
            by = str(story["by"])
            self.user_dict[by] = by
        return self.build_hnitem(story)

    def get_user(self, username):
        """Get a user by username

        >>> u = ApiConnector().get_user('pg')
        >>> u.get('id') == 'pg'
        True
        """
        url = self.make_user_endpoint(username)
        user = self.request(url)
        return self.build_hnitem(user)

    def get_updates(self):
        """Get recent updates

        See UpdatesItem and UpdatesSchema

        >>> u = ApiConnector().get_updates()
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
        return self.build_hnitem(updates)

    def get_max_item(self):
        """Get max item's id

        Examples
        --------

        >>> itemid = ApiConnector().get_max_item()
        >>> itemid > 8669130
        True
        """
        url = "https://hacker-news.firebaseio.com/v0/maxitem.json"
        itemid = self.request(url)
        return itemid

    #pylint: disable=logging-not-lazy
    def get_kids_recur(self, kids, level):
        """Recursive helper method for retrieving kids in comments"""
        for k in [str(k) for k in kids]:
            url = self.make_item_endpoint(k)
            jdata = self.request(url)
            if jdata == None or not jdata.get("by"):
                continue
            by = str(jdata["by"])
            self.user_dict[by] = by
            self.logger.debug("Found user: %s at level: %s" % (by, level))
            if jdata.get("kids"):
                self.get_kids_recur(jdata["kids"], level + 1)

    def get_kids(self, story):
        """Get all usernames from comments of a story

        >>> o = ApiConnector().get_kids({'kids':[1]})
        >>> len(o.keys()) == 10
        True

        >>> s = StoryItem({'kids':[1]})
        >>> o = ApiConnector().get_kids(s)
        >>> len(o.keys()) == 10
        True
        """
        try:
            story = story.json
        except AttributeError:
            pass
        if story == None or not story.get("kids"):
            return
        kids = story["kids"]
        self.get_kids_recur(kids, 0)
        return self.user_dict

    def is_api_item(self, obj):
        '''Returns true iff obj is an HN item

        >>> ApiConnector().is_api_item({'id':321})
        True

        >>> ApiConnector().is_api_item(None)
        False

        >>> ApiConnector().is_api_item({'id':123, 'deleted':'True'})
        True
        '''
        if obj == None:
            return False
        return not not obj.get('id')

    def is_valid_item(self, obj):
        '''Returns true iff obj is an undeleted HN item

        >>> ApiConnector().is_valid_item({'id':123})
        True

        >>> ApiConnector().is_valid_item(None)
        False

        >>> ApiConnector().is_valid_item({'id':123, 'deleted':'True'})
        False
        '''
        try:
            return self.is_api_item(obj) and not obj.is_deleted()
        except AttributeError:
            return self.is_api_item(obj) and not obj.get('deleted')

    def is_dead_item(self, obj):
        '''
        Return True iff obj is a dead HN item

        >>> ApiConnector().is_dead_item({'id':101})
        False

        >>> ApiConnector().is_dead_item({'id':101, 'dead':'true'})
        True

        >>> ApiConnector().is_dead_item(None)
        False
        '''
        return not not (self.is_api_item(obj) and obj.get('dead'))

    def is_story_item(self, item):
        '''Return True if item is a story item

        >>> ApiConnector().is_story_item(StoryItem({}))
        True

        >>> ApiConnector().is_story_item(PollItem({}))
        False
        '''
        return type(item) is StoryItem

if __name__ == '__main__':
    import doctest
    logging.disable(logging.CRITICAL)
    doctest.testmod(raise_on_error=True)
    logging.disable(logging.NOTSET)
