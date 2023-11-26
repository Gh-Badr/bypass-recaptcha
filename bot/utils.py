import yaml
from PIL import Image
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