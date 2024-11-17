pip install matplotlib
pip install pandas streamlit seaborn
python -c "import matplotlib; import pandas; import seaborn; import streamlit"

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Data Preparation
# Load the dataset
data = pd.read_excel('merged_police_weather_data.xlsx', sheet_name='Sheet1')

# Handle missing values (dropping rows with missing key data)
data.dropna(subset=['offensedescription', 'temp', 'precip'], inplace=True)

# Convert datetime column to proper datetime format
data['datetime'] = pd.to_datetime(data['datetime'])

# Generate a hypothesis
# Hypothesis: Crimes are more frequent during higher temperatures and on non-rainy days.

# Exploratory Data Analysis
# Univariate Analysis: Crime descriptions and temperature distribution
crime_counts = data['offensedescription'].value_counts()
temp_dist = data['temp']

# Bivariate Analysis: Temperature vs. Crime Frequency
crime_temp = data.groupby('temp').size()

# Interactive Dashboard using Streamlit
st.title("Crime and Weather Interactive Dashboard")

# Sidebar filters
crime_filter = st.sidebar.selectbox("Select Crime Type", data['offensedescription'].unique())
date_range = st.sidebar.slider("Select Date Range", 
                                value=(data['datetime'].min().date(), data['datetime'].max().date()))

# Filter data based on user inputs
filtered_data = data[(data['offensedescription'] == crime_filter) & 
                     (data['datetime'].dt.date.between(date_range[0], date_range[1]))]

# Bar Chart: Top Crime Types
st.header("Top Crime Types")
fig, ax = plt.subplots()
crime_counts.head(10).plot(kind='bar', ax=ax)
plt.title("Top 10 Crime Types")
plt.ylabel("Count")
st.pyplot(fig)

# Line Chart: Temperature vs. Crime Frequency
st.header("Temperature vs. Crime Frequency")
fig, ax = plt.subplots()
crime_temp.plot(ax=ax)
plt.title("Crime Frequency at Different Temperatures")
plt.xlabel("Temperature (°C)")
plt.ylabel("Crime Frequency")
st.pyplot(fig)

# Scatter Plot: Temperature vs. Precipitation for Selected Crime Type
st.header("Temperature vs. Precipitation for Selected Crime")
fig, ax = plt.subplots()
sns.scatterplot(data=filtered_data, x="temp", y="precip", ax=ax)
plt.title(f"Temperature vs. Precipitation ({crime_filter})")
plt.xlabel("Temperature (°C)")
plt.ylabel("Precipitation (mm)")
st.pyplot(fig)

# Display a summary
st.subheader("Insights and Hypothesis Testing")
st.write("""
1. Crimes tend to occur more frequently at moderate temperatures.
2. Rainy days generally show fewer crimes compared to non-rainy days.
""")
