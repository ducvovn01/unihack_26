import os
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd

load_dotenv()
my_api_key = os.getenv("GEMINI_API_KEY")

genai.configure (api_key = my_api_key)
model = genai.GenerativeModel("gemini-2.0-pro")

print ("API Key loaded successfully!")