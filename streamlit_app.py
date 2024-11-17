import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Data Preparation
# Load the dataset
dataTeam10 = pd.read_excel('merged_police_weather_data.xlsx', sheet_name='Sheet1')

# Handle missing values (dropping rows with missing key data)
dataTeam10.dropna(subset=['offensedescription', 'temp', 'precip'], inplace=True)

# Convert datetime column to proper datetime format
dataTeam10['datetime'] = pd.to_datetime(dataTeam10['datetime'])

# App Layout and Sections
st.title("Crime and Weather Analysis Dashboard")
st.sidebar.title("Navigation")
sectionTeam10 = st.sidebar.radio(
    "Go to",
    ["Introduction", "Data Exploration", "Insights", "Recommendations"]
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
    2. To Find patterns in crime frequency and severity in various conditions.
    3. To give actionable insights for law enforcement and city planners.
    """)

elif sectionTeam10 == "Data Exploration":
    # Data Exploration Section
    st.header("Data Exploration")

    # Univariate Analysis: Distribution of Crime Types
    st.subheader("Univariate Analysis: Crime Types")
    crime_countsTeam10 = dataTeam10['offensedescription'].value_counts()
    st.bar_chart(crime_countsTeam10.head(10))

    # Bivariate Analysis: Temperature vs. Crime Frequency
    st.subheader("Bivariate Analysis: Temperature vs. Crime Frequency")
    crime_tempTeam10 = dataTeam10.groupby('temp').size()
    fig, ax = plt.subplots()
    crime_tempTeam10.plot(ax=ax)
    plt.title("Crime Frequency at Different Temperatures")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Crime Frequency")
    st.pyplot(fig)

    # Multivariate Analysis: Temperature vs. Precipitation for Selected Crime Type
    st.subheader("Multivariate Analysis: Temperature vs. Precipitation")
    crime_filterTeam10 = st.sidebar.selectbox("Select Crime Type", dataTeam10['offensedescription'].unique())
    filtered_dataTeam10 = dataTeam10[dataTeam10['offensedescription'] == crime_filterTeam10]
    fig, ax = plt.subplots()
    sns.scatterplot(data=filtered_dataTeam10, x="temp", y="precip", ax=ax)
    plt.title(f"Temperature vs. Precipitation ({crime_filterTeam10})")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Precipitation (mm)")
    st.pyplot(fig)

elif sectionTeam10 == "Insights":
    # Insights Section
    st.header("Key Insights")
    st.write("""
    Based on the exploratory data analysis, the following insights were discovered:
    1. **Crimes occur more frequently at moderate temperatures**: The relationship indicates an increase in crime rates around 20-25°C.
    2. **Rainy days have fewer crimes**: Precipitation seems to act as a deterrent for certain types of crimes.
    3. **Crime types vary with weather conditions**: For example, thefts are more common during warmer days, while violent crimes appear to be evenly distributed across conditions.
    """)

elif sectionTeam10 == "Recommendations":
    # Recommendations Section
    st.header("Recommendations")
    st.write("""
    ### Suggested Actions:
    1. **Enhance law enforcement presence during moderate weather conditions**: Allocate more patrols on days with favorable weather to deter criminal activity.
    2. **Utilize weather forecasts for strategic planning**: Integrate weather data with crime prediction models to proactively deploy resources.
    3. **Community awareness campaigns**: Educate the public about crime trends under varying 
    """)
