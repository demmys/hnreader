from datetime import datetime, timedelta

from hacker_news_index import HackerNewsIndex

if __name__ == '__main__':
    index = HackerNewsIndex()
    last_updated_at = datetime.utcnow() - timedelta(hours=12)
    six_hours_since = datetime.utcnow() - timedelta(hours=6)
    index.filter_by_publish_time(last_updated_at, six_hours_since)
    index.set_scores()
    index.filter_by_score(100, 0)
    print(index)
