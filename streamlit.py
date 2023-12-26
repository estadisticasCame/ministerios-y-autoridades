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

presidencia_de_la_nacion = hojas[nombre_hojas[1]]
jefatura_gabinete = hojas[nombre_hojas[2]]
ministerio_defensa = hojas[nombre_hojas[3]]
ministerio_justicia = hojas[nombre_hojas[4]]
ministerio_seguridad = hojas[nombre_hojas[5]]
ministerio_interior = hojas[nombre_hojas[6]]
ministerio_salud = hojas[nombre_hojas[7]]
ministerio_relaciones_exteriores = hojas[nombre_hojas[8]]
ministerio_economia = hojas[nombre_hojas[9]]
ministerio_capital_humano = hojas[nombre_hojas[10]]
ministerio_infraestructura = hojas[nombre_hojas[11]]
diputados = hojas[nombre_hojas[12]]
senadores = hojas[nombre_hojas[13]]
gobernadores = hojas[nombre_hojas[14]]
buenos_aires = hojas[nombre_hojas[15]]
caba = hojas[nombre_hojas[16]]
catamarca = hojas[nombre_hojas[17]]
chaco = hojas[nombre_hojas[18]]
chubut = hojas[nombre_hojas[19]]
cordoba = hojas[nombre_hojas[20]]
corrientes = hojas[nombre_hojas[21]]
entrerios = hojas[nombre_hojas[22]]
formosa = hojas[nombre_hojas[23]]
jujuy = hojas[nombre_hojas[24]]
lapampa = hojas[nombre_hojas[25]]
larioja = hojas[nombre_hojas[26]]
mendoza = hojas[nombre_hojas[27]]
misiones = hojas[nombre_hojas[28]]
neuquen = hojas[nombre_hojas[29]]
rionegro = hojas[nombre_hojas[30]]
salta = hojas[nombre_hojas[31]]
sanjuan = hojas[nombre_hojas[32]]
sanluis = hojas[nombre_hojas[33]]
santacruz = hojas[nombre_hojas[34]]
santafe = hojas[nombre_hojas[35]]
santiagodelestero = hojas[nombre_hojas[36]]
tierradelfuego = hojas[nombre_hojas[37]]
tucuman = hojas[nombre_hojas[38]]


st.write("---")
import streamlit as st

# Estado de la sesión
if 'estado' not in st.session_state:
    st.session_state.estado = {
        'seleccion_boton': None,
        'seleccion_desplegable': None
    }

def pagina_gobierno_nacional():
    st.write("Contenido para Gobierno Nacional")
    hojas_nacional = nombre_hojas[1:15]
    opcion_seleccionada = st.selectbox("Seleccioná una opción", hojas_nacional)
    st.session_state.estado['seleccion_desplegable'] = opcion_seleccionada
    st.write(opcion_seleccionada)

def pagina_gobiernos_provinciales():
    st.write("Contenido para Gobiernos Provinciales")
    hojas_provincial = nombre_hojas[15:]
    opcion_seleccionada = st.selectbox("Seleccioná una opción", hojas_provincial, index=st.session_state.estado['seleccion_desplegable'])
    st.session_state.estado['seleccion_desplegable'] = opcion_seleccionada
    st.write(opcion_seleccionada)

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

# Mostrar la página correspondiente según el botón seleccionado
if st.session_state.estado['seleccion_boton'] == "gobierno_nacional":
    pagina_gobierno_nacional()
elif st.session_state.estado['seleccion_boton'] == "gobiernos_provinciales":
    pagina_gobiernos_provinciales()
