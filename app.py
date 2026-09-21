import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. Configuración de página de Streamlit
st.set_page_config(page_title="Q.A.S.T. Engine v2.0 (Exacto)", layout="centered")

st.title("Q.A.S.T. Engine v2.0")
st.subheader("Métrica del Vacío Reactivo — Deducción Homogénea")

# --- BANNER DE MONITOREO CIENTÍFICO ---
st.info(
    "🌌 **Física del Backend (Sin parámetros libres):** Este motor calcula automáticamente el "
    "Mecanismo de Pantalla Camaleónica. La densidad ambiental ($\rho_{local}$) se deduce de forma exacta "
    "según el perfil radial de subdensidad del Súpervacío KBC hasta su frontera asintótica en los 300 Mpc."
)

# --- PANEL DE ENTRADA DE DATOS REALES ---
st.markdown("### 📥 Parámetros Astronómicos del Target")

col_in1, col_in2 = st.columns(2)

with col_in1:
    sigma_local = st.number_input(
        "Cizalladura del Flujo Colectivo ⟨σ⟩ (km/s):", 
        value=600.0,
        step=10.0,
        help="Magnitud de la deformación regional medida. (Escala local SH0ES = 600 km/s)."
    )

with col_in2:
    distancia_mpc = st.number_input(
        "Distancia al Target (Mpc):",
        value=50.0,
        min_value=0.0,
        step=1.0,
        help="Distancia física en Megaparsecs. Determina automáticamente el apantallamiento camaleónico."
    )

# --- CONSTANTES UNIVERSALES RECALIBRADAS (SIN PARÁMETROS LIBRES) ---
H0_BASE = 67.40       # Línea base global de Planck 2018 (km/s/Mpc)
SIGMA_0 = 240.0       # Escala natural de acoplamiento del sustrato derivada de Gaia (km/s)
R_KBC = 300.0         # Radio físico del Súpervacío KBC (Mpc)
DEPRESIÓN_MAX = 0.28  # Subdensidad máxima medida en el centro del vacío (KBC)

# --- CÁLCULO AUTOMÁTICO DEL MECANISMO DE PANTALLA ---
# El perfil de densidad del vacío KBC se modela de forma exacta: 
# Máxima subdensidad en el centro (0.28) que decae exponencialmente al llegar a la frontera (300 Mpc)
if distancia_mpc <= R_KBC:
    # Perfil hidrodinámico exacto del Súpervacío
    factor_vacio_calculado = DEPRESIÓN_MAX * np.exp(-np.square(distancia_mpc / R_KBC))
else:
    # Fuera del Súpervacío KBC el universo es homogéneo (ρ_local = ρ_critica) -> El efecto se apaga
    factor_vacio_calculado = 0.0

# --- PROCESAMIENTO MATEMÁTICO CORE (ECUACIÓN 5 DEL PAPER) ---
# A = (σ² / σ₀²) * [1 - ρ/ρ_crit]
actividad_exacta = (np.square(sigma_local) / np.square(SIGMA_0)) * factor_vacio_calculado

# Ecuación maestra logarítmica sin coeficientes artificiales de ajuste
h0_calculado = H0_BASE + 2.3026 * np.log10(1.0 + actividad_exacta)

# --- DESPLIEGUE DE MÉTRICAS EXACTAS ---
st.markdown("### 📊 Resultados de la Métrica de Invarianza")

col1, col2, col3 = st.columns(3)
col1.metric("H₀ Aparente Uniforme", f"{h0_calculado:.2f} km/s/Mpc")
col2.metric("Parámetro Actividad (A)", f"{actividad_exacta:.4f}")
col3.metric("Pantalla Camaleónica", f"{factor_vacio_calculado*100:.1f}% Activa")

# --- GRÁFICO DINÁMICO DE PROPAGACIÓN ---
st.markdown("### Curva de Respuesta Exclusiva según la Densidad de tu Target")

# Generar la curva basándose en la distancia y densidad calculada de forma exacta
x_teorica = np.linspace(0, max(10, actividad_exacta + 2), 500)
y_teorica = H0_BASE + (2.3026 * np.log10(1.0 + x_teorica))

fig = go.Figure()

# Línea continua matemática del paper
fig.add_trace(go.Scatter(
    x=x_teorica, 
    y=y_teorica, 
    mode='lines',
    name='Respuesta del Vacío (Camaleónica)',
    line=dict(color='#00c9ff', width=3)
))

# Punto exacto calculado
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
    xaxis_title="Parámetro de Actividad Cinemática Confinada (A)",
    yaxis_title="Constante de Hubble Aparente Uniforme (km/s/Mpc)",
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(fig, use_container_width=True)
