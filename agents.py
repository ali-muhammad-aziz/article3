import os
from crewai import Agent, LLM  # Sahi tarika

from tools import tool

from dotenv import load_dotenv
load_dotenv()

## call gemini models
llm = LLM(model="gemini/gemini-2.0-flash-exp",
                           temperature=0.5,
                           api_key=os.getenv("GOOGLE_API_KEY"))

# Define Researcher Agent
news_researcher = Agent(
    role="News Researcher",
    goal="Find the latest information about a given topic from reliable sources.",
    backstory="An AI-powered researcher that gathers the most relevant news articles and insights.",
    verbose=False,
    memory =True,


    allow_delegation= True,
    tools=[tool],
    llm=llm
)

writer_agent = Agent(
    role="News Writer",
    goal="Summarize the collected news and write a well-structured article.",
    backstory="An AI journalist who writes engaging and informative articles.",
    verbose=False,
    memory=True,

    allow_delegation=False,
    tools=[tool],
    llm=llm
)
