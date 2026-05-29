import streamlit as st
import numpy as np
from scipy import stats as sp_stats
from utils.formulas import *

st.set_page_config(page_title="Prueba de Hipótesis - Una Muestra", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .page-header { font-family: 'Playfair Display', serif; font-size: 2.2rem; color: #1A3A5C; border-bottom: 3px solid #D4AF37; padding-bottom: 0.5rem; margin-bottom: 1.5rem; }
    .result-box { background: linear-gradient(135deg, #1A3A5C 0%, #2A5A8C 100%); border: 2px solid #D4AF37; border-radius: 14px; padding: 1.5rem 2rem; margin: 1.2rem 0; color: white; }
    .result-box h3 { color: #D4AF37; margin-top: 0; font-family: 'Playfair Display', serif; }
    .result-box .value { font-size: 1.3rem; font-weight: 600; color: #FFFFFF; padding: 0.3rem 0; border-bottom: 1px solid rgba(212,175,55,0.3); }
    .result-box .label { color: #AAC8E8; font-size: 0.9rem; }
    .section-card { background: #FFFFFF; border-radius: 12px; padding: 1.5rem; margin: 0.8rem 0; border: 1px solid #E0E6EC; box-shadow: 0 2px 8px rgba(26,58,92,0.06); }
    .sub-section-title { font-size: 1.3rem; color: #1A3A5C; border-left: 4px solid #D4AF37; padding-left: 0.8rem; margin: 1rem 0; font-weight: 600; }
    .reject { color: #FFD700; font-weight:bold; }
    .accept { color: #90EE90; font-weight:bold; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-header">🧪 Prueba de Hipótesis (Una Muestra)</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Media con σ Conocida (Z)", "Proporción (Z)", "Media con σ Desconocida (t)"])

with tab1:
    st.markdown('<div class="sub-section-title">Prueba de Hipótesis para la Media (σ conocida)</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        x_bar_z = c1.number_input("ẋ (media muestral)", value=52.0, format="%.4f", key="hz_xbar")
        mu0_z = c2.number_input("μ₀ (valor hipotético)", value=50.0, format="%.4f", key="hz_mu0")
        sigma_z = c3.number_input("σ (desv. poblacional)", min_value=0.0001, value=10.0, format="%.4f", key="hz_sigma")
        c1, c2 = st.columns(2)
        n_z = c1.number_input("n (tamaño de muestra)", min_value=1, value=100, key="hz_n")
        tail_z = c2.selectbox("Tipo de prueba", ["two (bilateral)", "left (unilateral izq)", "right (unilateral der)"], key="hz_tail")
        alpha_z = st.slider("Nivel de significancia (α)", 0.01, 0.10, 0.05, format="%.2f", key="hz_alpha")
        if st.button("Realizar Prueba Z", key="calc_hz"):
            tail_map = {"two (bilateral)": "two", "left (unilateral izq)": "left", "right (unilateral der)": "right"}
            z_stat, p_value = z_test_mean(x_bar_z, mu0_z, sigma_z, int(n_z), tail_map[tail_z])
            z_crit = sp_stats.norm.ppf(1 - alpha_z / 2) if tail_map[tail_z] == "two" else sp_stats.norm.ppf(alpha_z) if tail_map[tail_z] == "left" else sp_stats.norm.ppf(1 - alpha_z)
            decision = "RECHAZAR H₀" if p_value < alpha_z else "NO RECHAZAR H₀"
            decision_color = "reject" if p_value < alpha_z else "accept"
            st.markdown(f"""
            <div class="result-box">
                <h3>📊 Prueba Z para una Media</h3>
                <div class="value">Z<sub>calc</sub> = {z_stat:.4f}</div>
                <div class="label">Estadístico de prueba</div>
                <div class="value" style="margin-top:0.6rem;">p-valor = {p_value:.6f}</div>
                <div class="label">Significancia observada</div>
                <div class="value" style="margin-top:0.6rem;">Z<sub>crítico</sub> = {z_crit:.4f}</div>
                <div class="label">Valor crítico (α = {alpha_z:.2f})</div>
                <div class="value" style="margin-top:0.6rem; font-size:1.6rem;" class="{decision_color}">{decision}</div>
                <div class="label">p-valor {'<' if p_value < alpha_z else '≥'} α → {decision}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="sub-section-title">Prueba de Hipótesis para Proporción</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        x_prop = c1.number_input("x (número de éxitos)", min_value=0, value=45, key="hp_x")
        n_prop = c2.number_input("n (tamaño de muestra)", min_value=1, value=100, key="hp_n")
        p0_prop = st.number_input("p₀ (proporción hipotética)", min_value=0.001, max_value=0.999, value=0.5, format="%.4f", key="hp_p0")
        tail_p = st.selectbox("Tipo de prueba", ["two (bilateral)", "left (unilateral izq)", "right (unilateral der)"], key="hp_tail")
        alpha_p = st.slider("Nivel de significancia (α)", 0.01, 0.10, 0.05, format="%.2f", key="hp_alpha")
        if st.button("Realizar Prueba Z para Proporción", key="calc_hp"):
            p_hat = int(x_prop) / int(n_prop)
            tail_map = {"two (bilateral)": "two", "left (unilateral izq)": "left", "right (unilateral der)": "right"}
            z_stat, p_value = z_test_proportion(p_hat, p0_prop, int(n_prop), tail_map[tail_p])
            z_crit = sp_stats.norm.ppf(1 - alpha_p / 2) if tail_map[tail_p] == "two" else sp_stats.norm.ppf(alpha_p) if tail_map[tail_p] == "left" else sp_stats.norm.ppf(1 - alpha_p)
            decision = "RECHAZAR H₀" if p_value < alpha_p else "NO RECHAZAR H₀"
            st.markdown(f"""
            <div class="result-box">
                <h3>📊 Prueba Z para Proporción</h3>
                <div class="value">ṗ = {p_hat:.4f}</div>
                <div class="label">Proporción muestral</div>
                <div class="value" style="margin-top:0.6rem;">Z<sub>calc</sub> = {z_stat:.4f}</div>
                <div class="label">Estadístico de prueba</div>
                <div class="value" style="margin-top:0.6rem;">p-valor = {p_value:.6f}</div>
                <div class="label">Significancia observada</div>
                <div class="value" style="margin-top:0.6rem;">Z<sub>crítico</sub> = {z_crit:.4f}</div>
                <div class="value" style="margin-top:0.6rem; font-size:1.6rem;">{decision}</div>
                <div class="label">p-valor {'<' if p_value < alpha_p else '≥'} α</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="sub-section-title">Prueba de Hipótesis para la Media (σ desconocida - t de Student)</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        metodo_t = st.radio("Método", ["A partir de datos", "A partir de estadísticos"], key="ht_metodo")
        if metodo_t == "A partir de datos":
            datos_ht = st.text_area("Ingrese datos", "48, 50, 52, 49, 51, 53, 47, 50, 51, 49", height=80, key="datos_ht")
            mu0_t = st.number_input("μ₀ (valor hipotético)", value=50.0, format="%.4f", key="ht_mu0_data")
            tail_t = st.selectbox("Tipo de prueba", ["two (bilateral)", "left (unilateral izq)", "right (unilateral der)"], key="ht_tail_data")
            alpha_t = st.slider("Nivel de significancia (α)", 0.01, 0.10, 0.05, format="%.2f", key="ht_alpha_data")
            if st.button("Realizar Prueba t", key="calc_ht_data"):
                try:
                    datos = np.array([float(x.strip()) for x in datos_ht.split(",")])
                    x_bar_t = np.mean(datos)
                    s_t = np.std(datos, ddof=1)
                    n_t = len(datos)
                    tail_map = {"two (bilateral)": "two", "left (unilateral izq)": "left", "right (unilateral der)": "right"}
                    t_stat, p_value, df = t_test_mean(x_bar_t, mu0_t, s_t, n_t, tail_map[tail_t])
                    t_crit = sp_stats.t.ppf(1 - alpha_t / 2, df) if tail_map[tail_t] == "two" else sp_stats.t.ppf(alpha_t, df) if tail_map[tail_t] == "left" else sp_stats.t.ppf(1 - alpha_t, df)
                    decision = "RECHAZAR H₀" if p_value < alpha_t else "NO RECHAZAR H₀"
                    st.markdown(f"""
                    <div class="result-box">
                        <h3>📊 Prueba t para una Media</h3>
                        <div class="value">ẋ = {x_bar_t:.4f} &nbsp;|&nbsp; s = {s_t:.4f} &nbsp;|&nbsp; n = {n_t}</div>
                        <div class="label">Estadísticos muestrales</div>
                        <div class="value" style="margin-top:0.6rem;">t<sub>calc</sub> = {t_stat:.4f} &nbsp;|&nbsp; gl = {df}</div>
                        <div class="label">Estadístico de prueba y grados de libertad</div>
                        <div class="value" style="margin-top:0.6rem;">p-valor = {p_value:.6f}</div>
                        <div class="label">Significancia observada</div>
                        <div class="value" style="margin-top:0.6rem;">t<sub>crítico</sub> = {t_crit:.4f}</div>
                        <div class="value" style="margin-top:0.6rem; font-size:1.6rem;">{decision}</div>
                        <div class="label">p-valor {'<' if p_value < alpha_t else '≥'} α</div>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            c1, c2, c3 = st.columns(3)
            x_bar_ts = c1.number_input("ẋ (media muestral)", value=52.0, format="%.4f", key="ht_xbar")
            s_ts = c2.number_input("s (desv. muestral)", min_value=0.0001, value=8.0, format="%.4f", key="ht_s")
            n_ts = c3.number_input("n (tamaño muestra)", min_value=2, value=25, key="ht_n")
            mu0_ts = st.number_input("μ₀ (valor hipotético)", value=50.0, format="%.4f", key="ht_mu0")
            tail_ts = st.selectbox("Tipo de prueba", ["two (bilateral)", "left (unilateral izq)", "right (unilateral der)"], key="ht_tail_stats")
            alpha_ts = st.slider("Nivel de significancia (α)", 0.01, 0.10, 0.05, format="%.2f", key="ht_alpha_stats")
            if st.button("Realizar Prueba t", key="calc_ht_stats"):
                tail_map = {"two (bilateral)": "two", "left (unilateral izq)": "left", "right (unilateral der)": "right"}
                t_stat, p_value, df = t_test_mean(x_bar_ts, mu0_ts, s_ts, int(n_ts), tail_map[tail_ts])
                t_crit = sp_stats.t.ppf(1 - alpha_ts / 2, df) if tail_map[tail_ts] == "two" else sp_stats.t.ppf(alpha_ts, df) if tail_map[tail_ts] == "left" else sp_stats.t.ppf(1 - alpha_ts, df)
                decision = "RECHAZAR H₀" if p_value < alpha_ts else "NO RECHAZAR H₀"
                st.markdown(f"""
                <div class="result-box">
                    <h3>📊 Prueba t para una Media</h3>
                    <div class="value">ẋ = {x_bar_ts:.4f} &nbsp;|&nbsp; s = {s_ts:.4f} &nbsp;|&nbsp; n = {int(n_ts)}</div>
                    <div class="label">Estadísticos muestrales</div>
                    <div class="value" style="margin-top:0.6rem;">t<sub>calc</sub> = {t_stat:.4f} &nbsp;|&nbsp; gl = {df}</div>
                    <div class="label">Estadístico de prueba</div>
                    <div class="value" style="margin-top:0.6rem;">p-valor = {p_value:.6f}</div>
                    <div class="label">Significancia observada</div>
                    <div class="value" style="margin-top:0.6rem;">t<sub>crítico</sub> = {t_crit:.4f}</div>
                    <div class="value" style="margin-top:0.6rem; font-size:1.6rem;">{decision}</div>
                    <div class="label">p-valor {'<' if p_value < alpha_ts else '≥'} α</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
