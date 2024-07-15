import os
os.environ["OPENCV_IO_MAX_IMAGE_PIXELS"] = str(pow(2,40))
import cv2 as cv
import numpy as np
import zipfile
import tempfile
import json
from get_img_info import getImgInfo

def GeneratePreviewImage(image, img_name, hogel_dimensions, directional_resolution=None):
    if hogel_dimensions == 'N/A':
        print("Hogel dimensions are N/A, generating a blank image.")
        dim = (100, 100)
    else:
        dim = hogel_dimensions

    test_image = np.zeros((dim[1], dim[0], 3), dtype=np.uint8)
    directional_resolution = directional_resolution if directional_resolution != 'N/A' else (1, 1)

    offsetx, offsety = int(directional_resolution[0] / 2), int(directional_resolution[1] / 2)
    for y in range(dim[1]):
        for x in range(dim[0]):
            middle_x, middle_y = x * directional_resolution[0] + offsetx, y * directional_resolution[1] + offsety
            if middle_x < image.shape[1] and middle_y < image.shape[0]:
                test_image[y, x] = image[middle_y, middle_x]

    img_path = os.path.join("output", img_name)
    cv.imwrite(img_path, cv.flip(test_image, 0))
    print("Image saved to:", img_path)

def save_json_attributes(attributes, file_size, output_file="output/config.json"):
    existing_data = []
    if os.path.exists(output_file):
        with open(output_file, 'r') as json_file:
            existing_data = json.load(json_file)

    attributes.update({'fileSize': f"{file_size} bytes", 'downloadLink': "#"})
    existing_data.append({"lightFieldAttributes": attributes})

    with open(output_file, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)
    print("JSON data appended to:", output_file)

def check_existing_files(file_name, output_file="output/config.json"):
    base_name, ext = os.path.splitext(file_name)
    existing_files = []
    if os.path.exists(output_file):
        with open(output_file, 'r') as json_file:
            existing_files = [entry['lightFieldAttributes']['file'] for entry in json.load(json_file)]

    new_file_name = f"{base_name}-{len(existing_files)+1}{ext}" if file_name in existing_files else file_name
    return new_file_name

def process_image(file_path, file_extension, name_wo_ext):
    if file_extension.lower() in [".lf", ".zip"]:
        with zipfile.ZipFile(file_path, 'r') as zip_ref, zip_ref.open('config.json') as json_file:
            attributes = getImgInfo(json_file)
        if 'file' in attributes and attributes['file'] != 'N/A':
            with zip_ref.open(attributes['file']) as image_file:
                image_data = image_file.read()
                temp = tempfile.NamedTemporaryFile(delete=False)
                temp.write(image_data)
                temp.close()
                img = cv.imread(temp.name)
                file_size = len(image_data)
                os.unlink(temp.name)
        else:
            print("Missing critical 'file' attribute. Skipping this file.")
            return
    elif file_extension.lower() == ".json":
        with open(file_path, 'rb') as json_file:
            attributes = getImgInfo(json_file)
        if 'file' in attributes and attributes['file'] != 'N/A':
            image_path = os.path.join(os.path.dirname(file_path), attributes['file'])
            img = cv.imread(image_path)
            file_size = os.path.getsize(image_path) if img is not None else 0
        else:
            print("Missing critical 'file' attribute. Skipping this file.")
            return
    else:
        return

    if img is not None:
        output_image_name = check_existing_files(name_wo_ext + os.path.splitext(attributes['file'])[1])
        GeneratePreviewImage(img, output_image_name, attributes.get('hogelDimensions', (0, 0)), attributes.get('directionalResolution'))
        attributes['file'] = output_image_name
        save_json_attributes(attributes, file_size)

if __name__ == '__main__':
    if not os.path.exists('output'):
        os.makedirs('output')
    directory_path = input("Enter the path of the input folder: ")
    if not os.path.isdir(directory_path):
        print("The specified directory does not exist. Please check the path and try again.")
        exit()
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path):
            print("Reading file:", file_name)
            process_image(file_path, os.path.splitext(file_name)[1], os.path.splitext(file_name)[0])