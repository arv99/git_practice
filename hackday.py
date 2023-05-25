import streamlit as st
from PIL import Image
import altair as alt 
from requests_html import HTMLSession
import requests
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
from pyscbwrapper import SCB
import pyarrow
import re 




st.title(':technologist::fish:')

logo = Image.open("C:/Users/ahos/svg.png")
logo2 = Image.open("C:/Users/ahos/streamlit_svg.png")
logo3 = Image.open("C:/Users/ahos/gpt_svg.png")

col1, col2, col3 = st.columns(3)  # Create three columns

with col1:
    st.image(logo, width=250)

with col2:
    st.image(logo2, width=250)

with col3:
    st.image(logo3, width=100)    

st.markdown(
    """
    <h2 style="text-align: left; color: orange;">Hackday maj 2023</h2>
    """,
    unsafe_allow_html=True
)

st.markdown(
  f"<br><br><br><br>",
  unsafe_allow_html=True, #This allows you to use html code!
    )


# hitta rätt data i trädet
scb = SCB('sv', 'BE', 'BE0101')
scb.go_down('BE0101', 'BE0101C')
scb.go_down('BefArealTathetKon')

regioner = scb.get_variables()['region']
r = re.compile(r'.* län')
lan = list(filter(r.match, regioner))

scb.set_query(region=lan,
              tabellinnehåll=["Invånare per kvadratkilometer"])

scb_data = scb.get_data()

scb_uttag = scb_data['data']

koder = scb.get_query()['query'][0]['selection']['values']

landic = {}
for i in range(len(koder)):
  landic[koder[i]] = lan[i]


landata = {}

for kod in landic:
    landata[landic[kod]] = {}
    for i in range(len(scb_uttag)):
        if scb_uttag[i]['key'][0] == kod:
            landata[landic[kod]][scb_uttag[i]['key'][1]] = float(scb_uttag[i]['values'][0])

df = pd.DataFrame(landata)
df_long = df.reset_index().melt('index', var_name='County', value_name='Population')

# Define the default counties to display
default_counties = ["Stockholms län", "Västra Götalands län", "Skåne län"]

# Filter the dataframe to include only the default counties
filtered_df = df_long[df_long['County'].isin(default_counties)]


# Create a list of all available counties
all_counties = df_long['County'].unique()

# Initialize a list to store the selected counties
selected_counties = []

# Display checkboxes for each county in the sidebar
for county in all_counties:
    selected = st.sidebar.checkbox(county, value=(county in default_counties))
    if selected:
        selected_counties.append(county)

# Filter the dataframe based on the selected counties
filtered_df = df_long[df_long['County'].isin(selected_counties)]

# Create the chart
chart = alt.Chart(filtered_df).mark_line(strokeWidth=4).encode(
    x=alt.X('index', title='År'),  # Custom x-axis label
    y=alt.Y('Population', title='Invånare per kvadratkilometer'),  # Custom y-axis label
    color=alt.Color('County', title='')  # Add color encoding based on County
).properties(
    width=800,
    height=400
)

dots = chart.mark_circle(size=100).encode(
    tooltip=['index', 'Population']  # Display index and population values on hover
)

final_chart = chart + dots

# Display the chart
st.altair_chart(final_chart)




# Example of how to use markdown:
url_link = 'https://www.sbab.se/'
st.markdown(
  f"<div style='text-align: center;'>Steg-för-steg guide för hur man skapar en enkel streamlit <a href='{url_link}'>rapport</a>.</div><br>",
  unsafe_allow_html=True, #This allows you to use html code!
    )





     

