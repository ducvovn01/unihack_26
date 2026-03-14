import pandas as pd

def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

file_path = "data/melbourne_ta_reviews.csv"
data = load_data(file_path)
print(data.head())