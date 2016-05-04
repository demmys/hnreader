import feedparser

from hacker_news_entry import HackerNewsEntry

class HackerNewsIndex:
    RSS_URL = 'http://news.ycombinator.com/rss'

    def __init__(self):
        res = feedparser.parse(self.RSS_URL)
        self.entries = map(lambda raw: HackerNewsEntry(raw), res.entries)

    def filter_by_publish_time(self, since, till):
        self.entries = filter(lambda entry: True if since < entry.publish_time and entry.publish_time < till else False, self.entries)

    def filter_by_score(self, points_score, comments_score):
        self.entries = filter(lambda entry: True if points_score < entry.points_score and comments_score < entry.comments_score else False, self.entries)

    def set_scores(self):
        self.entries = filter(None, map(lambda entry: entry.set_score(), self.entries))

    def __repr__(self):
        return repr(list(self.entries) or self.entries)
