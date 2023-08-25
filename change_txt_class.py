import os
import sys

# Define the mapping of class labels to new labels
class_map = {5: 1, 4: 1, 3: 0, 2: 0, 1: 2, 0: 1}

# Get the input path from the command line argument
if len(sys.argv) < 2:
    print('Usage: python program.py <input_path>')
    sys.exit(1)
input_path = sys.argv[1]

# Loop through each txt file in the directory
for filename in os.listdir(input_path):
    if filename.endswith('.txt'):
        # Open the file and read its contents
        with open(os.path.join(input_path, filename), 'r') as f:
            lines = f.readlines()

        # Replace the class labels in each line with the new labels
        new_lines = []
        for line in lines:
            parts = line.strip().split()
            class_label = int(parts[0])
            new_label = class_map.get(class_label, 2)
            new_parts = [str(new_label)] + parts[1:]
            new_line = ' '.join(new_parts) + '\n'
            new_lines.append(new_line)

        # Write the new contents back to the file
        with open(os.path.join(input_path, filename), 'w') as f:
            f.writelines(new_lines)
