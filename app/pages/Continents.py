import streamlit as st # to raun >>> streamlit run app.py
import pandas as pd
import plotly.express as px
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from streamlit_option_menu import option_menu

# Title page
st.set_page_config(
    page_title= 'Dashboard',
    page_icon= ':earth_africa:',
    layout="wide"
)

df = pd.read_csv('data/cleaned_data/cleaned_data.csv')


# 1. Anker direkt beim Navigationsmenü setzen ( Scroll up)
st.markdown("<div id='nav-menu'></div>", unsafe_allow_html=True)


# 1. CSS: Erzwingt 0px oben und 50px unten
st.markdown("""
    <style>
    /* Entfernt den Standard-Abstand von Streamlit oben komplett */
    .block-container {
        padding-top: 2.5rem !important; 
    }

    /* Dein Menü-Block: 0px von oben, 50px nach unten */
    .stHorizontalBlock  {
        
        margin-top: 50px; /* Der gewünschte Abstand nach unten */
        
    }
    </style>
    """, unsafe_allow_html=True)


# Navigator Menü
# "orientation='horizontal'" macht es zu einer Leiste oben
selected = option_menu(
    None, ["Category", "Continents", "Age_Group", "Payment"], 
    icons=['house', 'globe','people', 'credit-card'], 
    default_index=1,  # 0 ist "Home"
    orientation="horizontal",
    styles={
        "container": {"border-radius": "0px", "background-color": "transparent", "padding": "0px !important"},
        "nav-link": {"color": "#39FF14", "font-family": "monospace", "font-size": "14px"},
        "nav-link-selected": {"background-color": "#3f6e2e", "color": "#39FF14"}
    }
)

if selected == "Category":
    st.switch_page("Home.py")
# ... (Continents muss hier nicht geswitcht werden)


elif selected == "Age_Group":
    st.switch_page("pages/Customer_age.py")

elif selected == "Payment":
    st.switch_page("pages/Payment.py")


# Slider als Range (Bereich) definieren
prices = st.sidebar.slider('Price :',
                        min_value=float(df["unit_price_usd"].min()),
                        max_value=float(df["unit_price_usd"].max()),
                        value=(float(df["unit_price_usd"].min()), float(df["unit_price_usd"].max())))

# Alle verfügbaren Gruppen
age_groups = ['18–24', '25–34', '35–44', '45–54', '55+']
selected_ages = []

st.sidebar.write("### Select Age Groups:")

# Für jede Gruppe eine Checkbox erstellen
for age in age_groups:
    if st.sidebar.checkbox(age, value=True): # value=True bedeutet standardmässig "An"
        selected_ages.append(age)

# WICHTIG: Falls keine Checkbox gewählt ist, nehmen wir alle (oder zeigen leeren DF)
if not selected_ages:
    st.sidebar.warning("Please select at least one age group!")

    
years = st.sidebar.multiselect('Year :',
                               options=df["year"].unique(),
                               default= df["year"].unique())

regions = st.sidebar.multiselect('Region :',
                               options=df["region"].unique(),
                               default= df["region"].unique())



# Query anpassen (sucht jetzt zwischen zwei Werten)
#filtered_df = df.query('year in @years and region in @regions and unit_price_usd >= @prices[0] and unit_price_usd <= @prices[1]')
# Deine bestehende Query (jetzt mit den Checkbox-Werten)
filtered_df = df.query(
    'year in @years and '
    'unit_price_usd >= @prices[0] and '
    'unit_price_usd <= @prices[1] and '
    'region in @regions and '
    'customer_age_group in @selected_ages'
)


# Main Title
# st.markdown (
#     "<h1 style='text-align: left; color:white; font-family: arial; font_size: 35px'>Apple Global Product Sales</h1>",
#     unsafe_allow_html= True 
# )


# Logo image and Text
col1, col2 = st.columns([1,5])
with col1:
    st.image("app/pages/new_apple_logo.png", width=70)

with col2 :
    st.write("## Continent sold by amount")
    st.write("Apple Global Product Sales")


# 1. Continent Sold by amount" 

fig = px.histogram(filtered_df, x= "region" ,color='region',
                    y='unit_price_usd' ,  title="Continent sold by amount" 
        )

st.plotly_chart(fig,  use_container_width=True)



# KPi's 2
South_America = round(filtered_df[ filtered_df["region"]== 'South America']["unit_price_usd"].sum())
Oceania = round(filtered_df[ filtered_df["region"]== 'Oceania']["unit_price_usd"].sum())
Europe = round(filtered_df[ filtered_df["region"]== 'Europe']["unit_price_usd"].sum())
Asia = round(filtered_df[ filtered_df["region"]== 'Asia']["unit_price_usd"].sum())
North_America = round(filtered_df[ filtered_df["region"]== 'North America']["unit_price_usd"].sum())
Africa = round(filtered_df[ filtered_df["region"]== 'Africa']["unit_price_usd"].sum())
Europe_Asia = round(filtered_df[ filtered_df["region"]== 'Europe/Asia']["unit_price_usd"].sum())
Middle_East = round(filtered_df[ filtered_df["region"]== 'Middle East']["unit_price_usd"].sum())


# Continents: 1
cont_1, cont_2, cont_3, cont_4 = st.columns(4)


cont_1.write( f'<h3> S. America: <br>{South_America}</h3>',
            unsafe_allow_html= True,)
cont_2.write( f'<h3>Oceania: <br>{Oceania}</h3>',
            unsafe_allow_html= True,)

cont_3.write( f'<h3>Europe: <br>{Europe}</h3>',
            unsafe_allow_html= True,)

cont_4.write( f'<h3>Asia: <br>{Asia}</h3>',
            unsafe_allow_html= True,)

# Continents: 2
cont_5, cont_6, cont_7, cont_8 = st.columns(4)

cont_5.write( f'<h3>N. America: <br>{North_America}</h3>',
            unsafe_allow_html= True,)
cont_6.write( f'<h3>Africa: <br>{Africa}</h3>',
            unsafe_allow_html= True,)
cont_7.write( f'<h3>Middle East: <br>{Middle_East}</h3>',
            unsafe_allow_html= True,)

cont_8.write( f'<h3>Middle East: <br>{Europe_Asia}</h3>',
            unsafe_allow_html= True,)


# Graphics 2
fig_1 = px.histogram(filtered_df, x= "country" ,color='country',
                      y='unit_price_usd' , title= "Solid Product by Countries")

st.plotly_chart(fig_1, use_container_width= True)




# Graphics 3
fig_1 = px.histogram(filtered_df, x= "country" ,color='customer_segment', facet_col= 'customer_segment', 
                      y='unit_price_usd' , title= "Solid Product by Countries")

st.plotly_chart(fig_1, use_container_width= True)

# KPI's


# KPIs berechnen basierend auf dem gefilterten DF
total_2022 = len(filtered_df[filtered_df['year'] == 2022])
total_2023 = len(filtered_df[filtered_df['year'] == 2023])
total_2024 = len(filtered_df[filtered_df['year'] == 2024])
total_all = len(filtered_df)

st.markdown("""
    <style>
    /* Desktop: 4 Spalten nebeneinander (Standard) */
    /* Mobile: Erzwinge 2 Spalten pro Reihe bei Bildschirmen unter 768px */
    @media (max-width: 768px) {
        [data-testid="column"] {
            width: 48% !important; /* Fast die Hälfte */
            flex: 1 1 45% !important;
            min-width: 45% !important;
            margin-bottom: 10px;
        }
        
        /* Verhindert das Übereinanderstapeln */
        [data-testid="stHorizontalBlock"] {
            flex-direction: row !important;
            flex-wrap: wrap !important;
        }
    }
    
    /* Optional: Text im KPI zentrieren */
    h3 { text-align: center; font-size: 1.2rem !important; }
    </style>
    """, unsafe_allow_html=True)

# Anzeige in den Spalten
kpi_1, kpi_2, kpi_3, kpi_4 = st.columns(4)

kpi_1.write( f'<h2> Total 2022:<br> {total_2022:,}</h2>',
            unsafe_allow_html= True,)
kpi_2.write( f'<h2> Total 2023: <br> {total_2023:,}</h2>',
            unsafe_allow_html= True)

kpi_3.write( f'<h2> Total 2022: <br> {total_2024:,}</h2>',
            unsafe_allow_html= True)
kpi_4.write( f'<h2> All Years:<br> {total_all:,}</h2>',
            unsafe_allow_html= True)

st.markdown("""
    <a href='#nav-menu' style='text-decoration:none;'>
        <button style='
            background-color: #39FF14; 
            color: white; 
            border: none; 
            padding: 10px 20px; 
            border-radius: 5px;
            cursor: pointer;'>
            Scroll up ↑
        </button>
    </a>
    """, unsafe_allow_html=True)