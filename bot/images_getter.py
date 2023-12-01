from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import yaml
import os

def get_image(url, driver):
    
    try:
        # Open the webpage
        driver.get(url)

        # find element with the css class recaptcha-checkbox-border that is inside an iframe with the title reCAPTCHA
        iframe = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[title="reCAPTCHA"]')))
        print("Found checkbox iframe element")
        driver.switch_to.frame(iframe)
        print("Switched to checkbox iframe")
        checkbox = driver.find_element(By.CSS_SELECTOR, '.recaptcha-checkbox-border')
        print("Found checkbox element")
        checkbox.click()

        # Switch to the old frame
        driver.switch_to.default_content()
        print("Switched to parent window")

        # Find the image iframe by its title
        imageIframe = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[title="recaptcha challenge expires in two minutes"]')))
        
        print("Found image iframe")
        driver.switch_to.frame(imageIframe)
        print("Switched to image iframe")

        # Find the object name
        object_name = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'strong'))).text
        print("Found object element:", object_name)

        # Find the first element
        img_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img')))
        print("Found img element")
        
        # Save the image with a name that includes the object name and a number
        images = os.listdir('images')
        images = [image for image in images if image.startswith(object_name)]
        image_number = len(images) + 1
        image_name = object_name + '-' + str(image_number) + '.png'
        img_element.screenshot("images/" + image_name)

        return object_name
    except Exception as e:
        return str(e)

def get_images(url):
    service = Service(executable_path=ChromeDriverManager().install())
    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(service=service)
    # Get 100 images (we get the image and then reload the page)
    for i in range(100):
        get_image(url, driver)
        driver.refresh()


with open('config/config.yml', 'r') as config_file:
    config = yaml.safe_load(config_file)
# Access the URL from the configuration
website_url = config.get('website_url')
print(website_url)

img_source = get_images(website_url)
print(img_source)

