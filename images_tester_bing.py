from bot.BingChatClient import BingChatClient
from PIL import Image
import os

def send_to_gpt(image_path, object, size):
    response = client.send_image_and_get_response(image_path, object, size)
    print("Bing's response: ", response)
    return response

def main():
    try:
        # Get the images from images folder (we will get one by one)
        images = os.listdir('images')
        # For each image
        for image in images:
            # Get the object name from the image name
            object_name = image.split('-')[0]
            # Get the size of the image using image size method
            actual_image = Image.open("images/" + image)
            length, width = actual_image.size
            if length <= 378 and width <= 378:
                size = 3
            elif length >= 380 and width >= 380:
                size = 4
            # Send the image and get the response (The response is a list of numbers that represent the grid)
            response = send_to_gpt("images/" + image, object_name, size)
            # save the response in a csv file
            with open('responses.csv', 'a') as f:
                f.write(image + ',' + str(response) + '\n')


    except Exception as e:
        print(e)
    
    finally:
        input("Press Enter to continue...")

if __name__ == "__main__":
    # Create the BingChatClient
    client = BingChatClient()
    client.start_chat()

    main()

    client.close()

