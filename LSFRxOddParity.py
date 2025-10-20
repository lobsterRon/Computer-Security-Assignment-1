def generate_keystream(initial_state: int, length: int) -> bytes:
    """
    Generate keystream bits based on LFSR + odd parity.
    - initial_state: 4-bit integer (e.g., 0b1110)
    - length: number of bytes (not bits) to produce
    """
    state = initial_state
    keystream_bits = ""

    # Generate enough bits (8 bits per byte)
    for _ in range(length * 8):
        bits = "{:04b}".format(state)
        ones = bits.count('1')
        parity = 1 if ones % 2 == 0 else 0
        keystream_bits += str(parity)

        # LFSR feedback
        newbit = (state ^ (state >> 1)) & 1
        state = (state >> 1) | (newbit << 3)

    # Convert bits to bytes
    keystream_bytes = bytearray()
    for i in range(0, len(keystream_bits), 8):
        byte = int(keystream_bits[i:i+8], 2)
        keystream_bytes.append(byte)

    return bytes(keystream_bytes)


def xor_encrypt(plaintext: str, keystream: bytes) -> bytes:
    pt_bytes = plaintext.encode('utf-8')
    ciphertext = bytes([p ^ k for p, k in zip(pt_bytes, keystream)])
    return ciphertext


def xor_decrypt(ciphertext: bytes, keystream: bytes) -> str:
    pt_bytes = bytes([c ^ k for c, k in zip(ciphertext, keystream)])
    return pt_bytes.decode('utf-8', errors='ignore')


# ===== Demo =====
plaintext = input("Enter plaintext: ")
key_str = input("Enter 4-bit key (e.g., 1110): ")

# Convert key to integer
initial_state = int(key_str, 2)

# Generate keystream of same length as plaintext
keystream = generate_keystream(initial_state, len(plaintext))

# Encryption
ciphertext = xor_encrypt(plaintext, keystream)
print("\nCiphertext (in hex):", ciphertext.hex().upper())

# Decryption (XOR again)
decrypted = xor_decrypt(ciphertext, keystream)
print("Decrypted text:", decrypted)