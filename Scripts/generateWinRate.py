def winRate(positions):
    totalWin = 0
    total = 0
    for p in positions:
        if p.getResult() == 'WIN': totalWin += 1
        total += 1
    return (str)(totalWin / total * 100) + "%"