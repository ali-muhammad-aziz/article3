from crewai import Crew, Process
from agents import news_researcher, writer_agent
from tasks import research_task, write_task

# Define the Crew with agents
crew = Crew(
    agents=[news_researcher, writer_agent],
    tasks=[research_task, write_task],
      Process=Process.sequential,
)

# Start the process with a specific topic
result = crew.kickoff(inputs={'topic': 'Dynamic Ai Traffic System'})

# Print the final result
print(result)