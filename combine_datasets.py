import json
import os
import shutil
import argparse


def combine_yolo_data(data1, data2, combined_data):
    os.makedirs(combined_data, exist_ok=True)

    # Combine annotation JSON files
    os.makedirs(os.path.join(combined_data, 'annotations'), exist_ok=True)
    for split in ['train']:
        with open(os.path.join(data1, 'annotations', f'{split}.json'), 'r') as f1, \
                open(os.path.join(data2, 'annotations', f'{split}.json'), 'r') as f2, \
                open(os.path.join(combined_data, 'annotations', f'{split}.json'), 'w') as fout:
            dataset1 = json.load(f1)
            dataset2 = json.load(f2)
            # Assign new IDs to images and annotations in the second dataset
            max_image_id = max([img["id"] for img in dataset1["images"]]) + 1
            max_annotation_id = max([ann["id"]
                                    for ann in dataset1["annotations"]]) + 1
            for img in dataset2["images"]:
                img["id"] += max_image_id
            for ann in dataset2["annotations"]:
                ann["id"] += max_annotation_id
                ann["image_id"] += max_image_id

            # Merge the two datasets
            merged_dataset = {
                "info": dataset1["info"],
                "images": dataset1["images"] + dataset2["images"],
                "annotations": dataset1["annotations"] + dataset2["annotations"],
                "categories": dataset1["categories"]
            }

            # Save the merged dataset to a new folder
            json.dump(merged_dataset, fout, indent=2)

            print(f"Merged annotations saved to {combined_data}")

    # copy images and labels
    for folder in ['images', 'labels']:
        os.makedirs(os.path.join(combined_data, folder), exist_ok=True)
        for split in ['train']:
            os.makedirs(os.path.join(combined_data,
                        folder, split), exist_ok=True)
            for data in [data1, data2]:
                src = os.path.join(data, folder, split)
                dst = os.path.join(combined_data, folder, split)
                for file in os.listdir(src):
                    shutil.copy(os.path.join(src, file),
                                os.path.join(dst, file))

    # Combine paths.txt files
    for split in ['train']:
        with open(os.path.join(data1, f'{split}.txt'), 'r') as f1, \
                open(os.path.join(data2, f'{split}.txt'), 'r') as f2, \
                open(os.path.join(combined_data, f'{split}.txt'), 'w') as fout:
            paths1 = f1.readlines()
            paths2 = f2.readlines()
            combined_paths = paths1 + paths2
            fout.writelines(combined_paths)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Combine two YOLO datasets")
    parser.add_argument("data1", type=str, help="First dataset directory")
    parser.add_argument("data2", type=str, help="Second dataset directory")
    parser.add_argument("combined_data", type=str,
                        help="Combined dataset directory")
    args = parser.parse_args()

    combine_yolo_data(args.data1, args.data2, args.combined_data)
