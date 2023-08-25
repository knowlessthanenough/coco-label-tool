import os
import sys
import json


def get_class_map_from_user():
    print('Enter the class mapping as space-separated key-value pairs, e.g. "1:2 2:0 3:1":')
    class_map_str = input()
    class_map = {}
    for pair in class_map_str.split():
        key, value = map(int, pair.split(':'))
        class_map[key] = value
    return class_map


# Get the class mapping from the user
class_map = get_class_map_from_user()

# Get the input path from the command line argument
if len(sys.argv) < 2:
    print('Usage: python program.py <input_path>')
    sys.exit(1)
input_path = sys.argv[1]

# Update the class IDs in the json files inside the annotations folder
for split in ['train', 'val']:
    with open(os.path.join(input_path, 'annotations', f'{split}.json'), 'r') as f:
        data = json.load(f)

    for ann in data['annotations']:
        old_category_id = ann['category_id']
        new_category_id = class_map.get(old_category_id, old_category_id)
        ann['category_id'] = new_category_id

    with open(os.path.join(input_path, 'annotations', f'{split}.json'), 'w') as f:
        json.dump(data, f, indent=2)

# Update the class IDs in the txt files inside the labels folder
for split in ['train', 'val']:
    for filename in os.listdir(os.path.join(input_path, 'labels', split)):
        if filename.endswith('.txt'):
            with open(os.path.join(input_path, 'labels', split, filename), 'r') as f:
                lines = f.readlines()

            new_lines = []
            for line in lines:
                parts = line.strip().split()
                class_label = int(parts[0])
                new_label = class_map.get(class_label, class_label)
                new_parts = [str(new_label)] + parts[1:]
                new_line = ' '.join(new_parts) + '\n'
                new_lines.append(new_line)

            with open(os.path.join(input_path, 'labels', split, filename), 'w') as f:
                f.writelines(new_lines)
