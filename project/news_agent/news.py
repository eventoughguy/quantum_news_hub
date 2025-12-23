import newspaper
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def extract_news(url_string):
    """ Extracts quantum computing news articles from the given source """
    #news_source = 'https://news.mit.edu/2025/device-enables-direct-communication-among-multiple-quantum-processors-0321'
    paper = newspaper.build(url_string, memoize_articles=False)

    #articles_data = []  # Store extracted articles

    for article in paper.articles:
        if 'quantum' in article.url.lower():
            try:
                article.download()
                article.parse()

                article_info = {
                    "title": article.title,
                    "url": article.url,
                    "summary": article.text  # Trim to 500 characters
                }

                print(f"Found first quantum computing article: {article.title}")
                logging.info(f"Extracted: {article.title}")

                return article_info  # Stop after first match

            except Exception as e:
                logging.warning(f"Error processing article {article.url}: {e}")

    return None
