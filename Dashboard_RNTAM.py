import streamlit as st
from streamlit_folium import st_folium
import folium
import geopandas as gpd
import pandas as pd
import glob
import os
import zipfile
import tempfile

# ==========================================================
# CONFIGURACIÓN GENERAL
# ==========================================================
st.set_page_config(
    page_title="Dashboard RNTambopata",
    page_icon="🛡️",
    layout="wide"
)

# ==========================================================
# ESTILOS CSS (Estilo Interfaz ArcGIS Pro Avanzado)
# ==========================================================
st.markdown("""
<style>
.block-container{
    padding-top:1.5rem;
    padding-bottom:1rem;
}
.title-container{
    border:1px solid #8b0000;
    border-radius:12px;
    background:#fff5f5;
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
/* Espaciado ultra-compacto para los sub-expanders */
.stExpander {
    margin-bottom: 4px !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# CABECERA
# ==========================================================
st.markdown("""
<div class="title-container">
<h2 style="margin:0; font-weight:bold; color:#8b0000;">
🛡️ VISOR OPERATIVO: MONITOREO DE MINERÍA ILEGAL - RNTAM 🛡️
</h2>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="custom-hr">', unsafe_allow_html=True)

# ==========================================================
# 🗺️ LÓGICA DE SANITIZACIÓN GEOESPACIAL
# ==========================================================
def sanitizar_geodataframe(gdf):
    """Elimina o convierte a texto cualquier columna temporal que Folium no pueda serializar"""
    if gdf is None or gdf.empty:
        return gdf
    for col in gdf.select_dtypes(include=['datetime64', 'timedelta64', 'datetimetz']).columns:
        gdf[col] = gdf[col].astype(str)
    for col in gdf.columns:
        if col.lower() in ['fecha', 'date', 'felea', 'time', 'timestamp'] or gdf[col].dtype == 'object':
            try:
                if any(isinstance(val, (pd.Timestamp, pd.Timedelta)) for val in gdf[col].dropna()):
                    gdf[col] = gdf[col].astype(str)
            except:
                pass
    return gdf

# ==========================================================
# 📊 ESCANEO AUTOMÁTICO DE ARCHIVOS ZIP (DATA/)
# ==========================================================
@st.cache_data
def escanear_capas_locales(directorio="data"):
    """Busca dinámicamente todos los archivos .zip dentro de la carpeta data"""
    capas_detectadas = {}
    if not os.path.exists(directorio):
        return capas_detectadas

    patron_zip = os.path.join(directorio, "*.zip")
    archivos_zip = glob.glob(patron_zip)

    for ruta_zip in archivos_zip:
        nombre_base = os.path.basename(ruta_zip).replace(".zip", "")
        try:
            gdf = gpd.read_file(f"zip://{ruta_zip}").to_crs("EPSG:4326")
            if not gdf.empty:
                gdf = sanitizar_geodataframe(gdf)
                capas_detectadas[nombre_base] = gdf
        except:
            pass
            
    return capas_detectadas

# Carga e inventariado
diccionario_capas = escanear_capas_locales()

# Base analítica de deforestación por hectáreas
datos_deforestacion_exclusiva = {
    "Ambito_de_control_Malinowski": 524.30,
    "Ambito_de_control_Otorongo": 341.20,
    "Ambito_de_control_Yarinal": 215.60,
    "Ambito_de_control_Azul": 160.50,
    "Ambito_de_control_Jorge_Chavez": 0.00,
    "Ambito_de_control_Huisene": 0.00,
    "Ambito_de_control_Briolo": 0.00,
    "Ambito_de_control_La_Torre": 0.00,
    "Ambito_de_control_Sandoval": 0.00
}

# ==========================================================
# COLUMNAS PRINCIPALES (1.5 : 1.4 : 1.1)
# ==========================================================
col_left, col_center, col_right = st.columns([1.5, 1.4, 1.1], gap="medium")

# ==========================================================
# PANEL IZQUIERDO: CONTENIDO (Tabla de Contenidos Estructurada)
# ==========================================================
simbologia_sectores = {}
capas_seleccionadas_nombres = []
gdf_usuario = None
nombre_capa_usuario = ""

with col_left:
    with st.container(height=780, border=True):
        st.markdown("<h4 style='color: #1e1e1e; margin-top:0; margin-bottom:5px;'>📊 Contents</h4>", unsafe_allow_html=True)
        st.caption("Estructura de Desplegables Cartográficos")
        
        # --------------------------------------------------
        # GRUPO 1: IMPORT EXTERNAL SHAPEFILE (.ZIP) - CERRADO POR DEFECTO
        # --------------------------------------------------
        with st.expander("📁 Import External Shapefile (.zip)", expanded=False):
            archivo_subido = st.file_uploader(
                "Subir archivo comprimido adicional:",
                type=["zip"],
                key="uploader_manual"
            )
            if archivo_subido is not None:
                try:
                    with tempfile.TemporaryDirectory() as tmpdir:
                        path_zip = os.path.join(tmpdir, archivo_subido.name)
                        with open(path_zip, "wb") as f:
                            f.write(archivo_subido.getbuffer())
                        with zipfile.ZipFile(path_zip, "r") as zip_ref:
                            zip_ref.extractall(tmpdir)
                        archivos_shp = glob.glob(os.path.join(tmpdir, "**", "*.shp"), recursive=True)
                        if archivos_shp:
                            gdf_usuario = gpd.read_file(archivos_shp[0]).to_crs("EPSG:4326")
                            gdf_usuario = sanitizar_geodataframe(gdf_usuario)
                            nombre_capa_usuario = os.path.basename(archivos_shp[0]).replace(".shp", "")
                            st.success(f"Capa '{nombre_capa_usuario}' cargada.")
                        else:
                            st.error("No hay archivo .shp dentro del .zip.")
                except Exception as e:
                    st.error(f"Error externo: {e}")
            
            if gdf_usuario is not None and not gdf_usuario.empty:
                st.markdown("---")
                ver_capa_usuario = st.checkbox(f"✨ {nombre_capa_usuario}", value=False)
                if ver_capa_usuario:
                    # Se le asigna un Key único para congelar su estado cerrado
                    with st.expander(f"🎨 Simbología - {nombre_capa_usuario}", expanded=False, key=f"exp_user_{nombre_capa_usuario}"):
                        c1, c2 = st.columns(2)
                        with c1: fill_u = st.color_picker("Relleno:", "#9b59b6", key="f_user")
                        with c2: stroke_u = st.color_picker("Borde:", "#8e44ad", key="s_user")
                        o1, o2 = st.columns(2)
                        with o1: opac_f_u = st.slider("Opac. Relleno:", 0.0, 1.0, 0.4, step=0.1, key="sl_f_user")
                        with o2: opac_s_u = st.slider("Opac. Borde:", 0.0, 1.0, 1.0, step=0.1, key="sl_s_user")
                        simbologia_sectores[nombre_capa_usuario] = {"fillColor": fill_u, "color": stroke_u, "fillOpacity": opac_f_u, "opacity": opac_s_u}

        # --------------------------------------------------
        # GRUPO 2: MAP LAYERS - ABIERTO POR DEFECTO
        # --------------------------------------------------
        with st.expander("🗺️ Map Layers", expanded=False):
            capa_satelite = st.checkbox("Google Satellite Baseline", value=True)
        
        lista_todos_reps = sorted(list(diccionario_capas.keys()))
        capas_institucionales = [c for c in lista_todos_reps if "anp" in c.lower() or "za_" in c.lower() or "pvc" in c.lower()]
        capas_ambitos = [c for c in lista_todos_reps if "ambito" in c.lower()]

        # --------------------------------------------------
        # GRUPO 3: CAPAS INSTITUCIONALES - ABIERTO POR DEFECTO
        # --------------------------------------------------
        with st.expander("🏛️ Capas Institucionales", expanded=False):
            if not capas_institucionales:
                st.caption("No se encontraron capas institucionales en la carpeta data/")
            else:
                for nombre_capa in capas_institucionales:
                    if "anp" in nombre_capa.lower(): nombre_limpio = "ANP RNTAM"
                    elif "za" in nombre_capa.lower(): nombre_limpio = "ZA RNTAM"
                    elif "pvc" in nombre_capa.lower(): nombre_limpio = "PVC RNTAM"
                    else: nombre_limpio = nombre_capa.replace("_", " ")

                    color_fill, color_stroke = "#27ae60", "#1e7e34"
                    opac_f_inicial = 0.0
                    
                    if "za" in nombre_capa.lower():
                        color_fill, color_stroke = "#e67e22", "#d35400"
                        opac_f_inicial = 0.1
                    elif "pvc" in nombre_capa.lower():
                        color_fill, color_stroke = "#ffffff", "#8b0000"
                        opac_f_inicial = 0.8

                    activo = st.checkbox(f"🔰 {nombre_limpio}", value=True, key=f"chk_{nombre_capa}")
                    if activo:
                        capas_seleccionadas_nombres.append(nombre_capa)
                        # SOLUCCIÓN: Key única vinculada al bucle para bloquear el estado cerrado por defecto
                        with st.expander(f"🎨 Symbology - {nombre_limpio}", expanded=False, key=f"exp_inst_{nombre_capa}"):
                            c1, c2 = st.columns(2)
                            with c1: fill_c = st.color_picker("Relleno:", color_fill, key=f"f_{nombre_capa}")
                            with c2: stroke_c = st.color_picker("Borde:", color_stroke, key=f"s_{nombre_capa}")
                            o1, o2 = st.columns(2)
                            with o1: opac_f_c = st.slider("Opac. Relleno:", 0.0, 1.0, opac_f_inicial, step=0.1, key=f"sf_{nombre_capa}")
                            with o2: opac_s_c = st.slider("Opac. Borde:", 0.0, 1.0, 1.0, step=0.1, key=f"ss_{nombre_capa}")
                            simbologia_sectores[nombre_capa] = {"fillColor": fill_c, "color": stroke_c, "fillOpacity": opac_f_c, "opacity": opac_s_c}

        # --------------------------------------------------
        # GRUPO 4: ÁMBITOS DE CONTROL - CERRADO POR DEFECTO
        # --------------------------------------------------
        with st.expander("📂 Ámbitos de Control", expanded=False):
            if not capas_ambitos:
                st.caption("No se encontraron ámbitos de control en la carpeta data/")
            else:
                for nombre_capa in capas_ambitos:
                    nombre_limpio = nombre_capa.replace("Ambito_de_control_", "Ambito de control ").replace("_", " ")
                    
                    color_fill, color_stroke = "#b22222", "#5c0000"
                    if "azul" in nombre_capa.lower(): color_fill, color_stroke = "#2980b9", "#1a4f73"
                    elif "malinowski" in nombre_capa.lower(): color_fill, color_stroke = "#e74c3c", "#781e1e"
                    elif "otorongo" in nombre_capa.lower(): color_fill, color_stroke = "#d35400", "#8e2a00"
                    elif "yarinal" in nombre_capa.lower(): color_fill, color_stroke = "#f39c12", "#b77000"
                    
                    activo = st.checkbox(f"🔸 {nombre_limpio}", value=False, key=f"chk_{nombre_capa}")
                    if activo:
                        capas_seleccionadas_nombres.append(nombre_capa)
                        # SOLUCCIÓN: Key única vinculada al bucle para bloquear el estado cerrado por defecto
                        with st.expander(f"🎨 Symbology - {nombre_limpio}", expanded=False, key=f"exp_amb_{nombre_capa}"):
                            c1, c2 = st.columns(2)
                            with c1: fill_c = st.color_picker("Relleno:", color_fill, key=f"f_{nombre_capa}")
                            with c2: stroke_c = st.color_picker("Borde:", color_stroke, key=f"s_{nombre_capa}")
                            o1, o2 = st.columns(2)
                            with o1: opac_f_c = st.slider("Opac. Relleno:", 0.0, 1.0, 0.3, step=0.1, key=f"sf_{nombre_capa}")
                            with o2: opac_s_c = st.slider("Opac. Borde:", 0.0, 1.0, 1.0, step=0.1, key=f"ss_{nombre_capa}")
                            simbologia_sectores[nombre_capa] = {"fillColor": fill_c, "color": stroke_c, "fillOpacity": opac_f_c, "opacity": opac_s_c}

# ==========================================================
# LÓGICA DE CONTROL DE ENCUADRE Y CÁLCULO CARTOGRÁFICO
# ==========================================================
gdfs_activos = [diccionario_capas[n] for n in capas_seleccionadas_nombres if n in diccionario_capas]
if gdf_usuario is not None and 'ver_capa_usuario' in locals() and ver_capa_usuario:
    gdfs_activos.append(gdf_usuario)

if gdfs_activos:
    gdfs_combinados = pd.concat(gdfs_activos, ignore_index=True)
    bounds = gdfs_combinados.total_bounds
    
    ha_afectadas = sum(datos_deforestacion_exclusiva.get(p, 0.0) for p in capas_seleccionadas_nombres)
    factor = len([n for n in capas_seleccionadas_nombres if "ambito" in n.lower()])
    cant_alertas = max(3, factor * 8) if factor > 0 else 3
    texto_delta = f"{len(gdfs_activos)} capas activas"
    
    datos_grafico = {n.replace("Ambito_de_control_", "PVC "): datos_deforestacion_exclusiva[n] for n in capas_seleccionadas_nombres if n in datos_deforestacion_exclusiva and datos_deforestacion_exclusiva[n] > 0}
else:
    bounds = [-69.8, -13.1, -69.2, -12.5] 
    ha_afectadas = 1241.60  
    cant_alertas = 3
    texto_delta = "Filtro Base Institucional"
    datos_grafico = {}

reporte_dinamico = """
El análisis geoespacial enfocado de forma exclusiva en los sectores activos del catálogo muestra los escenarios de control vinculados a actividades de minería aurífera ilegal. La cuantificación detallada en estas zonas específicas revela el impacto directo sobre la cobertura boscosa que altera los ecosistemas protegidos dentro del área de influencia analizada.

La información técnica procesada en esta vista proporciona los elementos de convicción geoespaciales necesarios para coordinar con la FEMA y las fuerzas del orden, orientando los recursos logísticos y de personal hacia los puntos calientes con mayor densidad de afectación.
"""

# ==========================================================
# PANEL CENTRAL (MÉTRICAS Y VISOR CARTOGRÁFICO DE COMANDO)
# ==========================================================
with col_center:
    st.markdown("<h3 style='color:#163b16; margin:0;'>📊 MÉTRICAS DE FISCALIZACIÓN TÁCTICA</h3>", unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    with m1: st.metric(label="🚨 Área Deforestada Seleccionada", value=f"{ha_afectadas:,.2f} Ha", delta=texto_delta, delta_color="inverse")
    with m2: st.metric(label="📡 Alertas Críticas Activas", value=str(cant_alertas), delta="Focos Detectados en Capa", delta_color="inverse")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#163b16; margin:0 0 10px 0;'>🗺️ VISOR DE COMANDO Y CONTROL</h3>", unsafe_allow_html=True)

    centro_mapa = [(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2]
    m = folium.Map(location=centro_mapa, zoom_start=11, control_scale=True)
    
    if capa_satelite:
        url_satelite = "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"
        folium.TileLayer(tiles=url_satelite, attr="Google Maps Satellite", name="Vista Satelital Operativa", overlay=False, control=False).add_to(m)

    # --- SOLUCIÓN DE BUG DE INICIALIZACIÓN DE ENTORNO DE PUNTOS ---
    fg_puntos = folium.FeatureGroup(name="Puntos de Control")
    hay_puntos = False

    # Renderizado dinámico seguro
    for nombre_capa in capas_seleccionadas_nombres:
        if nombre_capa in diccionario_capas and nombre_capa in simbologia_sectores:
            gdf_render = diccionario_capas[nombre_capa]
            config = simbologia_sectores[nombre_capa]
            
            if not gdf_render.empty and gdf_render.geometry.geom_type.iloc[0] == 'Point':
                hay_puntos = True
                for idx, row in gdf_render.iterrows():
                    if row.geometry:
                        coords = [row.geometry.y, row.geometry.x]
                        folium.CircleMarker(
                            location=coords,
                            radius=7,
                            popup=f"<b>Ubicación:</b><br>{nombre_capa.replace('_', ' ')}",
                            color=config["color"],
                            weight=2,
                            fill=True,
                            fill_color=config["fillColor"],
                            fill_opacity=config["opacity"]
                        ).add_to(fg_puntos)
            else:
                folium.GeoJson(
                    gdf_render,
                    name=f"📂 {nombre_capa.replace('_', ' ')}",
                    style_function=lambda x, f_c=config['fillColor'], s_c=config['color'], f_o=config['fillOpacity'], s_o=config['opacity']: {
                        'fillColor': f_c,
                        'color': s_c,
                        'weight': 2.5 if "anp" not in nombre_capa.lower() else 3.5,
                        'fillOpacity': f_o,
                        'opacity': s_o
                    }
                ).add_to(m)

    # Añadir los puntos al mapa de Folium únicamente si fueron procesados
    if hay_puntos:
        fg_puntos.add_to(m)

    # --- PINTAR LA CAPA COMPLEMENTARIA SUBIDA POR EL USUARIO ---
    if gdf_usuario is not None and 'ver_capa_usuario' in locals() and ver_capa_usuario:
        cfg_u = simbologia_sectores.get(nombre_capa_usuario, {"fillColor": "#9b59b6", "color": "#8e44ad", "fillOpacity": 0.4, "opacity": 1.0})
        folium.GeoJson(
            gdf_usuario,
            name=f"✨ {nombre_capa_usuario}",
            style_function=lambda x, f_c=cfg_u['fillColor'], s_c=cfg_u['color'], f_o=cfg_u['fillOpacity'], s_o=cfg_u['opacity']: {
                'fillColor': f_c,
                'color': s_c,
                'weight': 2.5,
                'fillOpacity': f_o,
                'opacity': s_o
            }
        ).add_to(m)

    m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    st_folium(m, width="100%", height=420, returned_objects=[])

# ==========================================================
# PANEL DERECHO (ANÁLISIS EXCLUSIVO DE PÉRDIDA BOSCOSA)
# ==========================================================
with col_right:
    with st.container(height=780, border=True):
        st.markdown("<h3 style='text-align:center; color:#8b0000; margin-top:0;'>📉 PÉRDIDA BOSCOSA</h3>", unsafe_allow_html=True)
        
        if datos_grafico:
            df_def = pd.DataFrame(list(datos_grafico.items()), columns=["Sector", "Hectáreas"])
            df_def = df_def.sort_values(by="Hectáreas", ascending=False)
            
            lista_colores_grafico = [simbologia_sectores.get(sec.replace("PVC ", "Ambito_de_control_"), {"fillColor": "#b22222"})["fillColor"] for sec in df_def["Sector"]]
            st.bar_chart(df_def.set_index("Sector"), y="Hectáreas", color=lista_colores_grafico[0] if lista_colores_grafico else "#b22222", horizontal=True, height=210)
        else:
            st.info("Active ámbitos en el panel izquierdo para poblar las estadísticas de pérdida.")
            st.markdown("<div style='height:165px;'></div>", unsafe_allow_html=True)
        
        st.markdown("<hr style='margin:10px 0;'>", unsafe_allow_html=True)
        st.markdown("#### 📋 INFORME SITUACIONAL DEL FRENTE")
        
        st.markdown(reporte_dinamico)
