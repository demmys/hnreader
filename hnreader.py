from bs4 import BeautifulSoup
import feedparser
import re
import urllib.parse
import urllib.request

class HackerNewsEntry:
    NUMBER_RE = re.compile(r'\d+')
    COMMENTS_RE = re.compile(r'(\d+) comments')

    def __init__(self, raw):
        self.title = raw['title']
        self.published = raw['published_parsed']
        self.content_url = raw['link']
        self.score_url = raw['comments']
        self.id = self.__get_id(self.score_url)

    def set_score(self):
        html = urllib.request.urlopen(self.score_url)
        soup = BeautifulSoup(html, 'html.parser')
        self.points_score = self.__get_points_score(soup)
        self.comments_score = self.__get_comments_score(soup)

    def __get_id(self, score_url):
        qs = urllib.parse.urlparse(score_url).query
        return urllib.parse.parse_qs(qs)['id'][0]

    def __get_points_score(self, soup):
        text = soup.find(id='score_{}'.format(self.id)).string
        res = self.NUMBER_RE.search(text)
        return int(res.group())

    def __get_comments_score(self, soup):
        links = soup.find_all('a', href='item?id={}'.format(self.id))
        for link in links:
            res = self.COMMENTS_RE.match(link.string)
            if res is not None:
                return int(res.group(1))
    def __repr__(self):
        return '<HackerNewsEntry title={} published={} content_url={} score_url={} id={} points_score={} comments_score={}>'.format(self.title, self.published, self.content_url, self.score_url, self.id, self.points_score, self.comments_score)

class HackerNewsIndex:
    RSS_URL = 'http://news.ycombinator.com/rss'

    def __init__(self):
        res = feedparser.parse(RSS_URL)
        self.entries = []
        for raw in res.entries:
            entry = HackerNewsEntry(raw)
            entry.set_score()
            self.entries.append(entry)

if __name__ == '__main__':
    index = HackerNewsIndex()
