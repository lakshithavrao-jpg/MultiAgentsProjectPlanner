# NEXUS - Agentic AI Project Command Center

NEXUS is a multi-agent AI project planning platform.

It converts project ideas into structured project plans using
four specialized AI agents.

## AI Agents

1. Requirement Analyst
2. Software Architect
3. Project Manager
4. Proposal Generator

## Technology Stack

- Python
- Streamlit
- Groq API
- GPT-OSS 20B
- SQLite
- ReportLab

## Installation

Create a virtual environment:

python -m venv .venv

Activate it:

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

## Environment Configuration

Create a .env file.

Add:

GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b

## Run Application

python -m streamlit run app.py

## Features

- AI-powered project requirement analysis
- Automated software architecture
- Project management planning
- Project proposal generation
- Project history
- PDF report generation
- Markdown report generation