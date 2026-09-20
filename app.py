import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. Configuración de página de Streamlit
st.set_page_config(page_title="Q.A.S.T. Engine", layout="centered")

# Datos curiosos iniciales
if st.button("Mostrar datos curiosos"):
    st.info(
        "📊 **Dato Práctico de la NASA (NED):** Las galaxias con un prefijo 'M' (como M33 o M31) "
        "pertenecen al Catálogo Messier y están en nuestro vecindario cósmico inmediato. Al estar tan cerca, "
        "su gravedad local domina sobre la expansión del tejido espacial, por lo que la base de datos NED suele "
        "mostrar velocidades observadas (cz) con valores negativos. ¡Esto significa que se están acercando a nosotros!"
    )
    st.balloons()

st.title("Q.A.S.T. Engine")
st.subheader("Modelo Herramienta Q.A.S.T. — Métrica del Observador")

# --- BANNER DE CORTE CIENTÍFICO (LÍMITES DE RIESS / SH0ES) ---
st.warning(
    "🌌 **Marco de Calibración Cosmológica (Límite de SH0ES):** "
    "Este motor opera dentro de la Burbuja Cinemática Local delimitada por el radio de la escalera de distancias de Adam Riess "
    " Dentro de este rango, los movimientos del entorno inflan la métrica local. "
    "A escalas macroscópicas superiores (universo profundo), el flujo se vuelve homogéneo e isotrópico, disipando la actividad "
    "cinemática y provocando que el valor medido de H₀ regrese de forma estricta a la base global de Planck (**67.4 km/s/Mpc**)."
)

# --- SECCIÓN DE INSTRUCCIONES PARA EL CÁLCULO ---
with st.expander("📖 Guía de uso: Cómo calcular la Velocidad Peculiar Corregida"):
    st.markdown(
        """
        Para evitar distorsiones por escalas de distancia en el universo profundo, debes ingresar el valor corregido. 
        Sigue estos pasos con los datos de la base de datos **NASA/IPAC (NED)**:
        
        1. **Busca la galaxia** en [NED](https://caltech.edu).
        2. **Identifica las variables crudas**:
            * Extrae la velocidad observada (\(V_{obs}\)): Usa la columna `cz (Helio)` o `cz (CMB)` en km/s.
            * Extrae la distancia (\(d\)): Usa la `Distancia media [Mpc]` (o la de CMB correspondiente).
        3. **Aplica la ecuación de control antes de ingresar el número**:
            \[\text{V}_{pec\_corr} = \vert{}V_{obs} - (67.4 \times d)\vert{}\]
        4. *Ejemplo (Messier 065)*: 
            * Con \(V_{obs} = 808.5 \text{ km/s}\) y \(d = 12.229 \text{ Mpc}\) 
            * Cálculo: \(\vert{}808.5 - (67.4 \times 12.229)\vert{} = \mathbf{15.29 \text{ km/s}}\).
        """
    )

# --- ENTRADA DE DATOS SIMPLIFICADA (COMO ANTES) ---
st.markdown("### 📥 Entrada de Parámetros")

# El usuario ingresa directamente la velocidad peculiar ya corregida matemáticamente
v_pec_corr_input = st.number_input(
    "Velocidad Peculiar Corregida (km/s):", 
    value=0 
    step=0.1,
    help="Ingresa el resultado absoluto de la ecuación: |V_obs - 67.4*d|. Asegúrate de estar dentro del rango local."
)

v_rot = st.number_input(
    "Velocidad de Rotación Sistema V_rot (km/s):", 
    value=240.0, 
    step=10.0,
    help="Velocidad de rotación de la galaxia del observador. Por defecto se usan 240 km/s (Vía Láctea)."
)

# --- PROCESAMIENTO MATEMÁTICO CORE ORIGINAL ---
H0_BASE = 67.4
v_pec_corr_abs = np.abs(v_pec_corr_input)

# Factor de Actividad Cinemática (A) basado en tu fórmula matemática pura
actividad = (v_pec_corr_abs / v_rot) * 100.0

# Ansatz Logarítmico del Tensor de Anclaje Cuántico
h0 = H0_BASE + 2.3 * np.log10(1.0 + actividad)


# --- DESPLIEGUE DE MÉTRICAS ---
st.markdown("### 📊 Resultados de la Métrica")

col1, col2 = st.columns(2)
col1.metric("H₀ Aparente Calculado", f"{h0:.2f} km/s/Mpc")
col2.metric("Actividad Cinemática (A)", f"{actividad:.2f}%")


# --- GRÁFICO DINÁMICO E INTERACTIVO ---
st.markdown("### Posición del Objeto sobre la Curva Teórica QAST")

# Generar la curva base del modelo adaptada dinámicamente al punto introducido
x_teorica = np.linspace(0, max(200, actividad + 20), 500)
y_teorica = H0_BASE + (2.3 * np.log10(1.0 + x_teorica))

fig = go.Figure()

# Línea continua de la ecuación matemática del paper
fig.add_trace(go.Scatter(
    x=x_teorica, 
    y=y_teorica, 
    mode='lines',
    name='Curva Teórica QAST',
    line=dict(color='#00c9ff', width=3)
))

# Punto exacto del objeto calculado
fig.add_trace(go.Scatter(
    x=[actividad], 
    y=[h0], 
    mode='markers+text',
    name='Objeto Medido',
    text=[f"H₀={h0:.2f}"],
    textposition="top left",
    marker=dict(color='#ff4b4b', size=12, symbol='circle', line=dict(color='white', width=2))
))

fig.update_layout(
    plot_bgcolor='#0e1117', 
    paper_bgcolor='#0e1117', 
    font_color="white",
    xaxis_title="Actividad Cinemática (A) %",
    yaxis_title="Constante de Hubble Aparente (km/s/Mpc)",
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(fig, use_container_width=True)
