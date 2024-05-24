def winRate(positions):
    totalWin = 0
    total = 0
    msg = ""
    for p in positions:
        if p.getResult() == 'WIN': totalWin += 1
        total += 1
    msg += "Winrate: " + (str)(totalWin / total * 100) + "%\n"
    msg += "Wins: " + (str)(totalWin) + "\n"
    msg += "Losses: " + (str)(total - totalWin) + "\n"
    print(msg)