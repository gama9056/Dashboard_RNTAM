import streamlit as st

# ========== CONFIGURACIÓN DE PÁGINA ==========
st.set_page_config(page_title="Dashboard RNTambopata", layout="wide", page_icon="🌿")

# ========== DISEÑO DE ESTILOS CSS CORREGIDO ==========
st.markdown("""
<style>
    /* 🚀 NUEVO: Quitar espacio superior de la app */
    .block-container {
        padding-top: 2rem !important;    /* Reduce el espacio interno superior de la página (por defecto suele ser 6rem). */
        padding-bottom: 2rem !important; /* Ajusta el espacio de abajo para que quede simétrico. */
    }

    .stAppViewMain > div {
        vertical-align: top;             /* Fuerza a que todo el contenido se alinee hacia el tope superior. */
    }

    /* Caja contenedora del Título Principal */
    .title-container {
        border: 1px solid #2c5f2d;       /* Define el marco: grosor (1px), estilo (solid = línea continua) y el color en hexadecimal (verde). */
        border-radius: 12px;             /* Redondea las esquinas de la caja. A más píxeles, más redondas se verán. */
        padding: 0px 20px;               /* El espacio interno: 0px arriba/abajo y 20px a los lados entre el texto y el borde verde. */
        margin-bottom: 15px;             /* El espacio externo inferior: separa la caja del título de lo que pongas abajo (las columnas). */
        background-color: #fefef7;       /* El color de fondo de la caja (en este caso, un tono hueso/crema muy suave). */
        box-shadow: 0 4px 10px rgba(0,0,0,0.03); /* Crea una sombra sutil abajo de la caja para darle un efecto flotante o de relieve. */
        text-align: center;              /* Centra horizontalmente todo el contenido (texto o emojis) que metas dentro de la caja. */
    }
</style>
""", unsafe_allow_html=True)

# ===========================================================================
# 1. 📦 CAJA DEL TÍTULO PRINCIPAL (AISLADA EN SU PROPIO CUADRO VERDE)
# ===========================================================================
st.markdown("""
<div class="title-container">
    <h2 style="color: #1e3a1e; margin: 0; padding-bottom: 5px; font-size: 1.8rem; font-weight: bold;">
        🌿 DASHBOARD - RESERVA NACIONAL TAMBOPATA 🌿
    </h2>
</div>
""", unsafe_allow_html=True)
