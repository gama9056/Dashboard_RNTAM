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

    /* Columnas laterales decorativas (Paneles Izquierdo y Derecho) */
    .side-decor {
        background-color: #eaf7ea;       /* 🎨 PERSONALIZAR: Color de fondo verde claro natural */
        min-height: 500px;               /* 📐 PERSONALIZAR: Altura mínima de las cajas laterales para estirarlas hacia abajo */
        border-radius: 12px;             /* 📐 PERSONALIZAR: Redondeo de esquinas de las cajas laterales */
        padding: 20px;                   /* 📐 PERSONALIZAR: Espacio interno para que el texto no choque con los bordes */
        color: #2c5f2d;                  /* 🎨 PERSONALIZAR: Color de las letras y títulos dentro de estos paneles */
        border: 1px dashed #97bc62;      /* 🎨 PERSONALIZAR: Estilo del borde: grosor (1px), estilo (dashed = punteado) y color */
        text-align: center;              /* Centra todo el contenido horizontalmente */
    }

    /* Contenedor temporal para el área del Mapa Central */
    .map-container {
        background-color: #e2f0e2;       /* 🎨 PERSONALIZAR: Fondo verde sutil para identificar el espacio del mapa */
        border-radius: 12px;             /* 📐 PERSONALIZAR: Redondeo de las esquinas del cuadro del mapa */
        padding: 60px 20px;              /* 📐 PERSONALIZAR: Espacio vertical (60px) para darle grosor/altura inicial a la caja */
        text-align: center;              /* Centra horizontalmente los textos y emojis del mapa */
        color: #2c5f2d;                  /* 🎨 PERSONALIZAR: Color de las letras temporales del mapa */
        margin-top: 10px;                /* Separación externa con el título superior de la sección */
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

# ===========================================================================
# 2. 🏢 ESTRUCTURA DE COLUMNAS PRINCIPALES (FILA 1: 25% - 50% - 25%)
# ===========================================================================
col_left, col_center, col_right = st.columns([1, 2, 1])

# ===== 🟢 COLUMNA IZQUIERDA (25%) - PANEL DE FILTROS / INFO =====
with col_left:
    st.markdown('<div class="side-decor">', unsafe_allow_html=True)
    st.markdown("🌱 **PANEL DE CONTROL**")
    st.markdown("---")
    st.markdown("🔍 **Filtros rápidos**")
    st.markdown("*(Espacio interactivo para filtros futuros)*")
    st.markdown("</div>", unsafe_allow_html=True)

# ===== 🔵 COLUMNA CENTRAL (50%) - CONTENIDO PRINCIPAL Y MAPA =====
with col_center:
    # Título de sección usando HTML limpio para conservar el estilo natural
    st.markdown('<h3 style="color: #1e3a1e; font-size: 1.2rem; font-weight: 600; margin: 0;">🗺️ ZONIFICACIÓN Y MONITOREO</h3>', unsafe_allow_html=True)
    
    # Caja contenedora del Mapa
    st.markdown("""
    <div class="map-container">
        🗺️ <strong>MAPA INTERACTIVO DE LA RESERVA</strong><br>
        (Aquí se integrará el visor de mapas con las capas geoespaciales correspondientes)
    </div>
    """, unsafe_allow_html=True)

# ===== 🟡 COLUMNA DERECHA (25%) - ALERTAS / ACTIVIDAD =====
with col_right:
    st.markdown('<div class="side-decor">', unsafe_allow_html=True)
    st.markdown("📢 **ACTIVIDAD RECIENTE**")
    st.markdown("---")
    st.markdown("• Monitoreo activo en la reserva sin novedades.")
    st.markdown("</div>", unsafe_allow_html=True)
