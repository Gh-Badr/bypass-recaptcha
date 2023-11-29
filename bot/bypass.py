from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bot.utils import move_to_challenge_frame

def bypassing_google_captcha(driver, size, index_imgs):

    images_indexes = [int(i) for i in index_imgs]

    try:
        # Return to the main document
        driver.switch_to.default_content()

        # move to challenge frame
        move_to_challenge_frame(driver)
        
        # Wait for the presence of <tr> elements
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "tr")))

        # Find and store the <tr> elements
        rows = driver.find_elements(By.TAG_NAME, "tr")

        # Click on the corresponding images
        for index in images_indexes:
            index = index - 1  # Adjust the index (base 0)
            row = rows[index // size]  # Select the row
            image = row.find_elements(By.TAG_NAME, "td")[index % size]  # Select the image
            image.click()

        # Click on the verification button
        verify = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "rc-button-default")))
        verify.click()

        # Check for the style change of the checkbox
        driver.switch_to.default_content()
        iframe = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[title="reCAPTCHA"]')))
        driver.switch_to.frame(iframe)
        checkmark = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,"recaptcha-checkbox-checkmark")))
        print("style")
        print(checkmark.get_attribute("style"))
        if checkmark.get_attribute("style"):
            return True
        return False

    except Exception as e:
        print("An error occurred:", e)
