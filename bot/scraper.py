from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bot.utils import move_to_challenge_frame

def open_img_frame(url,driver):

    try:
        # Open the webpage
        driver.get(url)
        input("Press enter to continue")
        # find element with the css class recaptcha-checkbox-border that is inside an iframe with the title reCAPTCHA
        iframe = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[title="reCAPTCHA"]')))
        print("Found checkbox iframe element")
        driver.switch_to.frame(iframe)
        print("Switched to checkbox iframe")
        checkbox = driver.find_element(By.CSS_SELECTOR, '.recaptcha-checkbox-border')
        print("Found checkbox element")
        checkbox.click()



    except Exception as e:
        print(e)
    
def scrape_img_source(driver):

    driver.switch_to.default_content()
    print("Switched to parent window")

    try:
        # move to challenge frame
        move_to_challenge_frame(driver)

        # Find the first image
        img_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img')))
        object_name = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'strong'))).text
        print("Found img and object elements")

        # Screenshot the image
        img_element.screenshot("images/image.png")
        size = int(img_element.get_attribute('class')[-1])
        print("Size: ", size)
        print("Object: ", object_name)

        return size,object_name

    except Exception as e:
        print(e)
        return False