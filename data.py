import os
import pandas as pd

def get_data_concept():
    df = pd.read_csv("data/melbourne_ta_reviews.csv")
    df_string = df.to_string()
    return df_string