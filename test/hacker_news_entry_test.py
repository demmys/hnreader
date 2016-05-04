import unittest
from datetime import datetime

from hacker_news_entry import HackerNewsEntry

class TestHackerNewsEntry(unittest.TestCase):
    def setUp(self):
        self.title = 'Article Title'
        self.id = '12345678'
        self.content_url = 'http://example.com/'
        self.score_url = 'https://news.ycombinator.com/item?id={}'.format(self.id)
        publish_time_str = 'Wed, 4 May 2016 01:41:27 +0000'
        self.publish_time = datetime.strptime(publish_time_str, '%a, %d %b %Y %H:%M:%S +0000')
        self.raw = {
            'link': self.content_url,
            'comments': self.score_url,
            'title': self.title,
            'published_parsed': self.publish_time.timetuple()
        }

    def test___init__(self):
        e = HackerNewsEntry(self.raw)
        self.assertEqual(e.title, self.title)
        self.assertEqual(e.content_url, self.content_url)
        self.assertEqual(e.score_url, self.score_url)
        self.assertEqual(e.id, self.id)
        self.assertEqual(e.publish_time, self.publish_time)
