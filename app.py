# Import necessary libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load dataset
@st.cache
def load_data(file_path):
    df = pd.read_excel(file_path)
    # Keep relevant columns and handle missing values
    columns_to_keep = ["name", "rating", "kd_ratio", "headshot_percent"]
    data = df[columns_to_keep]
    data = data.dropna()

    # Convert rating to numeric values
    def convert_rating(rating):
        if "Radiant" in str(rating):
            return 5.0
        elif "Immortal" in str(rating):
            return 4.0
        elif "Diamond" in str(rating):
            return 3.0
        elif "Platinum" in str(rating):
            return 2.0
        elif "Gold" in str(rating):
            return 1.0
        else:
            return np.nan

    data["rating"] = data["rating"].apply(convert_rating)
    return data

# Path to the dataset
DATA_FILE = "cleaned_dataset.xlsx"

# Load data
data = load_data(DATA_FILE)

# Streamlit UI
st.title("Player Classification Application")

# Display dataset preview
st.subheader("Dataset Preview")
st.write(data)

# Sidebar filter options
st.sidebar.subheader("Filter Options")
filter_type = st.sidebar.selectbox(
    "Select Filter Type",
    ["Rating", "KD Ratio", "Headshot Percentage"]
)

num_top_players = st.sidebar.slider(
    "Number of Top Players to Display",
    min_value=5,
    max_value=20,
    value=10
)

# Map filter types to actual column names
column_map = {
    "Rating": "rating",
    "KD Ratio": "kd_ratio",
    "Headshot Percentage": "headshot_percent"
}

# Select the correct column for filtering
selected_column = column_map.get(filter_type)

# Get top players
top_players = data.sort_values(by=selected_column, ascending=False).head(num_top_players)

# Display top players
st.subheader(f"Top {num_top_players} Players by {filter_type}")
st.write(top_players)

# Visualize top players
st.subheader("Visualization")
fig, ax = plt.subplots(figsize=(8, 6))
ax.barh(top_players["name"], top_players[selected_column], color="skyblue")
ax.set_xlabel(filter_type)
ax.set_ylabel("Player Name")
ax.set_title(f"Top {num_top_players} Players by {filter_type}")
st.pyplot(fig)
