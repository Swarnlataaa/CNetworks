def hamming_encode(data):
    # Ensure the input data has 4 bits
    if len(data) != 4:
        raise ValueError("Input data must be 4 bits long")

    # Calculate parity bits
    p1 = data[0] ^ data[1] ^ data[3]
    p2 = data[0] ^ data[2] ^ data[3]
    p3 = data[1] ^ data[2] ^ data[3]

    # Create the 7-bit codeword
    codeword = [p1, p2, data[0], p3, data[1], data[2], data[3]]

    return codeword

def hamming_decode(received_codeword):
    # Check for errors and correct if possible
    p1 = received_codeword[0] ^ received_codeword[2] ^ received_codeword[4] ^ received_codeword[6]
    p2 = received_codeword[1] ^ received_codeword[2] ^ received_codeword[5] ^ received_codeword[6]
    p3 = received_codeword[3] ^ received_codeword[4] ^ received_codeword[5] ^ received_codeword[6]

    error_position = p1 + p2 * 2 + p3 * 4

    if error_position != 0:
        # Flip the erroneous bit
        received_codeword[error_position - 1] ^= 1

    # Extract the original data bits
    decoded_data = [received_codeword[2], received_codeword[4], received_codeword[5], received_codeword[6]]

    return decoded_data

def main():
    # Example usage
    original_data = [1, 0, 1, 1]

    # Hamming encode
    codeword = hamming_encode(original_data)
    print("Original Data:", original_data)
    print("Encoded Codeword:", codeword)

    # Simulate an error in transmission by flipping a bit
    error_position = 3
    codeword[error_position - 1] ^= 1
    print("Received Codeword with Error:", codeword)

    # Hamming decode
    decoded_data = hamming_decode(codeword)
    print("Decoded Data:", decoded_data)

if __name__ == "__main__":
    main()
