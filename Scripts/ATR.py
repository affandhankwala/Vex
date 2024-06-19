from typing import List

def get_atr (actual_L: List, actual_H: List, position: int, minimum: int) -> float:
    # Return the average trading range of last 15 candles
    # Determine if we have even hit 15 candles

    total = min(minimum, position + 1)

    sum = 0
    for j in range(total):
        sum += (actual_H[position - j] - actual_L[position - j])
    return sum / total

