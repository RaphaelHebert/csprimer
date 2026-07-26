import os
import sys
# read the file as binary (hexdump)
# extract and interpret the header(s)
# extract the pixels
# rotate the pixel's bytes 90 degres (using matrix operation?)
# write a new the file (headers pixels etc) with the rotated image
# test the solution

# TODO extract the whole header (rewrite length and width size (swap if rotated))
# rewrite the file with new header and new image from rotated lines

def main():
    filePath = f'{os.getcwd()}/image-rotate/teapot.bmp'
    data = fileReader(filePath)
    data = rotate_image(data)

def fileReader(path: str):
    data = {}
    with open(path, 'rb') as f:
        # data = f.read(128)
        # data["bitmap_file_type"] = f.read(2);
        # data["bitmap_file_size"] = f.read(4);
        # # go to the offset 
        # f.read(4)
        # data["bitmap_offset"] = f.read(4);
        # hight and width in pixels
        f.seek(18)
        data["width_in_pixels"] = int.from_bytes(f.read(4), byteorder="little");
        f.seek(22)
        data["height_in_pixels"] = int.from_bytes(f.read(4), byteorder="little");
        # number of bites per pixels
        f.seek(28)
        data["number_of_bytes_per_pixels"] = int.from_bytes(f.read(2), byteorder="little") // 8;
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
        # extract image
        f.seek(data["pixel_offset"])
        data["image"] = f.read(data["image_byte_size"])

        # data["number_of_bits_per_pixels"] = f.read(2)
        return data
    
def rotate_image(data: bytes):
    # ALGO:
    # 1 - Split data in lines (image width)
    # 2 - Iterate over lines to create new lines

    # 1
    lines = [data["image"][i:i+(data["width_in_bytes"] // 3)] for i in range(0, data["image_byte_size"], data["width_in_bytes"])]

    print(len(lines))
    print(data["image_byte_size"])
    print(data["image_byte_size"])
    print(data["image_byte_size"]*3)

    print(data["header_bytes_size"])
    print(1260*1260)

    # print(lines[:-1][:-1])
    # 2 
    rotated_lines = [[0 for _ in line] for line in lines]
    for x, line in enumerate(lines):
        #  if we rotate 90 degres clockwise the first byte of the first line will be the last byte of the first line
        #  line index will be the len(line) - line_index 
        for y, byte in enumerate(line):
            if y >= len(line)//3:
                break
            rotated_lines[y][-x-1] = byte
    # return 
    print(rotated_lines)
    print(len(rotated_lines[0]))
    print(len(rotated_lines))
    
    return rotated_lines





main()