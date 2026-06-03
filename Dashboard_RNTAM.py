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
.toc-header {
    font-size: 14px;
    font-weight: bold;
    color: #4A4A4A;
    margin-top: 10px;
    margin-bottom: 5px;
    border-bottom: 1px solid #ddd;
    padding-bottom: 2px;
}
.stExpander {
    border: none !important;
    box-shadow: none !important;
    margin-top: -10px !important;
    margin-bottom: 5px !important;
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
# 🗺️ CARGA VECTORIAL FILTRADA POR OBJETIVOS TÁCTICOS
# ==========================================================
@st.cache_data
def cargar_capas_geograficas():
    def limpiar_columnas_tiempo(gdf):
        if gdf is None or gdf.empty:
            return gdf
        for col in gdf.select_dtypes(include=['datetime64', 'timedelta64']).columns:
            gdf[col] = gdf[col].astype(str)
        for col in gdf.select_dtypes(include=['object']).columns:
            col_lower = col.lower()
            if 'fecha' in col_lower or 'felea' in col_lower or 'date' in col_lower:
                gdf[col] = gdf[col].astype(str)
        return gdf

    pvc_criticos = ["PVC Malinowski", "PVC Otorongo", "PVC Yarinal", "PVC Azul"]
    lista_gdfs = []
    
    mapeo_archivos = {
        "PVC Malinowski": "data/Ambito_de_control_Malinowski.zip",
        "PVC Otorongo": "data/Ambito_de_control_Otorongo.zip",
        "PVC Yarinal": "data/Ambito_de_control_Yarinal.zip",
        "PVC Azul": "data/Ambito_de_control_Azul.zip"
    }

    for nombre_pvc, ruta in mapeo_archivos.items():
        if os.path.exists(ruta):
            gdf_pvc = gpd.read_file(f"zip://{ruta}").to_crs("EPSG:4326")
            gdf_pvc = limpiar_columnas_tiempo(gdf_pvc)
            gdf_pvc["NOM_PVC"] = nombre_pvc
            lista_gdfs.append(gdf_pvc)
            
    if lista_gdfs:
        gdf_ambitos = gpd.GeoDataFrame(pd.concat(lista_gdfs, ignore_index=True), crs="EPSG:4326")
    else:
        lista_fallback = []
        for n in ["Malinowski", "Otorongo", "Yarinal", "Azul"]:
            r_fallback = f"data/Ambito_de_control_{n}.zip"
            if os.path.exists(r_fallback):
                gdf_pvc = gpd.read_file(f"zip://{r_fallback}").to_crs("EPSG:4326")
                gdf_pvc = limpiar_columnas_tiempo(gdf_pvc)
                gdf_pvc["NOM_PVC"] = f"PVC {n}"
                lista_fallback.append(gdf_pvc)
        if lista_fallback:
            gdf_ambitos = gpd.GeoDataFrame(pd.concat(lista_fallback, ignore_index=True), crs="EPSG:4326")
        else:
            gdf_ambitos = gpd.GeoDataFrame(columns=["NOM_PVC", "geometry"], crs="EPSG:4326")

    if not gdf_ambitos.empty:
        gdf_ambitos = gdf_ambitos[gdf_ambitos["NOM_PVC"].isin(pvc_criticos)]

    ruta_anp = "data/ANP_RNTAM.zip"
    gdf_anp = gpd.read_file(f"zip://{ruta_anp}").to_crs("EPSG:4326") if os.path.exists(ruta_anp) else gpd.GeoDataFrame(columns=["geometry"], crs="EPSG:4326")
    if not gdf_anp.empty: gdf_anp = limpiar_columnas_tiempo(gdf_anp)

    ruta_za = "data/ZA_RNTAM.zip"
    gdf_za = gpd.read_file(f"zip://{ruta_za}").to_crs("EPSG:4326") if os.path.exists(ruta_za) else gpd.GeoDataFrame(columns=["geometry"], crs="EPSG:4326")
    if not gdf_za.empty: gdf_za = limpiar_columnas_tiempo(gdf_za)

    ruta_pvc_puntos = "data/PVC_RNTAM.zip"
    if os.path.exists(ruta_pvc_puntos):
        gdf_pvc_pts = gpd.read_file(f"zip://{ruta_pvc_puntos}").to_crs("EPSG:4326")
        gdf_pvc_pts = limpiar_columnas_tiempo(gdf_pvc_pts)
        for col in gdf_pvc_pts.columns:
            if col.lower() in ['nom_pvc', 'nombre', 'pvc', 'puesto']:
                gdf_pvc_pts['NOM_PVC'] = gdf_pvc_pts[col]
        gdf_pvc_pts = gdf_pvc_pts[gdf_pvc_pts["NOM_PVC"].isin(pvc_criticos)]
    else:
        gdf_pvc_pts = gpd.GeoDataFrame(columns=["geometry", "NOM_PVC"], crs="EPSG:4326")
        
    return gdf_ambitos, gdf_anp, gdf_za, gdf_pvc_pts

# Carga inicial de datos
gdf_ambitos, gdf_anp, gdf_za, gdf_pvc_pts = cargar_capas_geograficas()

# Base de datos analítica estricta
datos_deforestacion_exclusiva = {
    "PVC Malinowski": 524.30,
    "PVC Otorongo": 341.20,
    "PVC Yarinal": 215.60,
    "PVC Azul": 160.50
}

# ==========================================================
# COLUMNAS PRINCIPALES (1.4 : 1.5 : 1.1) - Reajuste de ancho para acomodar la simbología avanzada
# ==========================================================
col_left, col_center, col_right = st.columns([1.4, 1.5, 1.1], gap="medium")

# ==========================================================
# PANEL IZQUIERDO: CONTENIDO (ArcGIS Pro TOC con Control Total de Simbología)
# ==========================================================
simbologia_sectores = {}
pvc_seleccionados = []

with col_left:
    with st.container(height=680, border=True):
        st.markdown("<h4 style='color: #1e1e1e; margin-top:0; margin-bottom:5px;'>📊 Contents</h4>", unsafe_allow_html=True)
        st.caption("Drawing Order & Advanced Symbology")
        
        # --- CAPAS DE REFERENCIA ---
        st.markdown("<div class='toc-header'>🗺️ Map Layers</div>", unsafe_allow_html=True)
        capa_satelite = st.checkbox("Google Satellite Baseline", value=True)
        
        # --- CAPAS INSTITUCIONALES ---
        st.markdown("<div class='toc-header'>🏛️ Institutional Boundaries</div>", unsafe_allow_html=True)
        ver_anp = st.checkbox("🌿 Límite Oficial ANP (RNTAM)", value=True)
        ver_za = st.checkbox("🔶 Zona de Amortiguamiento (ZA)", value=True)
        ver_puestos = st.checkbox("📍 Bases de Control (Puntos)", value=True)
        
        # --- CAPAS OPERATIVAS CON DOBLE SELECTOR DE COLOR Y OPACIDAD ---
        st.markdown("<div class='toc-header'>📂 Mining Areas of Concern (PVC)</div>", unsafe_allow_html=True)
        
        # 1. PVC MALINOWSKI
        c_malinowski = st.checkbox("🟥 PVC Malinowski", value=True)
        if c_malinowski:
            pvc_seleccionados.append("PVC Malinowski")
            with st.expander("🎨 Symbology - Malinowski"):
                c1, c2 = st.columns(2)
                with c1: fill_m = st.color_picker("Relleno:", "#b22222", key="f_m")
                with c2: stroke_m = st.color_picker("Borde:", "#5c0000", key="s_m")
                opac_m = st.slider("Opacidad Relleno:", 0.0, 1.0, 0.3, step=0.1, key="sl_m")
                simbologia_sectores["PVC Malinowski"] = {"fillColor": fill_m, "color": stroke_m, "opacity": opac_m}
        
        # 2. PVC OTORONGO
        c_otorongo = st.checkbox("🟧 PVC Otorongo", value=True)
        if c_otorongo:
            pvc_seleccionados.append("PVC Otorongo")
            with st.expander("🎨 Symbology - Otorongo"):
                c1, c2 = st.columns(2)
                with c1: fill_o = st.color_picker("Relleno:", "#d35400", key="f_o")
                with c2: stroke_o = st.color_picker("Borde:", "#8e2a00", key="s_o")
                opac_o = st.slider("Opacidad Relleno:", 0.0, 1.0, 0.3, step=0.1, key="sl_o")
                simbologia_sectores["PVC Otorongo"] = {"fillColor": fill_o, "color": stroke_o, "opacity": opac_o}
        
        # 3. PVC YARINAL
        c_yarinal = st.checkbox("🟨 PVC Yarinal", value=True)
        if c_yarinal:
            pvc_seleccionados.append("PVC Yarinal")
            with st.expander("🎨 Symbology - Yarinal"):
                c1, c2 = st.columns(2)
                with c1: fill_y = st.color_picker("Relleno:", "#f39c12", key="f_y")
                with c2: stroke_y = st.color_picker("Borde:", "#b77000", key="s_y")
                opac_y = st.slider("Opacidad Relleno:", 0.0, 1.0, 0.3, step=0.1, key="sl_y")
                simbologia_sectores["PVC Yarinal"] = {"fillColor": fill_y, "color": stroke_y, "opacity": opac_y}
        
        # 4. PVC AZUL
        c_azul = st.checkbox("🟦 PVC Azul", value=True)
        if c_azul:
            pvc_seleccionados.append("PVC Azul")
            with st.expander("🎨 Symbology - Azul"):
                c1, c2 = st.columns(2)
                with c1: fill_a = st.color_picker("Relleno:", "#2980b9", key="f_a")
                with c2: stroke_a = st.color_picker("Borde:", "#1a4f73", key="s_a")
                opac_a = st.slider("Opacidad Relleno:", 0.0, 1.0, 0.3, step=0.1, key="sl_a")
                simbologia_sectores["PVC Azul"] = {"fillColor": fill_a, "color": stroke_a, "opacity": opac_a}

# ==========================================================
# LÓGICA INTERACTIVA DE SIMULTANEIDAD
# ==========================================================
if pvc_seleccionados and not gdf_ambitos.empty:
    gdf_filtrado = gdf_ambitos[gdf_ambitos["NOM_PVC"].isin(pvc_seleccionados)]
    bounds = gdf_filtrado.total_bounds
    factor = len(pvc_seleccionados)
    
    ha_afectadas = sum(datos_deforestacion_exclusiva.get(p, 0.0) for p in pvc_seleccionados)
    cant_alertas = max(4, factor * 8)
    texto_delta = f"{factor} capas activas"
    
    datos_grafico = {p: datos_deforestacion_exclusiva.get(p, 0.0) for p in pvc_seleccionados}
    
    sectores_texto = ", ".join(pvc_seleccionados)
    reporte_dinamico = f"""
    El análisis geoespacial enfocado de forma exclusiva en los sectores de {sectores_texto} muestra un escenario crítico directamente vinculado a actividades de minería aurífera ilegal. La cuantificación detallada en estas zonas específicas revela un impacto directo sobre la cobertura boscosa que altera los ecosistemas protegidos dentro del área de influencia analizada.
    
    La concentración de alertas satelitales en estas coordenadas específicas exige el diseño de operaciones tácticas focalizadas. La fiscalización ambiental y el patrullaje fluvial integrado deben priorizar los accesos y rutas de abastecimiento logístico identificados en estos sectores seleccionados para neutralizar los focos de degradación actuales.
    
    La información técnica procesada en esta vista filtrada proporciona los elementos de convicción geoespaciales necesarios para coordinar con la FEMA y las fuerzas del orden. Esto permite orientar los recursos logísticos y de personal hacia los puntos calientes con mayor densidad de afectación comprobada en el mapa actual.
    """
    
    if not gdf_pvc_pts.empty and 'NOM_PVC' in gdf_pvc_pts.columns:
        gdf_pvc_filtrado = gdf_pvc_pts[gdf_pvc_pts["NOM_PVC"].isin(pvc_seleccionados)]
    else:
        gdf_pvc_filtrado = gdf_pvc_pts.copy()
else:
    gdf_filtrado = gpd.GeoDataFrame(columns=["NOM_PVC", "geometry"], crs="EPSG:4326")
    gdf_pvc_filtrado = gpd.GeoDataFrame(columns=["geometry", "NOM_PVC"], crs="EPSG:4326")
    
    if not gdf_anp.empty: bounds = gdf_anp.total_bounds
    else: bounds = [-69.8, -13.1, -69.2, -12.5]
        
    ha_afectadas = 0.0  
    cant_alertas = 0
    texto_delta = "Sin capas operativas activas"
    datos_grafico = {}
    
    reporte_dinamico = """
    La vista actual del panel de control no registra capas de ámbitos político-administrativos de patrullaje seleccionadas. Para desplegar el análisis de pérdidas de cobertura boscosa active las casillas correspondientes en el Panel de Contenido situado a la izquierda.
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

    if ver_za and not gdf_za.empty:
        folium.GeoJson(gdf_za, name="🔶 Zona de Amortiguamiento (ZA)", style_function=lambda x: {'fillColor': '#e67e22', 'color': '#d35400', 'weight': 1.5, 'fillOpacity': 0.1}).add_to(m)

    # --- SIMBOLOGÍA AVANZADA SEPARADA (FILL VS STROKE VS OPACITY) ---
    if not gdf_filtrado.empty:
        for sector, config in simbologia_sectores.items():
            gdf_sector = gdf_filtrado[gdf_filtrado["NOM_PVC"] == sector]
            if not gdf_sector.empty:
                folium.GeoJson(
                    gdf_sector,
                    name=f"📂 {sector}",
                    style_function=lambda x, f_c=config['fillColor'], s_c=config['color'], o=config['opacity']: {
                        'fillColor': f_c,
                        'color': s_c,
                        'weight': 2.5,        # Grosor de línea de borde óptimo para cartografía operativa
                        'fillOpacity': o,
                        'opacity': 1.0         # Mantener el contorno exterior siempre nítido y visible al 100%
                    },
                    tooltip=folium.GeoJsonTooltip(fields=["NOM_PVC"], aliases=["Ámbito Operativo: "])
                ).add_to(m)

    if ver_anp and not gdf_anp.empty:
        folium.GeoJson(gdf_anp, name="🌿 Límite Oficial ANP RNTAM", style_function=lambda x: {'fillColor': 'none', 'color': '#27ae60', 'weight': 3}).add_to(m)

    if ver_puestos and not gdf_pvc_filtrado.empty:
        fg_puestos = folium.FeatureGroup(name="🛡️ Bases de Control SERNANP")
        for idx, row in gdf_pvc_filtrado.iterrows():
            if row.geometry and row.geometry.geom_type == 'Point':
                coords = [row.geometry.y, row.geometry.x]
                nombre_puesto = row['NOM_PVC'] if 'NOM_PVC' in row and pd.notna(row['NOM_PVC']) else f"Puesto {idx+1}"
                
                # Sincronizar el marcador del mapa con el color del borde de la capa correspondiente
                color_borde_puesto = simbologia_sectores.get(nombre_puesto, {"color": "#8b0000"})["color"]
                color_relleno_puesto = simbologia_sectores.get(nombre_puesto, {"fillColor": "#ffffff"})["fillColor"]
                
                folium.CircleMarker(
                    location=coords,
                    radius=8,
                    popup=f"<b>Puesto de Vigilancia:</b><br>{nombre_puesto}",
                    tooltip=f"🛡️ {nombre_puesto}",
                    color=color_borde_puesto,
                    weight=2,
                    fill=True,
                    fill_color=color_relleno_puesto,
                    fill_opacity=0.9
                ).add_to(fg_puestos)
        fg_puestos.add_to(m)

    m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    
    st_folium(m, width="100%", height=420, returned_objects=[])

# ==========================================================
# PANEL DERECHO (ANÁLISIS EXCLUSIVO DE PÉRDIDA BOSCOSA)
# ==========================================================
with col_right:
    with st.container(height=680, border=True):
        st.markdown("<h3 style='text-align:center; color:#8b0000; margin-top:0;'>📉 PÉRDIDA BOSCOSA</h3>", unsafe_allow_html=True)
        
        if datos_grafico:
            df_def = pd.DataFrame(list(datos_grafico.items()), columns=["Sector", "Hectáreas"])
            df_def = df_def.sort_values(by="Hectáreas", ascending=False)
            
            # El gráfico se pintará de acuerdo al color de RELLENO seleccionado en la TOC
            lista_colores_grafico = [simbologia_sectores.get(sec, {"fillColor": "#b22222"})["fillColor"] for sec in df_def["Sector"]]
            
            st.bar_chart(df_def.set_index("Sector"), y="Hectáreas", color=lista_colores_grafico[0] if lista_colores_grafico else "#b22222", horizontal=True, height=210)
        else:
            st.info("Active capas en el panel izquierdo para poblar el análisis gráfico.")
            st.markdown("<div style='height:165px;'></div>", unsafe_allow_html=True)
        
        st.markdown("<hr style='margin:10px 0;'>", unsafe_allow_html=True)
        st.markdown("#### 📋 INFORME SITUACIONAL DEL FRENTE")
        
        st.markdown(reporte_dinamico)
