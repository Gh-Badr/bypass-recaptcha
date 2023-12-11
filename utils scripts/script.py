import os
import csv
from PIL import Image

# Path to the folder containing the images
folder_path = "old-images"

# List to store the image names and sizes
image_data = []

# Iterate over the files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        # Get the full path of the image file
        image_path = os.path.join(folder_path, filename)
        
        # Open the image using PIL
        image = Image.open(image_path)
        
        # Get the width and height of the image
        width, height = image.size
        
        # Determine the size (3x3 or 4x4)
        size = "3" if width <= 378 and height <= 378 else "4"
        
        # Add the image name and size to the list
        image_data.append([filename, size])

# Path to the output CSV file
output_file = "image_data.csv"

# Write the image data to the CSV file
with open(output_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Image Name", "Size"])
    writer.writerows(image_data)
