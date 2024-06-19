import numpy as np
import pandas as pd
from typing import List
import os

# Input array

def generate_input(name, range):
    # open = CSVReader.returnWickData(name)['open'].values        # Open Values
    # close = CSVReader.returnWickData(name)['close'].values      # Close Values
    # high = CSVReader.returnWickData(name)['high'].values        # High Values
    # low = CSVReader.returnWickData(name)['low'].values          # Low Values
        
    # if range == 'open': return np.array(open)
    # elif range == 'close': return np.array(close)
    # elif range == 'high': return np.array(high)
    # elif range == 'low': return np.array(low)
    # else: return np.empty()

    return np.array(read_csv(name)[range].values)

def read_csv(name: str) -> List:
    script_path = os.path.dirname(os.path.abspath(__file__))
    relative_path = 'Files\\CandleData\\' + name
    file_path = os.path.join(script_path, relative_path)
    wick_data = pd.read_csv (file_path)
    #wick_text = wick_data [['Open', 'High', 'Low', 'Close']].to_string(index = False)
    return wick_data