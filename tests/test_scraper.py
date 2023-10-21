# Testing the scrapping process

import unittest
import yaml
from bot.scraper import scrape_h1_title

# Load the configuration from the config.yml file
with open('config/config.yml', 'r') as config_file:
    config = yaml.safe_load(config_file)
# Access the URL from the configuration
website_url = config.get('website_url')

class TestWebScraper(unittest.TestCase):
    def test_scrape_h1_title(self):
        h1_title = scrape_h1_title(website_url)
        self.assertIsNotNone(h1_title)
        self.assertEqual(h1_title,'Google reCAPTCHA test')

if __name__ == '__main__':
    unittest.main()