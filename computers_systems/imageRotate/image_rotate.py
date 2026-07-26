import os
import sys

def main():
    filePath = f'{os.getcwd()}/image-rotate/teapot.bmp'
    data = fileReader(filePath)
    rotate_image(data)
    create_image(data, filePath)

def fileReader(path: str):
    data = {}
    with open(path, 'rb') as f:
        # height and width in pixels
        f.seek(18)
        data["width_in_pixels"] = int.from_bytes(f.read(4), byteorder="little")
        f.seek(22)
        data["height_in_pixels"] = int.from_bytes(f.read(4), byteorder="little")
        # number of bites per pixels
        f.seek(28)
        data["number_of_bytes_per_pixels"] = int.from_bytes(f.read(2), byteorder="little") // 8
        # f size
        data["width_in_bytes"] = data["width_in_pixels"] * data["number_of_bytes_per_pixels"]
        data["height_in_bytes"] = data["height_in_pixels"] * data["number_of_bytes_per_pixels"]
        # f start and end 
        f.seek(14)
        data["header_bytes_size"] = int.from_bytes(f.read(4), byteorder="little");
        # image size
        f.seek(34)
        data["image_byte_size"] = int.from_bytes(f.read(4), byteorder="little");

        #  pixel offset
        f.seek(10)
        data["pixel_offset"] = int.from_bytes(f.read(4), "little")
        print(data)
        # extract image
        f.seek(data["pixel_offset"])
        data["image"] = f.read(data["image_byte_size"])
        # header
        f.seek(0)
        data["header"] = f.read(data["pixel_offset"])
        return data


def rotate_image(data):
    # make a representation of the pixel row and column:
    rows_and_columns = [data["image"][i: i + data["width_in_bytes"]] for i in range(0, data["image_byte_size"], data["width_in_bytes"])]
    pixels_in_rows_and_columns = [[row[i:i + data["number_of_bytes_per_pixels"]] for i in range(0, len(row), data["number_of_bytes_per_pixels"])] for row in rows_and_columns]
    new_image = [[b'0' for _ in range(0, data["height_in_pixels"])] for _ in range(0, data["width_in_pixels"])]

    # rotate the matrix 90 degrees clockwise
    for i, row in enumerate(pixels_in_rows_and_columns):
        for y, pixel in enumerate(row):
            new_image[-y - 1][-i - 1] = pixel
    for i, _ in enumerate(new_image):
        new_image[i] = b''.join(new_image[i][::-1])

    new_image = b''.join(new_image)
    data["image"] = new_image

def create_image(data, path):
    # create a new image with the rotated pixels
    new_file_path = f'{path[:-4]}_rotated.bmp'
    with open(new_file_path, 'wb') as f:
        f.write(data["header"])
        f.write(data["image"])

main()