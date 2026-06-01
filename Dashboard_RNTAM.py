import streamlit as st

# ========== CONFIGURACIÓN DE PÁGINA ==========
st.set_page_config(page_title="Dashboard RNTambopata", layout="wide", page_icon="🌿")

# ========== DISEÑO DE ESTILOS CSS CON GUÍA DE PERSONALIZACIÓN ==========
st.markdown("""
<style>
    /* Ajustes del espacio superior de la aplicación */
    .block-container {
        padding-top: 3rem !important;    /* 📐 PERSONALIZAR: Baja a 1rem o 2rem si quieres el título MÁS PEGADO al borde superior */
        padding-bottom: 3rem !important; /* 📐 PERSONALIZAR: Espacio muerto al final de la página */
    }

    .stAppViewMain > div {
        vertical-align: top;             /* Alinea el bloque base al tope de la pantalla */
    }

    /* Caja contenedora del Título Principal */
    .title-container {
        border: 1px solid #2c5f2d;       /* 🎨 PERSONALIZAR: Grosor (1px), estilo (solid) y color del borde (Hexadecimal) */
        border-radius: 12px;             /* 📐 PERSONALIZAR: Cambia a 0px para esquinas rectas o a 20px para más redondas */
        margin-bottom: 15px;             /* 📐 PERSONALIZAR: Espacio de separación (aire) entre esta caja y las columnas de abajo */
        background-color: #fefef7;       /* 🎨 PERSONALIZAR: Color de fondo. Usa #ffffff si prefieres blanco puro */
        box-shadow: 0 4px 10px rgba(0,0,0,0.03); /* 🎨 PERSONALIZAR: Sombra sutil. Sube 0.03 a 0.10 si quieres una sombra más marcada */
        
        /* Sistema Flexbox para centrado automático */
        display: flex;
        align-items: center;             /* Mantiene el texto centrado verticalmente sin importar la altura de la caja */
        justify-content: center;         /* Mantiene el texto centrado horizontalmente */
        height: 60px;                    /* 📐 PERSONALIZAR: Altura de la caja. Sube a 70px u 80px si notas el texto muy ajustado */
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
