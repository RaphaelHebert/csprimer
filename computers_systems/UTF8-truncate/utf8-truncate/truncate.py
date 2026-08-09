import os

path = f'{os.getcwd()}/cases'
test_path =  f'{os.getcwd()}/expected'
data = b''
l=0
with open(path, 'rb') as i:
    d = i.read()
    for i in d:
      byte = bytes(i)
      if byte & bytes(128) == 0 or byte & 0xfff00000 == 192 or byte & 0xff00000 == 128:
        data += byte  


print(data)








with open(test_path, 'rb') as f:
    test_data = f.read()
    print(test_data)
    assert data == test_data