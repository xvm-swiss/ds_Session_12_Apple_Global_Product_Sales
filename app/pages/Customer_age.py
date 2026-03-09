import streamlit as st # to raun >>> streamlit run app.py
import pandas as pd
import plotly.express as px
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from streamlit_option_menu import option_menu

# Title page
st.set_page_config(
    page_title= 'Dashboard',
    page_icon= ':family_man_woman_girl_boy:',
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


# Navigator
# "orientation='horizontal'" macht es zu einer Leiste oben
selected = option_menu(
    None, ["Category", "Continents", "Age_Group", "Payment"], 
    icons=['house', 'globe','people', 'credit-card'], 
    default_index=2,  # 0 ist "Home"
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

elif selected == "Payment":
    st.switch_page("pages/Payment.py")

if selected == "Continents":
    st.switch_page("pages/Continents.py")
# ... (Home muss hier nicht geswitcht werden)



# Slider als Range (Bereich) definieren
prices = st.sidebar.slider('Price :',
                        min_value=float(df["unit_price_usd"].min()),
                        max_value=float(df["unit_price_usd"].max()),
                        value=(float(df["unit_price_usd"].min()), float(df["unit_price_usd"].max())))

years = st.sidebar.multiselect('Year :',
                               options=df["year"].unique(),
                               default= df["year"].unique())



ages = st.sidebar.multiselect('Products: ',
                                  options= df["customer_age_group"].unique(),
                                  default= df["customer_age_group"].unique())


# Query anpassen (sucht jetzt zwischen zwei Werten)
filtered_df = df.query('year in @years and unit_price_usd >= @prices[0] and unit_price_usd <= @prices[1] and customer_age_group in @ages')


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
    st.write("## Customer age group")
    st.write("Apple Global Product Sales")



# Customer age group
fig_1= px.histogram(filtered_df, x= "customer_age_group" , color='customer_age_group',facet_col= 'category'  ,
            y='unit_price_usd', title= "Customer age group"
        )

st.plotly_chart(fig_1,  use_container_width=True)


# Die Payment Method, die du anzeigen möchtest
payment_list = ['18–24', '25–34', '35–44', '45–54', '55+']

# 6 Spalten erstellen
cols = st.columns(5)

# In einer Schleife berechnen und anzeigen
for col, cat_name in zip(cols, payment_list):
    # Berechnung nur auf dem gefilterten DF
    value = int(filtered_df[filtered_df["customer_age_group"] == cat_name]["unit_price_usd"].sum())
    
    # Anzeige in der jeweiligen Spalte
    col.write(f'<h4> {cat_name}: <br>{value:,}</h4>', unsafe_allow_html=True)


# Customer age group
fig_2= px.histogram(filtered_df, x= "customer_age_group" , color='payment_method',facet_col= 'payment_method'  ,
             title= "Customer age group"
        )

st.plotly_chart(fig_2,  use_container_width=True)

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

# Graphic most sold products

# fig_1 = px.histogram(filtered_df, x= "product_name" ,color='product_name', 
#              y='unit_price_usd' , title="Most sold products:"
#         )

# st.plotly_chart(fig_1, use_container_width= True)

# # Button
# if st.button("To the continent data"):
#     # Hier könnte Code zum Speichern stehen...
#     st.switch_page("pages/Continents.py")