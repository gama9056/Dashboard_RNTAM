import streamlit as st

# ==========================================================
# CONFIGURACIÓN DE PÁGINA
# ==========================================================
st.set_page_config(
    page_title="Dashboard RNTambopata",
    page_icon="🌿",
    layout="wide"
)

# ==========================================================
# CSS
# ==========================================================
st.markdown("""
<style>

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

.title-container{
    border:1px solid #2c5f2d;
    border-radius:12px;
    background:#fefef7;
    height:60px;
    display:flex;
    align-items:center;
    justify-content:center;
    margin-bottom:10px;
}

.custom-hr{
    border:0;
    height:1px;
    background:#dddddd;
    margin-top:10px;
    margin-bottom:20px;
}

.panel-box{
    border:1px solid #cedfce;
    border-radius:18px;
    background:#f8fbf8;
    padding:20px;
    min-height:540px;
}

.map-box{
    border:1px solid #dce8dc;
    border-radius:18px;
    background:#eef5ee;
    padding:50px;
    text-align:center;
    min-height:320px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# TÍTULO
# ==========================================================
st.markdown("""
<div class="title-container">
<h2 style="margin:0;color:#1e3a1e;">
🌿 DASHBOARD - RESERVA NACIONAL TAMBOPATA 🌿
</h2>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="custom-hr">', unsafe_allow_html=True)

# ==========================================================
# LISTA PVC
# ==========================================================
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

# ==========================================================
# COLUMNAS PRINCIPALES
# ==========================================================
col_left, col_center, col_right = st.columns(
    [1, 2, 1],
    gap="large"
)

# ==========================================================
# PANEL IZQUIERDO
# ==========================================================
with col_left:

    st.markdown("""
    <div class="panel-box">
    <h3 style="text-align:center;color:#1e3a1e;">
    🌱 PANEL DE CONTROL
    </h3>
    </div>
    """, unsafe_allow_html=True)

    pvc_seleccionados = st.multiselect(
        "🔍 Filtrar por Puesto de Control",
        options=lista_pvc,
        placeholder="Mostrando toda la Reserva..."
    )

    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)

    st.info(
        "Usa el filtro para aislar estadísticas de uno o varios PVC."
    )

# ==========================================================
# MÉTRICAS SIMULADAS
# ==========================================================
if pvc_seleccionados:

    cant_especies = (
        1234 // len(lista_pvc)
    ) * len(pvc_seleccionados)

    cant_visitantes = (
        8942 // len(lista_pvc)
    ) * len(pvc_seleccionados)

    cant_alertas = max(
        1,
        len(pvc_seleccionados) - 6
    )

    texto_delta = (
        f"{len(pvc_seleccionados)} PVC seleccionados"
    )

else:

    cant_especies = 1234
    cant_visitantes = 8942
    cant_alertas = 3

    texto_delta = "Total general RNTAM"

# ==========================================================
# COLUMNA CENTRAL
# ==========================================================
with col_center:

    st.subheader("📊 MÉTRICAS CLAVE")

    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric(
            "🦋 Especies registradas",
            f"{cant_especies:,}",
            texto_delta
        )

    with m2:
        st.metric(
            "👥 Visitantes 2025",
            f"{cant_visitantes:,}",
            texto_delta
        )

    with m3:
        st.metric(
            "🔥 Alertas SMART",
            cant_alertas,
            "Riesgo de presiones",
            delta_color="inverse"
        )

    st.markdown("")

    st.subheader("🗺️ ZONIFICACIÓN Y MONITOREO")

    texto_mapa = (
        "Vista general de la Reserva Nacional Tambopata"
        if not pvc_seleccionados
        else "Enfocando: " + ", ".join(pvc_seleccionados)
    )

    st.markdown(f"""
    <div class="map-box">
        <h4>🗺️ MAPA INTERACTIVO DE LA RESERVA</h4>

        <b>{texto_mapa}</b>

        <br><br>

        <span style="color:#666;">
        Aquí irá el mapa Folium con zoom automático.
        </span>
    </div>
    """, unsafe_allow_html=True)

# ==========================================================
# PANEL DERECHO
# ==========================================================
with col_right:

    st.markdown("""
    <div class="panel-box">
    <h3 style="text-align:center;color:#1e3a1e;">
    📢 ACTIVIDAD RECIENTE
    </h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    • Sincronización con SMART activa correctamente.

    • Patrullajes sin alertas rojas.

    • Puestos de vigilancia reportando conformidad.

    • Monitoreo actualizado.

    • Datos sincronizados con éxito.
    """)
