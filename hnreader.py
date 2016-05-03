import feedparser

class HackerNewsItem:
    def __init__(self, entry):
        self.title = entry['title']
        self.published = entry['published_parsed']
        self.commentURL = entry['comments']
        self.contentURL = entry['link']

class HackerNewsIndex:
    RSS_URL = 'http://news.ycombinator.com/rss'

    def __init__(self):
        res = feedparser.parse(RSS_URL)
        self.items = []
        for entry in res.entries:
            self.items.append(HackerNewsItem(entry))

if __name__ == '__main__':
    index = HackerNewsIndex()
