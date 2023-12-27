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
        st.dataframe(data)
        if (opcion_seleccionada == "Diputados" ) or (opcion_seleccionada == "Senadores"):
            try:
                data["CONCATENACION"] = data["Tratamiento"] + " " + data["Nombre y Apellido"]
            except:
                pass
            listado_provincias = data["Provincia"].unique().tolist()
            listado_provincias.insert(0,"-")
            filtro_provincia = st.selectbox("Seleccioná la provincia", listado_provincias)
            if filtro_provincia != "-":
                data = data[data["Provincia"].str.contains(filtro_provincia, na= False, case= False)]
                # Crear una lista de contenedores para imágenes y texto asociado
                # Crear una lista de contenedores para imágenes y texto asociado
                for texto1, texto2, texto3 in zip(data["CONCATENACION"], data["Email"] , data["Telefono"]):
                    with st.container(border=True):
                        # Crear columnas dentro del contenedor
                        col_imagen, col_texto = st.columns([0.7, 2.3])
                
                        # Mostrar la imagen en la primera columna
                        col_imagen.image("imgs/javier_milei.png")
                        # Aplica estilo solo a la columna de texto
                        col_texto.markdown(
                            f"<div style='line-height: 1.5; font-size: 17px;'>"
                            f"<strong>{texto1}</strong><br><a href='mailto:{texto2}</a><br><br>{texto3}"
                            "</div>",
                            unsafe_allow_html=True
                        )
            else:
                pass

        else:    
            try:
                data["CONCATENACION"] = data["TRATAMIENTO"] + " " + data["NOMBRE"] + " " + data["APELLIDO"] 
            except:
                pass
            # Crear una lista de contenedores para imágenes y texto asociado
            for texto1, texto2, texto3, texto4 in zip(data["CONCATENACION"], data["ENTE"], data["EMAIL1"] , data["TELEFONO1"]):
                with st.container(border=True):
                    # Crear columnas dentro del contenedor
                    col_imagen, col_texto = st.columns([0.7, 2.3])
            
                    # Mostrar la imagen en la primera columna
                    col_imagen.image("imgs/javier_milei.png")
                    # Aplica estilo solo a la columna de texto
                    # Aplica estilo solo a la columna de texto
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
    st.session_state.estado['seleccion_desplegable'] = opcion_seleccionada
    if opcion_seleccionada != "-":
        data = hojas[opcion_seleccionada]
        try:
            data["CONCATENACION"] = data["TRATAMIENTO"] + " " + data["NOMBRE"] + " " + data["APELLIDO"] 
        except:
            pass
        st.dataframe(data)

        for texto1, texto2, texto3, texto4 in zip(data["CONCATENACION"], data["ENTE"], data["EMAIL1"] , data["TELEFONO1"]):
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
