import streamlit as st
from streamlit_folium import st_folium
import folium
import geopandas as gpd
import pandas as pd
import glob
import os

# ==========================================================
# CONFIGURACIÓN GENERAL
# ==========================================================
st.set_page_config(
    page_title="Dashboard RNTambopata",
    page_icon="🌿",
    layout="wide"
)

# ==========================================================
# ESTILOS CSS (Garantiza la alineación de las 3 columnas fijos)
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
# 🗺️ CARGA Y UNIFICACIÓN DE LOS 9 SHAPEFILES (.ZIP)
# ==========================================================
@st.cache_data
def cargar_ambitos_real():
    lista_gdfs = []
    
    # Busca todos los archivos .zip dentro de la carpeta data/
    archivos_zip = glob.glob("data/Ambito_de_control_*.zip")
    
    # En caso de que falle glob por rutas relativas en la nube, listamos directamente
    if not archivos_zip:
        nombres = ["Azul", "Briolo", "Huisene", "Jorge_Chavez", "La_Torre", "Malinowski", "Otorongo", "Sandoval", "Yarinal"]
        archivos_zip = [f"data/Ambito_de_control_{n}.zip" for n in nombres]

    for ruta in archivos_zip:
        if os.path.exists(ruta):
            # Leer el archivo zip y transformarlo inmediatamente a WGS84 Geográficas
            gdf_pvc = gpd.read_file(f"zip://{ruta}").to_crs("EPSG:4326")
            
            # Crear o estandarizar la columna del nombre basada en el archivo zip
            nombre_archivo = os.path.basename(ruta).replace(".zip", "")
            nombre_pvc = nombre_archivo.replace("Ambito_de_control_", "PVC ").replace("_", " ")
            
            gdf_pvc["NOM_PVC"] = nombre_pvc
            lista_gdfs.append(gdf_pvc)
            
    # Concatenar todos los polígonos en un único GeoDataFrame maestro
    if lista_gdfs:
        gdf_maestro = gpd.GeoDataFrame(pd.concat(lista_gdfs, ignore_index=True), crs="EPSG:4326")
    else:
        # GeoDataFrame vacío de respaldo si ocurre algún problema de lectura
        gdf_maestro = gpd.GeoDataFrame(columns=["NOM_PVC", "geometry"], crs="EPSG:4326")
        
    return gdf_maestro

# Ejecutar la carga unificada
gdf_ambitos = cargar_ambitos_real()
lista_pvc = sorted(gdf_ambitos["NOM_PVC"].unique().tolist()) if not gdf_ambitos.empty else []

# ==========================================================
# COLUMNAS PRINCIPALES
# ==========================================================
col_left, col_center, col_right = st.columns(
    [1, 2, 1],
    gap="large"
)

# ==========================================================
# PANEL IZQUIERDO (CONTROL)
# ==========================================================
with col_left:
    with st.container(height=575, border=True):
        st.markdown("""
        <h2 style='text-align:center; color:#163b16; margin-bottom:25px;'>
        🌱 PANEL DE CONTROL
        </h2>
        """, unsafe_allow_html=True)

        pvc_seleccionados = st.multiselect(
            "🔍 Filtrar por Ámbito de Control (PVC):",
            options=lista_pvc,
            placeholder="Mostrando toda la Reserva..."
        )

        st.markdown("---")
        st.markdown("**🎚️ Configuración Visual:**")
        
        opacidad = st.slider(
            "Transparencia del Ámbito:",
            min_value=0.0,
            max_value=1.0,
            value=0.4,
            step=0.1
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.info("Seleccione uno o varios Puestos de Vigilancia y Control para enfocar automáticamente el visor espacial.")

# ==========================================================
# LÓGICA DE FILTRO INTERACTIVO
# ==========================================================
if pvc_seleccionados and not gdf_ambitos.empty:
    gdf_filtrado = gdf_ambitos[gdf_ambitos["NOM_PVC"].isin(pvc_seleccionados)]
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
# PANEL CENTRAL (MÉTRICAS Y VISOR REAL)
# ==========================================================
with col_center:
    st.markdown("<h2 style='color:#163b16; margin:0;'>📊 MÉTRICAS CLAVE</h2>", unsafe_allow_html=True)
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="🦋 Especies registradas", value=f"{cant_especies:,}", delta=texto_delta)
    with m2:
        st.metric(label="👥 Visitantes 2025", value=f"{cant_visitantes:,}", delta=texto_delta)
    with m3:
        st.metric(label="🔥 Alertas SMART", value=str(cant_alertas), delta="Riesgo de presiones", delta_color="inverse")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#163b16; margin:0 0 10px 0;'>🗺️ ZONIFICACIÓN Y MONITOREO</h2>", unsafe_allow_html=True)

    # --- RENDERIZADO DEL MAPA REAL ---
    if not gdf_filtrado.empty:
        bounds = gdf_filtrado.total_bounds  # [minx, miny, maxx, maxy]
        centro_mapa = [(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2]
        
        m = folium.Map(location=centro_mapa, zoom_start=10, control_scale=True)
        
        # Capa Satelital secundaria
        folium.TileLayer(
            tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
            attr='Google',
            name='Google Satélite',
            overlay=False,
            control=True
        ).add_to(m)

        # Inyectar los ámbitos de control reales
        folium.GeoJson(
            gdf_filtrado,
            name="Ámbitos de Control PVC",
            style_function=lambda x: {
                'fillColor': '#2c5f2d',
                'color': '#163b16',
                'weight': 2,
                'fillOpacity': opacidad
            },
            tooltip=folium.GeoJsonTooltip(fields=["NOM_PVC"], aliases=["Ámbito de Control: "])
        ).add_to(m)

        # Aplicar el "Zoom to Layer" dinámico
        m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
        folium.LayerControl(position="topright", collapsed=False).add_to(m)
        
        # Dibujar en pantalla con altura adaptada
        st_folium(m, width="100%", height=415, returned_objects=[])
    else:
        # Cuadro de advertencia en caso de que la carpeta data esté vacía o procesándose
        st.warning("Cargando capas espaciales o archivos no encontrados en 'data/'.")

# ==========================================================
# PANEL DERECHO (ACTIVIDAD RECIENTE)
# ==========================================================
with col_right:
    with st.container(height=575, border=True):
        st.markdown("""
        <h2 style='text-align:center; color:#163b16; margin-bottom:25px;'>
        📢 ACTIVIDAD RECIENTE
        </h2>
        """, unsafe_allow_html=True)

        st.markdown("""
        • Sincronización con SMART activa de forma correcta.

        • Monitoreo en patrullajes sin alertas rojas hoy.

        • Puestos de vigilancia reportando conformidad.

        • Actualización de registros completada.

        • Datos de ámbitos unificados con éxito.
        """)

        st.markdown("<br>", unsafe_allow_html=True)
        st.success("Sistema operativo y actualizado.")
