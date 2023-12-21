import binascii

def crc32(data):
    # Calculate CRC-32 using the binascii library
    crc = binascii.crc32(data) & 0xFFFFFFFF
    return crc

def simulate_error(data, error_position):
    # Simulate an error in transmission by flipping a bit
    corrupted_data = bytearray(data)
    corrupted_data[error_position - 1] ^= 1
    return corrupted_data

def main():
    # Example usage
    original_data = b"Hello, CRC!"

    # CRC encoding
    encoded_crc = crc32(original_data)
    print("Original Data:", original_data)
    print("Encoded CRC-32:", encoded_crc)

    # Simulate an error in transmission
    error_position = 10
    corrupted_data = simulate_error(original_data, error_position)
    print("Corrupted Data with Error:", corrupted_data)

    # CRC decoding
    decoded_crc = crc32(corrupted_data)
    print("Decoded CRC-32:", decoded_crc)

    # Check if CRC indicates an error
    if decoded_crc == 0:
        print("No errors detected.")
    else:
        print("Error detected!")

if __name__ == "__main__":
    main()
