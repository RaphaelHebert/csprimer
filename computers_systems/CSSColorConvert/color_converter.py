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
    # extract the css values
    hex_values = extract_hex(css)
    # convert
    conversion = convert_hex_to_dec(hex_values)
    file_updater(file_path, conversion)



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
            if len(rgb_hex) < 6:
                rgb.append(rgb_hex[i])
            elif i % 2 == 1:
                rgb.append(rgb_hex[i-1:i+1])
        res.append(rgb)
    return res

def convert_hex_to_dec(h: list[str]):
    res = {}
    for hex in h:
        dec = []
        hex_str =''.join(hex)
        for i in hex:
            if len(hex_str) < 6:
                i = bytes(i, "utf-8")
                dec.append((int(i, base=16) << 4) + int(i, base=16))
            else:   
                dec.append(int(i, base=16))
        if len(dec) % 4 == 0:
            dec[3] = f'/ {dec[3] / 255}'[:9]
        res[hex_str] = dec 
    return res


def file_updater(path: str, d: dict):
    # read file
    data = file_reader(path)
    # replace hex value to dec
    for k, v in d.items():
        print(d)
        v = [str(w) for w in v]
        if len(v) % 3 == 0:
            data = data.replace(f'#{k}', f'rgb({' '.join(v)})')
        elif len(v) % 4 == 0:
             data = data.replace(f'#{k}', f'rgba({' '.join(v)})')
    # write a new file
    f_name = f'{path.strip('.css')}_decimal.css'
    with open(f_name, 'w') as f:
        f.write(data)
    

main()