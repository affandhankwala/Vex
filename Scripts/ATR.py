def getATR (actual_L, actual_H, i, wicks):
    # Return the average trading range of last 15 candles
    # Determine if we have even hit 15 candles
    total = 0
    if i < wicks:
        total = i + 1
    else:
        total = wicks - 1      # 0 - 14 is 15 candles

    # Hold sum of ranges
    sum = 0
    diff = 0
    for j in range(total):
        # Gather range from high minus low
        diff = actual_H[j] - actual_L[j]
        sum += diff

    return sum / total