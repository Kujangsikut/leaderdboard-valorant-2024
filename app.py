import streamlit as st
import pandas as pd

# Load dataset
def load_data():
    file_path = "cleaned_dataset.xlsx"  # Use relative path for deployment
    try:
        data = pd.read_excel(file_path, sheet_name='Sheet1')
        return data
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

data = load_data()

if data is not None:
    # Streamlit App
    st.title("Leaderboard Application")
    st.markdown("Use this app to explore player leaderboard based on various metrics.")

    # Sidebar options
    metric_options = ["rating", "damage_round", "headshot_percent", "aces", "kd_ratio"]
    selected_metric = st.sidebar.selectbox("Select a metric to sort by:", metric_options)

    top_n = st.sidebar.slider("Select number of top players to display:", 5, 50, 10)

    # Sort and display leaderboard
    leaderboard = data.sort_values(by=selected_metric, ascending=False).head(top_n)
    st.subheader(f"Top {top_n} Players by {selected_metric.capitalize()}")
    st.table(leaderboard[["name", "tag", selected_metric]])
