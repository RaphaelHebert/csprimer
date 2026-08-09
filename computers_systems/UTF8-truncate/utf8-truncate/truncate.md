## Unicode ASCII UTF-8

Unicode and ASCII map graphemes to hexadecimal
UTF-8 encode the hexadecimal codepoint to binary
exp for unicode graphemes: https://symbl.cc/en/1F96A-sandwich-emoji/

## Difference UTF-8 UTF-16 UTF-32

JS uses UTF-16, so the length of a string will return the number of UTF-16 bytes couples the string takes to be encoded

UTF-16 and UTF-32 are fixed length and can be LE or BE
But in UTF-16 sometimes is needs more than one UTF-16 bytes couple

UTF-8 is variable length en always reads the same way (byte agnostic), backward compatible with ASCII size efficient (one byte for ASCII)

## UTF-8 encoding

check [UTF-8 on wiki](https://en.wikipedia.org/wiki/UTF-8)
ASCII char will start with 0....... the other 7 bits will be the payload

110..... will have one continuous bytes : 10......
1110.... 10...... 10......
11110... 10...... 10...... 10......

The bits of the hexadecimal codepoint are dispatched in the payloads
