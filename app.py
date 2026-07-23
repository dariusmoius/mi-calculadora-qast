import streamlit as st
# Esto fuerza el estilo oscuro para que se parezca a lo que tenías
st.set_page_config(page_title="Calculadora Q.A.S.T.", layout="centered")

# Puedes añadir CSS para cambiar colores si quieres
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    </style>
    """, unsafe_allow_html=True)
import numpy as np

st.title("Calculadora Cosmológica Q.A.S.T.")

v = st.number_input("Velocidad Peculiar (km/s)", value=0.0)
r = st.number_input("Rotación Observador", value=240.0)

if st.button("Calcular"):
    actividad = (abs(v) / r) * 100
    h0 = 67.4 + (2.3 * np.log10(1 + actividad))
    
    st.metric("H0 Aparente", f"{h0:.2f} km/s/Mpc")
    st.write(f"Nivel de Actividad: {actividad:.2f}%")
