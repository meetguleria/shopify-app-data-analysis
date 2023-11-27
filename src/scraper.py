import requests
from bs4 import BeautifulSoup
import csv
import os
import logging
import time
import random

logging.basicConfig(level=logging.INFO)

def generate_search_url(base_url, keyword):
    formatted_keywords = '+'.join(keyword.split())
    return f"{base_url}?q={formatted_keywords}&programs%5B%5D=built_for_shopify"

def fetch_category_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def parse_app_list(html):
    soup = BeautifulSoup(html, 'html.parser')
    apps = []

    # Find all search result cards
    for app_card in soup.find_all("div", {"data-app-card-wrap": ""}):
        app_name_tag = app_card.find("a", href=True)
        if app_name_tag:
            name = app_name_tag.get_text(strip=True)
            url = app_name_tag['href']
            apps.append((name, url))
    return apps

def save_to_csv(app_data, filename="scraped_data.csv"):
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writeheader()
        writer.writerow(app_data)

def run_search():
    for keyword in keywords:
        search_url = generate_search_url(base_url, keyword)
        category_page = fetch_category_page(search_url)
        if category_page:
            app_list = parse_app_list(category_page)
            for app_data in app_list:
                save_to_csv(app_data)

        delay = random.uniform(1, 10)
        time.sleep(delay)

keywords = ["product recommendations", "product suggestions", "sales forecasting", 
"market analysis"]

if __name__ == "__main__":
    base_url = "https://apps.shopify.com/search"
    logging.info("Starting scraping process.")
    run_search()
    logging.info("Scraping process completed")