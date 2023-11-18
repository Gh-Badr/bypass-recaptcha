import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import win32clipboard
from PIL import Image
import io

class GridVisionClient:
    def __init__(self):
        # Define the service that will be used to run the ChromeDriver
        self.service = Service(executable_path=ChromeDriverManager().install())
        # Define the Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--user-data-dir=C:/Users/mouad/AppData/Local/Google/Chrome/User Data")
        chrome_options.add_argument("--profile-directory=Profile 5")
        chrome_options.add_argument("--start-maximized")
        # Create the driver
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)

    def send_image_to_clipboard(self, image_path):
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

    def wait_for_not_disabled(self, locator):
        element = self.driver.find_element(locator[0], locator[1])
        if element.get_attribute("disabled"):
            return False
        else:
            return element
        
    def load_prompt_template(self, file_path):
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            return data['prompt_template']

    def prompt_image(self, image_path, object):
        # get the size of the image
        image = Image.open(image_path)
        width, height = image.size
        # Get the grid size
        if width <= 300 and height <= 300:
            grid_size = "3x3"
        elif width > 400 and height > 400:
            grid_size = "4x4"
        # Load the prompt template
        template = self.load_prompt_template(r"config/config.yml")
        # Replace the placeholders with the actual values
        prompt = template.format(grid_size=grid_size, object=object)

        print("Prompt: ", prompt)

        return prompt

    def start_chat(self):
        self.driver.get("https://chat.openai.com/g/g-K30O0wu7c-grid-vision")
        # Wait for this xpath 
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[1]/div/div[2]/div[2]/div[1]'), "Grid Vision"))
    

    def send_image_and_get_response(self, image_path, object):
        # Wait for the input area to be ready
        input_area = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#prompt-textarea')))

        # Find the chat input element and send a message
        chat_input = self.driver.find_element(By.ID, 'prompt-textarea')

        # Copy the image to clipboard
        self.send_image_to_clipboard(image_path)

        # Focus on the input area and paste the image from the clipboard
        input_area.click()
        input_area.send_keys(Keys.CONTROL, 'v')

        # Optionally send some text along with the image
        input_area.send_keys(self.prompt_image(image_path, object))

        # Send the message
        send_button = (By.XPATH, "//button[@data-testid=\"send-button\"]")
        # Wait until the send button is enabled
        send_button = WebDriverWait(self.driver, 30).until(
            lambda driver: self.wait_for_not_disabled(send_button)
        )
        send_button.click()

        # Wait for a response to appear
        # To do this we should wait for the aria-label="Stop generating" button to appear and then for the send button to appear again
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label=\"Stop generating\"]")))
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid=\"send-button\"]")))

        # Extract the response
        response = self.driver.find_element(By.XPATH, "//div[@data-testid=\"conversation-turn-3\"]//p").text

        # Split the response into cells
        cells = response.split(',')
        # Remove text from the cells

        return cells

    def close(self):
        self.driver.quit()
