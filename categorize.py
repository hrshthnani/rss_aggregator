def categorize_article(article):
    title = article['title'].lower()
    summary = article['summary'].lower()
    
    # Simple keyword-based categorization
    if any(word in title or word in summary for word in ['protest', 'riot', 'unrest', 'terrorism']):
        return 'Terrorism / protest / political unrest / riot'
    elif any(word in title or word in summary for word in ['happy', 'inspiring', 'uplifting', 'positive']):
        return 'Positive/Uplifting'
    elif any(word in title or word in summary for word in ['earthquake', 'flood', 'storm', 'disaster']):
        return 'Natural Disasters'
    else:
        return 'Others'
