import os
import shutil
import argparse
from sklearn.model_selection import train_test_split
from tqdm import tqdm

def main(base_dir, output_dir, test_size=0.1):
    # Define paths
    image_dir = os.path.join(base_dir, 'images')
    label_dir = os.path.join(base_dir, 'labels')

    # Create directories for the new structure
    for folder in ['train', 'val']:
        os.makedirs(os.path.join(output_dir, 'images', folder), exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'labels', folder), exist_ok=True)

    # Read all image filenames
    # Update this line to filter out non-image files or shortcuts
    images = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    images.sort()  # Sort the list to ensure reproducibility

    # Split data into train and validation sets
    train_images, val_images = train_test_split(images, test_size=test_size, random_state=42)

    def copy_files(files, src_image_dir, src_label_dir, dest_image_dir, dest_label_dir, set_name):
        txt_path = os.path.join(output_dir, f'{set_name}.txt')
        missing_labels = []  # List to keep track of images with missing labels
        with open(txt_path, 'w') as txt_file:
            for f in tqdm(files, desc=f"Copying {set_name} files"):
                img_src_path = os.path.join(src_image_dir, f)
                label_src_path = os.path.join(src_label_dir, os.path.splitext(f)[0] + '.txt')
                img_dest_path = os.path.join(dest_image_dir, f)
                label_dest_path = os.path.join(dest_label_dir, os.path.splitext(f)[0] + '.txt')

                # Copy image
                shutil.copy(img_src_path, img_dest_path)

                # Check if the label file exists before copying
                if os.path.exists(label_src_path):
                    shutil.copy(label_src_path, label_dest_path)
                    # Write relative image path to txt file
                    txt_file.write(f"./{os.path.relpath(img_dest_path, start=output_dir)}\n")
                else:
                    # Handle missing label file (e.g., log or skip)
                    missing_labels.append(f)

        # Optionally, log or print images with missing labels
        if missing_labels:
            print(f"Warning: Missing label files for {len(missing_labels)} images. These images were skipped.")
            # For debugging, print or log the list of images with missing labels
            # print("\n".join(missing_labels))


    # Copy files to their respective directories and generate txt files
    copy_files(train_images, image_dir, label_dir, os.path.join(output_dir, 'images', 'train'), os.path.join(output_dir, 'labels', 'train'), 'train')
    copy_files(val_images, image_dir, label_dir, os.path.join(output_dir, 'images', 'val'), os.path.join(output_dir, 'labels', 'val'), 'val')

    print("Dataset successfully split, copied, and indexed in .txt files.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split dataset into training and validation sets and generate .txt files.")
    parser.add_argument("base_dir", type=str, help="Path to the base directory containing 'image' and 'labels' folders.")
    parser.add_argument("output_dir", type=str, help="Path to the output directory where the new dataset structure will be created.")
    parser.add_argument("--test_size", type=float, default=0.1, help="Proportion of the dataset to include in the validation split.")

    args = parser.parse_args()

    main(args.base_dir, args.output_dir, args.test_size)
