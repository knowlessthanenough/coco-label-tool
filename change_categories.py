import json
import sys

# Check that the correct number of arguments were provided
if len(sys.argv) != 2:
    print("Usage: python3 change_categories.py input_file")
    sys.exit(1)

# Get the input file name from the command-line argument
input_file = sys.argv[1]

# Load the JSON file
with open(input_file, 'r') as f:
    data = json.load(f)

# Iterate through the annotations and change the category IDs
for ann in data['annotations']:
    if ann['category_id'] == 1:
        ann['category_id'] = 2
    elif ann['category_id'] in [2, 3]:
        ann['category_id'] = 0
    else:
        ann['category_id'] = 1

# Write the updated JSON data back to the input file
with open(input_file, 'w') as f:
    json.dump(data, f, indent=4)
