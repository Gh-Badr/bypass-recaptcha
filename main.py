from bot.GridVisionClient import GridVisionClient
import os
import random

def main():
    client = GridVisionClient()
    try:
        client.start_chat()
        # Get the image - for now, we will just pick a random image from the images folder
        # This part will be replaced by picking the image from the recaptcha website
        image_path = r"images/" + random.choice(os.listdir("images/"))
        print("Image path: ", image_path)
        # Get the object
        # Temporary hack - we will just use the image name to get the object
        # This part will be replaced by picked the object from the recaptcha website
        image_name = os.path.basename(image_path)
        object = image_name.split("-")[0].replace(".jpg", "")

        # Send the image and get the response (The response is a list of numbers that represent the grid)
        response = client.send_image_and_get_response(image_path, object)
        print("GPT-3's response: ", response)

    finally:
        input("Press Enter to continue...")
        client.close()


if __name__ == "__main__":
    main()

    