import math

class Position:
    def __init__ (self):
        self.direction = ''
        self.SL = 0
        self.TP = 0
        self.entryPrice = 0
        self.currentPrice = 0
        self.lot = 0
    
    # Getters
    def getDirection(self):
        return self.direction
    
    def getSL(self):
        return self.SL
    
    def getTP(self):
        return self.TP

    def getPosValue(self):
        # Value is equal to lotsize * 10 * SL pips
        return self.lot * 10 * (math.abs(self.entryPrice - self.SL))
    
    # Setters
    def setDirection (self, direction):
        self.direction = direction
    
    def setSL (self, SL):
        self.SL = SL

    def setTP (self, TP):
        self.TP = TP

    def setCurrentPrice(self, price):
        self.currentPricePrice = price

    def setLot(self, lot):
        self.lot = lot

    # Methods
    def enterTrade(self, price, direction, lotSize):
        self.entryPrice = price
        self.currentPrice = price
        self.direction = direction
        self.lot = lotSize

    def updatePrice(self, price):
        self.currentPrice = price

    def hitSL(self):
        # Determine if SL hit in trade
        return math.abs (self.currentPrice - self.entryPrice) >= self.SL
    
    def hitTP(self, target):
        # Determine if TP Hit in BUY
        if self.direction == 'BUY':
            return self.currentPrice - self.entryPrice >= target
        else:
            return self.entryPrice - self.currentPrice >= target
    
   

    


    
