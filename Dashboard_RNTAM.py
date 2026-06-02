import streamlit as st

# ==========================================================
# CONFIGURACIÓN GENERAL
# ==========================================================
st.set_page_config(
    page_title="Dashboard RNTambopata",
    page_icon="🌿",
    layout="wide"
)

# ==========================================================
# ESTILOS CSS
# ==========================================================
st.markdown("""
<style>

.block-container{
    padding-top:1.5rem;
    padding-bottom:1rem;
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
    background:#d9d9d9;
    margin-top:5px;
    margin-bottom:20px;
}

.map-container{
    background:#eef5ee;
    border:1px solid #d9e7d9;
    border-radius:15px;
    padding:40px;
    text-align:center;
    min-height:320px;
}

.stMetric{
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# CABECERA
# ==========================================================
st.markdown("""
<div class="title-container">
<h2 style="
margin:0;
font-weight:bold;
color:#163b16;
">
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

    with st.container(height=540, border=True):

        st.markdown("""
        <h2 style='
        text-align:center;
        color:#163b16;
        margin-bottom:25px;
        '>
        🌱 PANEL DE CONTROL
        </h2>
        """, unsafe_allow_html=True)

        pvc_seleccionados = st.multiselect(
            "🔍 Filtrar por Puesto de Control",
            options=lista_pvc,
            placeholder="Mostrando toda la Reserva..."
        )

        st.markdown("<br>", unsafe_allow_html=True)

        st.info(
            "Seleccione uno o varios Puestos de Vigilancia y Control para actualizar automáticamente los indicadores."
        )

# ==========================================================
# LÓGICA DE FILTRO
# ==========================================================
if pvc_seleccionados:

    factor = len(pvc_seleccionados)

    cant_especies = (1234 // 9) * factor
    cant_visitantes = (8942 // 9) * factor
    cant_alertas = max(1, factor - 6)

    texto_delta = f"{factor} PVC seleccionados"

else:

    cant_especies = 1234
    cant_visitantes = 8942
    cant_alertas = 3

    texto_delta = "Total general de la RNTAM"

# ==========================================================
# PANEL CENTRAL
# ==========================================================
with col_center:

    st.markdown("""
    <h2 style='color:#163b16;'>
    📊 MÉTRICAS CLAVE
    </h2>
    """, unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric(
            label="🦋 Especies registradas",
            value=f"{cant_especies:,}",
            delta=texto_delta
        )

    with m2:
        st.metric(
            label="👥 Visitantes 2025",
            value=f"{cant_visitantes:,}",
            delta=texto_delta
        )

    with m3:
        st.metric(
            label="🔥 Alertas SMART",
            value=str(cant_alertas),
            delta="Riesgo de presiones",
            delta_color="inverse"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <h2 style='color:#163b16;'>
    🗺️ ZONIFICACIÓN Y MONITOREO
    </h2>
    """, unsafe_allow_html=True)

    if pvc_seleccionados:
        texto_mapa = "📍 " + ", ".join(pvc_seleccionados)
    else:
        texto_mapa = "📍 Vista general de la Reserva Nacional Tambopata"

    st.markdown(f"""
    <div class="map-container">

        <h3 style="
        color:#163b16;
        margin-bottom:25px;
        ">
        🗺️ MAPA INTERACTIVO DE LA RESERVA
        </h3>

        <p style="
        font-size:18px;
        font-weight:bold;
        color:#163b16;
        ">
        {texto_mapa}
        </p>

        <br>

        <p style="
        color:#666;
        ">
        Aquí se integrará el mapa Folium con zoom automático,
        filtros espaciales y monitoreo en tiempo real.
        </p>

    </div>
    """, unsafe_allow_html=True)

# ==========================================================
# PANEL DERECHO
# ==========================================================
with col_right:

    with st.container(height=540, border=True):

        st.markdown("""
        <h2 style='
        text-align:center;
        color:#163b16;
        margin-bottom:25px;
        '>
        📢 ACTIVIDAD RECIENTE
        </h2>
        """, unsafe_allow_html=True)

        st.markdown("""
        • Sincronización con SMART activa correctamente.

        • Monitoreo de patrullajes sin alertas rojas.

        • Puestos de vigilancia reportando conformidad.

        • Actualización de registros completada.

        • Datos sincronizados exitosamente.
        """)

        st.markdown("<br>", unsafe_allow_html=True)

        st.success("Sistema operativo y actualizado.")
        
