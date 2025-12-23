#!/usr/bin/env python3
"""
Quantum News Daily Runner
This script orchestrates the daily quantum news processing workflow:
1. Fetch latest RSS articles
2. Generate AI summaries
3. Update database
"""

import asyncio
import logging
import sys
import os
from datetime import datetime
from enhanced_agent import QuantumNewsAgent
from enhanced_rss_parser import QuantumRSSParser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("quantum_news_daily.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

class DailyNewsProcessor:
    def __init__(self):
        self.agent = QuantumNewsAgent()
        self.parser = QuantumRSSParser()
        self.start_time = datetime.now()

    async def run_daily_process(self):
        """Execute the complete daily news processing workflow"""
        logging.info("=" * 60)
        logging.info(f"Starting daily quantum news processing at {self.start_time}")
        logging.info("=" * 60)

        try:
            # Step 1: Process new articles
            logging.info("Step 1: Processing new articles from RSS feed...")
            new_article_result = await self.agent.process_new_articles()

            if new_article_result['status'] == 'success':
                logging.info(f"✅ New article processed: {new_article_result['article']['title']}")
                logging.info(f"   Summary length: {len(new_article_result['summary'])} characters")
            elif new_article_result['status'] == 'no_new_articles':
                logging.info("ℹ️  No new articles found in RSS feed")
            else:
                logging.error(f"❌ Failed to process new articles: {new_article_result.get('message', 'Unknown error')}")

            # Step 2: Process any existing articles without summaries
            logging.info("Step 2: Processing existing articles without summaries...")
            backlog_result = await self.agent.process_existing_articles_without_summary()

            if 'error' in backlog_result:
                logging.error(f"❌ Error processing backlog: {backlog_result['error']}")
            else:
                processed = backlog_result['processed_count']
                total = backlog_result['total_articles']
                if processed > 0:
                    logging.info(f"✅ Processed {processed} out of {total} articles from backlog")
                else:
                    logging.info("ℹ️  No articles in backlog requiring processing")

            # Step 3: Generate processing summary
            end_time = datetime.now()
            duration = end_time - self.start_time

            logging.info("Step 3: Generating daily summary...")
            summary = await self.generate_daily_summary(new_article_result, backlog_result, duration)

            logging.info("=" * 60)
            logging.info("DAILY PROCESSING SUMMARY")
            logging.info("=" * 60)
            logging.info(summary)
            logging.info("=" * 60)
            logging.info(f"Daily processing completed at {end_time}")
            logging.info(f"Total processing time: {duration}")
            logging.info("=" * 60)

            return {
                'status': 'success',
                'new_articles': new_article_result,
                'backlog_processing': backlog_result,
                'duration': str(duration),
                'summary': summary
            }

        except Exception as e:
            logging.error(f"❌ Critical error in daily processing: {e}")
            logging.exception("Full error traceback:")
            return {
                'status': 'error',
                'error': str(e),
                'duration': str(datetime.now() - self.start_time)
            }

    async def generate_daily_summary(self, new_article_result, backlog_result, duration):
        """Generate a human-readable summary of the daily processing"""
        summary_parts = []

        # New articles summary
        if new_article_result['status'] == 'success':
            article = new_article_result['article']
            summary_parts.append(f"🆕 NEW ARTICLE PROCESSED:")
            summary_parts.append(f"   Title: {article['title']}")
            summary_parts.append(f"   Author: {article['author']}")
            summary_parts.append(f"   Publish Date: {article['publish_date']}")
            summary_parts.append(f"   Link: {article['link']}")
            summary_parts.append(f"   AI Summary Generated: ✅ ({len(new_article_result['summary'])} chars)")
        elif new_article_result['status'] == 'no_new_articles':
            summary_parts.append("🔄 NO NEW ARTICLES: RSS feed had no new articles to process")
        else:
            summary_parts.append(f"❌ NEW ARTICLE ERROR: {new_article_result.get('message', 'Unknown error')}")

        # Backlog processing summary
        if 'error' not in backlog_result:
            processed = backlog_result['processed_count']
            total = backlog_result['total_articles']
            if processed > 0:
                summary_parts.append(f"📚 BACKLOG PROCESSING: {processed}/{total} articles summarized")
            else:
                summary_parts.append("📚 BACKLOG: No articles requiring summary processing")
        else:
            summary_parts.append(f"❌ BACKLOG ERROR: {backlog_result['error']}")

        # Processing stats
        summary_parts.append(f"⏱️  PROCESSING TIME: {duration}")
        summary_parts.append(f"🕐 COMPLETED AT: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        return "\n".join(summary_parts)

    def get_database_stats(self):
        """Get current database statistics"""
        try:
            conn = sqlite3.connect(self.parser.db_path)
            cursor = conn.cursor()

            # Get various statistics
            stats = {}
            cursor.execute("SELECT COUNT(*) FROM quantum_news_rss")
            stats['total_articles'] = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM quantum_news_rss WHERE ai_summary IS NOT NULL AND ai_summary != ''")
            stats['summarized'] = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM quantum_news_rss WHERE ai_summary IS NULL OR ai_summary = ''")
            stats['pending'] = cursor.fetchone()[0]

            conn.close()
            return stats
        except Exception as e:
            logging.error(f"Error getting database stats: {e}")
            return None

def main():
    """Main entry point for daily processing"""
    try:
        processor = DailyNewsProcessor()
        result = asyncio.run(processor.run_daily_process())

        # Set exit code based on result
        if result['status'] == 'success':
            sys.exit(0)
        else:
            sys.exit(1)

    except KeyboardInterrupt:
        logging.info("Daily processing interrupted by user")
        sys.exit(130)
    except Exception as e:
        logging.error(f"Unexpected error in main: {e}")
        logging.exception("Full error traceback:")
        sys.exit(1)

if __name__ == "__main__":
    main()