import os
import struct

print(os.getcwd())
def read_hexdump(path: str) -> int:
    with open(path, 'r+b' ) as f:
        hex_list = struct.unpack('>Q', f.read())[0]
    return hex_list

def encode(a: int) -> int:
    # When you call to_bytes() without the length argument, Python tries to use the minimum number of bytes needed, but it has a safety check: it refuses to produce a result if the number is too big for a signed C long long (usually 64-bit signed) unless you specify the length.
    # For numbers ≥ 2^63, Python raises OverflowError when length is not provided.
    bits = a.bit_length()
    bytes = (bits + 7) // 8
    return a.to_bytes(bytes, byteorder='big', signed=False)

def decode(a: str, binary = False) -> int:
    # input is like b'\x00\x00\x00\x00\x00\x00\x00\x96'
    if not binary:
        return int.from_bytes(a, byteorder='big')
    print(a)
    n = ''.join(str(a).split(r'\x')[1:])
    print(n)
    res = ''
    # output the hexadecimal without the leading 0x chars 
    for byte in n:
        match byte:
            case '0':
                res += '0000'
            case '1':
                res += '0001'
            case '2':
                res += '00010'
            case '3':
                res += '0011'
            case '4':
                res += '0100'
            case '5':
                res += '0101'
            case '6':
                res += '0110'
            case '7':
                res += '0111'
            case '8':
                res += '1000'
            case '9':
                res += '1001'
            case 'a' | 'A':
                res += '1010'
            case 'b' | 'B':
                res += '1011'
            case 'c' | 'C':
                res += '1100'
            case 'd' | 'D':
                res += '1101'
            case 'e' | 'E':
                res += '1110'
            case 'f' | 'F':
                res += '1111'
    return res

def encode_base128_varint(n):
    # we receive plain hexadecimal for exp \x96
    # should output \x96\x01
    res = []
    while n > 0:
        # need to use 7 bits (the 8th bit will be the MSB)
        b = n % 128 
        n >>= 7
        if n > 0:
            b |= 0x80
        res.append(b)
    return bytes(res)

 

def decode_base128_varint(n: int):
    #  delete MSB 
    #  make it big endian
    # compute decimal value
    res = 0
    print(n)
    for byte in reversed(n):
        res <<= 7
        print('res:   ', res)
        res += byte & 0x7f
        print('res:   ', res)
        # remove the MSB

    return res








        



hex = read_hexdump('./varint/150.uint64')
# dec = decode(hex, binary=True)
# print(dec)
# print(encode(98446744073709551615)) # > max int (64-bit unsigned)
print(decode_base128_varint(encode_base128_varint(hex)))
# print(encode_base128_varint(hex))