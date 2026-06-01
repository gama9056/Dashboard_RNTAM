import streamlit as st

# ========== CONFIGURACIÓN DE PÁGINA ==========
st.set_page_config(page_title="Dashboard RNTambopata", layout="wide", page_icon="🌿")

# ========== DISEÑO DE CUADRÍCULA SIMÉTRICA (ESQUELETO VACÍO MEJORADO) ==========
/* Caja contenedora del Título Principal */
    .title-container {
        border: 2px solid #2c5f2d; /* Verde oscuro natural */
        border-radius: 12px;
        padding: 15px 20px;
        margin-bottom: 25px;
        background-color: #fefef7; /* Fondo sutilmente claro */
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        text-align: center;
    }

# ===========================================================================
# 1. 📦 CAJA DEL TÍTULO PRINCIPAL (AISLADA EN SU PROPIO CUADRO VERDE)
# ===========================================================================
st.markdown("""
<div class="title-container">
    <h2 style="color: #1e3a1e; margin: 0; padding-bottom: 5px; font-size: 1.8rem; font-weight: bold;">
        🌿 DASHBOARD - RESERVA NACIONAL TAMBOPATA 🌿
    </h2>
    <p style="color: #4a6b3c; margin: 0; font-size: 1rem;">
        Monitoreo de biodiversidad, visitas y conservación
    </p>
</div>
""", unsafe_allow_html=True)
