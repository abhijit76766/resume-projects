import argparse
import heapq
import itertools
import json
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional


@dataclass(order=True)
class Node:
    frequency: int
    order: int
    char: Optional[str] = field(default=None, compare=False)
    left: Optional["Node"] = field(default=None, compare=False)
    right: Optional["Node"] = field(default=None, compare=False)


def build_tree(text: str) -> Optional[Node]:
    counter = itertools.count()
    heap = [Node(freq, next(counter), char) for char, freq in Counter(text).items()]
    heapq.heapify(heap)
    if not heap:
        return None
    if len(heap) == 1:
        only = heapq.heappop(heap)
        return Node(only.frequency, next(counter), None, only, None)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        heapq.heappush(heap, Node(left.frequency + right.frequency, next(counter), None, left, right))
    return heap[0]


def build_codes(node: Optional[Node], prefix: str = "", codes: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    if codes is None:
        codes = {}
    if node is None:
        return codes
    if node.char is not None:
        codes[node.char] = prefix or "0"
        return codes
    build_codes(node.left, prefix + "0", codes)
    build_codes(node.right, prefix + "1", codes)
    return codes


def bits_to_bytes(bits: str) -> bytes:
    padding = (8 - len(bits) % 8) % 8
    bits += "0" * padding
    return bytes(int(bits[i : i + 8], 2) for i in range(0, len(bits), 8)), padding


def bytes_to_bits(data: bytes, padding: int) -> str:
    bits = "".join(f"{byte:08b}" for byte in data)
    return bits[:-padding] if padding else bits


def compress(input_path: Path, output_path: Path) -> None:
    text = input_path.read_text(encoding="utf-8")
    tree = build_tree(text)
    codes = build_codes(tree)
    encoded = "".join(codes[ch] for ch in text)
    payload, padding = bits_to_bytes(encoded)
    header = json.dumps({"codes": codes, "padding": padding}).encode("utf-8")
    output_path.write_bytes(len(header).to_bytes(4, "big") + header + payload)
    print(f"Compressed {input_path} -> {output_path}")
    print(f"Original: {len(text.encode('utf-8'))} bytes, compressed payload: {len(payload)} bytes")


def decompress(input_path: Path, output_path: Path) -> None:
    blob = input_path.read_bytes()
    header_size = int.from_bytes(blob[:4], "big")
    header = json.loads(blob[4 : 4 + header_size].decode("utf-8"))
    payload = blob[4 + header_size :]
    reverse_codes = {bits: char for char, bits in header["codes"].items()}
    bits = bytes_to_bits(payload, header["padding"])

    decoded = []
    current = ""
    for bit in bits:
        current += bit
        if current in reverse_codes:
            decoded.append(reverse_codes[current])
            current = ""
    output_path.write_text("".join(decoded), encoding="utf-8")
    print(f"Decompressed {input_path} -> {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Huffman file compressor")
    parser.add_argument("mode", choices=["compress", "decompress"])
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()

    if args.mode == "compress":
        compress(Path(args.input), Path(args.output))
    else:
        decompress(Path(args.input), Path(args.output))


if __name__ == "__main__":
    main()
