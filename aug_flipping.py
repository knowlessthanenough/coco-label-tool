import cv2
from random import randint, choice
import numpy as np
import json
from os import mkdir
from os.path import exists
from os.path import join
from shutil import copyfile as cp
import time
from tqdm import tqdm
import argparse
import os

# Required for Generating Unique Image IDs
start = time.time()

def flip_bbox_yolo(bbox):
    # yolo format bbox: [x_center, y_center, width, height]
    x_center, y_center, width, height = bbox
    flipped_x_center = 1 - x_center
    return [flipped_x_center, y_center, width, height]

def flip_bbox_coco(bbox, width):
    x, y, w, h = bbox
    x_new = width - x - w
    return [x_new, y, w, h]

def mod_flip(IMG):
    img_mod_l = [IMG]
    # Flip
    img_mod_l.append(cv2.flip(IMG, 1))
    return img_mod_l

def replace_id(old, id_num):
    new = []
    for i in old:
        tmp = {}
        for k in i.keys():
            tmp[k] = i[k]
        tmp['image_id'] = id_num
        new.append(tmp)
    return new

def get_annots_img_l(annot_img, high, width):
    req_l = []
    for i in annot_img:
        req_l.append(f"{i['category_id']} {i['bbox'][0] / width} {i['bbox'][1] / high} {i['bbox'][2] / width} {i['bbox'][3] / high}")
    return req_l

def worker(json_file, seg, input_path, output_path, img_id_counter, bbox_id_counter):
    new_json_dict = {}
    new_json_dict['categories'] = json_file['categories']
    new_json_dict['info'] = json_file['info']
    new_json_dict['annotations'] = []
    new_json_dict['images'] = []
    imgs = json_file['images']
    annots = json_file['annotations']

    image_paths = []

    for img in tqdm(imgs, unit="Images", dynamic_ncols=True, desc=f"Data Augmenting {seg.capitalize()} Set"):
        img_id = img['id']
        annot_img = [i for i in annots if i['image_id'] == img_id]
        f_name = img['file_name'].replace('\\', '/').rsplit('images/')[-1]

        img_read = cv2.imread(os.path.join(input_path, 'images', seg, f_name))
        h , w, _ = img_read.shape
        img_processed = mod_flip(img_read)

        for iterator, processed_img in enumerate(img_processed):
            img_id_counter += 1
            label_path = os.path.join(output_path, 'labels', seg, f"{f_name[:-4]}{iterator}.txt")
            try:
                cp(os.path.join(input_path, 'labels', seg, f"{f_name[:-4]}.txt"), label_path)
            except FileNotFoundError:
                with open(label_path, 'w') as f:
                    f.writelines([f"{line}\n" for line in get_annots_img_l(annot_img, h, w)])

            # yolo format (Flip the label txt file)
            if iterator == 1:  # Only flip when iterator is 1 (flipped image)
                with open(label_path, 'r') as f:
                    lines = f.readlines()
                flipped_lines = []
                for line in lines:
                    line_parts = line.strip().split()
                    category = int(line_parts[0])
                    bbox = [float(x) for x in line_parts[1:]]
                    flipped_bbox = flip_bbox_yolo(bbox)
                    flipped_line = f"{category} {flipped_bbox[0]} {flipped_bbox[1]} {flipped_bbox[2]} {flipped_bbox[3]}\n"
                    flipped_lines.append(flipped_line)
                with open(label_path, 'w') as f:
                    f.writelines(flipped_lines)
            output_image_path = os.path.join(output_path, 'images', seg, f"{f_name[:-4]}{iterator}.jpg")
            cv2.imwrite(output_image_path, processed_img)

            # Add image path to the list
            image_paths.append(f"./images/{seg}/{f_name[:-4]}{iterator}.jpg")

            # coco format (Flip the bbox in json file)
            new_json_dict['images'].append({'width': w, 'height': h, 'id': img_id_counter, 'file_name': f'images/{f_name[:-4]}{iterator}.jpg'})
            new_annotations = replace_id(annot_img, img_id_counter)
            # Convert bounding box coordinates from YOLO to COCO format
            for ann in new_annotations:
                if img_id_counter % 2 == 1 :
                    ann['bbox'] = flip_bbox_coco(ann['bbox'], w)
                else:
                    ann['bbox']
                ann['id'] = bbox_id_counter
                bbox_id_counter += 1
            new_json_dict['annotations'] += new_annotations

    with open(os.path.join(output_path, 'annotations/', f"{seg}"), 'w') as f:
        json.dump(new_json_dict, f, indent=2)

    with open(os.path.join(output_path, f"{seg}.txt"), 'w') as fp:
        for item in image_paths:
            # write each item on a new line
            fp.write("%s\n" % item)

    return img_id_counter, bbox_id_counter

def main(input_path, output_path):
    # Create File Structure
    if not exists(output_path):
        os.makedirs(output_path)

    for subdir in ['annotations', 'images', 'labels']:
        if not exists(os.path.join(output_path, subdir)):
            os.mkdir(os.path.join(output_path, subdir))

    for subdir in ['train', 'val']:
        if not exists(os.path.join(output_path, 'images', subdir)):
            os.mkdir(os.path.join(output_path, 'images', subdir))
        if not exists(os.path.join(output_path, 'labels', subdir)):
            os.mkdir(os.path.join(output_path, 'labels', subdir))

    # Open JSON Files
    val_annot_fi = json.load(open(os.path.join(input_path, 'annotations', 'val.json')))
    train_annot_fi = json.load(open(os.path.join(input_path, 'annotations', 'train.json')))

    # Actually Generating Data
    worker(val_annot_fi, 'val', input_path, output_path,0,0)
    worker(train_annot_fi, 'train', input_path, output_path,0,0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', help='Path to the input dataset directory')
    args = parser.parse_args()

    input_path = args.input_path
    output_path = os.path.join(input_path + "-aug")

    main(input_path, output_path)
