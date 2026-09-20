import streamlit as st
import numpy as np
import plotly.graph_objects as go
if st.button("Mostrar datos curiosos"):
    st.info("La constante de Hubble fue nombrada por Edwin Hubble.")
    st.balloons() # ¡Esto lanza globos en la pantalla!
st.set_page_config(page_title="Q.A.S.T. Engine", layout="centered")

st.title("Q.A.S.T. Engine")
st.write("Escribe un número y mira el resultado al instante:")

# Aquí está el truco: se calcula solo al escribir


st.title("MOTORQAST Engine")
st.subheader("Modelo de Anclaje Cuántico — Invarianza del Observador")

# H0 Base fijado por el modelo (Planck)
H0_BASE = 67.4

# --- PANEL LATERAL: SELECCIÓN DEL MÉTODO DE INGRESO ---
st.sidebar.header("📥 Entrada de Datos Crudos (NED)")
st.sidebar.write("Selecciona cómo vas a copiar los datos desde la pantalla de la NASA:")

opcion_marcador = st.sidebar.radio(
    "Marco de referencia elegido:"
    ["Usar datos de Helio"]
)

# Inicialización de variables de cálculo
v_obs = 0.0
distancia = 0.0

if opcion_marcador == " Usar datos de Helio":
    st.sidebar.markdown("---")
    st.sidebar.subheader("Datos Heliocéntricos")
    v_obs = st.sidebar.number_input(
        "Copiar de la columna 'cz (Helio) [km/s]':", 
        value=179.0, 
        step=1.0,
        help="Introduce el valor exacto de la primera columna de velocidad en NED (ej. para M33 es -179 o 179). El sistema toma el módulo automáticamente."
    )
    distancia = st.sidebar.number_input(
        "Copiar de la columna 'Distancia media [Mpc]':", 
        value=0.869, 
        step=0.01, 
        format="%.3f",
        help="Introduce el valor de la distancia física independiente que aparece al final de la fila de distancias en NED."
    
    )

# Velocidad de rotación característica (por defecto Vía Láctea)
v_rot = st.sidebar.number_input(
    "Velocidad de Rotación Sistema V_rot (km/s):", 
    value=240.0, 
    step=10.0,
    help="Velocidad de rotación del sistema del observador. Por defecto 240 km/s."
)

# --- PROCESAMIENTO MATEMÁTICO INVIOLABLE (TRAS BAMBALINAS) ---
# Forzamos el uso de valores absolutos para evitar errores si el usuario incluye el signo menos (-) de NED
v_obs_abs = np.abs(v_obs)
distancia_abs = np.abs(distancia)

# Ecuación de corrección exacta de tu paper: V_pec_corr = V_obs - (67.4 * d)
v_pec_corr = np.abs(v_obs_abs - (H0_BASE * distancia_abs))

# Factor de Actividad Cinemática (A) y Ansatz Logarítmico QAST
A = (v_pec_corr / v_rot) * 100.0
h0_aparente = H0_BASE + 2.3 * np.log10(1 + A)


# --- INTERFAZ PRINCIPAL DE RESULTADOS ---
st.markdown("### 📊 Verificación de la Métrica de Anclaje Cuántico")

# Cuadro informativo de blindaje
st.success(
    f"🔒 **Cálculo Blindado con Éxito:** El motor ha procesado los datos de la galaxia. "
    f"La **Velocidad Peculiar Corregida** deducida internamente es de **{v_pec_corr:.2f} km/s**."
)




# Despliegue de métricas principales
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Actividad Cinemática (A)", value=f"{A:.2f}%")
with col2:
    st.metric(label="H₀ Aparente Calculado", value=f"{h0_aparente:.2f} km/s/Mpc")

r = 240.0 # Valor fijo para que sea más fácil

# Cálculos automáticos
actividad = (abs(v) / r) * 100
h0 = 67.4 + (2.3 * np.log10(1 + actividad))

# Mostrar resultados
col1, col2 = st.columns(2)
col1.metric("H0 Aparente", f"{h0:.2f}")
col2.metric("Actividad", f"{actividad:.2f}%")

# Gráfico automático
x = np.linspace(0, 100, 100)
y = 67.4 + (2.3 * np.log10(1 + x))
fig = go.Figure(data=go.Scatter(x=x, y=y, line=dict(color='#00c9ff', width=3)))
fig.update_layout(plot_bgcolor='#0e1117', paper_bgcolor='#0e1117', font_color="white")
st.plotly_chart(fig, use_container_width=True)
