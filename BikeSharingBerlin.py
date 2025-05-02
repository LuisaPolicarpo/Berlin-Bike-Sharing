import streamlit as st
import pandas as pd
import requests
import pydeck as pdk

st.set_page_config(page_title="Berlin Bike Finder", page_icon="🚲", layout="wide")

# Title 
st.title("🚲 Berlin Bike Station Finder")
st.markdown("Search for a bike station and see current availability, address, and map location.")

# Load data from API
@st.cache_data
def load_data():
    url = "https://api.citybik.es/v2/networks/nextbike-berlin"
    response = requests.get(url)
    if response.status_code != 200:
        st.error(f"Failed to fetch data. Status code: {response.status_code}")
        return pd.DataFrame()
    data = response.json()
    stations = data['network']['stations']
    df = pd.DataFrame(stations)
    df['occupancy_rate'] = df['free_bikes'] / (df['free_bikes'] + df['empty_slots'])
    return df

df = load_data()

if not df.empty:
    station_names = df['name'].sort_values().unique().tolist()
    selected_station = st.selectbox("🔍 Search for a station", station_names)

    station = df[df['name'] == selected_station].iloc[0]

    st.subheader(f"🏢 {station['name']}")
    st.metric("🚲 Free Bikes", int(station['free_bikes']))
    st.metric("🏠 Empty Slots", int(station['empty_slots']))
    st.metric("Occupancy Rate", f"{station['occupancy_rate']:.0%}")

    # --- Map ---
    st.subheader("📍 Station Location")
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=station['latitude'],
            longitude=station['longitude'],
            zoom=15,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=pd.DataFrame([station]),
                get_position='[longitude, latitude]',
                get_radius=50,
                get_color='[200, 30, 0, 160]',
            )
        ],
    ))

    st.caption("Live data from CityBikes API")
else:
    st.warning("No station data available.")
