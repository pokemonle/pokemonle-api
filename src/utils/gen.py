def encode_gen(gens: set[int]) -> int:
    """Encodes a set of integers into an int."""
    """ (1,2,4) => 0b1011 => 11"""
    """ (3,4,7) => 0b1001100 => 76"""

    return sum([1 << (i - 1) for i in gens])  # 1 << i is equivalent to 2 ** i, but faster


def decode_gen(gen: int) -> set[int]:
    """Decodes an int into a set of integers."""
    """ 11 => (1,2,4)"""
    """ 76 => (3,4,7)"""
    binary = bin(gen)[2:][::-1]  # Convert to binary and reverse the string
    gens = set()
    for i, bit in enumerate(binary):
        if bit == '1':
            gens.add(i + 1)  # Add 1 to the index to get the original integer
    return gens
