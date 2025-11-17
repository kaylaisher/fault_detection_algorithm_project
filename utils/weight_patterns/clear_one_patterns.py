# utils/weight_patterns/clear_one_patterns.py

def clear_one(bit_width):
    """
    Generates patterns that clear one bit from all-ones:
      bit_width=4 → 0111, 1011, 1101, 1110
    """
    patterns = []
    for i in range(bit_width):
        arr = [1] * bit_width
        arr[i] = 0
        patterns.append(arr)
    return patterns


def explicit_last_zero(bit_width):
    """
    Explicit: 1111...1110 (LSB cleared)
    """
    arr = [1] * bit_width
    arr[-1] = 0
    return [arr]
