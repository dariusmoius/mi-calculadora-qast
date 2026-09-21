import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ============================================================
# Q.A.S.T. — Tensor de Anclaje · Motor de Cálculo
# Versión 2.2 — Código abierto · Sin preajustes
# Fórmula: H₀ = H₀_base + ln(10) · log₁₀[1 + (σ²/σ₀²)·(1 - ρ/ρ_crit)]
# ============================================================

st.set_page_config(
    page_title="Q.A.S.T. — Tensor de Anclaje",
    layout="centered"
)

st.title("Q.A.S.T. — Tensor de Anclaje")
st.subheader("Motor de Cálculo · Versión Abierta")

st.markdown(r"""
### Fórmula Unificada
$$
H_0^{\text{ap}} = H_0^{\text{base}} + \ln(10) \cdot \log_{10}\!\left[\,1 + \frac{\langle\sigma^2\rangle}{\sigma_0^2} \left(1 - \frac{\rho_{\text{local}}}{\rho_{\text{crítica}}}\right) \right]
$$

**Donde:**
- \(H_0^{\text{base}} = 67{,}4\ \mathrm{km/s/Mpc}\) → valor intrínseco (Planck 2020)
- \(\sigma_0 = 310\ \mathrm{km/s}\) → escala de referencia de cizalladura del Grupo Local
- \(\langle\sigma^2\rangle^{1/2}\) → cizalladura cuadrática media del entorno (km/s)
- \(\rho_{\text{local}}/\rho_{\text{crítica}}\) → densidad relativa del entorno (0 a 1)
- \(\ln(10) \approx 2{,}302585\) → factor de conversión, **no parámetro ajustado**
""")

st.info("📋 **Código sin valores predefinidos.** Todos los parámetros son ingresados por el usuario. Las constantes fundamentales están declaradas abajo y pueden verificarse.")

# ──────────────────────────────────────────────────────
# CONSTANTES — Declaradas explícitamente, SIN OCULTAR
# ──────────────────────────────────────────────────────
with st.expander("🔧 Constantes del modelo — Verificar"):
    H0_BASE    = 67.40       # km/s/Mpc — Planck 2020
    SIGMA_0    = 310.0       # km/s — escala de referencia
    FACTOR_LOG = np.log(10)  # = 2.302585093 — conversión ln → base 10
    
    st.markdown(f"""
    | Constante | Valor | Origen |
    |---|---|---|
    | \(H_0^{{base}}\) | {H0_BASE:.2f} km/s/Mpc | Planck 2018/2020 |
    | \(\sigma_0\) | {SIGMA_0:.1f} km/s | Grupo Local / flujo colectivo |
    | \(\ln(10)\) | {FACTOR_LOG:.6f} | Matemático, no ajuste |
    """)

# ──────────────────────────────────────────────────────
# ENTRADA DEL USUARIO — LIMPIA, SIN PRESETS
# ──────────────────────────────────────────────────────
st.markdown("### 📥 Ingreso de Datos")

st.markdown("""
Ingresa los valores calculados desde tus datos observacionales:
- **Cizalladura** ⟨σ²⟩¹ᐟ²: velocidad peculiar corregida del flujo colectivo del entorno (km/s)
- **Densidad relativa** ρ/ρ_crit: densidad media del entorno respecto a la densidad crítica (entre 0 y 1)
""")

sigma = st.number_input(
    "Cizalladura √⟨σ²⟩ (km/s):",
    min_value=0.0,
    step=1.0,
    format="%.1f",
    help="Valor obtenido del análisis del flujo peculiar de tu muestra"
)

rho_rel = st.number_input(
    "Densidad relativa ρ/ρ_crítica:",
    min_value=0.01,
    max_value=1.00,
    value=1.00,
    step=0.01,
    format="%.2f",
    help="1.0 = densidad crítica / universo homogéneo | < 1 = región subdensa"
)

# ──────────────────────────────────────────────────────
# CÁLCULO PASO A PASO — TOTALMENTE TRANSPARENTE
# ──────────────────────────────────────────────────────
st.markdown("### ⚙️ Desarrollo del Cálculo")

paso1 = np.square(sigma) / np.square(SIGMA_0)
paso2 = 1.0 - rho_rel
actividad = paso1 * paso2
h0_calc = H0_BASE + FACTOR_LOG * np.log1p(actividad)

st.markdown(f""")
