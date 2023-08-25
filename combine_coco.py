import sys
import os
import json

# Get the file paths from the command-line arguments
if len(sys.argv) < 3:
    print("Usage: python combine_coco_datasets.py path/to/annotations1.json path/to/annotations2.json")
    sys.exit(1)
annotations_file1 = sys.argv[1]
annotations_file2 = sys.argv[2]

# Load the annotations for the first dataset
with open(annotations_file1, "r") as f:
    dataset1 = json.load(f)

# Load the annotations for the second dataset
with open(annotations_file2, "r") as f:
    dataset2 = json.load(f)

# Assign new IDs to images and annotations in the second dataset
max_image_id = max([img["id"] for img in dataset1["images"]]) + 1
max_annotation_id = max([ann["id"] for ann in dataset1["annotations"]]) + 1
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

# Save the merged dataset to a new file in the same directory as the first input file
output_file = os.path.join(os.path.dirname(
    annotations_file1), "merged_annotations.json")
with open(output_file, "w") as f:
    json.dump(merged_dataset, f, indent=2)

print(f"Merged annotations saved to {output_file}")
