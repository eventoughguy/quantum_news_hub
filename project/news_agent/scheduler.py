#!/usr/bin/env python3
"""
Quantum News Scheduler
Runs the daily news processing at scheduled intervals
"""

import schedule
import time
import subprocess
import logging
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("quantum_news_scheduler.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def run_daily_processing():
    """Execute the daily processing script"""
    try:
        logging.info(f"Starting scheduled daily processing at {datetime.now()}")

        # Run the daily processing script
        result = subprocess.run(
            [sys.executable, "daily_runner.py"],
            capture_output=True,
            text=True,
            timeout=1800  # 30 minute timeout
        )

        if result.returncode == 0:
            logging.info("✅ Daily processing completed successfully")
            if result.stdout:
                logging.info(f"Output: {result.stdout}")
        else:
            logging.error(f"❌ Daily processing failed with return code {result.returncode}")
            if result.stderr:
                logging.error(f"Error output: {result.stderr}")

    except subprocess.TimeoutExpired:
        logging.error("❌ Daily processing timed out after 30 minutes")
    except Exception as e:
        logging.error(f"❌ Error running daily processing: {e}")

def main():
    """Main scheduler loop"""
    logging.info("Quantum News Scheduler started")
    logging.info("Scheduled to run daily at 8:00 AM")

    # Schedule daily processing at 8:00 AM
    schedule.every().day.at("08:00").do(run_daily_processing)

    # Optional: Run immediately on startup for testing
    # schedule.every().minute.do(run_daily_processing)  # Uncomment for testing

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

    except KeyboardInterrupt:
        logging.info("Scheduler stopped by user")
    except Exception as e:
        logging.error(f"Scheduler error: {e}")

if __name__ == "__main__":
    main()