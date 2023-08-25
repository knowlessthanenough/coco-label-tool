import argparse
import json


def remove_duplicate_images(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    image_id_map = {}
    unique_images = []
    unique_image_ids = set()
    next_id = 0

    for image in data['images']:
        image_id = image['id']
        file_name = image['file_name']

        if file_name not in unique_image_ids:
            unique_image_ids.add(file_name)
            image_id_map[image_id] = next_id
            image['id'] = next_id
            unique_images.append(image)
            next_id += 1

    data['images'] = unique_images

    unique_annotations = []
    for annotation in data['annotations']:
        old_image_id = annotation['image_id']
        if old_image_id in image_id_map:
            annotation['image_id'] = image_id_map[old_image_id]
            unique_annotations.append(annotation)

    data['annotations'] = unique_annotations

    with open(input_file, 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="path to input COCO JSON file")
    args = parser.parse_args()
    remove_duplicate_images(args.input_file)
