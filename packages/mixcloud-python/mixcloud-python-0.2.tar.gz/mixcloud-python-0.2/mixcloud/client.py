import six
import requests
from utils import check_response, check_paging


class MixcloudObject(object):
    """ Converts Mixcloud json response to object"""

    def __init__(self, response):
        for (key, value) in six.iteritems(response):
            # recursively view sub-dicts as objects
            if isinstance(value, (list, tuple)):
                setattr(self, key, [(MixcloudObject(x) if isinstance(x, dict) else x) for x in value])
            else:
                setattr(self, key, (MixcloudObject(value) if isinstance(value, dict) else value))


class Client(object):
    """Interacting with Mixcloud resources."""

    api_base = 'http://api.mixcloud.com'
    metadata_parm = '?metadata=1'
    oauth_url = 'https://www.mixcloud.com/oauth/'

    def get_user(self, username):
        return self.get(username)

    def get_categories(self, categories):
        return self.get(categories, 'categories')

    def get_tag(self, tag):
        return self.get(tag, 'tag')

    def get_url(self, url):
        return check_response(requests.get(url).json())

    def get_popular(self, limit):
        url = '{0}/{1}/?limit={2}'.format(self.api_base, 'popular', limit)
        return check_paging(self, requests.get(url).json())

    def get_hot(self, limit):
        url = '{0}/{1}/?limit={2}'.format(self.api_base, 'popular/hot', limit)
        return check_paging(self, requests.get(url).json())

    def get_new(self, limit):
        url = '{0}/{1}/?limit={2}'.format(self.api_base, 'new', limit)
        return check_paging(self, requests.get(url).json())

    def search(self, query, query_type):
        search_query = '{0}/search/?q={1}&type={2}'.format(self.api_base, query, query_type)
        return self.get_url(search_query)

    def get(self, name, link=None):
        if link:
            url = '{0}/{1}/{2}/{3}'.format(self.api_base, link, name,
                                           self.metadata_parm)
        else:
            url = '{0}/{1}/{2}'.format(self.api_base, name, self.metadata_parm)
        return check_response(requests.get(url).json())
