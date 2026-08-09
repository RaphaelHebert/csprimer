import os

path = f'{os.getcwd()}/cases'
test_path =  f'{os.getcwd()}/expected'

def truncate(line, l):
  if l >= len(line):
    return line
  while l > 0 and line[l] & 0xC0 == 0x80:
    l -= 1
  return line[:l]

res = b''
with open(path, 'rb') as f:
  lines = f.readlines()
  for line in lines:
    length = line[0]
    res += truncate(line[1:-1], length)
    res += b'\n'

test = b''
with open(test_path, 'rb') as f:
  test = f.read()

assert res == test
print('test passes')

