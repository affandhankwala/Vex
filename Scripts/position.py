import math

class Position:
    def __init__ (self):
        self.pair = ''
        self.direction = ''
        self.SL = 0
        self.TP = 0
        self.entryPrice = 0
        self.currentPrice = 0
        self.lot = 0
        self.result = ''
        self.rr = 1
        self.posValue = 0
    
    # Getters
    def getPair(self):
        return self.pair
    
    def getDirection(self):
        return self.direction
    
    def getSL(self):
        return round(self.SL, 4)
    
    def getTP(self):
        return round(self.TP, 4)
    
    def getLot(self):
        return round(self.lot)

    def getPosValue(self):
        return round(self.posValue, 4)
    
    def getResult(self):
        return self.result
    
    def getrr(self):
        return self.rr
    
    def getEntryPrice(self):
        return round(self.entryPrice, 4)
    
    def getSLPrice(self):
        if self.direction == 'BUY':
            return round(self.entryPrice - self.SL, 4)
        else:
            return round(self.entryPrice + self.SL, 4)
        
    def getTPPrice(self):
        if self.direction == 'BUY':
            return round(self.entryPrice + self.SL * self.rr, 4)
        else:
            return round(self.entryPrice - self.SL * self.rr, 4)
    
    # Setters
    def setDirection (self, direction):
        self.direction = direction
    
    def setSL (self, SL):
        self.SL = round(SL, 2)

    def setTP (self, TP):
        self.TP = round(TP, 2)

    def setCurrentPrice(self, price):
        self.currentPrice = round(price, 4)

    def setLot(self, lot):
        self.lot = round(lot, 4)

    # Methods
    def enterTrade(self, pair, price, direction, lot, SL, rr):
        self.pair = pair
        self.entryPrice = round(price, 4)
        self.currentPrice = round(price, 4)
        self.direction = direction
        self.lot = round(lot, 4)
        self.SL = round(SL, 4)
        self.rr = rr

        # Loss Value is equal to lotsize * 10 * SL pips
        self.posValue = self.lot * 10 * self.SL * 1000   

    def updatePrice(self, price):
        self.currentPrice = round(price, 4)

    def hitSL(self, low, high):
        # Determine if SL hit in trade
        if self.direction == 'BUY':
            return self.entryPrice - low >= self.SL
        else:
            return high - self.entryPrice >= self.SL
    
    def hitTP(self, low, high, rr):
        # Determine if TP Hit within the day
        # RR 1:1
        if self.direction == 'BUY':
            return high - self.entryPrice >= self.SL * rr
        else:
            return self.entryPrice - low >= self.SL * rr
    
    def setResult(self, result):
        self.result = result

    def invertValue(self):
        self.posValue = self.posValue * -1
    
    def profitValue(self):
        self.posValue = self.posValue * self.rr
    


    
