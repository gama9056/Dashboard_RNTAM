import streamlit as st

# ========== CONFIGURACIÓN DE PÁGINA ==========
st.set_page_config(page_title="Dashboard RNTambopata", layout="wide", page_icon="🌿")

# ========== DISEÑO DE CUADRÍCULA SIMÉTRICA (ESQUELETO VACÍO MEJORADO) ==========
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
