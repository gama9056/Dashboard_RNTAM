import streamlit as st
from streamlit_folium import st_folium
import folium
import geopandas as gpd
from shapely.geometry import Polygon

# ==========================================================
# CONFIGURACIÓN GENERAL
# ==========================================================
st.set_page_config(
    page_title="Dashboard RNTambopata",
    page_icon="🌿",
    layout="wide"
)

# ==========================================================
# ESTILOS CSS
# ==========================================================
st.markdown("""
<style>
.block-container{
    padding-top:1.5rem;
    padding-bottom:1rem;
}
.title-container{
    border:1px solid #2c5f2d;
    border-radius:12px;
    background:#fefef7;
    height:60px;
    display:flex;
    align-items:center;
    justify-content:center;
    margin-bottom:10px;
}
.custom-hr{
    border:0;
    height:1px;
    background:#d9d9d9;
    margin-top:5px;
    margin-bottom:20px;
}
.stMetric{
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# CABECERA
# ==========================================================
st.markdown("""
<div class="title-container">
<h2 style="margin:0; font-weight:bold; color:#163b16;">
🌿 DASHBOARD - RESERVA NACIONAL TAMBOPATA 🌿
</h2>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="custom-hr">', unsafe_allow_html=True)

# ==========================================================
# 🗺️ DATA GEOESPACIAL SIMULADA (Reemplazar luego con tu .shp)
# ==========================================================
# Creamos polígonos de prueba simulando ámbitos de control en Tambopata
@st.cache_data
def cargar_ambitos_control():
    # Coordenadas base aproximadas de Madre de Dios / Tambopata
    coordenadas_pvc = {
        "PVC Otorongo":    [[-69.70, -12.80], [-69.60, -12.80], [-69.60, -12.90], [-69.70, -12.90]],
        "PVC Azul":        [[-69.90, -12.95], [-69.75, -12.95], [-69.75, -13.10], [-69.90, -13.10]],
        "PVC Yarinal":     [[-69.60, -12.70], [-69.50, -12.70], [-69.50, -12.80], [-69.60, -12.80]],
        "PVC Malinowski":  [[-70.15, -12.90], [-69.95, -12.90], [-69.95, -13.05], [-70.15, -13.05]],
        "PVC La Torre":    [[-69.50, -12.60], [-69.40, -12.60], [-69.40, -12.70], [-69.50, -12.70]],
        "PVC Jorge Chávez":[[-69.35, -12.65], [-69.25, -12.65], [-69.25, -12.75], [-69.35, -12.75]],
        "PVC Sandoval":    [[-69.40, -12.55], [-69.30, -12.55], [-69.30, -12.65], [-69.40, -12.65]],
        "PVC Briolo":      [[-69.55, -12.85], [-69.45, -12.85], [-69.45, -12.95], [-69.55, -12.95]],
        "PVC Huisene":     [[-69.80, -12.65], [-69.70, -12.65], [-69.70, -12.75], [-69.80, -12.75]],
    }
    
    lista_features = []
    for nombre, coords in coordenadas_pvc.items():
        poligono = Polygon(coords)
        lista_features.append({"PVC": nombre, "geometry": poligono})
        
    gdf = gpd.GeoDataFrame(lista_features, crs="EPSG:4326")
    return gdf

# NOTA: En tu entorno real, para cargar tu Shapefile usarías:
# gdf_ambitos = gpd.read_file("ruta_de_tu_archivo/ambitos_pvc.shp").to_crs("EPSG:4326")
gdf_ambitos = cargar_ambitos_control()
lista_pvc = sorted(gdf_ambitos["PVC"].unique().tolist())

# ==========================================================
# COLUMNAS PRINCIPALES
# ==========================================================
col_left, col_center, col_right = st.columns([1, 2, 1], gap="large")

# ==========================================================
# PANEL IZQUIERDO (FILTROS Y TRANSPARENCIA)
# ==========================================================
with col_left:
    with st.container(height=540, border=True):
        st.markdown("<h2 style='text-align:center; color:#163b16; margin-bottom:25px;'>🌱 PANEL DE CONTROL</h2>", unsafe_allow_html=True)

        pvc_seleccionados = st.multiselect(
            "🔍 Filtrar por Ámbito de Control (PVC):",
            options=lista_pvc,
            placeholder="Mostrando toda la Reserva..."
        )

        st.markdown("---")
        st.markdown("**🎚️ Configuración de Capas:**")
        
        # Slider interactivo para regular la opacidad de los polígonos en tiempo real
        opacidad = st.slider(
            "Transparencia del Ámbito de Control:",
            min_value=0.0,
            max_value=1.0,
            value=0.4,
            step=0.1
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.info("Seleccione uno o varios PVC para enfocar automáticamente el mapa en sus respectivos límites espaciales.")

# ==========================================================
# LÓGICA DE FILTRO INTERACTIVO
# ==========================================================
if pvc_seleccionados:
    gdf_filtrado = gdf_ambitos[gdf_ambitos["PVC"].isin(pvc_seleccionados)]
    factor = len(pvc_seleccionados)
    cant_especies = (1234 // 9) * factor
    cant_visitantes = (8942 // 9) * factor
    cant_alertas = max(1, factor - 6)
    texto_delta = f"{factor} PVC seleccionados"
else:
    gdf_filtrado = gdf_ambitos.copy()
    cant_especies = 1234
    cant_visitantes = 8942
    cant_alertas = 3
    texto_delta = "Total general de la RNTAM"

# ==========================================================
# PANEL CENTRAL (MÉTRICAS Y VISOR GEOESPACIAL)
# ==========================================================
with col_center:
    st.markdown("<h2 style='color:#163b16; margin:0;'>📊 MÉTRICAS CLAVE</h2>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    with m1: st.metric(label="🦋 Especies registradas", value=f"{cant_especies:,}", delta=texto_delta)
    with m2: st.metric(label="👥 Visitantes 2025", value=f"{cant_visitantes:,}", delta=texto_delta)
    with m3: st.metric(label="🔥 Alertas SMART", value=str(cant_alertas), delta="Riesgo de presiones", delta_color="inverse")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#163b16; margin:0 0 10px 0;'>🗺️ ZONIFICACIÓN Y MONITOREO</h2>", unsafe_allow_html=True)

    # --- CONSTRUCCIÓN DEL MAPA INTERACTIVO CON FOLIUM ---
    
    # Calcular centro y límites para el "Zoom to Layer" automático
    bounds = gdf_filtrado.total_bounds  # Retorna [minx, miny, maxx, maxy]
    centro_mapa = [(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2]
    
    # Crear objeto Mapa Base (Por defecto carga OpenStreetMap)
    m = folium.Map(
        location=centro_mapa, 
        zoom_start=10, 
        control_scale=True
    )
    
    # Añadir capa Satelital de Google de forma secundaria
    google_satellite = folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Satélite',
        overlay=False,
        control=True
    )
    google_satellite.add_to(m)

    # Estilo visual de los ámbitos de control (Shapefile) utilizando la opacidad del slider
    def estilo_poligono(feature):
        return {
            'fillColor': '#2c5f2d',
            'color': '#163b16',
            'weight': 2,
            'fillOpacity': opacidad  # Conectado dinámicamente al slider del panel izquierdo
        }

    # Inyectar la capa del Shapefile filtrado al mapa
    capa_ambitos = folium.GeoJson(
        gdf_filtrado,
        name="Ámbitos de Control PVC",
        style_function=estilo_poligono,
        tooltip=folium.GeoJsonTooltip(fields=["PVC"], aliases=["Ámbito de Control: "])
    )
    capa_ambitos.add_to(m)

    # Ajustar dinámicamente la ventana de visualización (Zoom to Layer)
    m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])

    # Habilitar el selector de mapas y capas (Esquina superior derecha)
    folium.LayerControl(position="topright", collapsed=False).add_to(m)

    # Renderizar el mapa de Folium de manera responsiva dentro del flujo del Dashboard
    st_folium(m, width="100%", height=400, returned_objects=[])

# ==========================================================
# PANEL DERECHO (ACTIVIDAD RECIENTE)
# ==========================================================
with col_right:
    with st.container(height=540, border=True):
        st.markdown("<h2 style='text-align:center; color:#163b16; margin-bottom:25px;'>📢 ACTIVIDAD RECIENTE</h2>", unsafe_allow_html=True)
        st.markdown("""
        • Sincronización con SMART activa correctamente.
        • Monitoreo de patrullajes sin alertas rojas.
        • Puestos de vigilancia reportando conformidad.
        • Actualización de registros completada.
        • Datos sincronizados exitosamente.
        """)
        st.markdown("<br>", unsafe_allow_html=True)
        st.success("Sistema operativo y actualizado.")
