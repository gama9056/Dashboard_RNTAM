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
# 🗺️ CARGA VECTORIAL MULTICAPA (AUTOMÁTICA)
# ==========================================================
@st.cache_data
def cargar_capas_geograficas():
    # 1. CARGA Y UNIFICACIÓN DE LOS 9 ÁMBITOS DE CONTROL PVC
    lista_gdfs = []
    archivos_zip = glob.glob("data/Ambito_de_control_*.zip")
    
    if not archivos_zip:
        nombres = ["Azul", "Briolo", "Huisene", "Jorge_Chavez", "La_Torre", "Malinowski", "Otorongo", "Sandoval", "Yarinal"]
        archivos_zip = [f"data/Ambito_de_control_{n}.zip" for n in nombres]

    for ruta in archivos_zip:
        if os.path.exists(ruta):
            gdf_pvc = gpd.read_file(f"zip://{ruta}").to_crs("EPSG:4326")
            nombre_archivo = os.path.basename(ruta).replace(".zip", "")
            nombre_pvc = nombre_archivo.replace("Ambito_de_control_", "PVC ").replace("_", " ")
            gdf_pvc["NOM_PVC"] = nombre_pvc
            lista_gdfs.append(gdf_pvc)
            
    if lista_gdfs:
        gdf_ambitos = gpd.GeoDataFrame(pd.concat(lista_gdfs, ignore_index=True), crs="EPSG:4326")
    else:
        gdf_ambitos = gpd.GeoDataFrame(columns=["NOM_PVC", "geometry"], crs="EPSG:4326")

    # 2. CARGA DEL LÍMITE DE LA RESERVA (ANP)
    ruta_anp = "data/ANP_RNTAM.zip"
    if os.path.exists(ruta_anp):
        gdf_anp = gpd.read_file(f"zip://{ruta_anp}").to_crs("EPSG:4326")
    else:
        gdf_anp = gpd.GeoDataFrame(columns=["geometry"], crs="EPSG:4326")

    # 3. CARGA DE LA ZONA DE AMORTIGUAMIENTO (ZA)
    ruta_za = "data/ZA_RNTAM.zip"
    if os.path.exists(ruta_za):
        gdf_za = gpd.read_file(f"zip://{ruta_za}").to_crs("EPSG:4326")
    else:
        gdf_za = gpd.GeoDataFrame(columns=["geometry"], crs="EPSG:4326")
        
    return gdf_ambitos, gdf_anp, gdf_za

# Ejecutamos la lectura del entorno real en GitHub
gdf_ambitos, gdf_anp, gdf_za = cargar_capas_geograficas()
lista_pvc = sorted(gdf_ambitos["NOM_PVC"].unique().tolist()) if not gdf_ambitos.empty else []

# ==========================================================
# COLUMNAS PRINCIPALES
# ==========================================================
col_left, col_center, col_right = st.columns([1, 2, 1], gap="large")

# ==========================================================
# PANEL IZQUIERDO (CONTROLES Y FILTROS)
# ==========================================================
with col_left:
    with st.container(height=575, border=True):
        st.markdown("<h2 style='text-align:center; color:#163b16; margin-bottom:25px;'>🌱 PANEL DE CONTROL</h2>", unsafe_allow_html=True)

        pvc_seleccionados = st.multiselect(
            "🔍 Filtrar por Ámbito de Control (PVC):",
            options=lista_pvc,
            placeholder="Mostrando toda la Reserva..."
        )

        st.markdown("---")
        st.markdown("**🎚️ Transparencia de Capas:**")
        
        opacidad = st.slider(
            "Opacidad de Ámbitos PVC:",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.1
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.info("El visor aplicará un zoom automático dinámico basándose en los polígonos que filtre en la lista superior.")

# ==========================================================
# LÓGICA INTERACTIVA DE ENFOQUE (ZOOM TO LAYER)
# ==========================================================
if pvc_seleccionados and not gdf_ambitos.empty:
    gdf_filtrado = gdf_ambitos[gdf_ambitos["NOM_PVC"].isin(pvc_seleccionados)]
    bounds = gdf_filtrado.total_bounds
    factor = len(pvc_seleccionados)
    cant_especies = (1234 // 9) * factor
    cant_visitantes = (8942 // 9) * factor
    cant_alertas = max(1, factor - 6)
    texto_delta = f"{factor} PVC seleccionados"
else:
    gdf_filtrado = gdf_ambitos.copy()
    # Si no hay filtro, intenta enfocar el mapa usando el límite de toda la ANP o la ZA
    if not gdf_anp.empty:
        bounds = gdf_anp.total_bounds
    elif not gdf_ambitos.empty:
        bounds = gdf_ambitos.total_bounds
    else:
        bounds = [-69.8, -13.1, -69.2, -12.5] # Coordenadas de respaldo de Madre de Dios
        
    cant_especies = 1234
    cant_visitantes = 8942
    cant_alertas = 3
    texto_delta = "Total general de la RNTAM"

# ==========================================================
# PANEL CENTRAL (VISOR CARTOGRÁFICO)
# ==========================================================
with col_center:
    st.markdown("<h2 style='color:#163b16; margin:0;'>📊 MÉTRICAS CLAVE</h2>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    with m1: st.metric(label="🦋 Especies registradas", value=f"{cant_especies:,}", delta=texto_delta)
    with m2: st.metric(label="👥 Visitantes 2025", value=f"{cant_visitantes:,}", delta=texto_delta)
    with m3: st.metric(label="🔥 Alertas SMART", value=str(cant_alertas), delta="Riesgo de presiones", delta_color="inverse")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#163b16; margin:0 0 10px 0;'>🗺️ ZONIFICACIÓN Y MONITOREO</h2>", unsafe_allow_html=True)

    # Configuración de coordenadas base
    centro_mapa = [(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2]
    m = folium.Map(location=centro_mapa, zoom_start=10, control_scale=True)
    
    # Capa de satélite como mapa base por defecto
    folium.TileLayer(
        tiles='
