import asyncio
from pyppeteer import launch
import csv
import os
import logging
import time
import random

logging.basicConfig(level=logging.INFO)

base_url = "https://apps.shopify.com/search"

def generate_search_url(keyword):
    formatted_keywords = '+'.join(keyword.split())
    return f"{base_url}?q={formatted_keywords}&programs%5B%5D=built_for_shopify"

async def scrape_page(page, url):
    try: 
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
        await page.goto(url, { 'waitUntil': 'networkidle0'})
        await page.waitForSelector("#search_app_grid-content", {"timeout": 120000})
    except Exception as e:
        logging.warning("Retrying due to timeout...")
        await page.reload()
        await page.waitForSelector("#search_app_grid-content", {"timeout": 120000})

        await page.evaluate('_ => window.scrollBy(0, window.innerHeight)')
        apps = await page.evaluate('''() => {
            const apps = [];
            const appElements = document.querySelectorAll('#search_app_grid-content div[data-app-card-wrap]');
            for (const app of appElements) {
                const nameElement = app.querySelector('div.tw-text-heading-6 a');
                const name = nameElement ? nameElement.innerText: 'Unknown';
                const url = nameElement ? nameElement.href : 'Unknown';
                apps.push([name, url]);
            }
            return apps;
        }''')
        print("Sample extracted apps:", apps[:5])
        return apps
    except Exception as e:
        logging.error(f"An error occurred while scraping {url}: {e}")
        content = await page.content()
        logging.error("Page Content: " + content[:500])
        return []

def save_to_csv(app_data, filename="scraped_data.csv"):
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['App Name', 'URL'])
        for app in app_data:
            writer.writerow(app)

async def run_search():
    try:
        browser = await launch(headless=False)
        context = await browser.createIncognitoBrowserContext()
        page = await context.newPage()

        for keyword in ["product recommendations", "product suggestions", "sales forecasting", "market analysis"]:
            search_url = generate_search_url(keyword)
            apps = await scrape_page(page, search_url)
            save_to_csv(apps)
        
            delay = random.uniform(1, 10)
            await asyncio.sleep(delay)

    except Exception as e:
        logging.error(f"An error occurred in run_search: {e}")
    finally:
        await browser.close()

if __name__ == "__main__":
    logging.info("Starting scraping process.")
    asyncio.get_event_loop().run_until_complete(run_search())
    logging.info("Scraping process completed")