# File Compression Using Huffman Coding

Lossless compression using Huffman Coding. The Python version can compress and decompress text files, while the C++ version demonstrates the same algorithm in a compiled implementation.

## Python Usage

```bash
python huffman.py compress input.txt compressed.huff
python huffman.py decompress compressed.huff restored.txt
```

## C++ Usage

```bash
g++ huffman.cpp -std=c++17 -O2 -o huffman
./huffman
```

## Core Idea

The program counts character frequencies, builds an optimal prefix-free binary tree, converts characters to binary codes, and stores enough metadata to rebuild the tree during decompression.
