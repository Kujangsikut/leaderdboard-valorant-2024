# Import necessary libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay

# Load dataset
@st.cache
def load_data(file_path):
    df = pd.read_excel(file_path)
    columns_to_keep = ["name", "rating", "kd_ratio", "headshot_percent"]
    data = df[columns_to_keep]
    data = data.dropna()

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

# Streamlit UI
st.title("Player Classification Application")
uploaded_file = st.file_uploader("Upload your dataset (.xlsx)", type=["xlsx"])

if uploaded_file:
    data = load_data(uploaded_file)

    st.subheader("Dataset Preview")
    st.write(data)

    # Filter options
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

    # Apply filtering
    if filter_type == "Rating":
        top_players = data.sort_values(by="rating", ascending=False).head(num_top_players)
    elif filter_type == "KD Ratio":
        top_players = data.sort_values(by="kd_ratio", ascending=False).head(num_top_players)
    else:  # Headshot Percentage
        top_players = data.sort_values(by="headshot_percent", ascending=False).head(num_top_players)

    st.subheader(f"Top {num_top_players} Players by {filter_type}")
    st.write(top_players)

    # Visualize data
    st.subheader("Visualization")
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(top_players["name"], top_players[filter_type.lower().replace(" ", "_")], color="skyblue")
    ax.set_xlabel(filter_type)
    ax.set_ylabel("Player Name")
    ax.set_title(f"Top {num_top_players} Players by {filter_type}")
    st.pyplot(fig)
