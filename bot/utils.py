import yaml
from PIL import Image
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import win32clipboard
import io


def load_yaml_param(file_path, parameter):
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            return data[parameter]
        
def wait_for_not_disabled(driver, locator):
        element = driver.find_element(locator[0], locator[1])
        if element.get_attribute("disabled"):
            return False
        else:
            return element
        
def send_image_to_clipboard(image_path):
        # Get the image from the path
        image = Image.open(image_path)
        output = io.BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        # Send the image to the clipboard
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()

def move_to_challenge_frame(driver):
        # Possible titles for the secondary iframe (this is hardcoded, needs to be improved)
        iframe_titles = ["Le test reCAPTCHA expire dans deux minutes", "recaptcha challenge expires in two minutes"]

        # Variable to track if the iframe has been found
        iframe_found = False

        # Try switching to one of the iframes
        for title in iframe_titles:
            try:
                # Wait and switch to the iframe if available
                WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, f'iframe[title="{title}"]')))
                iframe_found = True
                break  
            except:
                # Continue trying with the next title 
                continue

        # Check if the iframe has been found
        if not iframe_found:
            raise Exception("The required iframe was not found.")