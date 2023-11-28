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

class GridVisionClient:
    def __init__(self):
        # Define the service that will be used to run the ChromeDriver
        self.service = Service(executable_path=ChromeDriverManager().install())
        # Define the Chrome options
        chrome_options = Options()
        user_data_dir = load_yaml_param(r"config/config.yml", "user-data-dir")
        chrome_options.add_argument(f"user-data-dir={user_data_dir}")
        profile_directory = load_yaml_param(r"config/config.yml", "profile-directory")
        chrome_options.add_argument(f"profile-directory={profile_directory}")
        # chrome_options.add_argument("--start-maximized")
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
        self.driver.get("https://chat.openai.com/g/g-K30O0wu7c-grid-vision")
        # Wait for this xpath 
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[1]/div/div[2]/div[2]/div[1]'), "Grid Vision"))
    

    def send_image_and_get_response(self, image_path, object, size):
        # Wait for the input area to be ready
        input_area = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#prompt-textarea')))

        # Copy the image to clipboard
        send_image_to_clipboard(image_path)

        # Focus on the input area and paste the image from the clipboard
        input_area.click()
        input_area.send_keys(Keys.CONTROL, 'v')

        # Optionally send some text along with the image
        input_area.send_keys(self.prompt_image(image_path, object, size))

        # Send the message
        send_button = (By.XPATH, "//button[@data-testid=\"send-button\"]")
        # Wait until the send button is enabled
        send_button = WebDriverWait(self.driver, 30).until(
            lambda driver: wait_for_not_disabled(driver, send_button)
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
        
        return cells

    def close(self):
        self.driver.quit()
