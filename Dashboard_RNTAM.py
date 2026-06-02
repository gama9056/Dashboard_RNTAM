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
# =
