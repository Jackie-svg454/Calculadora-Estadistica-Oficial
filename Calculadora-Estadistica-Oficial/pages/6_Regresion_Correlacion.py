import streamlit as st
import numpy as np
import pandas as pd
from scipy import stats as sp_stats
from utils.formulas import *
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Regresión Simple y Correlación", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .page-header { font-family: 'Playfair Display', serif; font-size: 2.2rem; color: #1A3A5C; border-bottom: 3px solid #D4AF37; padding-bottom: 0.5rem; margin-bottom: 1.5rem; }
    .result-box { background: linear-gradient(135deg, #1A3A5C 0%, #2A5A8C 100%); border: 2px solid #D4AF37; border-radius: 14px; padding: 1.5rem 2rem; margin: 1.2rem 0; color: white; }
    .result-box h3 { color: #D4AF37; margin-top: 0; font-family: 'Playfair Display', serif; }
    .result-box .value { font-size: 1.3rem; font-weight: 600; color: #FFFFFF; padding: 0.3rem 0; border-bottom: 1px solid rgba(212,175,55,0.3); }
    .result-box .label { color: #AAC8E8; font-size: 0.9rem; }
    .section-card { background: #FFFFFF; border-radius: 12px; padding: 1.5rem; margin: 0.8rem 0; border: 1px solid #E0E6EC; box-shadow: 0 2px 8px rgba(26,58,92,0.06); }
    .sub-section-title { font-size: 1.3rem; color: #1A3A5C; border-left: 4px solid #D4AF37; padding-left: 0.8rem; margin: 1rem 0; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-header">📈 Regresión Simple y Correlación</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Estimación (Recta de Regresión)", "Análisis de Correlación", "Inferencias sobre Parámetros"])

with tab1:
    st.markdown('<div class="sub-section-title">Estimación mediante la Recta de Regresión</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.write("Ingrese los pares de datos (X, Y):")
        c1, c2 = st.columns(2)
        with c1:
            x_data = st.text_area("Variable X (independiente)", "1, 2, 3, 4, 5, 6, 7, 8", height=100, key="reg_x")
        with c2:
            y_data = st.text_area("Variable Y (dependiente)", "2, 4, 5, 7, 8, 10, 11, 13", height=100, key="reg_y")
        st.markdown("**Predecir un nuevo valor:**")
        x_nuevo = st.number_input("X para predicción", value=9.0, format="%.2f", key="reg_pred")
        if st.button("Calcular Regresión", key="calc_reg"):
            try:
                x = np.array([float(v.strip()) for v in x_data.split(",")])
                y = np.array([float(v.strip()) for v in y_data.split(",")])
                if len(x) != len(y):
                    st.error("X y Y deben tener el mismo número de elementos")
                elif len(x) < 3:
                    st.error("Se necesitan al menos 3 pares de datos")
                else:
                    res = linear_regression(x, y)
                    y_pred_new = predict_regression(res["b0"], res["b1"], x_nuevo)
                    st.markdown(f"""
                    <div class="result-box">
                        <h3>📊 Recta de Regresión</h3>
                        <div class="value">ŷ = {res['b0']:.4f} + {res['b1']:.4f}·x</div>
                        <div class="label">Ecuación de la recta de regresión estimada</div>
                        <div class="value" style="margin-top:0.6rem;">b₀ = {res['b0']:.4f} &nbsp;|&nbsp; b₁ = {res['b1']:.4f}</div>
                        <div class="label">Coeficientes de regresión</div>
                        <div class="value" style="margin-top:0.6rem;">ŷ({x_nuevo:.2f}) = {y_pred_new:.4f}</div>
                        <div class="label">Predicción para X = {x_nuevo:.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    df_reg = pd.DataFrame({"X": x, "Y": y, "Ŷ (predicho)": res["y_pred"]})
                    st.dataframe(df_reg.style.format({"X": "{:.2f}", "Y": "{:.2f}", "Ŷ (predicho)": "{:.4f}"}), use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="sub-section-title">Análisis de Correlación</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.write("Ingrese los pares de datos (X, Y) para analizar la correlación:")
        c1, c2 = st.columns(2)
        with c1:
            x_corr = st.text_area("Variable X", "1, 2, 3, 4, 5, 6, 7, 8", height=100, key="corr_x")
        with c2:
            y_corr = st.text_area("Variable Y", "2, 4, 5, 7, 8, 10, 11, 13", height=100, key="corr_y")
        if st.button("Calcular Correlación", key="calc_corr"):
            try:
                x = np.array([float(v.strip()) for v in x_corr.split(",")])
                y = np.array([float(v.strip()) for v in y_corr.split(",")])
                if len(x) != len(y):
                    st.error("X y Y deben tener el mismo número de elementos")
                elif len(x) < 3:
                    st.error("Se necesitan al menos 3 pares de datos")
                else:
                    res = linear_regression(x, y)
                    fuerza = "Muy fuerte" if abs(res["r"]) >= 0.9 else "Fuerte" if abs(res["r"]) >= 0.7 else "Moderada" if abs(res["r"]) >= 0.5 else "Débil" if abs(res["r"]) >= 0.3 else "Muy débil"
                    direccion = "positiva" if res["r"] > 0 else "negativa"
                    st.markdown(f"""
                    <div class="result-box">
                        <h3>📊 Análisis de Correlación</h3>
                        <div class="value">r = {res['r']:.6f}</div>
                        <div class="label">Coeficiente de correlación de Pearson</div>
                        <div class="value" style="margin-top:0.6rem;">r² = {res['r2']:.6f}</div>
                        <div class="label">Coeficiente de determinación</div>
                        <div class="value" style="margin-top:0.6rem; font-size:1.1rem;">Correlación {fuerza} y {direccion}</div>
                        <div class="label">Interpretación</div>
                        <div class="value" style="margin-top:0.6rem;">{res['r2']*100:.2f}% de la variación en Y es explicada por X</div>
                        <div class="label">Porcentaje de variación explicada</div>
                    </div>
                    """, unsafe_allow_html=True)
                    fig = px.scatter(x=x, y=y, trendline="ols",
                                     title="Diagrama de Dispersión con Recta de Regresión",
                                     labels={"x": "Variable X", "y": "Variable Y"},
                                     color_discrete_sequence=["#1A3A5C"])
                    fig.update_traces(marker=dict(size=10, color="#1A3A5C", line=dict(width=2, color="#D4AF37")),
                                      selector=dict(type="scatter"))
                    fig.update_layout(
                        plot_bgcolor="#F0F4F8",
                        paper_bgcolor="#FFFFFF",
                        font=dict(color="#1A3A5C"),
                        showlegend=False,
                    )
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="sub-section-title">Inferencias sobre Parámetros de Población</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.write("Ingrese los datos para realizar inferencias sobre los coeficientes de regresión:")
        c1, c2 = st.columns(2)
        with c1:
            x_inf = st.text_area("Variable X", "1, 2, 3, 4, 5, 6, 7, 8", height=100, key="inf_x")
        with c2:
            y_inf = st.text_area("Variable Y", "2, 4, 5, 7, 8, 10, 11, 13", height=100, key="inf_y")
        alpha_inf = st.slider("Nivel de significancia (α)", 0.01, 0.10, 0.05, format="%.2f", key="inf_alpha")
        if st.button("Realizar Inferencias", key="calc_inf"):
            try:
                x = np.array([float(v.strip()) for v in x_inf.split(",")])
                y = np.array([float(v.strip()) for v in y_inf.split(",")])
                if len(x) != len(y):
                    st.error("X y Y deben tener el mismo número de elementos")
                elif len(x) < 3:
                    st.error("Se necesitan al menos 3 pares de datos")
                else:
                    res = linear_regression(x, y)
                    t_crit = sp_stats.t.ppf(1 - alpha_inf / 2, res["n"] - 2)
                    ci_b1_low = res["b1"] - t_crit * res["se_b1"]
                    ci_b1_high = res["b1"] + t_crit * res["se_b1"]
                    significancia = "SIGNIFICATIVO" if res["p_value_b1"] < alpha_inf else "NO SIGNIFICATIVO"
                    st.markdown(f"""
                    <div class="result-box">
                        <h3>📊 Inferencias sobre Parámetros</h3>
                        <div class="value">H₀: β₁ = 0 &nbsp; vs &nbsp; H₁: β₁ ≠ 0</div>
                        <div class="label">Hipótesis sobre la pendiente poblacional</div>
                        <div class="value" style="margin-top:0.6rem;">t = {res['t_b1']:.4f} &nbsp;|&nbsp; gl = {res['n'] - 2}</div>
                        <div class="label">Estadístico de prueba</div>
                        <div class="value" style="margin-top:0.6rem;">p-valor = {res['p_value_b1']:.6f}</div>
                        <div class="label">Significancia observada</div>
                        <div class="value" style="margin-top:0.6rem;">Error estándar (b₁) = {res['se_b1']:.4f}</div>
                        <div class="label">Error estándar del coeficiente de pendiente</div>
                        <div class="value" style="margin-top:0.6rem;">IC β₁: [{ci_b1_low:.4f}, {ci_b1_high:.4f}]</div>
                        <div class="label">Intervalo de confianza del {(1-alpha_inf)*100:.0f}% para β₁</div>
                        <div class="value" style="margin-top:0.6rem;">s = {res['s']:.4f} &nbsp;|&nbsp; SSE = {res['SSE']:.4f}</div>
                        <div class="label">Error estándar de estimación y suma de cuadrados residual</div>
                        <div class="value" style="margin-top:0.6rem; font-size:1.3rem;">{significancia}</div>
                        <div class="label">Conclusión: {'Rechazamos H₀. La pendiente es significativa.' if res['p_value_b1'] < alpha_inf else 'No rechazamos H₀. La pendiente no es significativa.'}</div>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
