import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Configuración de página amplia
st.set_page_config(page_title="Q.A.S.T. Engine", layout="wide")

# Estilo visual oscuro tipo Dashboard
st.markdown("""
    <style>
    .main {background-color: #0e1117;}
    .stMetric {background-color: #1c2533; padding: 15px; border-radius: 10px;}
    </style>
""", unsafe_allow_html=True)

# Encabezado
st.title("Q.A.S.T. | MOTOR DE CÁLCULO")

# --- FILA SUPERIOR: MÉTRICAS ---
col1, col2, col3, col4 = st.columns(4)
v_input = 0.0 # Valor por defecto
col1.metric("V_PECULIAR", "0.00 km/s")
col2.metric("ACTIVIDAD (A)", "0.00%")
col3.metric("H0 APARENTE", "67.40")
col4.metric("RESIDUO", "0.00")

# --- FILA INFERIOR: ENTRADA Y GRÁFICO ---
left_col, right_col = st.columns([1, 3])

with left_col:
    st.subheader("Modo de Entrada")
    if st.button("V_peculiar"): pass
    st.number_input("VELOCIDAD PECULIAR (KM/S)", key="vel")
    st.divider()
    st.write("ANCLAJE ROT.")
    st.metric("", "240")

with right_col:
    st.subheader("Análisis Curvo de Hubble")
    # Generar gráfico simple de ejemplo
    x = np.linspace(0, 100, 100)
    y = 67.4 + (2.3 * np.log10(1 + x))
    fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines', line=dict(color='#00c9ff', width=3)))
    fig.update_layout(plot_bgcolor='#0e1117', paper_bgcolor='#0e1117', font_color="white")
    st.plotly_chart(fig, use_container_width=True)
