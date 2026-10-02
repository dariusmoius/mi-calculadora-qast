import streamlit as st
# Esto fuerza el estilo oscuro para que se parezca a lo que tenías
st.set_page_config(page_title="Calculadora Q.A.S.T.", layout="centered")

import numpy as np
import plotly.graph_objects as go
# --- CONSTANTES PROYECTO Q.A.S.T. (VALORES FIJOS) ---
ROTACION_OBSERVADOR = 240 # Tensor de Anclaje fijo (Métrica Moio)
H_BASE = 67.4 # Sustrato Activo (Planck)
C_LOG = 2.3 # Módulo de Elasticidad de Moio
def ejecutar_sistema_fighter():
print("--- MOTOR DE CÁLCULO Q.A.S.T. (VERSION FIGHTER) ---")
print(f"Soberanía Técnica: H_base {H_BASE} | Anclaje Rotación
{ROTACION_OBSERVADOR}")
while True:
try:
print("\nMODO DE OBTENCIÓN:")
print("1. Cargar V_peculiar Corregida")
print("2. Calcular V_peculiar (Protocolo m, M, V_cmb)")
print("0. Salir")
opcion = input("Selección: ")
if opcion == "0":
break
if opcion == "1":
v_input = float(input("V_peculiar (km/s): "))
elif opcion == "2":
m = float(input("m (Magnitud Aparente): "))
M = float(input("M (Magnitud Absoluta): "))
v_cmb = float(input("V_cmb (Velocidad medida): "))
distancia = 10**((m - M + 5) / 5) / 1e6
v_input = v_cmb - (H_BASE * distancia)
print(f"-> Distancia calculada: {distancia:.4f} Mpc")
else:
continue
# --- CÁLCULO DE ACTIVIDAD Y H0 APARENTE ---
v_abs = abs(v_input)
# Actividad mecánica del sistema local
actividad = (v_abs / ROTACION_OBSERVADOR) * 100
# H0 Aparente con el residuo del anclaje (Fórmula Moio)
h0_apa = H_BASE + (C_LOG * np.log10(1 + actividad))
residuo = h0_apa - H_BASE
print("\n" + "!"*50)
print(f"ANCLAJE DE ROTACIÓN: {ROTACION_OBSERVADOR}")
print(f"ACTIVIDAD (A): {actividad:.4f}%")
print(f"H0 APARENTE: {h0_apa:.4f} km/s/Mpc")
print(f"RESIDUO CALCULADO: {residuo:.4f} km/s/Mpc")
print("!"*50)
# --- VISUALIZACIÓN DE LA MÉTRICA ---
v_rango = np.linspace(0, 1500, 300)
A_rango = (v_rango / ROTACION_OBSERVADOR) * 100
H_rango = H_BASE + (C_LOG * np.log10(1 + A_rango))
fig = go.Figure()
fig.add_trace(go.Scatter3d(
x=v_rango, y=A_rango, z=H_rango,
mode='lines', line=dict(color='cyan', width=4), name='Métrica Q.A.S.T.'
))
fig.add_trace(go.Scatter3d(
x=[v_abs], y=[actividad], z=[h0_apa],
mode='markers', marker=dict(size=12, color='red'), name='Punto de Anclaje'
))
fig.update_layout(
title=f'H0 APA: {h0_apa:.2f} | Residuo: {residuo:.2f} | A: {actividad:.2f}%',
template='plotly_dark',
scene=dict(
xaxis_title='V_peculiar (km/s)',
yaxis_title='Rotación/Actividad',
zaxis_title='H0 APARENTE'
)
)
fig.show()
except Exception as e:
print(f"Error técnico: {e}")
if __name__ == "__main__":
ejecutar_sistema_fighter()


