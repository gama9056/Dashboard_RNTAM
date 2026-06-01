import streamlit as st

# ========== CONFIGURACIÓN DE PÁGINA ==========
st.set_page_config(page_title="Dashboard Tambopata", layout="wide", page_icon="🌿")

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

# Contenedor principal
st.markdown('<div class="main-border">', unsafe_allow_html=True)

# Título principal
st.markdown('<h2 style="text-align: center; color: #1e3a1e;">🌿 DASHBOARD - RESERVA NACIONAL TAMBOPATA 🌿</h2>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #4a6b3c;">Monitoreo de biodiversidad, visitas y conservación</p>', unsafe_allow_html=True)
st.markdown('---')

# Primera fila de columnas (25% - 50% - 25%)
col_left, col_center, col_right = st.columns([1, 2, 1])

# ===== COLUMNA IZQUIERDA (25%) - PANEL DE FILTROS / INFO =====
with col_left:
    st.markdown('<div class="side-decor">', unsafe_allow_html=True)
    st.markdown("🌱 **PANEL DE CONTROL**")
    st.markdown("---")
    st.markdown("🔍 **Filtros rápidos**")
    st.markdown("*(Aquí irán filtros de fecha, zona, especie)*")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("📌 **Datos clave**")
    st.markdown("- Área protegida: 274,690 ha")
    st.markdown("- Altitud: 200–1,300 msnm")
    st.markdown("---")
    st.markdown("🦜 *Selector de grupos taxonómicos*")
    st.markdown("</div>", unsafe_allow_html=True)

# ===== COLUMNA CENTRAL (50%) - ESTRUCTURA PRINCIPAL =====
with col_center:
    st.markdown('<div class="center-content">', unsafe_allow_html=True)
    
    # --- FILA 1: MÉTRICAS SUPERIORES ---
    st.markdown('<div class="section-title">📈 MÉTRICAS CLAVE</div>', unsafe_allow_html=True)
    
    # 3 columnas para métricas (dentro de la columna central)
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.markdown('<div class="metric-card"><strong>🦋 Especies registradas</strong><br><span style="font-size:28px;">1,234</span><br><span style="font-size:12px;">+12 este año</span></div>', unsafe_allow_html=True)
    with metric_col2:
        st.markdown('<div class="metric-card"><strong>👥 Visitantes 2025</strong><br><span style="font-size:28px;">8,942</span><br><span style="font-size:12px;">↑ 15% vs 2024</span></div>', unsafe_allow_html=True)
    with metric_col3:
        st.markdown('<div class="metric-card"><strong>🔥 Alertas</strong><br><span style="font-size:28px;">3</span><br><span style="font-size:12px;">Activas (2 incendios, 1 aviso)</span></div>', unsafe_allow_html=True)
    
    # LÍNEA DIVISORIA
    st.markdown('<hr>', unsafe_allow_html=True)
    
    # --- FILA 2: GRÁFICO PRINCIPAL (ÁREA PARA MAPA O GRÁFICO DE BARRAS) ---
    st.markdown('<div class="section-title">🗺️ ZONIFICACIÓN Y MONITOREO</div>', unsafe_allow_html=True)
    
    # Aquí irá un mapa de la reserva o gráfico de avistamientos
    st.markdown("""
    <div style="background-color:#e2f0e2; border-radius:12px; padding:40px; text-align:center; color:#2c5f2d; margin:10px 0;">
        🗺️ <strong>MAPA INTERACTIVO DE LA RESERVA</strong><br>
        (Aquí se integrará un mapa con capas de vegetación, puntos de monitoreo, etc.)
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<hr>', unsafe_allow_html=True)
    
    # --- FILA 3: GRÁFICOS SECUNDARIOS (2 COLUMNAS) ---
    st.markdown('<div class="section-title">📊 TENDENCIAS Y COMPARATIVAS</div>', unsafe_allow_html=True)
    
    graph_col1, graph_col2 = st.columns(2)
    with graph_col1:
        st.markdown("""
        <div style="background:#f4f9f4; border-radius:12px; padding:20px; text-align:center; margin:5px;">
            📅 <strong>Avistamientos por mes</strong><br>
            (Gráfico de líneas o barras)
        </div>
        """, unsafe_allow_html=True)
    with graph_col2:
        st.markdown("""
        <div style="background:#f4f9f4; border-radius:12px; padding:20px; text-align:center; margin:5px;">
            🐾 <strong>Top especies observadas</strong><br>
            (Gráfico de barras horizontal)
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ===== COLUMNA DERECHA (25%) - NOTIFICACIONES / DATOS ADICIONALES =====
with col_right:
    st.markdown('<div class="side-decor">', unsafe_allow_html=True)
    st.markdown("📢 **ACTIVIDAD RECIENTE**")
    st.markdown("---")
    st.markdown("• 10:45 - Nuevo avistamiento de jaguar (Zona Norte)")
    st.markdown("• 09:20 - Patrullaje sin novedades")
    st.markdown("• Ayer - 85 visitantes registrados")
    st.markdown("---")
    st.markdown("⚠️ **Alertas climáticas**")
    st.markdown("🌧️ Probabilidad de lluvia: 70%")
    st.markdown("🌡️ Temperatura: 28°C / 22°C")
    st.markdown("---")
    st.markdown("🔄 *Última actualización: hoy*")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Pie de página opcional
st.markdown("""
<div style="text-align: center; color: #7a8e6b; font-size: 12px; margin-top: 20px;">
    🌿 Datos en tiempo real - Sistema de monitoreo Reserva Nacional Tambopata 🌿
</div>
""", unsafe_allow_html=True)
