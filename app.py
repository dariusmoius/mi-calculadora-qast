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
