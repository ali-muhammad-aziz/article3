import os
os.environ["CREWAI_DISABLE_TELEMETRY"] = "1"  # Disable telemetry if needed

import streamlit as st
import json
import re

# ===== CrewAI Imports =====
from crewai import Crew, Process
from agents import news_researcher, writer_agent
from tasks import research_task, write_task

# ===== Basic Page Configuration =====
st.set_page_config(
    page_title="Multi AI Agent Article Writer",
    layout="centered"
)

# ===== Custom CSS =====
st.markdown("""
<style>
body::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('https://images.rigzone.com/images/news/articles/ADNOC-Announces-Launch-of-Agentic-AI-Solution-178717-582x327.webp') no-repeat center center;
    background-size: cover;
    opacity: 0.3;
    z-index: -1;
}

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
h1 {
    font-weight: 700;
    text-align: center;
    /* Animated gradient background */
    background: linear-gradient(270deg, #00bcd4, #ff4081, #4caf50);
    background-size: 600% 600%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: animateGradient 5s ease infinite;
}

@keyframes animateGradient {
    0% {
        background-position: 0% 50%;
    }
    50% {
        background-position: 100% 50%;
    }
    100% {
        background-position: 0% 50%;
    }
}

/* Description styling */
.stMarkdown p {
    color: #cccccc;
    font-size: 1.1rem;
    text-align: center;
}

/* Force markdown headings to be bigger and white in .stMarkdown content */
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
.stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
    color: #ffffff !important;
    font-weight: bold !important;
    margin-top: 1.2em;
    margin-bottom: 0.6em;
}
.stMarkdown h1 { font-size: 2.2rem !important; }
.stMarkdown h2 { font-size: 1.8rem !important; }
.stMarkdown h3 { font-size: 1.6rem !important; }
.stMarkdown h4 { font-size: 1.4rem !important; }
.stMarkdown h5 { font-size: 1.2rem !important; }
.stMarkdown h6 { font-size: 1.1rem !important; }

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
    background-color: #b0b0b0;
    color: #121212;
    border: none;
    border-radius: 50px;
    padding: 1rem 2rem;
    font-size: 1.2rem;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.3s ease;
    display: block;
    margin: 10px auto 0 auto;
}
div.stButton > button:hover {
    background-color: #9b59b6;
}

/* Styling for code block output (just in case) */
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
st.title("Multi AI Agent Article Writer")
st.write("""
Enter a topic below and click **Run Research** to watch the Researcher Agent work first,
then pass its findings to the Writer Agent for a final article.
""")

# ===== Input Field =====
topic = st.text_input("Topic", placeholder="Enter your research topic here...")

# ===== Regex-based removal function =====
def remove_backticks_and_markdown_label(text) -> str:
    """
    Remove triple backticks and ANY 'markdown' substring (case-insensitive).
    This handles things like 'markdown:', 'Markdown', 'MARKDOWN' etc.
    """
    text_str = str(text)
    # Remove triple backticks
    text_str = text_str.replace('```', '')
    # Remove all forms of 'markdown' ignoring case
    text_str = re.sub(r'(?i)markdown', '', text_str)
    return text_str

# ===== Run the Agents on Button Click =====
if st.button("Generate Article"):
    if topic.strip():
        # Step 1: Researcher Agent
        with st.spinner("Researcher Agent is working..."):
            crew_research = Crew(
                agents=[news_researcher],
                tasks=[research_task],
                process=Process.sequential,
                verbose=False
            )
            research_result = crew_research.kickoff(inputs={'topic': topic.strip()})

        st.success("Researcher Agent completed its task!")
        st.info("Passing data to Writer Agent for final article...")

        # Convert research_result to string if needed
        if isinstance(research_result, dict):
            research_result_str = json.dumps(research_result)
        else:
            research_result_str = str(research_result)

        # Step 2: Writer Agent
        with st.spinner("Writer Agent is generating the final article..."):
            crew_writer = Crew(
                agents=[writer_agent],
                tasks=[write_task],
                process=Process.sequential,
                verbose=True
            )
            final_result = crew_writer.kickoff(inputs={
                'topic': topic.strip(),
                'research': research_result_str
            })

        st.success("Writer Agent completed the final article!")
        st.markdown("<h3 style='text-align: center; color: #ffffff;'>Final Article</h3>", unsafe_allow_html=True)

        try:
            # Check if final_result is valid JSON
            parsed = json.loads(final_result)
            # If writer agent returns JSON with a "markdown" field, render that
            if "markdown" in parsed:
                clean_markdown = remove_backticks_and_markdown_label(parsed["markdown"])
                st.markdown(clean_markdown, unsafe_allow_html=True)
            # Or if there's a "raw" field, use that
            elif "raw" in parsed:
                clean_raw = remove_backticks_and_markdown_label(parsed["raw"])
                st.markdown(clean_raw, unsafe_allow_html=True)
            else:
                # If no specific field, fallback to rendering the entire JSON as markdown
                clean_result = remove_backticks_and_markdown_label(final_result)
                st.markdown(clean_result, unsafe_allow_html=True)
        except:
            # If JSON parsing fails, just treat the result as markdown
            clean_result = remove_backticks_and_markdown_label(final_result)
            st.markdown(clean_result, unsafe_allow_html=True)
    else:
        st.warning("Please enter a valid topic!")

import litellm
import time

params = {
    "model": "vertexai/gemini-pro",  # Ya "gpt-4o" if switching
    "messages": [
        {"role": "user", "content": "What is AI?"}
    ],
    "api_key": "tumhara_actual_api_key"
}

# Retry Loop
for i in range(3):
    try:
        response = litellm.completion(**params)
        print("✅ Response:", response)
        break
    except litellm.InternalServerError as e:
        print(f"🔁 Attempt {i+1} failed: {e}")
        time.sleep(5)
