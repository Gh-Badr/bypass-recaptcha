import os
import random
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

def send_image_to_clipboard(image_path):
    image = Image.open(image_path)
    
    output = io.BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

# Define a function to check if the element is not disabled
def wait_for_not_disabled(driver, locator):
    element = driver.find_element(locator[0], locator[1])
    if element.get_attribute("disabled"):
        return False
    else:
        return element

# Write the prompt based on the image name
def prompt_image(image_path):
    # Get the image name
    image_name = os.path.basename(image_path)
    # get the size of the image
    image = Image.open(image_path)
    width, height = image.size

    prompt = "This is an image of a "

    if width <= 300 and height <= 300:
        prompt += "3x3 grid "
    elif width > 400 and height > 400:
        prompt += "4x4 grid "
    
    prompt += "(If the image does not contain a grid or the grid is not clear, just imagine that the image is seperated into equal squares according to the grid specified, and numbered from the top left square, going line by line, to the bottom right square). "
    prompt += "Based on this grid, identify the numbers of the cells containing the following: "
    prompt += image_name.split("-")[0].replace(".jpg", "")

    print("Prompt: ", prompt)

    return prompt


# Service to the ChromeDriver
service = Service(executable_path=ChromeDriverManager().install())

# Configure Chrome options to use the specified user profile
chrome_options = Options()
chrome_options.add_argument("--user-data-dir=C:/Users/mouad/AppData/Local/Google/Chrome/User Data")
chrome_options.add_argument("--profile-directory=Profile 5")
chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--proxy-server='direct://'")
# chrome_options.add_argument("--proxy-bypass-list=*")
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument('--allow-running-insecure-content')
# chrome_options.add_argument('--disable-web-security')
# chrome_options.add_argument('--window-size=1920,1080')
# chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')
# chrome_options.add_argument("--headless")

# Start a new Selenium WebDriver with the specified profile
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the chat page (This link is for a private GPT created by us, called Grid Vision)
driver.get("https://chat.openai.com/g/g-K30O0wu7c-grid-vision")
response = ""
try:
    # Wait for this xpath 
    WebDriverWait(driver, 30).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[1]/div/div[2]/div[2]/div[1]'), "Grid Vision"))
    # Wait for the input area to be ready
    input_area = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#prompt-textarea')))

    # Find the chat input element and send a message
    chat_input = driver.find_element(By.ID, 'prompt-textarea')

    # Send image to clipboard (random image from ../images)
    image_path = r"images/" + random.choice(os.listdir("images/"))
    print("Image path: ", image_path)
    # Copy the image to clipboard
    send_image_to_clipboard(image_path)
    
    # Focus on the input area and paste the image from the clipboard
    input_area.click()
    input_area.send_keys(Keys.CONTROL, 'v')

    # Optionally send some text along with the image
    input_area.send_keys(prompt_image(image_path))

    # Send the message
    send_button = (By.XPATH, "//button[@data-testid=\"send-button\"]")
    # Wait until the send button is enabled
    send_button = WebDriverWait(driver, 30).until(
        lambda driver: wait_for_not_disabled(driver, send_button)
    )
    send_button.click()

    # Wait for a response to appear
    # To do this we should wait for the aria-label="Stop generating" button to appear and then for the send button to appear again
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label=\"Stop generating\"]")))
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid=\"send-button\"]")))

    # Extract the response
    response = driver.find_element(By.XPATH, "//div[@data-testid=\"conversation-turn-3\"]//p").text
finally:
    # Print the response
    print("GPT-3's response: ", response)

    # Wait for user input to proceed, keeping the browser open
    input("Press Enter to continue...")

    # Close the browser
    driver.quit()
