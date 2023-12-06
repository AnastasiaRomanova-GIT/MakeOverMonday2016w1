# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 11:20:46 2023

@author: aorra
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
@st.cache
def load_data():
    data = pd.read_excel('DataSet.xlsx')
    # Clean and preprocess the data as needed
    data = data.dropna(subset=['SALARY', 'WAR', 'VALUE', 'SURPLUS VALUE', 'Age'])  # Dropping rows with missing essential data
    data['SALARY'] = pd.to_numeric(data['SALARY'], errors='coerce')
    return data

data = load_data()

# Streamlit layout
st.title('Is there a pattern in player\'s salaries?')

# Filters
player_filter = st.sidebar.multiselect('Select Players', data['PLAYER'].unique())
war_filter = st.sidebar.slider('WAR', float(data['WAR'].min()), float(data['WAR'].max()), (float(data['WAR'].min()), float(data['WAR'].max())))
value_filter = st.sidebar.slider('Value', float(data['VALUE'].min()), float(data['VALUE'].max()), (float(data['VALUE'].min()), float(data['VALUE'].max())))
surplus_filter = st.sidebar.slider('Surplus Value', float(data['SURPLUS VALUE'].min()), float(data['SURPLUS VALUE'].max()), (float(data['SURPLUS VALUE'].min()), float(data['SURPLUS VALUE'].max())))

# Filtering data
filtered_data = data[data['PLAYER'].isin(player_filter) & data['WAR'].between(*war_filter) & data['VALUE'].between(*value_filter) & data['SURPLUS VALUE'].between(*surplus_filter)]

# Charts
def plot_line_chart(x, y, hue, data, title):
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=x, y=y, hue=hue, data=data, marker='o')
    plt.title(title)
    st.pyplot(plt)

def plot_scatter_chart(x, y, data, title):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=x, y=y, data=data, s=100)  # larger dot size
    plt.title(title)
    st.pyplot(plt)

# Salary vs Age
st.header('Salary vs Age')
plot_line_chart('Age', 'SALARY', 'PLAYER', filtered_data, 'Salary vs Age')

# Salary vs WAR
st.header('Salary vs WAR')
plot_line_chart('WAR', 'SALARY', 'PLAYER', filtered_data, 'Salary vs WAR')

# Salary vs Value
st.header('Salary vs Value')
plot_line_chart('VALUE', 'SALARY', 'PLAYER', filtered_data, 'Salary vs Value')

# Salary vs Surplus Value
st.header('Salary vs Surplus Value')
plot_scatter_chart('SURPLUS VALUE', 'SALARY', filtered_data, 'Salary vs Surplus Value')
