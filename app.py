from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

def load_data(file_path):
    # Check if the file actually exists before trying to read it
    if not os.path.exists(file_path):
        print(f"ERROR: The file {file_path} was not found!")
        return pd.DataFrame() # Return empty data so the app doesn't crash
    return pd.read_csv(file_path)

@app.route('/')
def home():
    file_path = "data/melbourne_ta_reviews.csv"
    df = load_data(file_path)
    
    if df.empty:
        return "Error: CSV file missing or empty. Check your 'data' folder!"

    # DEBUG: This prints the real columns to your terminal
    print("--- REAL CSV COLUMNS ---")
    print(df.columns.tolist())
    print("------------------------")

    # Convert to list of dictionaries for the HTML
    reviews = df.head(10).to_dict(orient='records')
    
    return render_template('index.html', reviews=reviews)

if __name__ == '__main__':
    # Using port 5001 for Mac compatibility
    app.run(debug=True, port=5001)