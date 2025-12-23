import feedparser
import sqlite3

# RSS feed URL
rss_url = "https://news.mit.edu/topic/mitquantum-computing-rss.xml"

# Parse the feed
feed = feedparser.parse(rss_url)

# Connect to SQLite database (or create it)
conn = sqlite3.connect("quantum_news_rss.db")
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    published TEXT,
    author TEXT,
    link TEXT UNIQUE,
    summary TEXT
)
""")

# Insert entries into the database
if feed.bozo:
    print("Failed to parse RSS feed.")
else:
    for entry in feed.entries[:5]:  # Limit to 10 entries
        title = entry.get("title", "No Title")
        published = entry.get("published", "No Date")
        author = entry.get("author", "Unknown Author")
        link = entry.get("link", "")
        summary = entry.get("summary", "No Summary")

        try:
            cursor.execute("""
            INSERT OR IGNORE INTO articles (title, published, author, link, summary)
            VALUES (?, ?, ?, ?, ?)
            """, (title, published, author, link, summary))
        except Exception as e:
            print(f"Error inserting article: {e}")

    conn.commit()
    print("Articles saved to database.")

# Close connection
conn.close()
