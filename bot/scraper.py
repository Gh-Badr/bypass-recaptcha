from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
    
def scrape_img_source(url,driver):

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

        # Switch to the parent frame
        driver.switch_to.default_content()
        print("Switched to parent window")

        # Find the image iframe by its title
        imageIframe = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[title="Le test reCAPTCHA expire dans deux minutes"]')))
        
        # switch to image frame
        print("Found image iframe")
        driver.switch_to.frame(imageIframe)
        print("Switched to image iframe")

        # Find the first image
        img_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img')))
        object_name = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'strong'))).text
        print("Found img and object elements")

        # Screenshot the image
        img_element.screenshot("images/image.png")
        size = img_element.get_attribute('class')
        print("Size: ", size)
        print("Object: ", object_name)

        return size,object_name

    except Exception as e:
        print(e)
        return False
    finally:
        # Close the browser
        driver.quit()