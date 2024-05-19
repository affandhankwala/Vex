def getATR (actual_L, actual_H, i):
    # Return the average trading range of last 15 candles
    # Determine if we have even hit 15 candles
    total = 0
    if i < 15:
        total = i 
    else:
        total = 14      # 0 - 14 is 15 candles

    # Hold sum of ranges
    sum = 0
    for i in range(total):
        # Gather range from high minus low
        diff = actual_H[i] - actual_L[i]
        sum += diff

    return sum / diff