import feedparser
import sqlite3
import requests
from newspaper import Article
from datetime import datetime, date
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class QuantumRSSParser:
    def __init__(self, db_path="quantum_news_rss.db"):
        self.rss_url = "https://news.mit.edu/topic/mitquantum-computing-rss.xml"
        self.db_path = db_path
        self.setup_database()

    def setup_database(self):
        """Initialize database with updated schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create table with content field for full article content
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS quantum_news_rss (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            publish_date TEXT,
            article_link TEXT UNIQUE NOT NULL,
            content TEXT,
            ai_summary TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()
        conn.close()
        logging.info("Database initialized successfully")

    def extract_article_content(self, url):
        """Extract full article content from URL"""
        try:
            article = Article(url)
            article.download()
            article.parse()

            return {
                'title': article.title or 'No Title',
                'content': article.text or 'No Content',
                'authors': ', '.join(article.authors) if article.authors else 'Unknown Author',
                'publish_date': article.publish_date.strftime('%Y-%m-%d') if article.publish_date else str(date.today())
            }
        except Exception as e:
            logging.error(f"Error extracting content from {url}: {e}")
            return None

    def article_exists(self, link):
        """Check if article already exists in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM quantum_news_rss WHERE article_link = ?", (link,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists

    def save_article(self, title, author, publish_date, link, content):
        """Save article to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO quantum_news_rss (title, author, publish_date, article_link, content)
                VALUES (?, ?, ?, ?, ?)
            """, (title, author, publish_date, link, content))
            conn.commit()
            article_id = cursor.lastrowid
            logging.info(f"Article saved with ID: {article_id}")
            return article_id
        except sqlite3.IntegrityError:
            logging.warning(f"Article already exists: {link}")
            return None
        except Exception as e:
            logging.error(f"Error saving article: {e}")
            return None
        finally:
            conn.close()

    def fetch_latest_article(self):
        """Fetch the newest article from RSS feed if not already stored"""
        try:
            # Parse RSS feed
            feed = feedparser.parse(self.rss_url)

            if feed.bozo:
                logging.error("Failed to parse RSS feed")
                return None

            if not feed.entries:
                logging.info("No entries found in RSS feed")
                return None

            # Get the most recent entry
            latest_entry = feed.entries[0]
            article_link = latest_entry.get("link", "")

            # Check if we already have this article
            if self.article_exists(article_link):
                logging.info(f"Article already exists: {article_link}")
                return None

            # Extract full article content
            article_data = self.extract_article_content(article_link)
            if not article_data:
                logging.error(f"Failed to extract content from: {article_link}")
                return None

            # Use RSS metadata with fallbacks to extracted data
            title = latest_entry.get("title", article_data['title'])
            author = latest_entry.get("author", article_data['authors'])
            publish_date = latest_entry.get("published", article_data['publish_date'])
            content = article_data['content']

            # Save to database
            article_id = self.save_article(title, author, publish_date, article_link, content)

            if article_id:
                logging.info(f"Successfully processed new article: {title}")
                return {
                    'id': article_id,
                    'title': title,
                    'author': author,
                    'publish_date': publish_date,
                    'link': article_link,
                    'content': content
                }

            return None

        except Exception as e:
            logging.error(f"Error fetching RSS feed: {e}")
            return None

    def get_articles_without_summary(self):
        """Get articles that don't have AI summary yet"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, title, content, article_link
            FROM quantum_news_rss
            WHERE ai_summary IS NULL OR ai_summary = ''
        """)
        articles = cursor.fetchall()
        conn.close()
        return articles

    def update_article_summary(self, article_id, summary):
        """Update article with AI-generated summary"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE quantum_news_rss
                SET ai_summary = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (summary, article_id))
            conn.commit()
            logging.info(f"Summary updated for article ID: {article_id}")
            return True
        except Exception as e:
            logging.error(f"Error updating summary: {e}")
            return False
        finally:
            conn.close()

if __name__ == "__main__":
    parser = QuantumRSSParser()
    result = parser.fetch_latest_article()
    if result:
        print(f"New article processed: {result['title']}")
    else:
        print("No new articles to process")