import heapq
from collections import defaultdict, Counter

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    frequency = Counter(text)
    heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged_node = HuffmanNode(None, left.freq + right.freq)
        merged_node.left = left
        merged_node.right = right
        heapq.heappush(heap, merged_node)

    return heap[0]

def build_huffman_codes(node, current_code, huffman_codes):
    if node is not None:
        if node.char is not None:
            huffman_codes[node.char] = current_code
        build_huffman_codes(node.left, current_code + '0', huffman_codes)
        build_huffman_codes(node.right, current_code + '1', huffman_codes)

def compress_text(text, huffman_codes):
    compressed_text = ''.join(huffman_codes[char] for char in text)
    return compressed_text

def decompress_text(compressed_text, huffman_tree):
    decompressed_text = ''
    current_node = huffman_tree

    for bit in compressed_text:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char is not None:
            decompressed_text += current_node.char
            current_node = huffman_tree

    return decompressed_text

def main():
    original_text = "this is an example for huffman encoding"
    
    # Building Huffman tree
    huffman_tree = build_huffman_tree(original_text)
    
    # Building Huffman codes
    huffman_codes = {}
    build_huffman_codes(huffman_tree, '', huffman_codes)
    
    # Compression
    compressed_text = compress_text(original_text, huffman_codes)
    
    # Decompression
    decompressed_text = decompress_text(compressed_text, huffman_tree)
    
    # Display results
    print("Original Text: ", original_text)
    print("Compressed Text: ", compressed_text)
    print("Decompressed Text: ", decompressed_text)

if __name__ == "__main__":
    main()
