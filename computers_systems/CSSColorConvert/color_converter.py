import os
import re
from itertools import batched

# convert the value (write a dedicated function) and fille up the object's values
# rewrite the files ?
# write tests

def main():
    # open the file, extract and read their content
    file_path = f"{os.getcwd()}/color-convert/advanced.css"
    css = file_reader(file_path)
    print(css)
    # extract the css values
    hex_values = extract_hex(css)
    print(hex_values)
    # convert
    conversion = convert_hex_to_dec(hex_values)
    print(conversion)




def file_reader(path: str):
    with open(path, 'r') as f:
        data = f.read()
        return data

def extract_hex(s: str):
    css_values = re.findall("color: #\w{1,8};", s)
    # isolate hexadecimal value
    res = []
    for v in css_values:
        rgb = []
        rgb_hex = v.split('color: #')[1][:-1]
        for i, _ in enumerate(rgb_hex):
            if len(rgb_hex) % 2 != 0:
                rgb.append(rgb_hex[i])
            elif i % 2 == 1:
                rgb.append(rgb_hex[i-1:i+1])
            
        res.append(rgb)
    return res

def convert_hex_to_dec(h: list[str]):
    res = {}
    for hex in h:
        dec = []
        for i in hex:
            dec.append(int(i, base=16))
        res[''.join(hex)] = dec
    return res

main()