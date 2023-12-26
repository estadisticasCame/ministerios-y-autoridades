import pandas as pd
import streamlit as st
import openpyxl

columna1, columna2 = st.columns(2)
with columna1:
    st.title("Tablero de control")
    st.header("Ministerios y Autoridades")
    
with columna2:
    st.image("imgs/escudo.png")

# Realizamos la carga de datos y lo guardamos en cache de streamlit
@st.cache_data
def cargar_datos_excel():
    # Ingestamos el archivo de excel del meppi
    excel = pd.read_excel("Datos/Ministerios y autoridades.xlsx", sheet_name=None, engine = "openpyxl")
    # Almacenamos las hojas en un diccionario de Pandas
    hojas = {}
    for nombre_hoja, datos_hoja in excel.items():
        hojas[nombre_hoja] = datos_hoja

    return hojas

hojas = cargar_datos_excel()

st.write("---")

columna3, columna4 = st.columns(2)
with columna3:
    st.button("GOBIERNO NACIONAL")
    
    
with columna4:
    st.button("GOBIERNOS PROVINCIALES")
