import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

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

    # Linear Regression Analysis
    st.sidebar.header("Linear Regression Analysis")
    regression_target = st.sidebar.selectbox("Select target variable for regression:", metric_options)
    regression_features = st.sidebar.multiselect("Select feature variables for regression:", metric_options, default=metric_options)

    if regression_target and regression_features:
        # Convert selected columns to numeric and handle missing values
        X = data[regression_features].apply(pd.to_numeric, errors='coerce')
        y = pd.to_numeric(data[regression_target], errors='coerce')

        # Drop rows with missing values in X or y
        X = X.dropna()
        y = y.dropna()

        if len(regression_features) > 0:
            # Split the data into training and test sets
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Initialize and train the model
            model = LinearRegression()
            model.fit(X_train, y_train)

            # Calculate the R-squared score
            score = model.score(X_test, y_test)

            # Display the results
            st.subheader("Linear Regression Results")
            st.write(f"R-squared value: {score:.2f}")

            # Display the model coefficients
            coefficients = pd.DataFrame({"Feature": regression_features, "Coefficient": model.coef_})
            st.write("Model Coefficients:")
            st.table(coefficients)

    # Box Plot Visualization
    st.sidebar.header("Box Plot Visualization")
    boxplot_metric = st.sidebar.selectbox("Select a metric for box plot:", metric_options)

    if boxplot_metric:
        st.subheader(f"Box Plot for {boxplot_metric.capitalize()}")
        fig, ax = plt.subplots()
        sns.boxplot(data=data, y=boxplot_metric, ax=ax)
        st.pyplot(fig)
