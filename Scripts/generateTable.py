import os

def makeTable(name, positions, metrics):
    # metrics is arranged as follows:
    # [initialAccount, total, winRate, dollarDelta, percentDelta, maxDrawdown]
    generateArray(name, positions, metrics)

def generateArray(name, positions, metrics):
    account = metrics[0]
    # Print out all positions into output file
    # Rows = all positions + header

    # TODO: Print out Name of graph, Total Trades, Initial investment, Win Rate, $ & % Delta, Max Drawdown
     
    headers = ['#', 'Lot Size', 'RR', 'Direction', 'Entry ($)', 'SL ($)',
                'TP ($)', 'W/L', 'Gain ($)', 'Account ($)']
    rows, cols = len(positions) + 1, len(headers)
    table = [[None for _ in range(cols)] for _ in range(rows)]  
    # First row will be headers
    table[0] = headers
    for r in range(1, len(table)):
        
        table[r][0] = r
        p = positions[r - 1]

        table[r][1] = p.getLot()
        table[r][2] = p.getrr()
        table[r][3] = p.getDirection() 
        table[r][4] = p.getEntryPrice()
        table[r][5] = p.getSLPrice()
        table[r][6] = p.getTPPrice()
        table[r][7] = p.getResult()
        table[r][8] = p.getPosValue()

        account += table[r][8]
        table[r][9] = account
    
    # Write to output file
    script_path = os.path.dirname(os.path.abspath(__file__))
    relativePath = 'Output/table.txt'
    fileName = os.path.join(script_path, relativePath)
    writeToFile(fileName, name, table, metrics)

def writeToFile(fileName, name, table, metrics):
    with open(fileName, 'w') as file:
        # Write Metric information
        file.write("Name: " + name + "\n")
        file.write("Initial Account: " + (str)(metrics[0]) + "\n")
        file.write("Total Trades: " + (str)(metrics[1]) + "\n")
        file.write("Win Rate: " + (str)(metrics[2]) + "\n")
        file.write("$ (%) Gain:" + (str)(metrics[3]) + "(" + (str)(metrics[4]) + ")" + "\n")
        file.write("Max Drawdown: " + (str)(metrics[5]) + "\n")

        # Draw table
        for row in table:
            file.write(', '.join(map(str, row)) + '\n')

def drawTable(table):
    result = ''
    # Create a list of the size of each column 
    # Each element will have be a maximum of 4 decimals out
    sizeOfCol = [None for _ in range(len(table[0]))]
    for i in range(len(table[0])):
        maxLength = -1
        for j in range(len(table)):
            # Determine longest element per column
            temp = (str)(table[j][i])
            maxLength = max(len(temp), maxLength)

