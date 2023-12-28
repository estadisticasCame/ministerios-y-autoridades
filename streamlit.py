# Importamos las librerias a utilizar
import datetime
import pytz
import time
import pandas as pd
from github import Github
import io
import github
import pandas as pd
import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageOps
from io import BytesIO

def cargar_y_redimensionar_imagen_desde_url(url):
    response = requests.get(url)
    imagen = Image.open(BytesIO(response.content))
    return imagen
    
columna1, columna2 = st.columns([2,1])
with columna1:
    st.title("Tablero de control")
    st.header("Ministerios y Autoridades")
    
with columna2:
    st.image("imgs/escudo.png", width=150)
    


# Realizamos la carga de datos y lo guardamos en cache de streamlit
@st.cache_data
def cargar_datos_excel():
    # ACCEDEMOS A LOS DATOS EN TIEMPO REAL
    github_token = st.secrets["TOKEN"] 
    repo_name = st.secrets["REPO"]
    file_path = st.secrets["ARCHIVO"]   
        
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    contents = repo.get_contents(file_path)
    # Create a file-like object from the decoded content
    content_bytes = contents.decoded_content
    content_file = io.BytesIO(content_bytes)
    # Ingestamos el archivo de excel del meppi
    excel = pd.read_excel(content_file, sheet_name=None)
    # Almacenamos las hojas en un diccionario de Pandas
    hojas = {}
    nombre_hojas = []
    for nombre_hoja, datos_hoja in excel.items():
        hojas[nombre_hoja] = datos_hoja
        nombre_hojas.append(nombre_hoja)
        try:
            hojas[nombre_hoja].columns = hojas[nombre_hoja].iloc[0]
            # Elimina la primera fila, ya que ahora son nombres de columnas
            hojas[nombre_hoja] = hojas[nombre_hoja][1:]
            hojas[nombre_hoja]["IMAGEN_PREPROCESADA"] = pd.Series([])
            hojas[nombre_hoja] = hojas[nombre_hoja].reset_index(drop=True)
            hojas[nombre_hoja].fillna("", inplace=True)
            for i, imagen5 in enumerate(hojas[nombre_hoja]["URL IMAGEN"]):
                print(i, imagen5)
                if "github" in imagen5 :
                    imagen5 ="https://raw.githubusercontent.com/estadisticasCame/ministerios-y-autoridades/main/" + imagen5[72:] 
                else:
                    pass
                try:
                    imagen = cargar_y_redimensionar_imagen_desde_url(imagen5)
                    # Guardar la imagen preprocesada en el DataFrame
                    hojas[nombre_hoja].loc[i, "IMAGEN_PREPROCESADA"] = imagen
                except:
                    pass
        except:
            pass
    return hojas,nombre_hojas

hojas, nombre_hojas = cargar_datos_excel()

st.write("---")
# Estado de la sesión
if 'estado' not in st.session_state:
    st.session_state.estado = {
        'seleccion_boton': None,
        'seleccion_desplegable': None
    }

def pagina_gobierno_nacional():
    hojas_nacional = nombre_hojas[1:15]
    hojas_nacional.insert(0,"-")
    opcion_seleccionada = st.selectbox("Seleccioná una opción", hojas_nacional)
    st.write("---")
    st.session_state.estado['seleccion_desplegable'] = opcion_seleccionada
    if opcion_seleccionada != "-":
        data = hojas[opcion_seleccionada]
        data = data.loc[:, ~data.columns.duplicated()]
        if (opcion_seleccionada == "Diputados" ) or (opcion_seleccionada == "Senadores"):
            try:
                data["CONCATENACION"] = data["Tratamiento"] + " " + data["Nombre y Apellido"]
                # Suponiendo que tus columnas de fechas son del tipo datetime
                data["Inicio de Mandato"] = pd.to_datetime(data["Inicio de Mandato"])
                data["Fin del Mandato"] = pd.to_datetime(data["Fin del Mandato"])
                # Crear la nueva columna "MANDATO" con las fechas en el formato deseado
                data["MANDATO"] = (
                    data["Inicio de Mandato"].dt.strftime("%d/%m/%Y")
                    + " | "
                    + data["Fin del Mandato"].dt.strftime("%d/%m/%Y")
                )
            except:
                pass
            st.dataframe(data)  
            
            listado_provincias = data["Provincia"].unique().tolist()
            listado_provincias = [str(elemento) for elemento in listado_provincias]
            listado_provincias.sort()
            listado_provincias.insert(0,"Todos")
            filtro_provincia = st.selectbox("Seleccioná la provincia", listado_provincias)
            
            if filtro_provincia == "Todos":
                bloque = data["Bloque"].unique().tolist()
                bloque = [str(elemento) for elemento in bloque]
                bloque.sort()
                bloque.insert(0,"Todos")
                bloque_seleccionado = st.selectbox("Seleccioná el bloque", bloque)
                if st.checkbox("Buscar por apellido/nombre"):
                        apellido_filtro = st.sidebar.text_input('Escriba aquí')
                        data = data[data['CONCATENACION'].str.contains(apellido_filtro, case=False, na = False)]  
                else:
                    pass
                # PARA BUSCAR
                if bloque_seleccionado == "Todos":
                    # Crear una lista de contenedores para imágenes y texto asociado
                    for texto1, texto2, texto3, texto4, imagen5 in zip(data["CONCATENACION"], data["Email"] , data["Telefono"], data["MANDATO"], data["IMAGEN_PREPROCESADA"]):
                        # Reemplazar valores nulos con "-"
                        texto1 = texto1 if not pd.isna(texto1) else "-"
                        texto2 = texto2 if not pd.isna(texto2) else "-"
                        texto3 = texto3 if not pd.isna(texto3) else "-"
                        texto4 = texto4 if not pd.isna(texto4) else "-"
                        with st.container(border=True):
                            # Crear columnas dentro del contenedor
                            col_imagen, col_texto = st.columns([0.7, 2.3])
                            
                            try:  
                                col_imagen.image(imagen5)
                            except:
                                col_imagen.image("imgs/persona no encontrada.png")
                            # Aplica estilo solo a la columna de texto
                            col_texto.markdown(
                                f"<div style='line-height: 1.5; font-size: 17px;'>"
                                f"<strong>{texto1}</strong><br><a href='mailto:{texto2}'>{texto2}</a><br>{texto3}<br>Mandato: {texto4}"
                                "</div>",
                                unsafe_allow_html=True
                            )
                else:
                    data = data[data["Bloque"].str.contains(bloque_seleccionado, na= False, case= False)]
                    # Crear una lista de contenedores para imágenes y texto asociado
                    # Crear una lista de contenedores para imágenes y texto asociado
                    for texto1, texto2, texto3, texto4, imagen5 in zip(data["CONCATENACION"], data["Email"] , data["Telefono"], data["MANDATO"], data["IMAGEN_PREPROCESADA"]):
                        # Reemplazar valores nulos con "-"
                        texto1 = texto1 if not pd.isna(texto1) else "-"
                        texto2 = texto2 if not pd.isna(texto2) else "-"
                        texto3 = texto3 if not pd.isna(texto3) else "-"
                        texto4 = texto4 if not pd.isna(texto4) else "-"
                        with st.container(border=True):
                            # Crear columnas dentro del contenedor
                            col_imagen, col_texto = st.columns([0.7, 2.3])
                    
                            try:
                        
                                col_imagen.image(imagen5)
                            except:
                                col_imagen.image("imgs/persona no encontrada.png")
                            # Aplica estilo solo a la columna de texto
                            col_texto.markdown(
                                f"<div style='line-height: 1.5; font-size: 17px;'>"
                                f"<strong>{texto1}</strong><br><a href='mailto:{texto2}'>{texto2}</a><br>{texto3}<br>Mandato: {texto4}"
                                "</div>",
                                unsafe_allow_html=True
                            )
                    
            else:
                data = data[data["Provincia"].str.contains(filtro_provincia, na= False, case= False)]
                bloque = data["Bloque"].unique().tolist()
                bloque = [str(elemento) for elemento in bloque]
                bloque.sort()
                bloque.insert(0,"Todos")
                bloque_seleccionado = st.selectbox("Seleccioná el bloque", bloque)
                if st.checkbox("Buscar por apellido/nombre"):
                        apellido_filtro = st.sidebar.text_input('Escriba aquí')
                        data = data[data['CONCATENACION'].str.contains(apellido_filtro, case=False, na = False)]  
                else:
                    pass
                # PARA BUSCAR
                if bloque_seleccionado == "Todos":
                    # Crear una lista de contenedores para imágenes y texto asociado
                    for texto1, texto2, texto3, texto4, imagen5 in zip(data["CONCATENACION"], data["Email"] , data["Telefono"], data["MANDATO"], data["IMAGEN_PREPROCESADA"]):
                        # Reemplazar valores nulos con "-"
                        texto1 = texto1 if not pd.isna(texto1) else "-"
                        texto2 = texto2 if not pd.isna(texto2) else "-"
                        texto3 = texto3 if not pd.isna(texto3) else "-"
                        texto4 = texto4 if not pd.isna(texto4) else "-"
                        with st.container(border=True):
                            # Crear columnas dentro del contenedor
                            col_imagen, col_texto = st.columns([0.7, 2.3])
                    
                            try:
                             
                                # Mostrar la imagen en la primera columna
                                col_imagen.image(imagen5)
                            except:
                                col_imagen.image("imgs/persona no encontrada.png")
                            # Aplica estilo solo a la columna de texto
                            col_texto.markdown(
                                f"<div style='line-height: 1.5; font-size: 17px;'>"
                                f"<strong>{texto1}</strong><br><a href='mailto:{texto2}'>{texto2}</a><br>{texto3}<br>Mandato: {texto4}"
                                "</div>",
                                unsafe_allow_html=True
                            )
                else:
                    data = data[data["Bloque"].str.contains(bloque_seleccionado, na= False, case= False)]
                    # Crear una lista de contenedores para imágenes y texto asociado
                    # Crear una lista de contenedores para imágenes y texto asociado
                    for texto1, texto2, texto3, texto4, imagen5 in zip(data["CONCATENACION"], data["Email"] , data["Telefono"], data["MANDATO"], data["IMAGEN_PREPROCESADA"]):
                        # Reemplazar valores nulos con "-"
                        texto1 = texto1 if not pd.isna(texto1) else "-"
                        texto2 = texto2 if not pd.isna(texto2) else "-"
                        texto3 = texto3 if not pd.isna(texto3) else "-"
                        texto4 = texto4 if not pd.isna(texto4) else "-"
                        with st.container(border=True):
                            # Crear columnas dentro del contenedor
                            col_imagen, col_texto = st.columns([0.7, 2.3])
                    
                            try:
                     
                                # Mostrar la imagen en la primera columna
                                col_imagen.image(imagen5)
                            except:
                                col_imagen.image("imgs/persona no encontrada.png")
                            # Aplica estilo solo a la columna de texto
                            col_texto.markdown(
                                f"<div style='line-height: 1.5; font-size: 17px;'>"
                                f"<strong>{texto1}</strong><br><a href='mailto:{texto2}'>{texto2}</a><br>{texto3}<br>Mandato: {texto4}"
                                "</div>",
                                unsafe_allow_html=True
                            )
                pass

        else:    
            try:
                data["CONCATENACION"] = data["TRATAMIENTO"] + " " + data["NOMBRE"] + " " + data["APELLIDO"] 
            except:
                pass
             # PARA BUSCAR
            if st.checkbox("Buscar por apellido/nombre"):
                apellido_filtro = st.sidebar.text_input('Escriba aquí')
                data = data[data['CONCATENACION'].str.contains(apellido_filtro, case=False, na = False)]  
            else:
                pass   
            # Crear una lista de contenedores para imágenes y texto asociado
            for texto1, texto2, texto3, texto4, imagen5 in zip(data["CONCATENACION"], data["ENTE"], data["EMAIL1"] , data["TELEFONO1"], data["IMAGEN_PREPROCESADA"]):
                # Reemplazar valores nulos con "-"
                texto1 = texto1 if not pd.isna(texto1) else "-"
                texto2 = texto2 if not pd.isna(texto2) else "-"
                texto3 = texto3 if not pd.isna(texto3) else "-"
                texto4 = texto4 if not pd.isna(texto4) else "-"
        
                with st.container(border=True):
                    # Crear columnas dentro del contenedor
                    col_imagen, col_texto = st.columns([0.7, 2.3])
                    try:
                        
                                # Mostrar la imagen en la primera columna
                        col_imagen.image(imagen5)
                    except:
                        col_imagen.image("imgs/persona no encontrada.png")
                    # Aplica estilo solo a la columna de texto
                    col_texto.markdown(
                        f"<div style='line-height: 1.5; font-size: 17px;'>"
                        f"<strong>{texto1}</strong><br>{texto2}<br><a href='mailto:{texto3}'>{texto3}</a><br>{texto4}"
                        "</div>",
                        unsafe_allow_html=True
                    )

def pagina_gobiernos_provinciales():
    hojas_provincial = nombre_hojas[15:]
    hojas_provincial.insert(0,"-")
    opcion_seleccionada = st.selectbox("Seleccioná una opción", hojas_provincial)
    st.write("---")
    st.session_state.estado['seleccion_desplegable'] = opcion_seleccionada
    if opcion_seleccionada != "-":
        data = hojas[opcion_seleccionada]
        try:
            data["CONCATENACION"] = data["TRATAMIENTO"] + " " + data["NOMBRE"] + " " + data["APELLIDO"] 
        except:
            pass
        # PARA BUSCAR
        if st.checkbox("Buscar por apellido/nombre"):
            apellido_filtro = st.sidebar.text_input('Escriba aquí')
            data = data[data['CONCATENACION'].str.contains(apellido_filtro, case=False, na = False)]  
        else:
            pass
        for texto1, texto2, texto3, texto4 in zip(data["CONCATENACION"], data["ENTE"], data["EMAIL1"] , data["TELEFONO1"]):
            # Reemplazar valores nulos con "-"
            texto1 = texto1 if not pd.isna(texto1) else "-"
            texto2 = texto2 if not pd.isna(texto2) else "-"
            texto3 = texto3 if not pd.isna(texto3) else "-"
            texto4 = texto4 if not pd.isna(texto4) else "-"
            with st.container(border=True):
                # Crear columnas dentro del contenedor
                col_imagen, col_texto = st.columns([0.7, 2.3])
        
                # Mostrar la imagen en la primera columna
                col_imagen.image("imgs/javier_milei.png")
                # Aplica estilo solo a la columna de texto
                col_texto.markdown(
                    f"<div style='line-height: 1.5; font-size: 17px;'>"
                    f"<strong>{texto1}</strong><br>{texto2}<br><a href='mailto:{texto3}'>{texto3}</a><br>{texto4}"
                    "</div>",
                    unsafe_allow_html=True
                )            


# Crear columnas
columna3, columna4 = st.columns(2)

with columna3:
    if st.button("GOBIERNO NACIONAL", use_container_width=True):
        st.session_state.estado['seleccion_boton'] = "gobierno_nacional"
        st.session_state.estado['seleccion_desplegable'] = None

with columna4:
    if st.button("GOBIERNOS PROVINCIALES", use_container_width=True):
        st.session_state.estado['seleccion_boton'] = "gobiernos_provinciales"
        st.session_state.estado['seleccion_desplegable'] = None

st.write("---")

# Mostrar la página correspondiente según el botón seleccionado
if st.session_state.estado['seleccion_boton'] == "gobierno_nacional":
    pagina_gobierno_nacional()
elif st.session_state.estado['seleccion_boton'] == "gobiernos_provinciales":
    pagina_gobiernos_provinciales()
