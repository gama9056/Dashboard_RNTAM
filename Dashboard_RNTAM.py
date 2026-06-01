import streamlit as st

# ========== CONFIGURACIÓN DE PÁGINA ==========
st.set_page_config(page_title="Dashboard Tambopata", layout="wide", page_icon="🌿")

# ========== DISEÑO DE CUADRÍCULA SIMÉTRICA (ESQUELETO VACÍO MEJORADO) ==========
st.markdown("""
<style>
    /* Borde exterior principal */
    .main-border {
        border: 2px solid #2c5f2d;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        background-color: #fefef7;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    
    /* Centrar contenido */
    .center-content {
        text-align: center;
        padding: 10px;
    }
    
    /* Tarjetas para métricas */
    .metric-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 15px;
        margin: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border-left: 4px solid #2c5f2d;
        text-align: center;
    }
    
    /* Columna lateral decorativa con estilo natural */
    .side-decor {
        background-color: #eaf7ea;
        min-height: 500px;
        border-radius: 12px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: #2c5f2d;
        font-size: 14px;
        padding: 20px;
        text-align: center;
        border: 1px dashed #97bc62;
    }
    
    /* Títulos de sección */
    .section-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1e3a1e;
        margin-bottom: 15px;
        border-bottom: 2px solid #97bc62;
        display: inline-block;
        padding-bottom: 4px;
    }
    
    hr {
        margin: 25px 0;
        border-color: #d4e6d4;
    }
</style>
""", unsafe_allow_html=True)

# Contenedor principal
st.markdown('<div class="main-border">', unsafe_allow_html=True)

# Título principal
st.markdown('<h2 style="text-align: center; color: #1e3a1e;">🌿 DASHBOARD - RESERVA NACIONAL TAMBOPATA 🌿</h2>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #4a6b3c;">Monitoreo de biodiversidad, visitas y conservación</p>', unsafe_allow_html=True)
st.markdown('---')

# Primera fila de columnas (25% - 50% - 25%)
col_left, col_center, col_right = st.columns([1, 2, 1])
