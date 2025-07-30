from crewai import Task
from tools import tool
from agents import news_researcher, writer_agent

research_task = Task(
   
    description=" Conduct thorough research on {topic} using the SerperDevTool. Use SerperDevTool to search for the latest news, trends, and updates related to the given topic. Gather reliable and relevant information from multiple sources to ensure accuracy and comprehensiveness.",
   
    tools=[tool], 
    expected_output="A well-structured research report on {topic} with key insights. A summarized report of the latest news articles and sources.",
     agent=news_researcher,
)

# Writing Task
write_task = Task(
    description=(
        "Write a formal, well-structured article in markdown format about {topic}, "
        "using the research from {research}. Use headings, paragraphs, bullet points, "
        "and a concluding section. Keep it professional and polished."
    ),
 expected_output="A multi-paragraph markdown article about {topic}.",
    tools=[tool],
    agent=writer_agent,
    async_execution=False,
    output_file='article_{topic}.md'
)

