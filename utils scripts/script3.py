import csv

input_file = 'responses/noms_images.csv'
output_file = 'reordered_noms_images.csv'

# Read data from the input file
data = []
with open(input_file, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        data.append(row)

# Reorder the first column
reordered_data = []
image_names = []
numbers = []
for row in data:
    image_names.append(row[0])
    numbers.append(row[1:])

# reorder the images names (instead of a-1, a-10, a-11, a-2, b-1... we want a-1, a-2, a-10, a-11, b-1...)
# For this we take all images with same prefix (a, b, c...) and sort them by their number
# Let's do this for each prefix
reordered_image_names = []
prefixes = set([image_name.split('-')[0] for image_name in image_names])
# Sort the prefixes
prefixes = sorted(prefixes)

for prefix in prefixes:
    # Get all images with the same prefix
    images_with_same_prefix = [image_name for image_name in image_names if image_name.split('-')[0] == prefix]
    # Sort them by their number
    sorted_images_with_same_prefix = sorted(images_with_same_prefix, key=lambda image_name: int(image_name.split('-')[1].split('.')[0]))
    # Add them to the reordered image names
    reordered_image_names.extend(sorted_images_with_same_prefix)

# assemble the reordered data
for i in range(len(reordered_image_names)):
    reordered_data.append([reordered_image_names[i]] + numbers[i])

# Write the updated data to the output file
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(reordered_data)
