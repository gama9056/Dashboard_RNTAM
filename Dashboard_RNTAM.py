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

    /* Cajas Contenedoras para los paneles laterales */
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
# 📋 LISTA OFICIAL DE LOS 9 PVC DE LA RNTAM
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

# ===== 🟢 COLUMNA IZQUIERDA (25%) - PANEL DE FILTROS NATIVOS =====
with col_left:
    # Se abre la estructura decorativa
    st.markdown('<div class="side-panel-box">', unsafe_allow_html=True)
    
    # Encabezado estático del panel
    st.markdown('<h3 style="color: #1e3a1e; font-size: 1.2rem; font-weight: bold; margin-top: 0; text-align: center;">🌱 PANEL DE CONTROL</h3>', unsafe_allow_html=True)
    st.markdown('<hr style="border: 0; height: 1px; background-color: #cedfce; margin: 10px 0;">', unsafe_allow_html=True)
    
    st.markdown('<p style="color: #1e3a1e; font-weight: bold; margin-bottom: 8px; font-size: 0.95rem;">🔍 Filtrar por Puesto de Control (PVC):</p>', unsafe_allow_html=True)
    
    # Control interactivo de Streamlit inyectado directamente
    pvc_seleccionados = st.multiselect(
        label="Selecciona uno o varios puntos de interés:",
        options=lista_pvc,
        default=[],
        placeholder="Mostrando toda la Reserva...",
        label_visibility="collapsed"
    )
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<p style='color: #555; font-size: 0.85rem; font-style: italic; text-align: center;'>Usa el buscador de arriba para aislar las estadísticas de un puesto específico.</p>", unsafe_allow_html=True)
    
    # Cierre seguro de la caja
    st.markdown('</div>', unsafe_allow_html=True)


# ===== 🛠️ LÓGICA DE SIMULACIÓN INTERACTIVA (CORREGIDA) =====
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


# ===== 🔵 COLUMNA CENTRAL (50%) - CONTENIDO PRINCIPAL =====
with col_center:
    # Sub-sección: Métricas Clave
    st.markdown('<h3 style="color: #1e3a1e; font-size: 1.2rem; font-weight: bold; margin: 0 0 10px 0;">📊 MÉTRICAS CLAVE</h3>', unsafe_allow_html=True)
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="🦋 Especies registradas", value=f"{cant_especies:,}", delta=texto_delta)
    with m2:
        st.metric(label="👥 Visitantes 2025", value=f"{cant_visitantes:,}", delta=texto_delta)
    with m3:
        st.metric(label="🔥 Alertas SMART", value=str(cant_alertas), delta="Riesgo de presiones", delta_color="inverse")
        
    st.markdown("<br>",
