import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import geopy
from geopy.geocoders import Nominatim
import time

st.title("Health data in Lebanon")
# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
data=pd.read_csv(r"C:\Users\Nour Abd El Ghani\Downloads\4a0321bc971cc2f793d3367fd0b55a34_20240905_102823.csv")
#data
if st.checkbox('Show data'):
    st.write("Dataset Overview:")
    st.dataframe(data)
    
st.subheader("COVID-19 Cases by Area")



# Assuming the dataset has columns 'refArea' and 'Nb of Covid-19 cases'
if 'refArea' in data.columns and 'Nb of Covid-19 cases' in data.columns:
    
    # Sidebar: Select Area
    areas = data['refArea'].unique()
    selected_areas = st.sidebar.multiselect("Select Areas:", areas, default=areas)

    # Sidebar: Toggle between raw data and percentage
    show_percentage = st.sidebar.checkbox("Show as percentage of total cases", value=False)

    # Filter the dataset based on selected areas
    filtered_data = data[data['refArea'].isin(selected_areas)]

    # Adjust the y-axis if showing percentages
    if show_percentage:
        total_cases = filtered_data['Nb of Covid-19 cases'].sum()
        filtered_data['Nb of Covid-19 cases'] = (filtered_data['Nb of Covid-19 cases'] / total_cases) * 100

    # Bar Chart: COVID-19 Cases by Area
    fig_bar = px.bar(filtered_data, x='refArea', y='Nb of Covid-19 cases',
                     title="COVID-19 Cases by Area",
                     labels={'refArea': 'Area', 'Nb of Covid-19 cases': 'Number of Cases' if not show_percentage else 'Percentage of Cases'},
                     template='plotly_dark')
    
    # Pie Chart: Distribution of Cases by Area
    fig_pie = px.pie(filtered_data, values='Nb of Covid-19 cases', names='refArea',
                     title="COVID-19 Case Distribution by Area",
                     template='plotly_dark')

    # Layout adjustments for bar chart and pie chart
    fig_bar.update_layout(transition_duration=500)
    fig_pie.update_traces(textinfo='percent+label' if show_percentage else 'label')

    # Display the Bar Chart
    st.plotly_chart(fig_bar)

    # Display the Pie Chart
    st.plotly_chart(fig_pie)

    # Additional Metric: Display total number of cases for selected areas
    total_cases_selected = filtered_data['Nb of Covid-19 cases'].sum() if not show_percentage else 100
    st.write(f"Total cases in selected areas: **{total_cases_selected:.2f}**")

else:
    st.error("Columns 'refArea' or 'Nb of Covid-19 cases' not found in the dataset.")
    


# Assuming `filtered_data` is the DataFrame used for the bar chart
if 'refArea' in data.columns and 'Nb of Covid-19 cases' in data.columns:
    

    
   
    # Bar Chart with Annotations
    fig_bar = px.bar(filtered_data, x='refArea', y='Nb of Covid-19 cases',
                     title="COVID-19 Cases by Area",
                     labels={'refArea': 'Area', 'Nb of Covid-19 cases': 'Number of Cases' if not show_percentage else 'Percentage of Cases'},
                     template='plotly_dark')
    
    # Adding annotations
    fig_bar.update_traces(texttemplate='%{y}', textposition='outside')

    # Add hover info
    fig_bar.update_traces(hoverinfo='x+y')
    
    # Display the Bar Chart
    st.plotly_chart(fig_bar)


# Pie Chart with Exploded Sections and Custom Colors
fig_pie = px.pie(filtered_data, values='Nb of Covid-19 cases', names='refArea',
                 title="COVID-19 Case Distribution by Area",
                 template='plotly_dark',
                 color_discrete_sequence=px.colors.qualitative.Set1)

# Explode specific sections (optional)
fig_pie.update_traces(pull=[0.1 if area in selected_areas else 0 for area in filtered_data['refArea']])

# Add hover info
fig_pie.update_traces(hoverinfo='label+percent+value')

# Display the Pie Chart
st.plotly_chart(fig_pie)
