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
    data['month'] = data['datetime'].dt.month
    return data

dataTeam10 = load_data()

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
    2. Find patterns in crime frequency and severity in various conditions.
    3. Provide actionable insights for law enforcement and city planners.
    """)

elif sectionTeam10 == "Data Exploration":
    st.header("Data Exploration")

    # Filters: Crime Type and Month
    st.sidebar.header("Filters")
    crime_filterTeam10 = st.sidebar.selectbox("Select Crime Type", dataTeam10['offensedescription'].unique())
    month_filterTeam10 = st.sidebar.selectbox(
        "Select Month",
        options={
            1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
            7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
        },
        format_func=lambda x: {
            1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
            7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
        }.get(x, "Unknown")
    )

    # Filter data
    filtered_dataTeam10 = dataTeam10[
        (dataTeam10['offensedescription'] == crime_filterTeam10) &
        (dataTeam10['month'] == month_filterTeam10)
    ]

    # Univariate Analysis: Crime Types
    st.subheader("Univariate Analysis: Crime Types")
    crime_countsTeam10 = dataTeam10['offensedescription'].value_counts()
    st.bar_chart(crime_countsTeam10.head(10))

    # Bivariate Analysis: Temperature vs. Crime Frequency
    st.subheader("Bivariate Analysis: Temperature vs. Crime Frequency")
    crime_tempTeam10 = filtered_dataTeam10.groupby('temp').size()
    fig, ax = plt.subplots()
    crime_tempTeam10.plot(ax=ax)
    plt.title(f"Crime Frequency at Different Temperatures ({crime_filterTeam10})")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Crime Frequency")
    st.pyplot(fig)

    # Multivariate Analysis: Temperature vs. Precipitation
    st.subheader("Multivariate Analysis: Temperature vs. Precipitation")
    fig, ax = plt.subplots()
    sns.scatterplot(data=filtered_dataTeam10, x="temp", y="precip", ax=ax)
    plt.title(f"Temperature vs. Precipitation ({crime_filterTeam10})")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Precipitation (mm)")
    st.pyplot(fig)

elif sectionTeam10 == "Insights":
    st.header("Key Insights")
    st.write("""
    1. **Crimes occur more frequently at moderate temperatures**: Increase around 20-25°C.
    2. **Rainy days have less crimes**: Precipitation acts as a deterrant.
    3. **Crime types changes with weather conditions**: E.g., thefts increase on warmer days.
    """)

elif sectionTeam10 == "Recommendations":
    st.header("Recommendations")
    st.write("""
    ### Suggested Actions:
    1. Focus patrols in high-crime areas during moderate weather conditions..
    2. Integrate weather forecasts for strategic planning.
    3. Use predictive models to allocate resources based on weather-crime patterns.
    4. Install smart surveillance systems in weather-prone crime hotspots.
    """)
