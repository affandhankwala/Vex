def metrics(positions, account):
    initialAccount = account
    minimum = initialAccount                     # Keep track of lowest account falls
    totalWin = 0
    total = 0
    msg = ""
    for p in positions:
        # Determine how many wins
        if p.getResult() == 'WIN': totalWin += 1
        total += 1
        # Accumulate account value per trade
        account += p.getPosValue()
        minimum = min(account, minimum)

    # Calculate metrics
    winRate = round(totalWin / total * 100, 2)
    dollarDelta = round(account - initialAccount, 2)
    percentDelta = round((account / initialAccount - 1) * 100, 2)
    maxDrawdown = round((minimum / initialAccount - 1) * 100, 2)
    
    return [initialAccount, total, winRate, dollarDelta, percentDelta, maxDrawdown]