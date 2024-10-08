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

# Load data from the provided URL
@st.cache_data
def load_data():
    try:
        url = "https://raw.githubusercontent.com/akarsh323/mydplearning/master/data/df_reduced.csv"
        df = pd.read_csv(url)
        
        # Display data preview and unique 'Type' values for debugging
        st.write("Data Preview:", df.head())
        st.write("Unique 'Type' Values:", df['Type'].unique())
        
        # Ensure required columns exist
        required_columns = ['Type', 'Hour', 'Period', 'Road_Surface_Conditions', 'Urban_or_Rural_Area', 'Accidents']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"Missing columns: {', '.join(missing_columns)}. Please check your CSV file.")
            return None, None, None, None
        
        # Split data into separate DataFrames based on column presence
        accident_by_hour = df[df['Type'].str.strip() == 'Hour']
        accident_by_period = df[df['Type'].str.strip() == 'Period']
        road_surface_conditions = df[df['Type'].str.strip() == 'Road_Surface']
        urban_rural = df[df['Type'].str.strip() == 'Urban_Rural']
        
        return accident_by_hour, accident_by_period, road_surface_conditions, urban_rural
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None, None

accident_by_hour, accident_by_period, road_surface_conditions, urban_rural = load_data()

if accident_by_hour is None:
    st.stop()  # Stop the app if data isn't loaded correctly

# Show hour-wise accident data
if not accident_by_hour.empty:
    st.subheader("Number of Accidents by Hour")
    st.write(accident_by_hour.head())  # Display the data for debugging
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
    st.write(accident_by_period.head())  # Display the data for debugging
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
    st.write(road_surface_conditions.head())  # Display the data for debugging
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
    st.write(urban_rural.head())  # Display the data for debugging
    urban_rural_chart = alt.Chart(urban_rural).mark_arc().encode(
        theta=alt.Theta(field='Accidents', type='quantitative'),
        color=alt.Color(field='Urban_or_Rural_Area', type='nominal'),
        tooltip=['Urban_or_Rural_Area:N', 'Accidents:Q']
    ).properties(height=400, width=600)
    st.altair_chart(urban_rural_chart)
else:
    st.warning("No data available for urban vs. rural areas.")
