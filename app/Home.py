import streamlit as st # to raun >>> streamlit run app.py
import pandas as pd
import plotly.express as px
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from streamlit_option_menu import option_menu



# Title page
st.set_page_config(
    page_title= 'Dashboard',
    page_icon= ':bar_chart:',
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
    icons=['house', 'globe', 'people', 'credit-card'], 
    default_index=0,  # 0 ist "Home"
    orientation="horizontal",
    styles={
        "container": {"border-radius": "0px", "background-color": "transparent", "padding": "0px !important"},
        "nav-link": {"color": "#39FF14", "font-family": "monospace", "font-size": "14px"},
        "nav-link-selected": {"background-color": "#3f6e2e", "color": "#39FF14"}
    }
)

if selected == "Continents":
    st.switch_page("pages/Continents.py")
# ... (Home muss hier nicht geswitcht werden)

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



products = st.sidebar.multiselect('Products: ',
                                  options= df["category"].unique(),
                                  default= df["category"].unique())


# Deine bestehende Query (jetzt mit den Checkbox-Werten)
filtered_df = df.query(
    'year in @years and '
    'unit_price_usd >= @prices[0] and '
    'unit_price_usd <= @prices[1] and '
    'category in @products and '
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
    st.write("## Best-selling category products")
    st.write("Apple Global Product Sales")



# Best-selling product
fig_1= px.histogram(filtered_df, x= "category" ,color='category',
              y='units_sold' , title="Best-selling category products:<br>" \
              "AirPods, Accessories, Apple Watch, Mac, iPhone, iPad",
        )

st.plotly_chart(fig_1,  use_container_width=True)


# Die Kategorien 1, die du anzeigen möchtest
category_list = ['AirPods', 'Accessories', 'Apple Watch']

# 6 Spalten erstellen
cols = st.columns(3)

# In einer Schleife berechnen und anzeigen
for col, cat_name in zip(cols, category_list):
    # Berechnung nur auf dem gefilterten DF
    value = int(filtered_df[filtered_df["category"] == cat_name]["units_sold"].sum())
    
    # Anzeige in der jeweiligen Spalte
    col.write(f'<h3> {cat_name}: <br>{value:,}</h3>', unsafe_allow_html=True)

#-------------- 2 ------------------------------
# Die Kategorien 2, die du anzeigen möchtest
category_list_2 = ['Mac', 'iPhone', 'iPad']

# 6 Spalten erstellen
cols_2 = st.columns(3)

# In einer Schleife berechnen und anzeigen
for col_2, cat_name in zip(cols_2, category_list_2):
    # Berechnung nur auf dem gefilterten DF
    value = int(filtered_df[filtered_df["category"] == cat_name]["units_sold"].sum())
    
    # Anzeige in der jeweiligen Spalte
    col_2.write(f'<h3> {cat_name}: <br>{value:,}</h3>', unsafe_allow_html=True)

# Categories
# cat_1, cat_2, cat_3, cat_4, cat_5, cat_6  = st.columns(6)

# #All_category = int(filtered_df['category']["units_sold"].sum())
# AirPods = int(filtered_df[ filtered_df["category"] == 'AirPods']["units_sold"].sum())
# Accessories = int(filtered_df [ filtered_df ["category"] == 'Accessories']["units_sold"].sum())
# Apple_Watch = int(filtered_df [ filtered_df ["category"] == 'Apple Watch']["units_sold"].sum())
# Mac = int(filtered_df [ filtered_df ["category"] == 'Mac']["units_sold"].sum())
# iPhone = int(filtered_df [ filtered_df ["category"] == 'iPhone']["units_sold"].sum())
# iPad = int(filtered_df [ filtered_df ["category"] == 'iPad']["units_sold"].sum())

# cat_1.write(f'<H6> AirPods: <br>{AirPods}</h6>', unsafe_allow_html = True)
# cat_2.write(f'<H6> Accessories: <br>{Accessories}</h6>', unsafe_allow_html = True)
# cat_3.write(f'<H6> Apple Watch: <br>{Apple_Watch}</h6>', unsafe_allow_html = True)
# cat_4.write(f'<H6> Mac: <br>{Mac}</h6>', unsafe_allow_html = True)
# cat_5.write(f'<H6> iPhone: <br>{iPhone}</h6>', unsafe_allow_html = True)
# cat_6.write(f'<H6> iPad: <br>{iPad}</h6>', unsafe_allow_html = True)

# Graphic most sold products

fig_1 = px.histogram(filtered_df, x= "product_name" ,color='product_name', 
             y='unit_price_usd' , title="Most sold products:"
        )

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


#Ich habe kpi_1.write durch st.metric ersetzt. 
# Das sieht in Streamlit-Dashboards professioneller aus 
# und benötigt kein unsafe_allow_html.
# kpi_1.metric("Total 2022", f"{total_2022:,}")
# kpi_2.metric("Total 2023", f"{total_2023:,}")
# kpi_3.metric("Total 2024", f"{total_2024:,}")
# kpi_4.metric("Total All Years", f"{total_all:,}")


# # Button
# if st.button("To the continent data"):
#     # Hier könnte Code zum Speichern stehen...
#     st.switch_page("pages/Continents.py")

# # Viel Inhalt...
# for i in range(50):
#     st.write(f"Inhalt Zeile {i}")

# 2. Button zum Navigationsmenü
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