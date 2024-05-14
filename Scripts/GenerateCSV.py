import CSVReader
import numpy as np

# Input array

def generate_input(name, range):
    open = CSVReader.returnWickData(name)['Open'].values        # Open Values
    close = CSVReader.returnWickData(name)['Close'].values      # Close Values
    high = CSVReader.returnWickData(name)['High'].values        # High Values
    low = CSVReader.returnWickData(name)['Low'].values          # Low Values
        
    if range == 'open': return np.array(open)
    elif range == 'close': return np.array(close)
    elif range == 'high': return np.array(high)
    elif range == 'low': return np.array(low)
    else: return np.empty()
