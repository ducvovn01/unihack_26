import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

from data import get_data_concept
from styles import load_css

# -------------------------
# Setup
# -------------------------
load_dotenv()
my_api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=my_api_key)

st.set_page_config(
    page_title="Melbourne Hidden Gems",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()

# -------------------------
# Header
# -------------------------
st.markdown("""
<div class="header-wrap">
    <div class="navbar">
        <div class="navbar-title">Melbourne Hidden Gems</div>
        <div class="navbar-subtitle">Smart restaurant discovery for food lovers</div>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------
# Load Data
# -------------------------
data = get_data_concept()
if data is None:
    st.error("Failed to load data. Check data.py for path issues.")
    st.stop()

# Clean columns
data["priceLevel"] = data["priceLevel"].fillna("").astype(str).str.strip()
data["address"] = data["address"].fillna("").astype(str).str.strip()
data["name"] = data["name"].fillna("").astype(str).str.strip()
data["category"] = data["category"].fillna("").astype(str).str.strip()

# -------------------------
# Sidebar Filters
# -------------------------
with st.sidebar:
    st.header("Your Preferences")

    budget = st.selectbox("Budget", ["All", "$", "$$ - $$$", "$$$$"])

    suburbs = sorted(
        data["address"]
        .str.extract(r"([A-Za-z\s]+),\s*Victoria", expand=False)
        .dropna()
        .str.strip()
        .unique()
    )
    area = st.selectbox("Area/Suburb", ["All"] + list(suburbs))

# -------------------------
# Apply Filters
# -------------------------
filtered = data.copy()

if budget != "All":
    filtered = filtered.loc[filtered["priceLevel"] == budget]

if area != "All":
    filtered = filtered.loc[
        filtered["address"].str.contains(area, case=False, na=False, regex=False)
    ]

filtered = filtered.sort_values(
    by=["rankingPosition", "rating", "numberOfReviews"],
    ascending=[True, False, False]
).head(10)

# -------------------------
# AI Chatbot Setup
# -------------------------
dataset_preview = filtered[
    ["name", "rankingPosition", "priceLevel", "category", "rating", "address", "numberOfReviews"]
].to_dict(orient="records")

system_instructions = f"""
You are an assistant that helps users find restaurants in Melbourne.

Use only the restaurant data provided below.
Do not invent restaurants that are not in the data.
If the user asks for recommendations, prefer restaurants that match the active filters.

Active filters:
- Budget: {budget}
- Area/Suburb: {area}

Available filtered restaurant data:
{dataset_preview}

When answering:
- recommend restaurants from the provided data only
- be concise and useful
- mention name, rating, price level, and suburb or address
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=system_instructions
)

# Better session logic:
# your original version only creates chat_session once, so if filters change,
# the chatbot may still use old filter data.
if (
    "chat_session" not in st.session_state
    or st.session_state.get("last_budget") != budget
    or st.session_state.get("last_area") != area
):
    st.session_state.chat_session = model.start_chat(history=[])
    st.session_state.last_budget = budget
    st.session_state.last_area = area

with st.sidebar:
    st.markdown("---")
    st.subheader("AI Food Assistant")

    for message in st.session_state.chat_session.history:
        role = "assistant" if message.role == "model" else "user"
        with st.chat_message(role):
            st.markdown(message.parts[0].text)

    user_input = st.chat_input("Ask for restaurant tips...")
    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.chat_session.send_message(user_input)
                st.markdown(response.parts[0].text)

# -------------------------
# Hero Section
# -------------------------
col_hero_left, col_hero_right = st.columns([1.05, 1], gap="large")

with col_hero_left:
    st.image("food.webp", use_container_width=True)

with col_hero_right:
    st.markdown("""
    <div style="padding: 20px 10px 10px 10px;">
        <div class="small-badge">Melbourne Food Guide</div>
        <div class="hero-title">Find top-rated restaurants faster</div>
        <div class="hero-text">
            Discover highly rated Melbourne restaurants by budget and suburb, then use the AI assistant
            in the sidebar for quick suggestions based on your preferences.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='section-title'>Restaurant Discovery Platform</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='section-text'>Browse filtered recommendations and compare ratings to make a better dining choice.</div>",
    unsafe_allow_html=True
)

# -------------------------
# Add lat/lon via geocoding (Nominatim - free, no key)
# -------------------------
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Cache geocoding results (first run slow, later instant)
@st.cache_data(ttl=86400 * 7)  # 24 hours
def get_lat_lon(address):
    if not address or pd.isna(address):
        return None, None
    try:
        geolocator = Nominatim(user_agent="melbourne_hidden_gems_app_2026_v1", timeout=15)
        location = geolocator.geocode(address, timeout=10)
        if location:
            return location.latitude, location.longitude
        return None, None
    except Exception:
        return None, None

# Only geocode if columns missing
if 'lat' not in filtered.columns or 'lon' not in filtered.columns:
    with st.spinner("Adding map locations (first time may take 20-60s)..."):
        lat_lon = filtered['address'].apply(get_lat_lon)
        filtered['lat'] = lat_lon.apply(lambda x: x[0])
        filtered['lon'] = lat_lon.apply(lambda x: x[1])

# Filter out rows without coordinates
map_ready = filtered.dropna(subset=['lat', 'lon'])

import pydeck as pdk
import streamlit as st

layer = pdk.Layer(
    'ScatterplotLayer',
    data=map_ready,
    get_position=['lon', 'lat'],           
    get_radius=100,                        
    get_fill_color=[255, 80, 80, 220],     
    pickable=True,                         
    auto_highlight=True,                  
    opacity=0.8
)

tooltip = {
    "html": """
    <b>{name}</b><br>
    📍 {address}<br>
    ⭐ {rating} 
    """,
    "style": {
        "background": "rgba(0, 0, 0, 0.85)",
        "color": "white",
        "font-family": "Arial, sans-serif",
        "padding": "10px",
        "border-radius": "6px",
        "max-width": "300px"
    }
}

if not map_ready.empty:
    view_state = pdk.ViewState(
        latitude=map_ready['lat'].mean(),
        longitude=map_ready['lon'].mean(),
        zoom=11,          
        pitch=0,
        bearing=0
    )
else:
    view_state = pdk.ViewState(
        latitude=-37.8136, longitude=144.9631,  
        zoom=11
    )

st.pydeck_chart(
    pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style='dark',
        map_provider='carto'  
    )
)
# -------------------------
# Main Recommendations
# -------------------------
st.subheader(f"Top Recommendations ({len(filtered)})")

if filtered.empty:
    st.warning("No matches found. Try different filters!")
else:
    for _, row in filtered.iterrows():
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"### {row['name']}")
                st.caption(
                    f"Rank {int(row['rankingPosition'])} • {row['priceLevel']} • {row['category']}"
                )
                st.write(row["address"])

                if row["rating"] >= 4.5 and row["rankingPosition"] > 20:
                    st.success("Possible Hidden Gem")

            with col2:
                st.metric("Rating", f"{row['rating']} ⭐")

# -------------------------
# Footer
# -------------------------
st.markdown("""
<div class="footer">
    <strong>Melbourne Hidden Gems</strong><br>
     • Designed for restaurant discovery in Melbourne •
</div>
""", unsafe_allow_html=True)