import math

class Position:
    def __init__ (self):
        self.direction = ''
        self.SL = 0
        self.TP = 0
        self.entryPrice = 0
        self.currentPrice = 0
        self.lot = 0
        self.result = ''
        self.rr = 1
    
    # Getters
    def getDirection(self):
        return self.direction
    
    def getSL(self):
        return self.SL
    
    def getTP(self):
        return self.TP
    
    def getLot(self):
        return self.lot

    def getPosValue(self):
        # Value is equal to lotsize * 10 * SL pips
        return self.lot * 10 * self.SL * 1000    
    
    def getResult(self):
        return self.result
    
    def getrr(self):
        return self.rr
    
    def getEntryPrice(self):
        return self.entryPrice
    
    def getSLPrice(self):
        if self.direction == 'BUY':
            return self.entryPrice - self.SL
        else:
            return self.entryPrice + self.SL
        
    def getTPPrice(self):
        if self.direction == 'BUY':
            return self.entryPrice + self.SL * self.rr
        else:
            return self.entryPrice - self.SL * self.rr
    
    # Setters
    def setDirection (self, direction):
        self.direction = direction
    
    def setSL (self, SL):
        self.SL = SL

    def setTP (self, TP):
        self.TP = TP

    def setCurrentPrice(self, price):
        self.currentPrice = price

    def setLot(self, lot):
        self.lot = lot

    # Methods
    def enterTrade(self, price, direction, lotSize, SL, rr):
        self.entryPrice = price
        self.currentPrice = price
        self.direction = direction
        self.lot = lotSize
        self.SL = SL
        self.rr = rr

    def updatePrice(self, price):
        self.currentPrice = price

    def hitSL(self, low, high):
        # Determine if SL hit in trade
        if self.direction == 'BUY':
            return self.entryPrice - low >= self.SL
        else:
            return high - self.entryPrice >= self.SL
    
    def hitTP(self, low, high, rr):
        # Determine if TP Hit within the dayu
        # RR 1:1
        if self.direction == 'BUY':
            return high - self.entryPrice >= self.SL * rr
        else:
            return self.entryPrice - low >= self.SL * rr
    
    def setResult(self, result):
        self.result = result

    


    
