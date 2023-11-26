import requests
from bs4 import BeautifulSoup
import csv
import os

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

    #Replace 

    return apps

def save_to_csv(app_data, filename="scraped_data.csv"):
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['App Name', 'URL'])
        if not file_exists:
            writer.writeheader()
        writer.writerow({ 'App Name': app_data[0], 'URL': app_data[1] })