import streamlit as st

# ========== CONFIGURACIÓN DE PÁGINA ==========
st.set_page_config(page_title="Dashboard RNTambopata", layout="wide", page_icon="🌿")

# ========== DISEÑO DE ESTILOS CSS CON GUÍA DE PERSONALIZACIÓN ==========
st.markdown("""
<style>
    /* Ajustes del espacio superior de la aplicación */
    .block-container {
        padding-top: 2rem !important;    
        padding-bottom: 2rem !important; 
    }

    .stAppViewMain > div {
        vertical-align: top;             
    }

    /* Caja contenedora del Título Principal */
    .title-container {
        border: 1px solid #2c5f2d;       
        border-radius: 12px;             
        margin-bottom: 10px;             
        background-color: #fefef7;       
        box-shadow: 0 4px 10px rgba(0,0,0,0.03); 
        
        display: flex;
        align-items: center;             
        justify-content: center;         
        height: 60px;                    
    }

    /* Estilo para la línea divisoria sutil */
    .custom-hr {
        border: 0;
        height: 1px;                     
        background-color: #e0e0e0;       
        margin-top: 5px;                 
        margin-bottom: 20px;             
    }

    /* 🚀 NUEVO ENFOQUE: Cajas Contenedoras Universales para inyección nativa */
    .side-panel-box {
        background-color: #f9fbf9;       /* 🎨 PERSONALIZAR: Fondo verde-grisáceo claro */
        border: 1px dashed #cedfce;      /* 🎨 PERSONALIZAR: Marco punteado */
        border-radius: 12px;             
        padding: 20px;                   
        min-height: 540px;               /* 📐 PERSONALIZAR: Altura para equiparar columnas */
        margin-bottom: 20px;
    }

    /* Contenedor del Mapa Central */
    .map-container {
        background-color: #eef5ee;       
        border-radius: 12px;             
        padding: 50px 20px;              
        text-align: center;              
        color: #2c5f2d;                  
        margin-top: 10px;                
        border: 1px solid #e0eee0;
    }
</style>
""", unsafe_allow_html=True)

# ===========================================================================
# 1. 📦 CAJA DEL TÍTULO PRINCIPAL
# ===========================================================================
st.markdown("""
<div class="title-container">
    <h2 style="color: #1e3a1e; margin: 0; font-size: 1.8rem; font-weight: bold; line-height: 1;">
        🌿 DASHBOARD - RESERVA NACIONAL TAMBOPATA 🌿
    </h2>
</div>
""", unsafe_allow_html=True)

# LÍNEA DIVISORIA SUTIL
st.markdown('<hr class="custom-hr">', unsafe_allow_html=True)

# ===========================================================================
# 🚀 PRE-PROCESAMIENTO: LISTA OFICIAL DE LOS 9 PVC DE LA RNTAM
# ===========================================================================
lista_pvc = [
    "PVC Otorongo",
    "PVC Azul",
    "PVC Yarinal",
    "PVC Malinowski",
    "PVC La Torre",
    "PVC Jorge Chávez",
    "PVC Sandoval",
    "PVC Briolo",
    "PVC Huisene"
]

# ===========================================================================
# 2. 🏢 ESTRUCTURA DE COLUMNAS PRINCIPALES (FILA 1: 25% - 50% - 25%)
# ===========================================================================
col_left, col_center, col_right = st.columns([1, 2, 1])

# ===== 🟢 COLUMNA IZQUIERDA (25%) - PANEL DE FILTROS NATIVOS INTERNOS =====
with col_left:
    # Abrimos la caja estilizada usando un div limpio contenedor global
    st.markdown('<div class="side-panel-box">', unsafe_allow_html=True)
    
    # Encabezado interno del panel
    st.markdown('<h3 style="color: #1e3a1e; font-size: 1.2rem; font-weight: bold; margin-top: 0; text-align: center;">🌱 PANEL DE CONTROL</h3>', unsafe_allow_html=True)
    st.markdown('<hr style="border: 0; height: 1px; background-color: #cedfce; margin: 10px 0;">', unsafe_allow_html=True)
    
    # Título del filtro interactivo
    st.markdown('<p style="color: #1e3a1e; font-weight: bold; margin-bottom: 5px; font-size: 0.95rem;">🔍 Filtrar por Puesto de Control (PVC):</p>', unsafe_allow_html=True)
    
    # 🎯 CONTROL NATIVO: Al estar dentro del bloque html y el with de la columna, se dibuja adentro perfectamente
    pvc_seleccionados = st.multiselect(
        label="Selecciona uno o varios puntos de interés:",
        options=lista_pvc,
        default=[],
        placeholder="Mostrando toda la Reserva...",
        label_visibility="collapsed" # Escondemos la etiqueta nativa fea para usar nuestro diseño HTML
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p style='color: #555; font-size: 0.85rem; font-style: italic; text-align: center;'>Usa el buscador de arriba para aislar las estadísticas de un puesto específico.</p>", unsafe_allow_html=True)
    
    # Cerramos la caja de forma segura
    st.markdown('</div>', unsafe_allow_html=True)


# ===== 🛠️ LÓGICA DE SIMULACIÓN INTERACTIVA =====
if pvc_seleccionados:
    cant_especies = 1234 // len(lista_pvc) * len(pvc_seleccionados)
    cant_visitantes = 8942 // len(lista_pvc) * len(pvc_seleccionados)
    cant_alertas = max(1, len(pvc_seleccionados) - 6)
    texto_delta = f"Filtrado para {len(pvc_seleccionados)} PVC"
else:
    cant_especies = 1234
    cant_visitantes = 8942
    cant_alertas = 3
    texto_delta = "Total general de la RNTAM"


# ===== 🔵 COLUMNA CENTRAL (50%) - CONTENIDO PRINCIPAL (MÉTRICAS Y MAPA) =====
with col_center:
    # Sub-sección: Métricas Clave
    st.markdown('<h3 style="color: #1e3a1e; font-size: 1.2rem; font-weight: bold; margin: 0 0 10px 0;">📊 MÉTRICAS CLAVE</h3>', unsafe_allow_html=True)
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="🦋 Especies registradas", value=f"{cant_especies:",}", delta=texto_delta)
    with m2:
        st.metric(label="👥 Visitantes 2025", value=f"{cant_visitantes:",}", delta=texto_delta)
    with m3:
        st.metric(label="🔥 Alertas SMART", value=str(cant_alertas), delta="Riesgo de presiones", delta_color="inverse")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sub-sección: Zonificación y Mapa
    st.markdown('<h3 style="color: #1e3a1e; font-size: 1.2rem; font-weight: bold; margin: 10px 0 0 0;">🗺️ ZONIFICACIÓN Y MONITOREO</h3>', unsafe_allow_html=True)
    
    texto_mapa = f"Enfocando visor en: {', '.join(pvc_seleccionados)}" if pvc_seleccionados else "Vista general de la Reserva Nacional Tambopata"
    
    st.markdown(f"""
    <div class="map-container">
        🗺️ <strong>MAPA INTERACTIVO DE LA RESERVA</strong><br>
        <span style="font-size: 0.95rem; color: #1e3a1e; font-weight: bold;">📍 {texto_mapa}</span><br>
        <span style="font-size: 0.85rem; color: #555;">(Pronto reemplazaremos esta caja por el mapa real de Folium con zoom automático)</span>
    </div>
    """, unsafe_allow_html=True)


# ===== 🟡 COLUMNA DERECHA (25%) - ACTIVIDAD RECIENTE =====
with col_right:
    st.markdown('<div class="side-panel-box">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #1e3a1e; font-size: 1.2rem; font-weight: bold; margin-top: 0; text-align: center;">📢 ACTIVIDAD RECIENTE</h3>', unsafe_allow_html=True)
    st.markdown('<hr style="border: 0; height: 1px; background-color: #cedfce; margin: 10px 0;">', unsafe_allow_html=True)
    st.markdown("""
        <ul style="font-size: 0.9rem; color: #333; padding-left: 20px; line-height: 1.6; margin-top: 15px;">
            <li>Sincronización con SMART activa de forma correcta.</li>
            <li>Monitoreo en patrullajes sin alertas rojas hoy.</li>
            <li>Puestos de vigilancia reportando conformidad.</li>
        </ul>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
