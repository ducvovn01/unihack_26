import os
import pandas as pd

def get_data_concept():
    data = pd.read_csv("data/melbourne_ta_reviews.csv")
    df = pd.DataFrame(data)
    
    return df