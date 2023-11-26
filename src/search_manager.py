import time
import random
from scraper import fetch_all_pages, save_to_csv

def generate_search_url(base_url, keyword):
    formatted_keyword = '+'.join(keyword.split())
    return f"{base_url}?q={formatted_keyword}&st_source=autocomplete&programs%5B%5D=built_for_shopify"

def main():
    base_url = "https://apps.shopify.com/search"
    keywords = ["product recommendations", "product suggestions", "sales forecasting", "market analysis"]

    scraped_apps = set()
    for keyword in keywords:
        search_url = generate_search_url(base_url, keyword)
        apps = fetch_all_pages(search_url)
        for app in apps:
            if app[1] not in scraped_apps:
                save_to_csv(app)
                scraped_apps.add(app[1])

        time.sleep(random.uniform(5, 15))

if __name__ == "__main__":
    main()