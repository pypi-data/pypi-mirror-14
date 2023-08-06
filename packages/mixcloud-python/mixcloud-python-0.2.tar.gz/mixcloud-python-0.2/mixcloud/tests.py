__author__ = 'saidali'

import unittest
import requests
from mixcloud.client import Client


class TestMixCloudMethods(unittest.TestCase):
    def setUp(self):
        self.mix_cloud = Client()

    def test_get_user(self):
        user_kasa_object = self.mix_cloud.get_user('Kasa007')
        user_kasa_json = requests.get('http://api.mixcloud.com/kasa007/').json()

        self.assertEqual(user_kasa_object.username, user_kasa_json['username'])
        self.assertEqual(user_kasa_object.city, user_kasa_json['city'])
        self.assertEqual(user_kasa_object.name, user_kasa_json['name'])
        self.assertEqual(user_kasa_object.pictures.small, user_kasa_json['pictures']['small'])
        self.assertEqual(user_kasa_object.pictures.medium, user_kasa_json['pictures']['medium'])
        self.assertFalse(user_kasa_object.is_pro)

    def test_get_categories(self):
        deep_house_json = requests.get('http://api.mixcloud.com/categories/deep-house/').json()
        deep_house_object = self.mix_cloud.get_categories('deep-house')

        self.assertEqual(deep_house_object.url, deep_house_json['url'])
        self.assertEqual(deep_house_object.name, deep_house_json['name'])
        self.assertEqual(deep_house_object.key, deep_house_json['key'])
        self.assertEqual(deep_house_object.slug, deep_house_json['slug'])
        self.assertEqual(deep_house_object.format, deep_house_json['format'])

    def test_get_tag(self):
        funk_json = requests.get('http://api.mixcloud.com/tag/funk/').json()
        funk_object = self.mix_cloud.get_tag('funk')

        self.assertEquals(funk_object.url, funk_json['url'])
        self.assertEquals(funk_object.name, funk_json['name'])
        self.assertEquals(funk_object.key, funk_json['key'])

    def test_get_popular(self):
        popular_tracks_json = requests.get('http://api.mixcloud.com/popular/?limit=2').json()
        popular_tracks_object = self.mix_cloud.get_popular(limit=2)

        self.assertEquals(len(popular_tracks_object.data), len(popular_tracks_json['data']))
        self.assertEquals(popular_tracks_object.paging.next, popular_tracks_json['paging']['next'])

    def test_get_hot(self):
        hot_tracks_json = requests.get('http://api.mixcloud.com/popular/hot/?limit=5').json()
        hot_tracks_object = self.mix_cloud.get_hot(limit=5)

        self.assertEquals(hot_tracks_object.paging.next, hot_tracks_json['paging']['next'])
        self.assertEquals(len(hot_tracks_object.data), len(hot_tracks_json['data']))

        self.assertEquals(hot_tracks_object.data[0].name, hot_tracks_json['data'][0]['name'])
        self.assertEquals(hot_tracks_object.data[1].name, hot_tracks_json['data'][1]['name'])
        self.assertEquals(hot_tracks_object.data[2].url, hot_tracks_json['data'][2]['url'])
        self.assertEquals(hot_tracks_object.data[3].key, hot_tracks_json['data'][3]['key'])

        self.assertEquals(hot_tracks_object.data[0].tags[0].url, hot_tracks_json['data'][0]['tags'][0]['url'])
        self.assertEquals(hot_tracks_object.data[0].tags[0].name, hot_tracks_json['data'][0]['tags'][0]['name'])
        self.assertEquals(hot_tracks_object.data[0].tags[0].key, hot_tracks_json['data'][0]['tags'][0]['key'])

    def test_get_hot_next_paging(self):
        hot_tracks_json = requests.get('http://api.mixcloud.com/popular/hot/?limit=5').json()
        hot_tracks_object = self.mix_cloud.get_hot(limit=5)

        hot_tracks_json = requests.get(hot_tracks_json['paging']['next']).json()
        hot_tracks_json = requests.get(hot_tracks_json['paging']['next']).json()

        hot_tracks_object = hot_tracks_object.next_paging()
        hot_tracks_object = hot_tracks_object.next_paging()

        self.assertEquals(hot_tracks_object.paging.next, hot_tracks_json['paging']['next'])
        self.assertEquals(len(hot_tracks_object.data), len(hot_tracks_json['data']))

        self.assertEquals(hot_tracks_object.data[0].name, hot_tracks_json['data'][0]['name'])
        self.assertEquals(hot_tracks_object.data[1].name, hot_tracks_json['data'][1]['name'])
        self.assertEquals(hot_tracks_object.data[2].url, hot_tracks_json['data'][2]['url'])
        self.assertEquals(hot_tracks_object.data[3].key, hot_tracks_json['data'][3]['key'])

        self.assertEquals(hot_tracks_object.data[0].tags[0].url, hot_tracks_json['data'][0]['tags'][0]['url'])
        self.assertEquals(hot_tracks_object.data[0].tags[0].name, hot_tracks_json['data'][0]['tags'][0]['name'])
        self.assertEquals(hot_tracks_object.data[0].tags[0].key, hot_tracks_json['data'][0]['tags'][0]['key'])

    def test_get_hot_previous_paging(self):
        hot_tracks_json = requests.get('http://api.mixcloud.com/popular/hot/?limit=5').json()
        hot_tracks_object = self.mix_cloud.get_hot(limit=5)

        hot_tracks_json = requests.get(hot_tracks_json['paging']['next']).json()
        hot_tracks_json = requests.get(hot_tracks_json['paging']['next']).json()
        hot_tracks_json = requests.get(hot_tracks_json['paging']['previous']).json()

        hot_tracks_object = hot_tracks_object.next_paging()
        hot_tracks_object = hot_tracks_object.next_paging()
        hot_tracks_object = hot_tracks_object.previous_paging()

        self.assertEquals(hot_tracks_object.paging.next, hot_tracks_json['paging']['next'])
        self.assertEquals(len(hot_tracks_object.data), len(hot_tracks_json['data']))

        self.assertEquals(hot_tracks_object.data[0].name, hot_tracks_json['data'][0]['name'])
        self.assertEquals(hot_tracks_object.data[1].name, hot_tracks_json['data'][1]['name'])
        self.assertEquals(hot_tracks_object.data[2].url, hot_tracks_json['data'][2]['url'])
        self.assertEquals(hot_tracks_object.data[3].key, hot_tracks_json['data'][3]['key'])

        self.assertEquals(hot_tracks_object.data[0].tags[0].url, hot_tracks_json['data'][0]['tags'][0]['url'])
        self.assertEquals(hot_tracks_object.data[0].tags[0].name, hot_tracks_json['data'][0]['tags'][0]['name'])
        self.assertEquals(hot_tracks_object.data[0].tags[0].key, hot_tracks_json['data'][0]['tags'][0]['key'])

    def test_get_new(self):
        new_tracks_json = requests.get('http://api.mixcloud.com/new/?limit=5').json()
        new_tracks_object = self.mix_cloud.get_new(limit=5)

        self.assertEquals(len(new_tracks_object.data), len(new_tracks_json['data']))
        self.assertEquals(new_tracks_object.data[0].name, new_tracks_json['data'][0]['name'])
        self.assertEquals(new_tracks_object.data[0].play_count, new_tracks_json['data'][0]['play_count'])
        self.assertEquals(new_tracks_object.data[1].name, new_tracks_json['data'][1]['name'])
        self.assertEquals(new_tracks_object.data[2].url, new_tracks_json['data'][2]['url'])
        self.assertEquals(new_tracks_object.data[3].key, new_tracks_json['data'][3]['key'])

    def test_get_new_next_paging(self):
        new_tracks_json = requests.get('http://api.mixcloud.com/popular/hot/?limit=5').json()
        new_tracks_object = self.mix_cloud.get_hot(limit=5)

        new_tracks_json = requests.get(new_tracks_json['paging']['next']).json()
        new_tracks_json = requests.get(new_tracks_json['paging']['next']).json()

        new_tracks_object = new_tracks_object.next_paging()
        new_tracks_object = new_tracks_object.next_paging()

        self.assertEquals(new_tracks_object.paging.next, new_tracks_json['paging']['next'])
        self.assertEquals(new_tracks_object.paging.previous, new_tracks_json['paging']['previous'])

        self.assertEquals(len(new_tracks_object.data), len(new_tracks_json['data']))

        self.assertEquals(new_tracks_object.data[0].name, new_tracks_json['data'][0]['name'])
        self.assertEquals(new_tracks_object.data[1].name, new_tracks_json['data'][1]['name'])
        self.assertEquals(new_tracks_object.data[2].url, new_tracks_json['data'][2]['url'])
        self.assertEquals(new_tracks_object.data[3].key, new_tracks_json['data'][3]['key'])

        self.assertEquals(new_tracks_object.data[0].tags[0].url, new_tracks_json['data'][0]['tags'][0]['url'])
        self.assertEquals(new_tracks_object.data[0].tags[0].name, new_tracks_json['data'][0]['tags'][0]['name'])
        self.assertEquals(new_tracks_object.data[0].tags[0].key, new_tracks_json['data'][0]['tags'][0]['key'])

    def test_get_new_previous_paging(self):
        new_tracks_json = requests.get('http://api.mixcloud.com/popular/hot/?limit=5').json()
        new_tracks_object = self.mix_cloud.get_hot(limit=5)

        new_tracks_json = requests.get(new_tracks_json['paging']['next']).json()
        new_tracks_json = requests.get(new_tracks_json['paging']['next']).json()
        new_tracks_json = requests.get(new_tracks_json['paging']['previous']).json()

        new_tracks_object = new_tracks_object.next_paging()
        new_tracks_object = new_tracks_object.next_paging()
        new_tracks_object = new_tracks_object.previous_paging()

        self.assertEquals(new_tracks_object.paging.next, new_tracks_json['paging']['next'])
        self.assertEquals(new_tracks_object.paging.previous, new_tracks_json['paging']['previous'])
        self.assertEquals(len(new_tracks_object.data), len(new_tracks_json['data']))

        self.assertEquals(new_tracks_object.data[0].name, new_tracks_json['data'][0]['name'])
        self.assertEquals(new_tracks_object.data[1].name, new_tracks_json['data'][1]['name'])
        self.assertEquals(new_tracks_object.data[2].url, new_tracks_json['data'][2]['url'])
        self.assertEquals(new_tracks_object.data[3].key, new_tracks_json['data'][3]['key'])

        self.assertEquals(new_tracks_object.data[0].tags[0].url, new_tracks_json['data'][0]['tags'][0]['url'])
        self.assertEquals(new_tracks_object.data[0].tags[0].name, new_tracks_json['data'][0]['tags'][0]['name'])
        self.assertEquals(new_tracks_object.data[0].tags[0].key, new_tracks_json['data'][0]['tags'][0]['key'])

    def test_search(self):
        search_url_json = requests.get('http://api.mixcloud.com/search/?q=kasa007&type=user').json()
        search_url_object = self.mix_cloud.search('kasa007', 'user')
        self.assertEquals(search_url_object.data[0].name, search_url_json['data'][0]['name'])
        self.assertEquals(search_url_object.data[0].username, search_url_json['data'][0]['username'])
        self.assertEquals(search_url_object.data[0].key, search_url_json['data'][0]['key'])

    def test_get_url(self):
        get_url_json = requests.get('http://api.mixcloud.com/spartacus/').json()
        get_url_object = self.mix_cloud.get_url('http://api.mixcloud.com/spartacus/')

        self.assertEquals(get_url_object.username, get_url_json['username'])
        self.assertEquals(get_url_object.city, get_url_json['city'])
        self.assertEquals(get_url_object.favorite_count, get_url_json['favorite_count'])
        self.assertEquals(get_url_object.url, get_url_json['url'])


if __name__ == "__main__":
    unittest.main()
