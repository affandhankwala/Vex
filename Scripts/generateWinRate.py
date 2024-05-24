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
    winRate = totalWin / total
    dollarDelta = account - initialAccount
    percentDelta = account / initialAccount - 1
    maxDrawdown = minimum / initialAccount - 1
    
    return [initialAccount, total, winRate, dollarDelta, percentDelta, maxDrawdown]