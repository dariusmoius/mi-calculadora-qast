import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Q.A.S.T. Engine", layout="centered")

st.title("Q.A.S.T. Engine")
st.write("Escribe un número y mira el resultado al instante:")

# Aquí está el truco: se calcula solo al escribir
v = st.number_input("Velocidad Peculiar (km/s)", value=0.0, step=0.1)
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
