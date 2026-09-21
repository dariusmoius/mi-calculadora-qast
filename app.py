import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. Configuración de página de Streamlit
st.set_page_config(page_title="Q.A.S.T. Engine v2.0 (Guiado)", layout="centered")

st.title("Q.A.S.T. Engine v2.0")
st.subheader("Métrica del Vacío Reactivo — Deducción Homogénea")

# --- BANNER DE MONITOREO CIENTÍFICO ---
st.info(
    "🌌 **Física del Backend (Sin parámetros libres):** Este motor calcula automáticamente el "
    "Mecanismo de Pantalla Camaleónica. La densidad ambiental se deduce según el "
    "perfil radial de subdensidad del Súpervacío KBC hasta su frontera en los 300 Mpc."
)

# --- TABLA DE GUÍA Y PRESETS REALES ---
st.markdown("### 📖 Guía de Calibración Rápida")
st.markdown(
    "Selecciona un entorno astronómico real de la lista para cargar sus parámetros exactos, "
    "o elige 'Ingreso Manual' para introducir tus propios datos medidos utilizando la tabla como referencia."
)

# Diccionario con los datos reales exactos del Cuadro I del artículo
presets_astronomicos = {
    "Ingreso Manual ✍️": {"sigma": 240.0, "dist": 15.0, "desc": "Introduce tus propios valores en las casillas de abajo."},
    "Fondo Cósmico (Fondo CMB) 🛰️": {"sigma": 0.0, "dist": 0.0, "desc": "Absoluto reposo cosmológico. El efecto Q.A.S.T. vale cero."},
    "Máser NGC 4258 (Anclaje geométrico) 🌌": {"sigma": 220.0, "dist": 7.2, "desc": "Galaxia local utilizada por SH0ES para calibrar distancias mediante máseres de agua."},
    "Grupo Local (Entorno Vía Láctea) 🪐": {"sigma": 310.0, "dist": 2.0, "desc": "Velocidad colectiva de nuestro cúmulo inmediato de galaxias."},
    "Escala SH0ES (Burbuja Cinemática Local) 🚀": {"sigma": 600.0, "dist": 50.0, "desc": "Límite regional donde el Flujo Colectivo infla de forma máxima el H₀ aparente."},
    "Universo Profundo (Fuera de KBC) ☄️": {"sigma": 600.0, "dist": 350.0, "desc": "Más allá de 300 Mpc, la densidad apaga por completo el efecto Q.A.S.T."},
}

# Selector visual en la App
seleccion = st.selectbox("🎯 Seleccionar un entorno de calibración:", list(presets_astronomicos.keys()))

# Mostrar descripción del preset seleccionado
st.caption(f"ℹ️ *{presets_astronomicos[seleccion]['desc']}*")

# --- PANEL DE ENTRADA DE DATOS (CON VALORES DINÁMICOS) ---
st.markdown("### 📥 Parámetros Astronómicos del Target")

col_in1, col_in2 = st.columns(2)

with col_in1:
    # Si es manual permite editar, si es un preset se bloquea con el valor correcto
    valor_sigma_base = presets_astronomicos[seleccion]["sigma"]
    sigma_local = st.number_input(
        "Cizalladura Flujo Colectivo ⟨σ⟩ (Equivale a Velocidad Peculiar en km/s):", 
        value=valor_sigma_base,
        step=10.0,
        help="Magnitud de la deformación regional medida (Bulk Flow)."
    )

with col_in2:
    valor_dist_base = presets_astronomicos[seleccion]["dist"]
    distancia_mpc = st.number_input(
        "Distancia al Target (Mpc):",
        value=valor_dist_base,
        min_value=0.0,
        step=1.0,
        help="Distancia física real en Megaparsecs a la galaxia o estructura."
    )

# --- CONSTANTES UNIVERSALES RECALIBRADAS (CUADRO I) ---
H0_BASE = 67.40       # Línea base global de Planck
SIGMA_0 = 240.0       # Escala natural derivada de Gaia (km/s)
R_KBC = 300.0         # Radio físico del Súpervacío KBC (Mpc)
DEPRESIÓN_MAX = 0.28  # Subdensidad máxima medida en el centro de la burbuja

# --- CÁLCULO AUTOMÁTICO DEL MECANISMO DE PANTALLA ---
if distancia_mpc <= R_KBC:
    # Perfil hidrodinámico exacto del Súpervacío: decae exponencialmente hacia la frontera
    factor_vacio_calculado = DEPRESIÓN_MAX * np.exp(-np.square(distancia_mpc / R_KBC))
else:
    # Fuera del Súpervacío KBC el efecto cuántico queda apantallado por la alta densidad
    factor_vacio_calculado = 0.0

# --- PROCESAMIENTO MATEMÁTICO CORE (ECUACIÓN 5 DEL PAPER) ---
actividad_exacta = (np.square(sigma_local) / np.square(SIGMA_0)) * factor_vacio_calculado
h0_calculado = H0_BASE + 2.3026 * np.log10(1.0 + actividad_exacta)

# --- DESPLIEGUE DE MÉTRICAS ---
st.markdown("### 📊 Resultados de la Métrica de Invarianza")

col1, col2, col3 = st.columns(3)
col1.metric("H₀ Aparente Uniforme", f"{h0_calculado:.2f} km/s/Mpc")
col2.metric("Parámetro Actividad (A)", f"{actividad_exacta:.4f}")
col3.metric("Pantalla Camaleónica", f"{factor_vacio_calculado*100:.1f}% Activa")

# --- GRÁFICO DINÁMICO DE PROPAGACIÓN ---
st.markdown("### Curva de Respuesta Exclusiva según tu Target")

x_teorica = np.linspace(0, max(10, actividad_exacta + 2), 500)
y_teorica = H0_BASE + (2.3026 * np.log10(1.0 + x_teorica))

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x_teorica, 
    y=y_teorica, 
    mode='lines',
    name='Respuesta del Vacío (Camaleónica)',
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
    xaxis_title="Parámetro de Actividad Cinemática Confinada (A)",
    yaxis_title="Constante de Hubble Aparente Uniforme (km/s/Mpc)",
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(fig, use_container_width=True)
