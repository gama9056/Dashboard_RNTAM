import streamlit as st

# ========== CONFIGURACIÓN DE PÁGINA ==========
st.set_page_config(page_title="Dashboard RNTambopata", layout="wide", page_icon="🌿")

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


# ========== CONTENEDOR PRINCIPAL (TODO DENTRO DEL BORDE) ==========
# Abrimos el contenedor principal
st.markdown('<div class="main-border">', unsafe_allow_html=True)

# ✅ TÍTULO Y SUBTÍTULO DENTRO DE UNA CAJA BIEN ALINEADA
st.markdown("""
<div style="text-align: center; padding: 10px 0;">
    <h2 style="color: #1e3a1e; margin: 0; padding-bottom: 5px;">🌿 DASHBOARD - RESERVA NACIONAL TAMBOPATA 🌿</h2>
    <p style="color: #4a6b3c; margin: 0;">Monitoreo de biodiversidad, visitas y conservación</p>
</div>
<hr style="margin: 15px 0; border-color: #d4e6d4;">
""", unsafe_allow_html=True)
