Absolutely, let's enhance the `README.md` to include sections that detail the input data format and the output data structure the script expects and generates. Here's the updated `README.md`:

```markdown
# Dataset Splitter for YOLO Format

This Python script automates the process of shuffling and splitting a dataset of images and their corresponding YOLO format labels into training and validation sets. It supports datasets where each image file has a corresponding `.txt` label file in YOLO format. The script also generates `train.txt` and `val.txt`, containing the paths to the images in the training and validation sets, respectively.

## Features

- Shuffles and splits image datasets into training (90%) and validation (10%) sets by default.
- Copies images and their corresponding labels into structured directories for easy use in training models.
- Generates `train.txt` and `val.txt` files listing the relative paths of images in the training and validation sets.
- Gracefully handles missing label files by skipping images without corresponding labels.
- Displays a progress bar during file copying operations.

## Installation

Ensure you have Python 3.6 or later installed on your system. This script requires `sklearn` for splitting the dataset and `tqdm` for displaying the progress bar.

To install the required Python packages, run:

```bash
pip install scikit-learn tqdm
```

## Input Data Format

The script expects the input dataset to be organized into two directories:

- `image`: Contains all raw image files. Supported formats include `.jpg`, `.jpeg`, and `.png`.
- `labels`: Contains all the label files in YOLO format, where each label file is a `.txt` file with the same name as its corresponding image.

### Example Structure Before Running the Script

```
your_dataset/
├── images/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
└── labels/
    ├── image1.txt
    ├── image2.txt
    └── ...
```

## Output Data Structure

After running the script, the dataset will be divided into training and validation sets, structured as follows:

```
output_directory/
├── images/
│   ├── train/
│   │   ├── image1.jpg
│   │   └── ...
│   └── val/
│       └── image2.jpg
├── labels/
│   ├── train/
│   │   ├── image1.txt
│   │   └── ...
│   └── val/
│       └── image2.txt
├──train.txt
│
└──val.txt        
```

Additionally, `train.txt` and `val.txt` files will be generated in the `output_directory`, listing the relative paths to the images in their respective sets.

## Usage

1. Prepare your dataset according to the input data format described above.
2. Run the script from the command line, specifying the path to your dataset and the desired output directory for the split dataset.

```bash
python split_dataset.py <path_to_your_dataset> <path_to_output_directory> [--test_size <validation_split_ratio>]
```

### Example

```bash
python split_dataset.py C:\datasets\my_dataset C:\datasets\processed_dataset --test_size 0.2
```

## Handling Missing Labels

The script checks for the existence of label files corresponding to each image. If a label file is missing, the image is skipped, and a warning is printed at the end of the script's execution. This ensures the integrity of your training and validation sets by including only images with proper labels.

## Contributing

Feel free to fork this repository and submit pull requests to contribute to the development of this script. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
```

### Additional Considerations

- **Input Data Format**: Make sure to specify any particularities about the YOLO format labels your script expects, such as the structure of the `.txt` files if they need to adhere to a specific version of YOLO or any additional file requirements.
- **Output Data Structure**: The structure is designed to separate the images and labels into training and validation sets, making it straightforward to use this dataset for model training. The `train.txt` and `val.txt` files serve as indices to the images, which can be particularly useful for loading the dataset in machine learning frameworks.

This README now includes comprehensive sections on both the input and output formats, providing clear instructions for users to prepare their datasets and understand the structure of the processed output.