import csv

def extract_number(image_name):
    return int(image_name.split('-')[-1].split('.')[0])

def sort_key(line):
    image_name = line[0]
    return image_name.split('-')[0], extract_number(image_name)

# Read data from the CSV file
with open('responses_updated.csv', 'r') as file:
    reader = csv.reader(file)
    lines = list(reader)

# Sort the lines based on image names
sorted_lines = sorted(lines, key=sort_key)

# Write the sorted lines back to the CSV file
with open('reordered_respones.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(sorted_lines)
