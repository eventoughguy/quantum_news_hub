import os
import asyncio
from dotenv import load_dotenv
from google.genai import types
from google.adk.agents.llm_agent import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
import logging
from enhanced_rss_parser import QuantumRSSParser

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class QuantumNewsAgent:
    def __init__(self, google_api_key=None):
        # Load API key from parameter, environment variable, or .env file
        if google_api_key:
            os.environ['GOOGLE_API_KEY'] = google_api_key
        elif not os.environ.get('GOOGLE_API_KEY'):
            raise ValueError("Google API key not found. Please set GOOGLE_API_KEY in your .env file or pass it as a parameter.")

        self.rss_parser = QuantumRSSParser()

    async def summarize_article_content(self, content):
        """Generate AI summary for article content"""
        try:
            session_service = InMemorySessionService()
            session = await session_service.create_session(
                state={}, app_name='quantum_news_app', user_id='user_fs'
            )

            # Truncate content if too long (to avoid token limits)
            max_content_length = 8000
            if len(content) > max_content_length:
                content = content[:max_content_length] + "..."
                logging.info("Content truncated due to length")

            prompt = f"""
            Please summarize the following quantum computing article in exactly 250 words.
            Make the summary engaging and accessible to general readers while preserving the key technical concepts.
            Use plain English and avoid jargon where possible.

            Article content:
            {content}
            """

            content_obj = types.Content(role='user', parts=[types.Part(text=prompt)])

            root_agent = LlmAgent(
                model='gemini-2.0-flash',
                name='quantum_news_summarizer',
                instruction='You are an expert science communicator specializing in quantum computing. Create engaging, accessible 250-word summaries that make complex quantum concepts understandable to general audiences.',
            )

            runner = Runner(
                app_name='quantum_news_app',
                agent=root_agent,
                session_service=session_service,
            )

            logging.info("Generating AI summary...")

            async for event in runner.run_async(
                session_id=session.id,
                user_id=session.user_id,
                new_message=content_obj
            ):
                if event.is_final_response():
                    if event.content and event.content.parts:
                        summary = event.content.parts[0].text
                        logging.info("Summary generated successfully")
                        return summary
                    elif event.actions and event.actions.escalate:
                        error_msg = f"Agent escalated: {event.error_message or 'No specific message.'}"
                        logging.error(error_msg)
                        return None

            return None

        except Exception as e:
            logging.error(f"Error generating summary: {e}")
            return None

    async def process_new_articles(self):
        """Process new articles and generate summaries"""
        try:
            # Fetch latest article from RSS
            new_article = self.rss_parser.fetch_latest_article()

            if new_article:
                logging.info(f"Processing new article: {new_article['title']}")

                # Generate AI summary
                summary = await self.summarize_article_content(new_article['content'])

                if summary:
                    # Update article with summary
                    success = self.rss_parser.update_article_summary(new_article['id'], summary)
                    if success:
                        logging.info("Article processed and summary saved successfully")
                        return {
                            'article': new_article,
                            'summary': summary,
                            'status': 'success'
                        }
                    else:
                        logging.error("Failed to save summary to database")
                        return {'status': 'error', 'message': 'Failed to save summary'}
                else:
                    logging.error("Failed to generate summary")
                    return {'status': 'error', 'message': 'Failed to generate summary'}
            else:
                logging.info("No new articles to process")
                return {'status': 'no_new_articles'}

        except Exception as e:
            logging.error(f"Error processing articles: {e}")
            return {'status': 'error', 'message': str(e)}

    async def process_existing_articles_without_summary(self):
        """Process existing articles that don't have summaries"""
        try:
            articles = self.rss_parser.get_articles_without_summary()
            processed_count = 0

            for article_id, title, content, link in articles:
                logging.info(f"Processing existing article: {title}")

                summary = await self.summarize_article_content(content)

                if summary:
                    success = self.rss_parser.update_article_summary(article_id, summary)
                    if success:
                        processed_count += 1
                        logging.info(f"Summary generated for: {title}")
                    else:
                        logging.error(f"Failed to save summary for: {title}")
                else:
                    logging.error(f"Failed to generate summary for: {title}")

            return {'processed_count': processed_count, 'total_articles': len(articles)}

        except Exception as e:
            logging.error(f"Error processing existing articles: {e}")
            return {'processed_count': 0, 'error': str(e)}

async def main():
    """Main function for testing"""
    agent = QuantumNewsAgent()

    # Process new articles
    result = await agent.process_new_articles()
    print(f"New article processing result: {result}")

    # Process existing articles without summaries
    backlog_result = await agent.process_existing_articles_without_summary()
    print(f"Backlog processing result: {backlog_result}")

if __name__ == "__main__":
    asyncio.run(main())