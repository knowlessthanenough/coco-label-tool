import json
import sys

# Get the file name from the command line argument
if len(sys.argv) < 2:
    print("Please provide the file name as a command line argument.")
    sys.exit(1)

file_name = sys.argv[1]

# Load the JSON file
with open(file_name, 'r') as f:
    data = json.load(f)

# Create a list to store the file names
file_names = []

# Loop through the images and check for repeated file names
for image in data['images']:
    if image['file_name'] in file_names:
        print(f"Repeated file name: {image['file_name']}")
    else:
        file_names.append(image['file_name'])
        
