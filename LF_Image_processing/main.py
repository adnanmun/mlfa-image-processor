import os

# Overwriting OPENCV enviornment variable
os.environ["OPENCV_IO_MAX_IMAGE_PIXELS"] = pow(2, 40).__str__()
import cv2 as cv
import numpy as np
import zipfile
from io import BytesIO
from get_img_info import getImgInfo
import tempfile


def GeneratePreviewImage(image, img_name, directional_resolution, hogel_dimensions):
    dim = hogel_dimensions
    test_image = np.zeros((dim[1], dim[0], 3), dtype=np.uint8)

    print(dim)
    offsetx = int(directional_resolution[0] / 2)
    offsety = int(directional_resolution[1] / 2)

    for y in range(0, dim[1]):
        for x in range(0, dim[0]):
            print(x, y)
            middle_x = x * directional_resolution[0] + offsetx
            middle_y = y * directional_resolution[1] + offsety
            test_image[y, x] = image[middle_y, middle_x]

    preview_image = cv.flip(test_image, 0)
    img_path = os.path.join("output", img_name)
    cv.imwrite(img_path, preview_image)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    hogel_dimensions = None
    directional_resolution = None
    png_file = None
    img = None
    directory_path = os.path.join(os.path.dirname(__file__), "input_images")

    files = os.listdir(directory_path)

    for index in range(0, len(files)):
        file_name = files[index]
        file_path = os.path.join(directory_path, file_name)
        name_wo_ext, file_extension = os.path.splitext(file_name)

        if os.path.isfile(file_path):
            print("Reading file:", file_name)
            print("Name:", name_wo_ext)
            print("Extension:", file_extension)

            if file_extension == ".lf":
                with open(file_path, 'rb') as file:
                    lf_content = file.read()
                zip_data = BytesIO(lf_content)
                # print(zip_data)

                with zipfile.ZipFile(zip_data, 'r') as zip_ref:
                    with zip_ref.open('config.json') as json_file:
                        hogel_dimensions, directional_resolution, png_file = getImgInfo(json_file)
                        if any(var is None for var in (hogel_dimensions, directional_resolution, png_file)):
                            print("One or more attributes not found. Skipping this file.")
                            continue

                    with zip_ref.open(png_file) as image_file:
                        temp = tempfile.NamedTemporaryFile(delete=False)

                        temp.write(image_file.read())
                        temp.close()
                        img = cv.imread(temp.name)
                        os.unlink(temp.name)
                        print("Success!!")

            elif file_extension == ".json":
                with open(file_path, 'rb') as json_file:
                    hogel_dimensions, directional_resolution, png_file = getImgInfo(json_file)
                    if any(var is None for var in (hogel_dimensions, directional_resolution, png_file)):
                        print("One or more attributes not found. Skipping this file.")
                        continue

                    print("PNG file:", png_file)
                    img_path = os.path.join(directory_path, png_file)

                    img = cv.imread(img_path)

        if img is not None:

            image_type = img.dtype
            print("Image type:", image_type)
            GeneratePreviewImage(img, png_file, directional_resolution, hogel_dimensions)
            img = None

        else:
            print("Error: Could not open or find the image.")
