import streamlit as st

# ========== CONFIGURACIÓN DE PÁGINA ==========
st.set_page_config(page_title="Dashboard RNTambopata", layout="wide", page_icon="🌿")

# ========== DISEÑO DE ESTILOS CSS CON GUÍA DE PERSONALIZACIÓN ==========
st.markdown("""
<style>
    /* Ajustes del espacio superior de la aplicación */
    .block-container {
        padding-top: 2rem !important;    /* 📐 PERSONALIZAR: Espacio pegado al tope superior */
        padding-bottom: 2rem !important; /* 📐 PERSONALIZAR: Espacio al final de la página */
    }

    .stAppViewMain > div {
        vertical-align: top;             
    }

    /* Caja contenedora del Título Principal */
    .title-container {
        border: 1px solid #2c5f2d;       /* 🎨 PERSONALIZAR: Grosor y color verde del borde */
        border-radius: 12px;             /* 📐 PERSONALIZAR: Redondeo de esquinas */
        margin-bottom: 10px;             /* Separación con la línea divisoria */
        background-color: #fefef7;       /* 🎨 PERSONALIZAR: Color de fondo hueso suave */
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
        background-color: #e0e0e0;       /* 🎨 PERSONALIZAR: Color gris muy claro para no saturar */
        margin-top: 5px;                 
        margin-bottom: 20px;             /* Separación directa con los bloques de abajo */
    }

    /* Columnas laterales decorativas (Paneles Izquierdo y Derecho) */
    .side-decor {
        background-color: #f9fbf9;       /* 🎨 PERSONALIZAR: Fondo verde-grisáceo ultraclaro */
        min-height: 520px;               /* 📐 PERSONALIZAR: Altura para emparejar con el centro */
        border-radius: 12px;             
        padding: 20px;                   
        color: #2c5f2d;                  
        border: 1px dashed #cedfce;      /* 🎨 PERSONALIZAR: Borde punteado suave */
    }

    /* Contenedor del Mapa Central */
    .map-container {
        background-color: #eef5ee;       /* 🎨 PERSONALIZAR: Fondo sutil para el área del mapa */
        border-radius: 12px;             
        padding: 50px 20px;              /* Grosor interno vertical */
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
# 2. 🏢 ESTRUCTURA DE COLUMNAS PRINCIPALES (FILA 1: 25% - 50% - 25%)
# ===========================================================================
col_left, col_center, col_right = st.columns([1, 2, 1])

# ===== 🟢 COLUMNA IZQUIERDA (25%) - PANEL DE FILTROS =====
with col_left:
    st.markdown("""
    <div class="side-decor">
        <h3 style="color: #1e3a1e; font-size: 1.2rem; font-weight: bold; margin-top: 0; text-align: center;">🌱 PANEL DE CONTROL</h3>
        <hr style="border: 0; height: 1px; background-color: #cedfce; margin: 10px 0;">
        <p style="font-size: 0.95rem; text-align: center; color: #555;">🔍 <strong>Filtros rápidos</strong></p>
        <p style="font-size: 0.85rem; text-align: center; color: #777; font-style: italic;">(Espacio interactivo para los selectores de datos futuros)</p>
    </div>
    """, unsafe_allow_html=True)

# ===== 🔵 COLUMNA CENTRAL (50%) - CONTENIDO PRINCIPAL (MÉTRICAS Y MAPA) =====
with col_center:
    # Sub-sección: Métricas Clave
    st.markdown('<h3 style="color: #1e3a1e; font-size: 1.2rem; font-weight: bold; margin: 0 0 10px 0;">📊 MÉTRICAS CLAVE</h3>', unsafe_allow_html=True)
    
    # Grid de 3 columnas nativas de Streamlit para albergar tus tarjetas internas
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="🦋 Especies registradas", value="1,234", delta="+12 este año")
    with m2:
        st.metric(label="👥 Visitantes 2025", value="8,942", delta="↑ 15% vs 2024")
    with m3:
        st.metric(label="🔥 Alertas", value="3", delta="Activas (2 incendios, 1 aviso)", delta_color="inverse")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sub-sección: Zonificación y Mapa
    st.markdown('<h3 style="color: #1e3a1e; font-size: 1.2rem; font-weight: bold; margin: 10px 0 0 0;">🗺️ ZONIFICACIÓN Y MONITOREO</h3>', unsafe_allow_html=True)
    st.markdown("""
    <div class="map-container">
        🗺️ <strong>MAPA INTERACTIVO DE LA RESERVA</strong><br>
        <span style="font-size: 0.85rem; color: #555;">(Aquí se integrará el visor de mapas con las capas geoespaciales correspondientes)</span>
    </div>
    """, unsafe_allow_html=True)

# ===== 🟡 COLUMNA DERECHA (25%) - ACTIVIDAD RECIENTE =====
with col_right:
    st.markdown("""
    <div class="side-decor">
        <h3 style="color: #1e3a1e; font-size: 1.2rem; font-weight: bold; margin-top: 0; text-align: center;">📢 ACTIVIDAD RECIENTE</h3>
        <hr style="border: 0; height: 1px; background-color: #cedfce; margin: 10px 0;">
        <ul style="font-size: 0.9rem; color: #333; padding-left: 20px; line-height: 1.6;">
            <li>Monitoreo activo en la reserva sin novedades críticas.</li>
            <li>Puestos de vigilancia reportando conformidad en tiempo real.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
