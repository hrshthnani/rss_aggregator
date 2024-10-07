from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'
    id = Column(String, primary_key=True)
    title = Column(String)
    link = Column(String)
    summary = Column(Text)
    published = Column(DateTime)  # This will store the datetime object
    category = Column(String)

# Initialize the database
engine = create_engine('sqlite:///news.db')  # Path to SQLite database
Base.metadata.create_all(engine)  # Create the 'articles' table if it doesn't exist
Session = sessionmaker(bind=engine)
session = Session()
