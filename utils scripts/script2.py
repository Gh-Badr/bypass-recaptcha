import os
import csv
from PIL import Image

# Path to the folder containing the images
folder_path = "old-images"

# Path to the existing CSV file
input_file = "reordered_noms_images.csv"

# Dictionary to store the existing data
existing_data = {}

# Read the existing data into the dictionary
with open(input_file, "r") as file:
    reader = csv.reader(file)
    for row in reader:
        existing_data[row[0]] = row

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
        
        # If the image name is in the dictionary, append the size
        if filename in existing_data:
            existing_data[filename].append(size)

output_file = "reordered_human_responses.csv"
# Write the updated data back to the CSV file
with open(output_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(existing_data.values())