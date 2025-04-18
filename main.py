# main.py
from crewai import Agent, Task, Crew
from pydantic import BaseModel
from typing import Optional, List, Dict
from crewai_tools import ScrapeWebsiteTool
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model_name="gpt-4o", temperature=0.7)

# ---------------------------
#  Output Schema
# ---------------------------
class ScrapedArticle(BaseModel):
    title: str
    author: Optional[str] = None
    date: Optional[str] = None
    summary: Optional[str] = None
    paragraphs: List[str]
    keywords: Optional[List[str]] = None
    reading_time: Optional[str] = None
    source_url: Optional[str] = None
    images: Optional[List[str]] = None
    metadata: Optional[Dict[str, str]] = None


# ---------------------------
# Tool: Prebuilt Web Scraper Tool
# ---------------------------
scraper_tool = ScrapeWebsiteTool()

# ---------------------------
# Agents
# ---------------------------

scraper_agent = Agent(
    role="Data Collection and Structuring Expert",
    goal="Collect content from the given URL and produce detailed and structured data",
    backstory=(
        "You are an expert at collecting meaningful content from websites, analyzing page structures, "
        "and presenting the information clearly according to a predefined schema."
    ),
    llm=llm,
    tools=[scraper_tool],
    verbose=True
)

writer_agent = Agent(
    role="Creative Content Writer",
    goal="Transform structured data into meaningful and compelling text",
    backstory=(
        "You are a creative writer who summarizes JSON-formatted content in an engaging way "
        "and transforms it into more readable text."
    ),
    llm=llm,
    verbose=True
)

# ---------------------------
# Tasks
# ---------------------------

scrape_task = Task(
    description=(
        "Please analyze the content of the following URL in detail: {url}\n\n"
        "You are required to extract the following information and return it in JSON format according to the 'ScrapedArticle' Pydantic schema:\n"
        "- Title (title)\n"
        "- Author (author)\n"
        "- Publication date (date)\n"
        "- Paragraphs within the content (paragraphs)\n"
        "- Summary of the content (summary)\n"
        "- Keywords (keywords)\n"
        "- Estimated reading time (reading_time)\n"
        "- Source page URL (source_url)\n"
        "- Image URLs on the page (images)\n"
        "- Page metadata such as title and description (metadata)\n\n"
        "You must return all of this strictly in JSON format that complies with the `ScrapedArticle` schema."
    ),
    agent=scraper_agent,
    expected_output="Structured JSON data containing the features of URL according to the ScrapedArticle model schema.", 
    output_pydantic=ScrapedArticle
)

write_task = Task(
    description=(
        "Using the `ScrapedArticle` data provided by the Scraper task, generate a user-friendly and fluent piece of writing.\n\n"
        "- It should be no more than 3 paragraphs.\n"
        "- Write a meaningful, informative, and concise text.\n"
        "- Clearly explain the essence and importance of the topic.\n"
        "- Creatively embed the data into the context.\n"
        "- Only use the data provided by the Scraper task. Do not add or make up anything yourself."
    ),
    agent=writer_agent,
    expected_output="A long and detailed text about the content of the web page",
    context=[scrape_task]
)

# ---------------------------
# Crew Definition
# ---------------------------

crew = Crew(
    agents=[scraper_agent, writer_agent],
    tasks=[scrape_task, write_task],
    verbose=True
)

# ---------------------------
# Initialization
# ---------------------------

#  A dynamic URL can be specified here
inputs = {
        "url": "https://en.wikipedia.org/wiki/Web_scraping"
    }

if __name__ == "__main__":
    final_output = crew.kickoff(inputs=inputs)
    print("\n--- Final Output ---\n")
    print(final_output)
