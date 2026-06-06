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
# URL de despliegue sugerida: deepsentinel-jackson-gamaniel-carmona-manturano
# ==========================================================
st.set_page_config(
    page_title="Dashboard RNTAM",
    page_icon="🌿",
    layout="wide"
)

# ==========================================================
# ESTILOS CSS (Estilo Interfaz Avanzado)
# ==========================================================
st.markdown("""
<style>
.block-container{
    padding-top:3rem;
    padding-bottom:1rem;
}
.title-container {
    border: 1px solid #c2d5c2;
    border-radius: 12px;
    background: #f7faf7;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 10px;
    padding: 0 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02);
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
<h2 style="margin:0; font-weight:bold; color:#2e4a3e;">
🌿 Dashboard - Reserva Nacional Tambopata 🌿
</h2>
</div>
""", unsafe_allow_html=True)
st.markdown('<hr class="custom-hr">', unsafe_allow_html=True)

# ==========================================================
# 🗺️ LÓGICA DE SANITIZACIÓN GEOESPACIAL
# ==========================================================
def sanitizar_geodataframe(gdf):
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

diccionario_capas = escanear_capas_locales()

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

def obtener_nombre_operativo(internal_name):
    if "pvc" in internal_name.lower(): return "🔰 PVC RNTAM"
    if "anp" in internal_name.lower(): return "🔰 ANP RNTAM"
    if "za" in internal_name.lower(): return "🔰 ZA RNTAM"
    if "ambito" in internal_name.lower():
        return internal_name.replace("Ambito_de_control_", "🔸 Ámbito de control ").replace("_", " ")
    return f"✨ {internal_name}"

# ==========================================================
# COLUMNAS PRINCIPALES (1 : 2 : 1)
# ==========================================================
col_left, col_center, col_right = st.columns([1, 2, 1], gap="medium")

# ==========================================================
# PANEL IZQUIERDO: CONTENIDO
# ==========================================================
simbologia_sectores = {}
capas_seleccionadas_nombres = []

if "capas_usuario" not in st.session_state:
    st.session_state.capas_usuario = {}

with col_left:
    with st.container(height=780, border=True):
        st.markdown("<h4 style='color: #1e1e1e; margin-top:0; margin-bottom:5px;'>📊 Contents</h4>", unsafe_allow_html=True)
        st.caption("Estructura Cartográfica")
        
        # --------------------------------------------------
        # GRUPO 1: IMPORT EXTERNAL SHAPEFILE (.ZIP)
        # --------------------------------------------------
        with st.expander("📁 Import External Shapefile (.zip)", expanded=False):
            archivos_subidos = st.file_uploader(
                "Subir capas adicionales:",
                type=["zip"],
                key="uploader_manual",
                accept_multiple_files=True
            )
            
            if archivos_subidos:
                for archivo in archivos_subidos:
                    try:
                        with tempfile.TemporaryDirectory() as tmpdir:
                            path_zip = os.path.join(tmpdir, archivo.name)
                            with open(path_zip, "wb") as f:
                                f.write(archivo.getbuffer())
                            with zipfile.ZipFile(path_zip, "r") as zip_ref:
                                zip_ref.extractall(tmpdir)
                            archivos_shp = glob.glob(os.path.join(tmpdir, "**", "*.shp"), recursive=True)
                            
                            if archivos_shp:
                                gdf_temp = gpd.read_file(archivos_shp[0]).to_crs("EPSG:4326")
                                gdf_temp = sanitizar_geodataframe(gdf_temp)
                                nombre_capa_temp = os.path.basename(archivos_shp[0]).replace(".shp", "")
                                
                                if nombre_capa_temp not in st.session_state.capas_usuario:
                                    st.session_state.capas_usuario[nombre_capa_temp] = gdf_temp
                                    st.toast(f"Capa '{nombre_capa_temp}' agregada.", icon="✨")
                    except Exception as e:
                        st.error(f"Error: {e}")
            
            if st.session_state.capas_usuario:
                st.markdown("---")
                st.caption("📦 Capas Temporales")
                for nombre_capa in list(st.session_state.capas_usuario.keys()):
                    c_chk, c_cfg = st.columns([0.8, 0.2])
                    with c_chk:
                        ver_capa = st.checkbox(f"✨ {nombre_capa}", value=False, key=f"chk_user_{nombre_capa}")
                    with c_cfg:
                        with st.popover("⚙️"):
                            st.markdown("**Simbología**")
                            c1, c2 = st.columns(2)
                            with c1: fill_u = st.color_picker("Relleno", "#9b59b6", key=f"f_user_{nombre_capa}")
                            with c2: stroke_u = st.color_picker("Borde", "#8e44ad", key=f"s_user_{nombre_capa}")
                            opac_f_u = st.slider("Opacidad Relleno", 0.0, 1.0, 0.4, step=0.1, key=f"sf_user_{nombre_capa}")
                            opac_s_u = st.slider("Opacidad Borde", 0.0, 1.0, 1.0, step=0.1, key=f"ss_user_{nombre_capa}")
                    
                    simbologia_sectores[nombre_capa] = {"fillColor": fill_u, "color": stroke_u, "fillOpacity": opac_f_u, "opacity": opac_s_u}
                    if ver_capa:
                        capas_seleccionadas_nombres.append(nombre_capa)

        # --------------------------------------------------
        # GRUPO 2: CAPAS INSTITUCIONALES
        # --------------------------------------------------
        with st.expander("🏛️ Capas Institucionales", expanded=False):
            orden_institucional = [
                {"patron": "pvc", "limpio": "PVC RNTAM", "fill": "#ffffff", "stroke": "#8b0000", "opac": 0.8},
                {"patron": "anp", "limpio": "ANP RNTAM", "fill": "#27ae60", "stroke": "#1e7e34", "opac": 0.0},
                {"patron": "za_", "limpio": "ZA RNTAM", "fill": "#e67e22", "stroke": "#d35400", "opac": 0.1}
            ]
            
            lista_todos_reps = list(diccionario_capas.keys())
            capas_encontradas_inst = []
            
            for item in orden_institucional:
                for nombre_capa in lista_todos_reps:
                    if item["patron"] in nombre_capa.lower() and nombre_capa not in capas_encontradas_inst:
                        capas_encontradas_inst.append((nombre_capa, item))
            
            if not capas_encontradas_inst:
                st.caption("No se encontraron capas en data/")
            else:
                for nombre_capa, info in capas_encontradas_inst:
                    c_chk, c_cfg = st.columns([0.8, 0.2])
                    with c_chk:
                        activo = st.checkbox(f"🔰 {info['limpio']}", value=False, key=f"chk_{nombre_capa}")
                    with c_cfg:
                        with st.popover("⚙️"):
                            st.markdown("**Simbología**")
                            c1, c2 = st.columns(2)
                            with c1: fill_c = st.color_picker("Relleno", info["fill"], key=f"f_{nombre_capa}")
                            with c2: stroke_c = st.color_picker("Borde", info["stroke"], key=f"s_{nombre_capa}")
                            opac_f_c = st.slider("Opac. Relleno", 0.0, 1.0, info["opac"], step=0.1, key=f"sf_{nombre_capa}")
                            opac_s_c = st.slider("Opac. Borde", 0.0, 1.0, 1.0, step=0.1, key=f"ss_{nombre_capa}")
                            
                    simbologia_sectores[nombre_capa] = {"fillColor": fill_c, "color": stroke_c, "fillOpacity": opac_f_c, "opacity": opac_s_c}
                    if activo:
                        capas_seleccionadas_nombres.append(nombre_capa)

        # --------------------------------------------------
        # GRUPO 3: ÁMBITOS DE CONTROL
        # --------------------------------------------------
        with st.expander("📂 Ámbitos de Control", expanded=False):
            orden_ambitos_solicitado = [
                "otorongo", "azul", "yarinal", "malinowski", 
                "la_torre", "jorge_chavez", "sandoval", "briolo", "huisene"
            ]
            
            capas_ambitos_encontradas = [c for c in lista_todos_reps if "ambito" in c.lower()]
            capas_ambitos_ordenadas = []
            
            for patron in orden_ambitos_solicitado:
                for nombre_capa in capas_ambitos_encontradas:
                    if patron in nombre_capa.lower() and nombre_capa not in capas_ambitos_ordenadas:
                        capas_ambitos_ordenadas.append(nombre_capa)
            
            if not capas_ambitos_ordenadas:
                st.caption("No se encontraron ámbitos en data/")
            else:
                for nombre_capa in capas_ambitos_ordenadas:
                    nombre_limpio = nombre_capa.replace("Ambito_de_control_", "Ámbito de control ").replace("_", " ")
                    color_fill, color_stroke = "#b22222", "#5c0000"
                    
                    if "azul" in nombre_capa.lower(): color_fill, color_stroke = "#2980b9", "#1a4f73"
                    elif "malinowski" in nombre_capa.lower(): color_fill, color_stroke = "#e74c3c", "#781e1e"
                    elif "otorongo" in nombre_capa.lower(): color_fill, color_stroke = "#d35400", "#8e2a00"
                    elif "yarinal" in nombre_capa.lower(): color_fill, color_stroke = "#f39c12", "#b77000"
                    
                    c_chk, c_cfg = st.columns([0.8, 0.2])
                    with c_chk:
                        activo = st.checkbox(f"🔸 {nombre_limpio}", value=False, key=f"chk_{nombre_capa}")
                    with c_cfg:
                        with st.popover("⚙️"):
                            st.markdown("**Simbología**")
                            c1, c2 = st.columns(2)
                            with c1: fill_c = st.color_picker("Relleno", color_fill, key=f"f_{nombre_capa}")
                            with c2: stroke_c = st.color_picker("Borde", color_stroke, key=f"s_{nombre_capa}")
                            opac_f_c = st.slider("Opac. Relleno", 0.0, 1.0, 0.3, step=0.1, key=f"sf_{nombre_capa}")
                            opac_s_c = st.slider("Opac. Borde", 0.0, 1.0, 1.0, step=0.1, key=f"ss_{nombre_capa}")
                            
                    simbologia_sectores[nombre_capa] = {"fillColor": fill_c, "color": stroke_c, "fillOpacity": opac_f_c, "opacity": opac_s_c}
                    if activo:
                        capas_seleccionadas_nombres.append(nombre_capa)

        # --------------------------------------------------
        # GRUPO 4: MAP LAYERS
        # --------------------------------------------------
        with st.expander("🗺️ Map Layers", expanded=False):
            capa_satelite = st.checkbox("Google Satélite", value=False)

        # --------------------------------------------------
        # ✨ GRUPO 5: 🔄 DRAWING ORDER (MULTISELECT)
        # --------------------------------------------------
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("🔄 Drawing Order", expanded=True):
            capas_ordenadas_para_dibujo = []
            if capas_seleccionadas_nombres:
                st.caption("Orden de dibujo (de izquierda a derecha).")
                
                # Crear diccionario inverso para mostrar nombres amigables
                mapa_nombres_limpios = {n: obtener_nombre_operativo(n) for n in capas_seleccionadas_nombres}
                mapa_inverso = {v: k for k, v in mapa_nombres_limpios.items()}
                nombres_amigables = list(mapa_nombres_limpios.values())
                
                orden_dibujo_usuario = st.multiselect(
                    "Orden de capas a renderizar:",
                    options=nombres_amigables,
                    default=nombres_amigables,
                    key="multiselect_orden",
                    label_visibility="collapsed"
                )
                
                capas_ordenadas_para_dibujo = [mapa_inverso[lbl] for lbl in orden_dibujo_usuario]
            else:
                st.caption("Activa capas para definir su orden.")

# ==========================================================
# LÓGICA DE CONTROL DE ENCUADRE Y CÁLCULO CARTOGRÁFICO
# ==========================================================
gdfs_activos = [diccionario_capas[n] for n in capas_seleccionadas_nombres if n in diccionario_capas]

for n in capas_seleccionadas_nombres:
    if n in st.session_state.capas_usuario:
        gdfs_activos.append(st.session_state.capas_usuario[n])

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
    
    fg_puntos = folium.FeatureGroup(name="Puntos de Control")
    hay_puntos = False
    
    orden_final_renderizado = capas_ordenadas_para_dibujo if capas_seleccionadas_nombres else capas_seleccionadas_nombres

    for nombre_capa in orden_final_renderizado:
        if nombre_capa in diccionario_capas:
            gdf_render = diccionario_capas[nombre_capa]
            config = simbologia_sectores.get(nombre_capa, {"fillColor": "#27ae60", "color": "#1e7e34", "fillOpacity": 0.3, "opacity": 1.0})
            
            if not gdf_render.empty and gdf_render.geometry.geom_type.iloc[0] == 'Point':
                hay_puntos = True
                for idx, row in gdf_render.iterrows():
                    if row.geometry:
                        coords = [row.geometry.y, row.geometry.x]
                        folium.CircleMarker(
                            location=coords,
                            radius=7,
                            popup=f"<b>Ubicación:</b><br>{nombre_capa.replace('_', ' ')}",
                            color=config.get("color", "#1e7e34"),
                            weight=2,
                            fill=True,
                            fill_color=config.get("fillColor", "#27ae60"),
                            fill_opacity=config.get("opacity", 1.0)
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
                
        elif nombre_capa in st.session_state.capas_usuario:
            gdf_user_render = st.session_state.capas_usuario[nombre_capa]
            cfg_u = simbologia_sectores.get(nombre_capa, {"fillColor": "#9b59b6", "color": "#8e44ad", "fillOpacity": 0.4, "opacity": 1.0})
            
            folium.GeoJson(
                gdf_user_render,
                name=f"✨ {nombre_capa}",
                style_function=lambda x, f_c=cfg_u['fillColor'], s_c=cfg_u['color'], f_o=cfg_u['fillOpacity'], s_o=cfg_u['opacity']: {
                    'fillColor': f_c,
                    'color': s_c,
                    'weight': 2.5,
                    'fillOpacity': f_o,
                    'opacity': s_o
                }
            ).add_to(m)
                
    if hay_puntos:
        fg_puntos.add_to(m)
        
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
            
            lista_colores_grafico = [
                simbologia_sectores.get(sec.replace("PVC ", "Ambito_de_control_"), {"fillColor": "#b22222"})["fillColor"] 
                for sec in df_def["Sector"]
            ]
            st.bar_chart(df_def.set_index("Sector"), y="Hectáreas", color=lista_colores_grafico[0] if lista_colores_grafico else "#b22222", horizontal=True, height=210)
        else:
            st.info("Active ámbitos en el panel izquierdo para poblar las estadísticas de pérdida.")
            st.markdown("<div style='height:165px;'></div>", unsafe_allow_html=True)
        
        st.markdown("<hr style='margin:10px 0;'>", unsafe_allow_html=True)
        st.markdown("#### 📋 INFORME SITUACIONAL DEL FRENTE")
        
        st.markdown(reporte_dinamico)
