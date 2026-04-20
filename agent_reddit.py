import os
import json
import logging
import requests
from dotenv import load_dotenv
from apify_client import ApifyClient

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("RedditAgent")

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")

def find_reddit_pain_points():
    """Tool: Scrapes Google for Reddit threads discussing prediction market problems."""
    logger.info("Executing Apify search for Reddit pain points...")
    client = ApifyClient(APIFY_API_TOKEN)
    
    # Using a Google Dork to target Reddit complaints specifically
    run_input = {
        "queries": "site:reddit.com/r/predictionmarkets OR site:reddit.com/r/crypto \"prediction market\" (problem OR issue OR sucks OR fees OR liquidity)",
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
        return results
    except Exception as e:
        logger.error(f"Apify scraping failed: {e}")
        return []

def generate_reddit_reply(thread_context):
    """Feeds the thread context to the LLM to generate a natural, non-spam reply."""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "openrouter/free",
        "messages": [
            {
                "role": "system", 
                # Forcing a highly natural, human-like talking tone to bypass spam filters
                "content": "You are a casual, relatable Reddit user. You write in a natural talking tone. Absolutely no formal language, no bullet points, and no marketing jargon. You must sound completely human."
            },
            {
                "role": "user", 
                "content": f"Read this snippet from a Reddit thread where someone is complaining about prediction markets: '{thread_context}'. Write a short 1-2 sentence reply. Empathize with their specific problem naturally, and casually mention you just started looking into CrowdWisdomTrading as an alternative. Keep it super low-key."
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return "Error generating reply."
    except Exception as e:
        return f"LLM Error: {e}"

def run_outreach_agent():
    logger.info("Initializing Reddit Outreach Agent...")
    threads = find_reddit_pain_points()
    
    if not threads:
        logger.warning("No Reddit threads found.")
        return
        
    print("\n" + "="*70)
    print("🚀 REDDIT OUTREACH CAMPAIGN (5 DRAFTS)")
    print("="*70)
    
    for i, thread in enumerate(threads, 1):
        logger.info(f"Drafting reply for thread {i}/5...")
        reply = generate_reddit_reply(thread['snippet'])
        
        print(f"\n[TARGET {i}]")
        print(f"Thread Title: {thread['title']}")
        print(f"Link: {thread['url']}")
        print(f"Pain Point Context: {thread['snippet']}")
        print(f"--> DRAFTED REPLY:\n\"{reply}\"")
        
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    run_outreach_agent()