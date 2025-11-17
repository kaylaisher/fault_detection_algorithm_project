# utils/weight_patterns/one_hot_patterns.py

def one_hot(bit_width):
    patterns = []
    for i in range(bit_width):
        arr = [0] * bit_width
        arr[i] = 1
        patterns.append(arr)
    return patterns
