# CWT Product Marketing Agent System

## Project Overview
This repository contains a backend Python project designed to automate market research and targeted outreach within the prediction markets space for CrowdWisdomTrading. The system utilizes an agentic framework approach, leveraging Apify for data scraping and OpenRouter (using high-tier free LLMs) as the reasoning engine.

## Architectural Approach
The project is divided into three distinct, specialized agents that handle the complete marketing workflow:

### 1. The Researcher & Analyst Agent (`agent_researcher.py`)
* **Objective:** Identify competitors and synthesize a market presence report.
* **Mechanism:** This agent utilizes a custom tool built with the Apify Google Search scraper to pull real-time data on CrowdWisdomTrading's competitors. The raw data is then routed to an OpenRouter LLM, which parses the snippets and generates a formatted, tiered competitive analysis report.

### 2. The Reddit Outreach Specialist (`agent_reddit.py`)
* **Objective:** Find user pain points on Reddit and draft highly natural, non-spam replies positioning the product as a solution.
* **Mechanism:** This agent uses advanced Google Dorks via Apify to isolate specific Reddit threads (`r/predictionmarkets`, `r/crypto`) where users are complaining about fees, liquidity, or platform issues. It then feeds this context to an LLM prompted specifically to utilize a casual, relatable "human-like" tone to draft outreach replies.

### 3. The Closed Learning Loop (`agent_learning_loop.py`)
* **Objective:** Implement a self-reflection mechanism to ensure outreach quality.
* **Mechanism:** Operating as an evaluator, this agent takes drafted replies and critiques them against a set of anti-spam criteria. If a draft sounds too formal or promotional, the loop identifies the problematic phrasing and regenerates a refined, conversational output before final submission.

## Tech Stack
* **Language:** Python
* **LLM Provider:** OpenRouter API (utilizing automatic routing `openrouter/free` to ensure highest available bandwidth and model stability).
* **Data Scraping:** Apify API (Google Search Scraper).

## Local Setup & Execution

### 1. Environment Configuration
Ensure you have Python installed, then set up your isolated environment and install the required dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: .\venv\Scripts\activate
pip install apify-client python-dotenv requests

### 2. API Keys
Create a `.env` file in the root directory and add your platform tokens:
```env
OPENROUTER_API_KEY="your_openrouter_key"
APIFY_API_TOKEN="your_apify_key"

### 3. Running the Agents
Execute the agents individually to view their real-time logging and final outputs:

```bash
python agent_researcher.py
python agent_reddit.py
python agent_learning_loop.py