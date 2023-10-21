# This file is for accessing the web page

import requests
from bs4 import BeautifulSoup

def scrape_h1_title(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        h1_title = soup.find('h1').text
        return h1_title
    except Exception as e:
        return str(e)
