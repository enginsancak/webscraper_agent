# webscraper_agent
An AI-powered dual-agent system that scrapes content from a given URL and transforms it into a human-readable summary using GPT-4o. Includes structured data extraction with a Pydantic schema and creative content generation.

## 🚀 Features

- 🔗 **URL-based Web Scraping**
- 🧠 **Dual-Agent Architecture** (Scraper + Writer)
- 🧾 **Structured Output Schema** using `pydantic`
- ✍️ **GPT-4o-Powered Natural Language Generation**
- 🛠️ **Built-in Tool** `ScrapeWebsiteTool` from `crewai_tools`

---

## 🧱 System Overview

This project uses two cooperative AI agents powered by OpenAI's GPT-4o model:

### 🧹 Scraper Agent
- **Role:** Data Collection and Structuring Expert  
- **Goal:** Extracts meaningful content (title, author, date, paragraphs, keywords, images, etc.) from a given URL.
- **Output:** JSON structured according to a custom `ScrapedArticle` schema.

### ✍️ Writer Agent
- **Role:** Creative Content Writer  
- **Goal:** Takes the structured data from the Scraper Agent and rewrites it into a clear, human-friendly narrative with up to 3 meaningful paragraphs.
- **Output:** Readable, high-level summary of the web page.

---

## 🛠️ Technologies & Tools

| Technology | Description |
|------------|-------------|
| **Python** | Main programming language |
| **CrewAI** | Framework for building multi-agent systems |
| **LangChain (OpenAI)** | GPT-based LLM interfaces |
| **Pydantic** | Validates and enforces structured schema (`ScrapedArticle`) |
| **ScrapeWebsiteTool** | Prebuilt scraping tool that extracts visible content from any valid URL |
| **dotenv** | For securely loading environment variables such as the OpenAI API key 
