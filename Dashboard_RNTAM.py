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

# Primera fila de columnas (25% - 50% - 25%)
col_left, col_center, col_right = st.columns([1, 2, 1])
