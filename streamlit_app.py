import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load data with caching
@st.cache_data
def load_data():
    data = pd.read_excel('merged_police_weather_data.xlsx', sheet_name='Sheet1')
    data.dropna(subset=['offensedescription', 'temp', 'precip'], inplace=True)
    data['datetime'] = pd.to_datetime(data['datetime'])
    return data

dataTeam10 = load_data()

# App Layout and Sections
st.title("Crime and Weather Analysis Dashboard")
st.sidebar.title("Navigation")
sectionTeam10 = st.sidebar.radio(
    "Go to",
    ["Introduction", "EDA", "Interactive Dashboard", "Insights", "Recommendations"]
)

if sectionTeam10 == "Introduction":
    # Introduction Section
    st.header("Introduction")
    st.write("""
    ### Problem Statement:
    Understanding the relationship between weather conditions and crime patterns 
    in Dallas to gain insights for crime prevention and policy-making.

    ### Objectives:
    1. Explore how weather conditions (e.g., temperature, precipitation) influence crime rates.
    2. Identify patterns in crime frequency and severity across different weather conditions.
    3. Provide actionable insights for law enforcement and city planners.
    """)

elif sectionTeam10 == "EDA":
    # EDA Section
    st.header("Exploratory Data Analysis (EDA)")

    # Univariate Analysis: Histograms or Box Plots
    st.subheader("Univariate Analysis")
    st.write("Distribution of Temperature")
    fig, ax = plt.subplots()
    sns.histplot(dataTeam10['temp'], kde=True, ax=ax, bins=20)
    plt.title("Distribution of Temperature")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Frequency")
    st.pyplot(fig)

    st.write("Box Plot of Precipitation")
    fig, ax = plt.subplots()
    sns.boxplot(x=dataTeam10['precip'], ax=ax)
    plt.title("Box Plot of Precipitation")
    st.pyplot(fig)

    # Bivariate Analysis: Scatter Plot
    st.subheader("Bivariate Analysis")
    st.write("Temperature vs. Crime Frequency")
    crime_tempTeam10 = dataTeam10.groupby('temp').size()
    fig, ax = plt.subplots()
    crime_tempTeam10.plot(ax=ax)
    plt.title("Crime Frequency at Different Temperatures")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Crime Frequency")
    st.pyplot(fig)

    # Multivariate Analysis: Correlation Heatmap
    st.subheader("Multivariate Analysis")
    st.write("Correlation Heatmap")
    numerical_cols = ['temp', 'precip', 'humidity', 'windspeed']
    correlation = dataTeam10[numerical_cols].corr()
    fig, ax = plt.subplots()
    sns.heatmap(correlation, annot=True, cmap="coolwarm", ax=ax)
    plt.title("Correlation Heatmap")
    st.pyplot(fig)

elif sectionTeam10 == "Interactive Dashboard":
    # Interactive Dashboard Section
    st.header("Interactive Dashboard")

    # Filter: Crime Type
    st.sidebar.header("Interactive Filter")
    crime_filterTeam10 = st.sidebar.selectbox("Select Crime Type", dataTeam10['offensedescription'].unique())
    filtered_dataTeam10 = dataTeam10[dataTeam10['offensedescription'] == crime_filterTeam10]

    # Visualization 1: Crime Types Distribution (with filter)
    st.subheader("Visualization 1: Crime Types Distribution")
    st.write("Distribution of the selected crime type.")
    
    # Filtered data for the selected crime type
    filtered_countsTeam10 = dataTeam10[dataTeam10['offensedescription'] == crime_filterTeam10]['offensedescription'].value_counts()
    
    # Horizontal Bar Chart
    fig, ax = plt.subplots(figsize=(8, 4))
    filtered_countsTeam10.plot(kind='barh', ax=ax, color='skyblue')
    plt.title(f"Distribution of '{crime_filterTeam10}'")
    plt.xlabel("Frequency")
    plt.ylabel("Crime Type")
    plt.gca().invert_yaxis()  # Reverse the order for better readability
    st.pyplot(fig)
    


    # Visualization 2: Scatter Plot for Selected Crime Type
    st.subheader("Visualization 2: Temperature vs. Precipitation")
    fig, ax = plt.subplots()
    sns.scatterplot(data=filtered_dataTeam10, x="temp", y="precip", ax=ax)
    plt.title(f"Temperature vs. Precipitation ({crime_filterTeam10})")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Precipitation (mm)")
    st.pyplot(fig)

    # Visualization 3: Line Chart of Crime Frequency by Temperature
    st.subheader("Visualization 3: Temperature vs. Crime Frequency")
    crime_tempTeam10 = filtered_dataTeam10.groupby('temp').size()
    fig, ax = plt.subplots()
    crime_tempTeam10.plot(ax=ax)
    plt.title(f"Crime Frequency at Different Temperatures ({crime_filterTeam10})")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Crime Frequency")
    st.pyplot(fig)

elif sectionTeam10 == "Insights":
    st.header("Key Insights")
    st.write("""
    1. **Crimes occur more frequently at moderate temperatures**: Increase around 20-25°C.
    2. **Rainy days have fewer crimes**: Precipitation acts as a deterrent.
    3. **Crime types vary with weather conditions**: E.g., thefts increase on warmer days.
    """)

elif sectionTeam10 == "Recommendations":
    st.header("Recommendations")
    st.write("""
    ### Suggested Actions:
    1. Focus patrols in high-crime areas during moderate weather conditions.
    2. Use predictive models to allocate resources based on weather-crime patterns.
    3. Install smart surveillance systems in weather-prone crime hotspots.
    4. Educate the public with alerts and seasonal safety campaigns.
    """)
