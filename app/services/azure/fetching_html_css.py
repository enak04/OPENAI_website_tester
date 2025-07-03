import requests
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # /Backend/app/azure_services
themes2_path = os.path.abspath(os.path.join(BASE_DIR, "..","..", "data", "themes2.json")) 

def call_fetch_html_css_api(store_url: str, store_id: str, base_url: str = "http://127.0.0.1:5000"):
    endpoint = f"{base_url}/fetch-html-css-and-index"
    payload = {
        "url": store_url,
        "store_id": store_id
    }
    print(payload)

    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling fetch-html-css API for {store_id}: {e}")
        return None

if __name__ == "__main__":
    # Load themes2 JSON
    try:
        with open(themes2_path, "r", encoding="utf-8") as f:
            themes = json.load(f)
    except Exception as e:
        print(f"Failed to load themes2.json: {e}")
        exit(1)

    for theme in themes:
        store_url = theme["url"]
        store_id = theme["title"].lower()  # assuming title is like "FreshGo" → "freshgo"

        print(f"\nCalling API for: {store_id}")
        result = call_fetch_html_css_api(store_url, store_id)

        if result:
            print(f"API Response for {store_id}:", result)
        else:
            print(f"Failed to fetch HTML/CSS for {store_id}")