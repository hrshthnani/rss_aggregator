import feedparser
from datetime import datetime

def fetch_articles():
    feeds = [
        'http://rss.cnn.com/rss/cnn_topstories.rss',
        'http://qz.com/feed',
        'http://feeds.foxnews.com/foxnews/politics',
        'http://feeds.reuters.com/reuters/businessNews',
        'http://feeds.feedburner.com/NewshourWorld',
        'https://feeds.bbci.co.uk/news/world/asia/india/rss.xml'
    ]
    
    articles = []
    
    for feed in feeds:
        parsed_feed = feedparser.parse(feed)
        
        for entry in parsed_feed.entries:
            # Handle the case where 'published' might not exist
            published_str = entry.get('published', None)
            published_dt = None  # Default if 'published' is missing

            if published_str:
                try:
                    # Convert the string to datetime object
                    published_dt = datetime.strptime(published_str, "%a, %d %b %Y %H:%M:%S %Z")
                except ValueError:
                    print(f"Error parsing date: {published_str}")

            article = {
                'title': entry.get('title', 'No Title Available'),
                'link': entry.get('link', ''),
                'summary': entry.get('summary', 'No Summary Available'),
                'published': published_dt,  # Store as datetime object
            }
            articles.append(article)
    
    return articles

