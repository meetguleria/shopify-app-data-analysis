import time
import random
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import logging

logging.basicConfig(level=logging.INFO)

base_url = "https://apps.shopify.com/search"

def generate_search_url(keyword):
    formatted_keywords = '+'.join(keyword.split())
    return f"{base_url}?q={formatted_keywords}&programs%5B%5D=built_for_shopify"

def scrape_page(driver, url, scraped_urls):
    try:
        driver.get(url)
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.ID, 
        "search_app_grid-content")))
        apps = []

        while True:
            # Scrolling will be done in phases:
            # Phase 1: Scroll down to 30-40% of the page
            scroll_1 = random.uniform(0.3, 0.4) * driver.execute_script("return document.body.scrollHeight")
            driver.execute_script(f"window.scrollTo(0, {scroll_1});")
            time.sleep(random.uniform(1, 3))

            # Phase 2: Quick random scroll up 3-7% of the initial scroll
            scroll_up = scroll_1 * random.uniform(0.8, 0.9)
            driver.execute_script(f"window.scrollBy(0, -{scroll_up});")
            time.sleep(random.uniform(0.5, 1))

            #Phase 3: Scroll down to 80-90% of the page
            scroll_2 = random.uniform(0.8, 0.9) * driver.execute_script("return document.body.scrollHeight")
            driver.execute_script(f"window.scrollTo(0, {scroll_2});")
            time.sleep(random.uniform(1, 3))

            # Extract app information
            app_elements = driver.find_elements(By.CSS_SELECTOR, '#search_app_grid-content div[data-app-card-wrap]')
            for app in app_elements:
                name = app.find_element(By.CSS_SELECTOR, 'div.tw-text-heading-6 a').text
                app_url = app.find_element(By.CSS_SELECTOR, 'div.tw-text-heading-6 a').get_attribute('href')
                apps.append([name, app_url])

                # Check for Duplicates
                if app_url not in scraped_urls:
                    apps.append([name, app_url])
                    scraped_urls.add(app_url)
            try: 
                next_button_selector = "#pagination_controls > div > section > section.tw-block.lg\\:tw-hidden > div > a:nth-child(1)"
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, next_button_selector))
                )
                next_button.click()
                WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.ID, "search_app_grid-context")))
                time.sleep(random.uniform(1, 10))
            except NoSuchElementException:
                break 
            except Exception as e:
                logging.error(f"Error interacting with pagination: {e}")
                break
        return apps

    except Exception as e:
        logging.error(f"An error occurred while scraping {url}: {e}")
        return []

def save_to_csv(app_data, filename="scraped_data.csv"):
    file_exists = os.path.isfile(filename)
    with open (filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['App Name', 'URL'])
        for app in app_data:
            writer.writerow(app)

def run_search():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    #initialize the chrome driver
    driver = webdriver.Chrome(options=options)
    scraped_urls = set()

    try:
        for keyword in ["product recommendations", "product suggestions", "sales forecasting", "market analysis"]:
            search_url = generate_search_url(keyword)
            apps = scrape_page(driver, search_url, scraped_urls)
            save_to_csv(apps)

            time.sleep(random.uniform(1, 10))

    except Exception as e:
        logging.error(f"An error ocurred in run_search: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    logging.info("Starting scraping process.")
    run_search()
    logging.info("Scraping process completed")