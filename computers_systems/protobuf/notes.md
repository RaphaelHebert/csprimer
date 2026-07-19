# Low-Level Systems & Serialization Study Notes

## Topic: Protobuf Varints, Bitwise Architecture, and Engine Numerics

---

### 1. Base 128 Varints (Variable-Length Quantities)

Varints are a highly efficient serialization scheme used to encode integers using a variable number of bytes, ensuring that smaller values occupy minimal space.

- **Capacity & Scale:** Base 128 varints allow encoding unsigned 64-bit integers using **1 to 10 bytes**. Ten bytes are required because $10 \times 7 \text{ bits} = 70 \text{ bits}$, which provides enough capacity to fully wrap a 64-bit integer space.
- **The Continuation Bit Architecture:**
  - Every byte in a varint uses its **Most Significant Bit (MSB)**—the 8th bit—as a metadata flag known as the _continuation bit_.
  - `MSB = 1`: Indicates that the current byte is followed by subsequent bytes.
  - `MSB = 0`: Indicates that this byte is the terminal (last) byte of the sequence.
  - The remaining **7 lower bits** store the actual payload payload data.
- **Endianness Mapping:** Varints are arranged in **Little-Endian** formatting. The least significant groups of bits are serialized first. During parsing/decoding, these 7-bit blocks must be extracted sequentially and shifted into place from right to left.

#### Varint Encoding Visualization (Example: Encoding the decimal value `300`)

```
Decimal: 300 ──> Binary: 00000010 01011000 (Fits in 9 bits: 1 0010 1100)

1. Split into 7-bit groups from right to left:
   Group 1 (least significant): 0101100
   Group 2 (most significant):  0000010

2. Set the Continuation Bit (MSB):
   Group 1 (Has more bytes coming) ──> Set MSB to 1 ──> 10101100 (0xAC)
   Group 2 (Terminal byte)         ──> Set MSB to 0 ──> 00000010 (0x02)

Resulting Byte Stream (Little-Endian): [ 0xAC, 0x02 ]
```

- **Protobuf Built-in Mappings:** In Protocol Buffers, varint architecture serializes the following data types natively:
  - `int32`, `int64`
  - `uint32`, `uint64`
  - `sint32`, `sint64` _(Leverages ZigZag encoding to fold signed integers into positive spaces)_
  - `bool` _(Stored simply as a `00` or `01` varint block)_
  - `enum`

---

### 2. Signed vs. Unsigned Integer Bit Representation

Understanding bit-level topology is vital to analyzing serialization boundaries.

```
Unsigned 8-bit Integer (Max: 255)
 ┌───┬───┬───┬───┬───┬───┬───┬───┐
 │128│ 64│ 32│ 16│ 8 │ 4 │ 2 │ 1 │  <-- All bits represent numerical value
 └───┴───┴───┴───┴───┴───┴───┴───┘

Signed 8-bit Integer (Two's Complement)
 ┌───┬───┬───┬───┬───┬───┬───┬───┐
 │MSB│ 64│ 32│ 16│ 8 │ 4 │ 2 │ 1 │  <-- MSB (Most Significant Bit) acts as Sign
 └───┴───┴───┴───┴───┴───┴───┴───┘
   │
   ├──> MSB = 0: Positive Number
   └──> MSB = 1: Negative Number (Processed via Two's Complement)
```

- **Unsigned Integers:** Every bit cell represents an explicit power of two ($2^0$ up to $2^{n-1}$). The dynamic range spans from $0$ to $2^n - 1$.
- **Signed Integers (Two's Complement):** The left-most bit cell (MSB) acts as a structural sign indicator.
  _ `MSB = 1` $
  -> Evaluates as a negative quantity.
  _ `MSB = 0` $
  -> Evaluates as a positive quantity.
- **The Varint Two's Complement Catch:** In classic Two's complement representation, small negative numbers like `-1` populate all available bits with ones (e.g., `0xFFFFFFFF`). If you pass a standard negative number straight into a standard varint engine, the system interprets it as a huge unsigned value, bloating the payload size to the maximum **10 bytes**.
- **The Protobuf Fix (`sint32`/`sint64`):** Protocol Buffers resolves this using **ZigZag Encoding**. ZigZag maps signed integers onto a single line of positive values, interleaving them so small negative numbers take up small spaces:
  _ `0` -> `0`
  _ `-1` -> `1`
  _ `1` -> `2`
  _ `-2` -> `3`

---

### 3. Hexdump File Analysis & Inspections

When analyzing serialized byte buffers or binary data outputs directly on disk, a hex dump tool provides legible structural tracking.

- **Canonical Utility Command:** `hexdump -C <filename>`
- **Structural Breakdown of Output:**

```
  Offset Column        Raw Hexadecimal Bytes (16 bytes per row)          ASCII Text Preview
┌──────────────┐ ┌───────────────────────────────────────────────┐ ┌────────────────────────┐
 00000000  08     f1 96 01 12 07 74 65 73  74 69 6e 67 0a 03 61 62  │.....testing..ab│
 00000010  63                                                       │c│
└──────────────┘ └───────────────────────────────────────────────┘ └────────────────────────┘
```

1.  **Left Column (Hex Offset):** Indicates the byte address relative to the beginning of the file (e.g., `00000000` is byte index 0).
2.  **Middle Matrix (Hex Payload):** Emits the literal hex characters for exactly 16 bytes per line, divided by an extra space into two 8-byte blocks for readability.
3.  **Right Column (ASCII Grid):** Converts the hex sequences directly to readable characters. Standard printable symbols appear clearly; control codes or non-printable binary parts are safely replaced by placeholder dots (`.`).

---

### 4. Low-Level Bitwise Manipulation & Shifting

Masking and shifting allow systems to compress, extract, and rearrange raw data components within bytes.

- **Bitwise OR (`|`):** Sets specific bits to `1`. Commonly used during encoding to turn on the continuation bit on a newly created byte chunk:
  ```c
  byte = payload_chunk | 0x80; // Forces the MSB to 1
  ```
- **Bitwise AND (`&`):** Acts as a clean isolation mask to clear out unwanted bits. Essential during decoding to wipe away the continuation bit and retrieve raw payload values:
  ```c
  clean_payload = serialized_byte & 0x7F; // Strips out the MSB, keeping lower 7 bits
  ```
- **Bitwise XOR (`^`):** Flips bits when matching against a structural mask. This toggling logic underpins the fast conversions inside ZigZag encoding pipelines.
- **Bit Shifting Operations:**
  - **Logical Right Shift (`>>>`):** Shifts bits to the right while filling vacant spaces with zeros. Used when encoding to chop off the next 7 bits of a number: `value >>> 7`.
  - **Left Shift (`<<`):** Shifts bits to the left, introducing zeros on the right. Crucial during decoding to assemble the final integer out of individual 7-bit blocks: `decoded_value |= (clean_payload << shift_amount)`.

---

### 5. Number Representation in JavaScript

The JavaScript runtime engine deals with numbers in a specialized way that introduces risks when working with low-level systems data.

- **The Floating-Point Default:** By standard design, JavaScript stores all standard numbers as **IEEE 754 Double-Precision Floating-Point values**. It does not possess separate native `int` or `float` primitive types in its core layout.
- **The Safe Integer Boundary:** Because some bit space inside double-precision floats must be used for fractions and exponents, JavaScript can only guarantee exact integer precision up to **$2^{53} - 1$** (`Number.MAX_SAFE_INTEGER`). Attempting to manipulate 64-bit values above this threshold leads to rounding loss.
- **The 32-Bit Bitwise Constraint:** When running bitwise operators (`&`, `|`, `~`, `^`, `<<`, `>>`), JavaScript implicitly casts the target values down into **32-bit signed integers**.
  - _The Risk:_ If you pass a large 64-bit numeric value through a standard bitwise shift or mask, JavaScript chops off the upper bits, causing immediate value distortion.
- **The Modern Solution (`BigInt`):** To manage true 64-bit structures (like Protobuf's native `int64`/`uint64`), modern JS applications use the explicit **`BigInt`** data type (e.g., `const val = 9007199254740992n;`). `BigInt` handles arbitrary precision integers safely and allows full bitwise math operations across the 64-bit landscape without truncation.
