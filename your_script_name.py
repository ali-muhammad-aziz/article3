import os
os.environ["CREWAI_DISABLE_TELEMETRY"] = "1"  # Disable telemetry if needed

import streamlit as st
import json

# ===== CrewAI Imports =====
from crewai import Crew, Process  # type: ignore
from agents import news_researcher, writer_agent
from tasks import research_task, write_task

# ===== Basic Page Configuration =====
st.set_page_config(
    page_title="AI Research Assistant",
    layout="centered"
)

# ===== Custom CSS Styling for Dark Theme =====
st.markdown("""
<style>
/* Dark background for the body */
body {
    background-color: #121212;
    color: #e0e0e0;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
/* Main container styling */
.stApp {
    background: #1e1e1e;
    border-radius: 15px;
    padding: 2rem;
    max-width: 900px;
    margin: 2rem auto;
    box-shadow: 0 10px 20px rgba(0,0,0,0.7);
}
/* Title styling */
h1 {
    color: #ffffff !important;
    text-align: center;
    font-weight: 700;
}
/* Description styling */
.stMarkdown p {
    color: #cccccc;
    font-size: 1.1rem;
    text-align: center;
}
/* Input field styling: white text on dark background */
.stTextInput input {
    background-color: #333333 !important;
    color: #ffffff !important;
    border: 1px solid #444444;
    border-radius: 5px;
    padding: 0.5rem;
}
/* Label styling for the input */
.stTextInput > label {
    color: #bbbbbb;
    font-weight: 600;
    font-size: 1.1rem;
}
/* Button styling */
div.stButton > button {
    background-color: #bb86fc;
    color: #121212;
    border: none;
    border-radius: 50px;
    padding: 1rem 2rem;         /* Increased padding */
    font-size: 1.2rem;          /* Increased font size */
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.3s ease;
    display: block;             /* Make button a block element */
    margin: 30px auto 0 auto;             /* Center the button */
}
div.stButton > button:hover {
    background-color: #9b59b6;
}

/* Styling for code block output */
pre {
    background-color: #2e2e2e;
    color: #e0e0e0;
    padding: 1rem;
    border-radius: 5px;
    overflow-x: auto;
}
</style>
""", unsafe_allow_html=True)

# ===== Title and Description =====
st.title("AI Research Assistant")
st.write("Enter a topic below and click **Run Research** to get the latest insights.")

# ===== User Input =====
topic = st.text_input("Topic", placeholder="Enter your research topic here...")

# ===== Run the Agent on Button Click =====
if st.button("Run Research"):
    if topic.strip():
        with st.spinner("Running research, please wait..."):
            crew = Crew(
                agents=[news_researcher, writer_agent],
                tasks=[research_task, write_task],
                process=Process.sequential,
                verbose=True
            )
            result = crew.kickoff(inputs={'topic': topic.strip()})
        st.success("Research Completed!")
        st.markdown("<h3 style='text-align: center; color: #ffffff;'>Research Result</h3>", unsafe_allow_html=True)
        try:
            parsed = json.loads(result)
            formatted_json = json.dumps(parsed, indent=2)
            st.code(formatted_json, language="json")
        except Exception as e:
            st.write(result)
    else:
        st.warning("Please enter a valid topic!")
