import os
import json
import logging
import requests
from dotenv import load_dotenv
from apify_client import ApifyClient

# Configure logging for extra assessment points
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ResearcherAgent")

# Load the environment variables
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")

def search_competitors(query: str):
    """Tool: Scrapes Google for competitor data using Apify."""
    logger.info(f"Executing Apify search for: {query}")
    client = ApifyClient(APIFY_API_TOKEN)
    
    run_input = {
        "queries": query,
        "maxPagesPerQuery": 1,
        "resultsPerPage": 5,
        "countryCode": "us",
    }
    
    try:
        run = client.actor("apify/google-search-scraper").call(run_input=run_input)
        results = []
        
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            organic_results = item.get("organicResults", [])
            for res in organic_results[:5]:
                results.append({
                    "title": res.get("title"),
                    "url": res.get("url"),
                    "snippet": res.get("description")
                })
                
        logger.info(f"Successfully retrieved {len(results)} results from Apify.")
        return results
        
    except Exception as e:
        logger.error(f"Apify scraping failed: {e}")
        return []

def run_researcher_agent(company_name: str, product_url: str):
    """The core agent logic integrating the tool and the LLM."""
    logger.info(f"Initializing Researcher Agent for {company_name}")
    
    # Step 1: Use the tool to gather raw data
    search_query = f"{company_name} prediction markets competitors"
    raw_data = search_competitors(search_query)
    
    if not raw_data:
        logger.warning("No data found to analyze.")
        return
        
    # Step 2: Feed data to the LLM for synthesis
    logger.info("Sending raw data to OpenRouter for synthesis...")
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Convert raw data list to a readable string for the prompt
    data_string = json.dumps(raw_data, indent=2)
    
    data = {
        "model": "openrouter/free",
        "messages": [
            {
                "role": "system", 
                "content": "You are an elite Market Research Agent. Your job is to analyze raw search data and identify key competitors and product positioning."
            },
            {
                "role": "user", 
                "content": f"Analyze the following search results for {company_name} ({product_url}). Identify the main competitors and briefly summarize their market presence based ONLY on this data:\n\n{data_string}"
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            reply = response.json()['choices'][0]['message']['content']
            logger.info("Analysis complete.")
            
            print("\n" + "="*60)
            print("📊 RESEARCHER AGENT REPORT")
            print("="*60)
            print(reply)
            print("="*60 + "\n")
            
        else:
            logger.error(f"OpenRouter Error {response.status_code}: {response.text}")
            
    except Exception as e:
        logger.error(f"LLM synthesis failed: {e}")

if __name__ == "__main__":
    # Target specified in the project scope
    run_researcher_agent("CrowdWisdomTrading", "https://www.crowdwisdomtrading.com/")