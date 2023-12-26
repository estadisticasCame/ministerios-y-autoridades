import pandas as pd
import streamlit as st

columna1, columna2 = st.columns([2,1])
with columna1:
    st.title("Tablero de control")
    st.header("Ministerios y Autoridades")
    
with columna2:
    st.image("imgs/escudo.png", width=150)

# Realizamos la carga de datos y lo guardamos en cache de streamlit
@st.cache_data
def cargar_datos_excel():
    # Ingestamos el archivo de excel del meppi
    excel = pd.read_excel("Datos/Ministerios y autoridades.xlsx", sheet_name=None)
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
    st.session_state.estado['seleccion_desplegable'] = opcion_seleccionada
    if opcion_seleccionada != "-":
        data = hojas[opcion_seleccionada]
        try:
            data["CONCATENACION"] = data["TRATAMIENTO"] + " " + data["NOMBRE"] + " " + data["APELLIDO"] 
        except:
            pass
        st.dataframe(data)
       # Crear una lista de contenedores para imágenes y texto asociado
        contenedores = []
        
        # Llenar la lista de contenedores con imágenes y texto asociado
        for  texto1, texto2 in zip( data["CONCATENACION"], data["ENTE"]):
            contenedor = st.container(border=True)
            
            # Crear columnas dentro del contenedor
            col_imagen, col_texto = contenedor.columns([1, 2])
            
            # Mostrar la imagen en la primera columna
            col_imagen.image("imgs/javier_milei.png")
            
            # Mostrar el texto en la segunda columna
            col_texto.write(f"**{texto1}:** {texto2}")
            
            contenedores.append(contenedor)

            # Colocar los contenedores en una fila
            #fila_contenedores = st.columns(len(contenedores))
            for i, contenedor in enumerate(contenedores):
                st.write(contenedor)

def pagina_gobiernos_provinciales():
    hojas_provincial = nombre_hojas[15:]
    hojas_provincial.insert(0,"-")
    opcion_seleccionada = st.selectbox("Seleccioná una opción", hojas_provincial)
    st.session_state.estado['seleccion_desplegable'] = opcion_seleccionada
    if opcion_seleccionada != "-":
        data = hojas[opcion_seleccionada]
        try:
            data["CONCATENACION"] = data["TRATAMIENTO"] + " " + data["NOMBRE"] + " " + data["APELLIDO"] 
        except:
            pass
        st.dataframe(data)
        # Crear una lista de contenedores para imágenes y texto asociado
        contenedores = []
        # Llenar la lista de contenedores con imágenes y texto asociado
        for texto1, texto2 in zip( data["CONCATENACION"], data["ENTE"]):
            contenedor = st.container(border=True)
            contenedor.image("imgs/javier_milei.png")
            contenedor.write(f"**{texto1}:**")
            contenedor.write(f"{texto2}:")
            contenedores.append(contenedor)
        
        # Colocar los contenedores en una fila
        fila_contenedores = st.columns(len(contenedores))
        for i, contenedor in enumerate(contenedores):
            fila_contenedores[i].subheader(f"Elemento {i + 1}")
            fila_contenedores[i].write(contenedor)
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
