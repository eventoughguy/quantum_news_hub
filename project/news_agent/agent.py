import os
import asyncio
from google.genai import types
from google.adk.agents.llm_agent import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
#from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from news import *


os.environ['GOOGLE_API_KEY'] = ''
 
#input_url='https://news.mit.edu/2025/device-enables-direct-communication-among-multiple-quantum-processors-0321'
#input_url='https://arxiv.org/pdf/2305.08056'

async def summarize_news(input_url):
    session_service = InMemorySessionService()
    # session = session_service.create_session(
    #     state={}, app_name='quantume_news_app', user_id='user_fs'
    # )
    
    session = await session_service.create_session(
        state={}, app_name='quantume_news_app', user_id='user_fs'
    )


    news_extract = extract_news(input_url)
    #query = "\n".join([article["summary"] for article in news_extract])
    query=news_extract['summary']
    print(f"User Query: '{query[:50]}'")

    content = types.Content(role='user', parts=[types.Part(text=query)])
    root_agent = LlmAgent(
        model='gemini-2.0-flash',
        name='news_assistant',

        instruction='summarize the article into 250 words summary with plain English and make sure it sounds interesting.',
        # tools=tools,
    )

    runner = Runner(
        app_name='quantume_news_app',
        agent=root_agent,
        session_service=session_service,
    )

    print("Running agent...")

    try:
  
        async for event in runner.run_async(
            session_id=session.id, user_id=session.user_id, new_message=content
        ):
            
            if event.is_final_response():
                if event.content and event.content.parts:

                    # Assuming text response in the first part
                    final_response_text = event.content.parts[0].text
                elif event.actions and event.actions.escalate: # Handle potential errors/escalations
                    final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
                # Add more checks here if needed (e.g., specific error codes)
                break # Stop processing events once the final response is found
    
        return news_extract, final_response_text


    except Exception as e:
        print(f"Error while running async: {e}")



# if __name__ == '__main__':
#     try:
#         asyncio.run(async_main())
#     except Exception as e:
#         print(f"An error occurred: {e}")