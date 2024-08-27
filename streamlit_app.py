import streamlit as st
import pandas as pd
import altair as alt

st.title('🎈 Data Visualization for Accidents')
st.write('Be safe!')
st.info('This is a visualization app.')

with st.expander('About this app'):
    st.markdown('This app helps you predict and visualize accident data.')
    st.info('Explore the dataset and gain insights about UK accidents.')

st.subheader("What's the reason for UK accidents? Let's explore!")

# Load data from a single CSV file
@st.cache_data
def load_data():
    df = pd.read_csv("data/summary.csv")
    
    # Check the data structure
    st.write("Data Preview:", df.head())
    st.write("Data Types:", df.dtypes)
    
    # Split data into separate DataFrames based on column presence
    accident_by_hour = df[df['Type'] == 'Hour']
    accident_by_period = df[df['Type'] == 'Period']
    road_surface_conditions = df[df['Type'] == 'Road_Surface']
    urban_rural = df[df['Type'] == 'Urban_Rural']
    
    return accident_by_hour, accident_by_period, road_surface_conditions, urban_rural

accident_by_hour, accident_by_period, road_surface_conditions, urban_rural = load_data()

# Ensure data is loaded correctly
if accident_by_hour.empty or accident_by_period.empty or road_surface_conditions.empty or urban_rural.empty:
    st.error("One or more datasets are empty. Please check your CSV file and data filtering.")

# Show hour-wise accident data
if not accident_by_hour.empty:
    st.subheader("Number of Accidents by Hour")
    hour_chart = alt.Chart(accident_by_hour).mark_bar().encode(
        x=alt.X('Hour:O', title='Hour'),
        y=alt.Y('Accidents:Q', title='Number of Accidents'),
        color='Hour:O'
    ).properties(height=400, width=600)
    st.altair_chart(hour_chart)
else:
    st.warning("No data available for accidents by hour.")

# Show day vs night accident data
if not accident_by_period.empty:
    st.subheader("Number of Accidents: Day vs. Night")
    period_chart = alt.Chart(accident_by_period).mark_bar().encode(
        x=alt.X('Period:N', title='Period'),
        y=alt.Y('Accidents:Q', title='Number of Accidents'),
        color='Period:N'
    ).properties(height=400, width=600)
    st.altair_chart(period_chart)
else:
    st.warning("No data available for accidents by period.")

# Show road surface conditions
if not road_surface_conditions.empty:
    st.subheader("Accidents by Road Surface Conditions")
    road_surface_chart = alt.Chart(road_surface_conditions).mark_bar().encode(
        x=alt.X('Road_Surface_Conditions:N', title='Road Surface Conditions', sort='-y'),
        y=alt.Y('Accidents:Q', title='Number of Accidents'),
        color='Road_Surface_Conditions:N'
    ).properties(height=400, width=600)
    st.altair_chart(road_surface_chart)
else:
    st.warning("No data available for road surface conditions.")

# Show accidents in urban vs. rural areas
if not urban_rural.empty:
    st.subheader("Accidents in Urban vs. Rural Areas")
    urban_rural_chart = alt.Chart(urban_rural).mark_arc().encode(
        theta=alt.Theta(field='Accidents', type='quantitative'),
        color=alt.Color(field='Urban_or_Rural_Area', type='nominal'),
        tooltip=['Urban_or_Rural_Area:N', 'Accidents:Q']
    ).properties(height=400, width=600)
    st.altair_chart(urban_rural_chart)
else:
    st.warning("No data available for urban vs. rural areas.")
