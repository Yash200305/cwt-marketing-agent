import os
from dotenv import load_dotenv
from apify_client import ApifyClient

# Load the environment variables from your .env file
load_dotenv()

# Initialize the ApifyClient with your token
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
client = ApifyClient(APIFY_API_TOKEN)

# Prepare the actor input parameters
run_input = {
    "queries": "CrowdWisdomTrading prediction markets competitors",
    "maxPagesPerQuery": 1,
    "resultsPerPage": 5,
    "countryCode": "us",
}

print("Starting Apify Google Search actor... (This may take a minute)")

# Run the official Google Search scraper actor and wait for it to finish
run = client.actor("apify/google-search-scraper").call(run_input=run_input)

print("Fetch complete! Here are the top results:\n")

# The actual search results are nested inside the 'organicResults' list
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    organic_results = item.get("organicResults", [])
    
    # Loop through just the first 5 results
    for res in organic_results[:5]: 
        print(f"Title: {res.get('title')}")
        print(f"URL: {res.get('url')}")
        print(f"Snippet: {res.get('description')}")
        print("-" * 50)