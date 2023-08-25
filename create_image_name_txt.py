import os
import sys

# Get the folder path from the command-line argument
if len(sys.argv) < 2:
    print("Usage: python get_image_names.py /path/to/folder")
    sys.exit(1)
folder_path = sys.argv[1]

# Get the file names of all images in the folder
image_names = []
for filename in os.listdir(folder_path):
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        image_names.append(filename)

# Write the image names to a text file in the same directory as the folder
output_path = os.path.join(os.path.dirname(
    folder_path), os.path.basename(folder_path)) + ".txt"
with open(output_path, "w") as f:
    for name in image_names:
        f.write("./images/" + os.path.basename(folder_path) + "/" + name + "\n")

print(f"Image names saved to {output_path}")
