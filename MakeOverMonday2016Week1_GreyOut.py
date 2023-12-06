import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to load and preprocess the dataset
@st.cache  # Cache the data to prevent reloading on every interaction
def load_data():
    # Reading the dataset from the specified path
    data = pd.read_excel('DataSet.xlsx')
    # Dropping rows where essential data is missing
    data = data.dropna(subset=['SALARY', 'WAR', 'VALUE', 'SURPLUS VALUE', 'Age'])
    # Convert the SALARY column to numeric, handling non-numeric entries
    data['SALARY'] = pd.to_numeric(data['SALARY'], errors='coerce')
    return data

# Loading the dataset
data = load_data()

# Setting up the title of the Streamlit app
st.title('Is there a pattern in player\'s salaries?')

# Adding filters in the sidebar for user interaction
player_filter = st.sidebar.multiselect('Select Players', data['PLAYER'].unique())
war_filter = st.sidebar.slider('WAR', float(data['WAR'].min()), float(data['WAR'].max()), (float(data['WAR'].min()), float(data['WAR'].max())))
value_filter = st.sidebar.slider('Value', float(data['VALUE'].min()), float(data['VALUE'].max()), (float(data['VALUE'].min()), float(data['VALUE'].max())))
surplus_filter = st.sidebar.slider('Surplus Value', float(data['SURPLUS VALUE'].min()), float(data['SURPLUS VALUE'].max()), (float(data['SURPLUS VALUE'].min()), float(data['SURPLUS VALUE'].max())))

# Function to plot a line chart
def plot_line_chart(x, y, hue, data, title, player_filter):
    plt.figure(figsize=(10, 6))
    if player_filter:
        # If players are selected, grey out the non-selected players
        remaining_data = data[~data['PLAYER'].isin(player_filter)]
        sns.lineplot(x=x, y=y, hue=hue, data=remaining_data, marker='o', color='lightgrey', legend=False)
        filtered_data = data[data['PLAYER'].isin(player_filter)]
        sns.lineplot(x=x, y=y, hue=hue, data=filtered_data, marker='o')
    else:
        # If no players are selected, show all players in color
        sns.lineplot(x=x, y=y, hue=hue, data=data, marker='o')
    plt.title(title)
    st.pyplot(plt)

# Function to plot a scatter chart
def plot_scatter_chart(x, y, data, title, player_filter):
    plt.figure(figsize=(10, 6))
    if player_filter:
        # If players are selected, grey out the non-selected players
        remaining_data = data[~data['PLAYER'].isin(player_filter)]
        sns.scatterplot(x=x, y=y, data=remaining_data, s=100, color='lightgrey', legend=False)
        filtered_data = data[data['PLAYER'].isin(player_filter)]
        sns.scatterplot(x=x, y=y, data=filtered_data, s=100)
    else:
        # If no players are selected, show all players in color
        sns.scatterplot(x=x, y=y, data=data, s=100)
    plt.title(title)
    st.pyplot(plt)

# Displaying the charts with headers
st.header('Salary vs Age')
plot_line_chart('Age', 'SALARY', 'PLAYER', data, 'Salary vs Age', player_filter)

st.header('Salary vs WAR')
plot_line_chart('WAR', 'SALARY', 'PLAYER', data, 'Salary vs WAR', player_filter)

st.header('Salary vs Value')
plot_line_chart('VALUE', 'SALARY', 'PLAYER', data, 'Salary vs Value', player_filter)

st.header('Salary vs Surplus Value')
plot_scatter_chart('SURPLUS VALUE', 'SALARY', data, 'Salary vs Surplus Value', player_filter)
