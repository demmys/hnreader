from bs4 import BeautifulSoup
from datetime import datetime
import re
import time
import urllib.parse
import urllib.request

class HackerNewsEntry:
    NUMBER_RE = re.compile(r'\d+')
    COMMENTS_RE = re.compile(r'(\d+) comments')

    def __init__(self, raw):
        self.title = raw['title']
        self.content_url = raw['link']
        self.score_url = raw['comments']
        self.publish_time = datetime.fromtimestamp(time.mktime(raw['published_parsed']))
        self.id = self.__get_id(self.score_url)

    def set_score(self):
        try:
            html = urllib.request.urlopen(self.score_url)
            soup = BeautifulSoup(html, 'html.parser')
            self.points_score = self.__get_points_score(soup)
            self.comments_score = self.__get_comments_score(soup)
            return self
        except:
            logging.error('Exception caught while parsing score from %s.', self.score_url, exc_info=True, stack_info=True)
            return None

    def __get_id(self, score_url):
        qs = urllib.parse.urlparse(score_url).query
        return urllib.parse.parse_qs(qs)['id'][0]

    def __get_points_score(self, soup):
        text = soup.find(id='score_{}'.format(self.id)).get_text()
        res = self.NUMBER_RE.search(text)
        return int(res.group())

    def __get_comments_score(self, soup):
        links = soup.find_all('a', href='item?id={}'.format(self.id))
        for link in links:
            res = self.COMMENTS_RE.match(link.get_text())
            if res is not None:
                return int(res.group(1))

    def __repr__(self):
        if hasattr(self, 'points_score'):
            return '<HackerNewsEntry title={} publish_time={} content_url={} score_url={} id={} points_score={} comments_score={}>'.format(self.title, self.publish_time, self.content_url, self.score_url, self.id, self.points_score, self.comments_score)
        return '<HackerNewsEntry title={} publish_time={} content_url={} score_url={} id={}>'.format(self.title, self.publish_time, self.content_url, self.score_url, self.id)
