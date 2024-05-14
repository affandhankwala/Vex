import pandas as pd
import os

def returnWickData(fileName):
    script_path = os.path.dirname(os.path.abspath(__file__))

    relative_path = 'Files/' + fileName

    file_path = os.path.join(script_path, relative_path)

    wick_data = pd.read_csv (file_path)

    #wick_text = wick_data [['Open', 'High', 'Low', 'Close']].to_string(index = False)
    return wick_data
