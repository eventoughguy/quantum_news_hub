import sqlite3
from agent import summarize_news
import asyncio

input_url = 'https://news.mit.edu/2025/device-enables-direct-communication-among-multiple-quantum-processors-0321'

async def async_main():
    conn = sqlite3.connect("quantum_news.db")
    cursor = conn.cursor()

    # ✅ Ensure the table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            url TEXT UNIQUE,
            summary TEXT,      
        )
    """)

    # ✅ Check if the URL already exists
    cursor.execute("SELECT title, summary FROM news WHERE url = ?", (input_url,))
    existing_entry = cursor.fetchone()

    if existing_entry and existing_entry[1]:  # If summary exists, return it
        print(f"⚠️ Skipping summarization, URL already exists: {input_url}")
        conn.close()
        return

    print(f"🔄 URL not found in database, generating summary...")

    # ✅ Generate summary for the new entry
    try:
        news_extract, summary = await summarize_news(input_url)

        # ✅ Ensure `news_extract` contains valid data
        title = news_extract.get("title", "").strip()

        if not title or not summary:
            print(f"❌ Error: Missing title or summary for URL: {input_url}")
            return

        # ✅ Check if the title already exists before inserting
        cursor.execute("SELECT id FROM news WHERE title = ?", (title,))
        title_exists = cursor.fetchone()

        if title_exists:
            print(f"⚠️ Skipping insertion: Title already exists in the database ({title})")
            conn.close()
            return

        # ✅ Insert into the database
        cursor.execute("INSERT INTO news (title, url, summary) VALUES (?, ?, ?)", (title, input_url, summary))
        conn.commit()
        print(f"✅ New summary saved to database: {input_url}")

    except Exception as e:
        print(f"❌ An error occurred while summarizing: {e}")

    finally:
        conn.close()  # ✅ Ensure database connection is closed

if __name__ == '__main__':
    try:
        asyncio.run(async_main())
    except Exception as e:
        print(f"❌ An error occurred: {e}")