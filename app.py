from flask import Flask, render_template, request
from models import Article, session
import feedparser
from dateutil import parser

# List of RSS feeds
RSS_FEEDS = [
    'http://rss.cnn.com/rss/cnn_topstories.rss',
    'http://qz.com/feed',
    'http://feeds.foxnews.com/foxnews/politics',
    'http://feeds.reuters.com/reuters/businessNews',
    'http://feeds.feedburner.com/NewshourWorld',
    'https://feeds.bbci.co.uk/news/world/asia/india/rss.xml',
]

def categorize_article(title):
    if "terror" in title.lower() or "protest" in title.lower() or "unrest" in title.lower() or "riot" in title.lower():
        return "Terrorism / protest / political unrest / riot"
    elif "positive" in title.lower() or "uplifting" in title.lower():
        return "Positive/Uplifting"
    elif "earthquake" in title.lower() or "flood" in title.lower() or "hurricane" in title.lower() or "tsunami" in title.lower():
        return "Natural Disasters"
    else:
        return "Others"

def fetch_articles():
    articles = []
    for feed in RSS_FEEDS:
        parsed_feed = feedparser.parse(feed)
        for entry in parsed_feed.entries:
            published_date = entry.published if 'published' in entry else None
            if published_date:
                try:
                    published = parser.parse(published_date)
                except Exception as e:
                    print(f"Error parsing date: {published_date}")
                    published = None
            else:
                published = None

            article = {
                'id': entry.link,
                'title': entry.title,
                'link': entry.link,
                'summary': entry.summary if 'summary' in entry else 'No Summary Available',
                'published': published,
                'category': categorize_article(entry.title),
            }
            articles.append(article)
    return articles

def save_articles():
    articles = fetch_articles()
    for article_data in articles:
        existing_article = session.query(Article).filter_by(id=article_data['id']).first()
        if existing_article:
            print(f"Article with id {article_data['id']} already exists. Skipping.")
            continue
        
        article = Article(
            id=article_data['id'],
            title=article_data['title'],
            link=article_data['link'],
            summary=article_data['summary'],
            published=article_data['published'],
            category=article_data['category'],
        )
        session.add(article)
    session.commit()

app = Flask(__name__)

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', None)

    # Set the number of articles per page
    per_page = 5
    query = session.query(Article)

    if category:
        query = query.filter_by(category=category)

    total_articles = query.count()
    articles = query.offset((page - 1) * per_page).limit(per_page).all()
    total_pages = (total_articles + per_page - 1) // per_page  # Calculate total pages

    return render_template('index.html', articles=articles, category=category, page=page, total_pages=total_pages)

@app.route('/update_articles')
def update_articles():
    save_articles()
    return "Articles updated successfully!"

if __name__ == '__main__':
    app.run(debug=True)
