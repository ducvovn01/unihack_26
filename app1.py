# app.py
import streamlit as st
from data import load_data

st.set_page_config(page_title="Melbourne Hidden Gems", layout="wide")

st.title("Melbourne Hidden Gems 🍴🗺️")
st.markdown("Discover top-rated Melbourne restaurants – great value, hidden spots, no tourist traps!")

data = load_data("data/melbourne_ta_reviews.csv")
if data is None:
    st.error("Failed to load data. Check data.py for path issues.")
    st.stop()

# Simple sidebar filters
with st.sidebar:
    st.header("Your Preferences")
    budget = st.selectbox("Budget", ["All", "$", "$$ - $$$"])
    # Extract unique suburbs roughly
    suburbs = sorted(data['address'].str.extract(r'([A-Za-z\s]+),\s*Victoria', expand=False).dropna().unique())
    area = st.selectbox("Area/Suburb", ["All"] + suburbs)

# Apply filters
filtered = data.copy()
if budget != "All":
    filtered = filtered[filtered['priceLevel'].str.contains(budget, na=False)]
if area != "All":
    filtered = filtered[filtered['address'].str.contains(area, case=False, na=False)]

# Show top matches (best ranking first)
filtered = filtered.head(10)  # limit to top 10 for demo

if filtered.empty:
    st.warning("No matches found. Try different filters!")
else:
    st.subheader(f"Top Recommendations ({len(filtered)})")
    for _, row in filtered.iterrows():
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{row['name']}**")
                st.caption(f"Rank {int(row['rankingPosition'])} • {row['priceLevel']} • {row['category']}")
                st.caption(row['address'])
                if row['rankingPosition'] > 20:
                    st.success("Hidden Gem – High rating, less crowded!")
            with col2:
                st.metric("Rating", f"{row['rating']} ⭐")

# Placeholder for map (next step)
st.subheader("Map View (coming soon)")