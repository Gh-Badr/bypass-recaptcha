from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bot.utils import load_yaml_param, send_image_to_clipboard, wait_for_not_disabled
from PIL import Image
import time

class BingChatClient:
    def __init__(self):
        # Define the service that will be used to run the EdgeDriver
        self.service = Service(executable_path=ChromeDriverManager().install())
        # Define the Edge options
        chrome_options = Options()
        user_data_dir = load_yaml_param(r"config/config.yml", "user-data-dir")
        chrome_options.add_argument(f"user-data-dir={user_data_dir}")
        profile_directory = load_yaml_param(r"config/config.yml", "profile-directory")
        chrome_options.add_argument(f"profile-directory={profile_directory}")
        chrome_options.add_argument("--start-maximized")
        # Create the driver
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)

    def prompt_image(self, image_path, object, size):
        # get the size of the image
        image = Image.open(image_path)
        grid_size = str(size) + 'x' + str(size)
        # Load the prompt template
        template = load_yaml_param(r"config/config.yml", "prompt-template")
        # Replace the placeholders with the actual values
        prompt = template.format(grid_size=grid_size, object=object)

        print("Prompt: ", prompt)

        return prompt

    def start_chat(self):
        self.driver.get("https://www.bing.com/search?form=WSBCTB&toWww=1&redig=C514C489F4134B8EB3B4F8A2E34B91F5&q=Que+peut+fair+le+nouveau+chat+de+Bing%3F&showconv=1")
        try:
            # Wait for the accept/reject cookies button to be ready
            cookies_button = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#bnp_btn_reject')))
            # Click on the reject button
            cookies_button.click()
            # Wait for the "later" button to be ready
            later_button = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/header/div/div[3]/div/div/div/div')))
            # Click on the "later" button
            later_button.click()
        except:
            print("Ignoring cookies and later button")
        
    def send_image_and_get_response(self, image_path, object, size):
        print("Sending image and getting response")
        # Wait for the image area to be ready that is inside a shadow root
        parent = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.cib-serp-main')))
        shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', parent)
        parent_2 = shadow_root.find_element(By.CSS_SELECTOR, '#cib-action-bar-main')
        shadow_root_2 = self.driver.execute_script('return arguments[0].shadowRoot', parent_2)
        image_area = shadow_root_2.find_element(By.CSS_SELECTOR, '#camera-container > button > svg-icon')
        # Click on the image area
        image_area.click()
        parent_3 = shadow_root_2.find_element(By.CSS_SELECTOR, 'cib-visual-search')
        shadow_root_3 = self.driver.execute_script('return arguments[0].shadowRoot', parent_3)
        # Wait for the image input to be ready
        image_input = shadow_root_3.find_element(By.CSS_SELECTOR, '.paste-input')
        # Copy the image to clipboard
        send_image_to_clipboard(image_path)        

        # Focus on the input area and paste the image from the clipboard
        image_input.click()
        image_input.send_keys(Keys.CONTROL, 'v')

        # Get the input area
        input_area_parent = shadow_root_2.find_element(By.CSS_SELECTOR, 'cib-text-input')
        input_shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', input_area_parent)

        input_area = input_shadow_root.find_element(By.CSS_SELECTOR, '#searchbox')

        # Optionally send some text along with the image
        input_area.send_keys(self.prompt_image(image_path, object, size))

        # Wait for the send button to be ready
        time.sleep(4)

        input_area.send_keys(Keys.ENTER)

        # Wait for a response to appear
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#stop-responding-button > span")))
        # Wait for the span to have the text Response stopped
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#stop-responding-button > span"), "Response stopped"))

        # Get the last element in the document with class response-message-group
        response = self.driver.find_elements(By.CSS_SELECTOR, ".response-message-group")[-1].text

        # Split the response into cells
        cells = response.split(',')

        # Remove text (if it exists) from the cells ( CAN CAUSE PROBLEM )
        for i in range(len(cells)):
            for j in range(len(cells[i])):
                if cells[i][j].isdigit():
                    cells[i] = cells[i][j]
                    break
        
        return cells

    def close(self):
        self.driver.quit()
