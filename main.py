from bot.GridVisionClient import GridVisionClient
from bot.utils import load_yaml_param
from bot.scraper import scrape_img_source
from bot.bypass import bypassing_google_captcha

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import yaml

def send_to_gpt(object, size):
    client = GridVisionClient()
    client.start_chat()
    response = client.send_image_and_get_response("images/image.png", object, size)
    print("GPT-3's response: ", response)
    client.close()
    return response


def main():
    

    url = load_yaml_param("config/config.yml","website_url")

    try:

        # Initialize the Chrome WebDriver
        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        
        # Get the picked the object from the recaptcha website
        size, object = scrape_img_source(url,driver)

        # Send the image and get the response (The response is a list of numbers that represent the grid)
        response = send_to_gpt(object, size)

        # Apply GPT response to bypass recaptcha
        bypassing_google_captcha(driver, size, response)

    except Exception as e:
        print(e)
    
    finally:
        input("Press Enter to continue...")


if __name__ == "__main__":
    main()

    