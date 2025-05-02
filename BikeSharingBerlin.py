{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyNytedW/pld2kcXUY5rJYaC",
      #"include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/LuisaPolicarpo/Berlin-Bike-Sharing/blob/main/BikeSharingBerlin.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "tQizLQ1vX7s-"
      },
      "outputs": [],
      "source": [
        "import streamlit as st\n",
        "import pandas as pd\n",
        "import requests\n",
        "import pydeck as pdk\n",
        "\n",
        "st.set_page_config(page_title=\"Berlin Bike Finder\", page_icon=\"🚲\", layout=\"wide\")\n",
        "\n",
        "# Title\n",
        "st.title(\"🚲 Berlin Bike Station Finder\")\n",
        "st.markdown(\"Search for a bike station and see current availability, address, and map location.\")\n",
        "\n",
        "# Load data from API\n",
        "@st.cache_data\n",
        "\n",
        "def load_data():\n",
        "    url = \"https://api.citybik.es/v2/networks/nextbike-berlin\"\n",
        "    response = requests.get(url)\n",
        "    if response.status_code != 200:\n",
        "        st.error(f\"Failed to fetch data. Status code: {response.status_code}\")\n",
        "        return pd.DataFrame()\n",
        "    data = response.json()\n",
        "    stations = data['network']['stations']\n",
        "    df = pd.DataFrame(stations)\n",
        "    df['occupancy_rate'] = df['free_bikes'] / (df['free_bikes'] + df['empty_slots'])\n",
        "    return df\n",
        "\n",
        "\n",
        "df = load_data()\n",
        "\n",
        "if not df.empty:\n",
        "    station_names = df['name'].sort_values().unique().tolist()\n",
        "    selected_station = st.selectbox(\"🔍 Search for a station\", station_names)\n",
        "\n",
        "    station = df[df['name'] == selected_station].iloc[0]\n",
        "\n",
        "    st.subheader(f\"🏢 {station['name']}\")\n",
        "\n",
        "    #col1 = st.columns(1)\n",
        "    #with col1:\n",
        "    st.metric(\"🚲 Free Bikes\", int(station['free_bikes']))\n",
        "    st.metric(\"🏠 Empty Slots\", int(station['empty_slots']))\n",
        "    st.metric(\"Occupancy Rate\", f\"{station['occupancy_rate']:.0%}\")\n",
        "\n",
        "\n",
        "    # --- Map ---\n",
        "    st.subheader(\"📍 Station Location\")\n",
        "    st.pydeck_chart(pdk.Deck(\n",
        "        map_style='mapbox://styles/mapbox/light-v9',\n",
        "        initial_view_state=pdk.ViewState(\n",
        "            latitude=station['latitude'],\n",
        "            longitude=station['longitude'],\n",
        "            zoom=15,\n",
        "            pitch=0,\n",
        "        ),\n",
        "        layers=[\n",
        "            pdk.Layer(\n",
        "                'ScatterplotLayer',\n",
        "                data=pd.DataFrame([station]),\n",
        "                get_position='[longitude, latitude]',\n",
        "                get_radius=50,\n",
        "                get_color='[200, 30, 0, 160]',\n",
        "            )\n",
        "        ],\n",
        "    ))\n",
        "\n",
        "    st.caption(\"Live data from CityBikes API\")\n",
        "\n",
        "else:\n",
        "    st.warning(\"No station data available.\")"
      ]
    }
  ]
}
