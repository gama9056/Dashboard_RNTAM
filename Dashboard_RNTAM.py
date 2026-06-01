import streamlit as st

# ========== CONFIGURACIÓN DE PÁGINA ==========
st.set_page_config(page_title="Dashboard RNTambopata", layout="wide", page_icon="🌿")

# ========== DISEÑO DE ESTILOS CSS CORREGIDO ==========
st.markdown("""
<style>
    /* Quitar espacio superior de la app */
    .block-container {
        padding-top: 3rem !important;    
        padding-bottom: 3rem !important; 
    }

    .stAppViewMain > div {
        vertical-align: top;             
    }

    /* Caja contenedora del Título Principal */
    .title-container {
        border: 1px solid #2c5f2d;       
        border-radius: 12px;             
        margin-bottom: 15px;             
        background-color: #fefef7;       
        box-shadow: 0 4px 10px rgba(0,0,0,0.03); 
        
        /* 🚀 NUEVO: Sistema Flexbox para centrado vertical perfecto */
        display: flex;
        align-items: center;        /* Centra el texto verticalmente de forma matemática */
        justify-content: center;     /* Centra el texto horizontalmente */
        height: 60px;               /* 💡 GRADUACIÓN: Cambia este número (ej. 50px, 70px) para hacer la caja más delgada o alta */
    }
</style>
""", unsafe_allow_html=True)

# ===========================================================================
# 1. 📦 CAJA DEL TÍTULO PRINCIPAL (AISLADA EN SU PROPIO CUADRO VERDE)
# ===========================================================================
st.markdown("""
<div class="title-container">
    /* 🚀 CAMBIO: Quitamos padding-bottom y dejamos margin: 0 para evitar que empuje el texto hacia abajo */
    <h2 style="color: #1e3a1e; margin: 0; font-size: 1.8rem; font-weight: bold; line-height: 1;">
        🌿 DASHBOARD - RESERVA NACIONAL TAMBOPATA 🌿
    </h2>
</div>
""", unsafe_allow_html=True)
