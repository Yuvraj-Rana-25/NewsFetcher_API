# main.py

import os
import requests
from dotenv import load_dotenv
import json

# 1. Loaded API key
load_dotenv()
API_KEY = os.getenv('NEWSDATA_API_KEY')

# 2. Defined function to fetch headlines
def fetch_headlines(topic, language='en', country='in'):
    url = 'https://newsdata.io/api/1/news'
    params = {
        'apikey': API_KEY,
        'q': topic,
        'language': language,
        'country': country
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Failed to fetch news: {response.status_code}")
        return []

    data = response.json()
    return data.get('results', [])

# 3. Defined function to save headlines to file
def save_to_json(headlines, filename='headlines.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(headlines, f, indent=4)
    print(f"Saved {len(headlines)} headlines to {filename}")

# 4. Script entry point
if __name__ == '__main__':
    topic = input("Enter a topic to search for news: ").strip()
    headlines = fetch_headlines(topic)

    if not headlines:
        print("No news found.")
    else:
        for i, article in enumerate(headlines[:5], start=1):
            print(f"{i}. {article['title']}")

        save_to_json(headlines)

# 5. Save headlines to database
from db import save_to_db

headlines = fetch_headlines(topic)
save_to_db(headlines, topic)
