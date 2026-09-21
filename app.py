import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. Configuración de página de Streamlit
st.set_page_config(page_title="Q.A.S.T. Engine v2.0 (Corregido)", layout="centered")

st.title("Q.A.S.T. Engine v2.0")
st.subheader("Métrica del Vacío Reactivo — Deducción Homogénea")

# --- BANNER DE MONITOREO CIENTÍFICO ---
st.info(
    "🌌 **Física del Backend (Primeros Principios):** Corrección de base logarítmica. "
    "El factor $2.3026$ ($\ln 10$) acopla el espacio de fases tensorial utilizando la métrica euleriana "
    "del logaritmo natural de la acción."
)

# --- TABLA DE GUÍA RÁPIDA ---
st.markdown("### 📖 Guía de Calibración Rápida")

presets_astronomicos = {
    "Ingreso Manual ✍️": {"sigma": 0.0, "desc": "Introduce tu valor de velocidad en la casilla de abajo."},
    "Fondo Cósmico (Fondo CMB) 🛰️": {"sigma": 0.0, "desc": "Absoluto reposo cosmológico. El efecto Q.A.S.T. vale cero."},
    "Máser NGC 4258 (Anclaje geométrico) 🌌": {"sigma": 220.0, "desc": "Velocidad de deformación en la galaxia de calibración NGC 4258."},
    "Grupo Local (Entorno Vía Láctea) 🪐": {"sigma": 310.0, "desc": "Velocidad colectiva de nuestro cúmulo inmediato de galaxias."},
    "Escala SH0ES (Burbuja Cinemática Local) 🚀": {"sigma": 600.0, "desc": "Límite regional donde el Flujo Colectivo infla de forma máxima el H₀ aparente."},
}

seleccion = st.selectbox("🎯 Seleccionar un entorno de calibración:", list(presets_astronomicos.keys()))
st.caption(f"ℹ️ *{presets_astronomicos[seleccion]['desc']}*")

# --- PANEL DE ENTRADA DE DATOS ---
st.markdown("### 📥 Parámetro Astronómico")

valor_sigma_base = presets_astronomicos[seleccion]["sigma"]
sigma_local = st.number_input(
    "Cizalladura Flujo Colectivo ⟨σ⟩ (Velocidad Peculiar en km/s):", 
    value=valor_sigma_base,
    min_value=0.0,
    step=10.0,
    key="sigma_input"
)

# --- CONSTANTES UNIVERSALES REALES ---
H0_BASE = 67.40       # Base cosmológica de Planck
SIGMA_0 = 240.0       # Escala de acoplamiento de Gaia (km/s)
DISTANCIA_FIJA = 50.0 # Calibración estándar asumida en el plano local de SH0ES (Mpc)
R_KBC = 300.0         
DEPRESIÓN_MAX = 0.28  

# Cálculo automático de la pantalla camaleónica interna
factor_vacio_calculado = DEPRESIÓN_MAX * np.exp(-np.square(DISTANCIA_FIJA / R_KBC))

# --- PROCESAMIENTO MATEMÁTICO CORE CON LOGARITMO NATURAL ---
# Actividad adimensional cuadrática escalada del nuevo paper
actividad_exacta = (np.square(sigma_local) / np.square(SIGMA_0)) * factor_vacio_calculado

# Ecuación fundamental corregida usando np.log() [Logaritmo Natural]
COEFICIENTE_QAST = 2.302585
h0_calculado = H0_BASE + COEFICIENTE_QAST * np.log(1.0 + actividad_exacta)

# --- DESPLIEGUE DE MÉTRICAS ---
st.markdown("### 📊 Resultados de la Métrica")

col1, col2 = st.columns(2)
col1.metric("H₀ Aparente Uniforme", f"{h0_calculado:.2f} km/s/Mpc")
col2.metric("Parámetro Actividad (A)", f"{actividad_exacta:.4f}")

# --- GRÁFICO DINÁMICO DE PROPAGACIÓN ---
st.markdown("### Curva de Respuesta del Vacío")

x_max_dinamico = max(10.0, actividad_exacta + 2.0)
x_teorica = np.linspace(0, x_max_dinamico, 500)
y_teorica = H0_BASE + (COEFICIENTE_QAST * np.log(1.0 + x_teorica))

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x_teorica, 
    y=y_teorica, 
    mode='lines',
    name='Respuesta del Vacío',
    line=dict(color='#00c9ff', width=3)
))

fig.add_trace(go.Scatter(
    x=[actividad_exacta], 
    y=[h0_calculado], 
    mode='markers+text',
    name='Target Evaluado',
    text=[f"H₀={h0_calculado:.2f}"],
    textposition="top left",
    marker=dict(color='#ff4b4b', size=12, symbol='circle', line=dict(color='white', width=2))
))

fig.update_layout(
    plot_bgcolor='#0e1117', 
    paper_bgcolor='#0e1117', 
    font_color="white",
    xaxis_title="Parámetro de Actividad (A)",
    yaxis_title="Constante de Hubble Aparente Uniforme (km/s/Mpc)",
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(fig, use_container_width=True)
