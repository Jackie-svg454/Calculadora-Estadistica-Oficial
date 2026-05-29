import streamlit as st
import numpy as np
from utils.formulas import *
from scipy import stats as sp_stats

st.set_page_config(page_title="Distribuciones de Probabilidad", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .page-header { font-family: 'Playfair Display', serif; font-size: 2.2rem; color: #1A3A5C; border-bottom: 3px solid #D4AF37; padding-bottom: 0.5rem; margin-bottom: 1.5rem; }
    .result-box { background: linear-gradient(135deg, #1A3A5C 0%, #2A5A8C 100%); border: 2px solid #D4AF37; border-radius: 14px; padding: 1.5rem 2rem; margin: 1.2rem 0; color: white; }
    .result-box h3 { color: #D4AF37; margin-top: 0; font-family: 'Playfair Display', serif; }
    .result-box .value { font-size: 1.3rem; font-weight: 600; color: #FFFFFF; padding: 0.3rem 0; border-bottom: 1px solid rgba(212,175,55,0.3); }
    .result-box .label { color: #AAC8E8; font-size: 0.9rem; }
    .section-card { background: #FFFFFF; border-radius: 12px; padding: 1.5rem; margin: 0.8rem 0; border: 1px solid #E0E6EC; box-shadow: 0 2px 8px rgba(26,58,92,0.06); }
    .sub-section-title { font-size: 1.3rem; color: #1A3A5C; border-left: 4px solid #D4AF37; padding-left: 0.8rem; margin: 1rem 0; font-weight: 600; }
    .st-emotion-cache-1r4qj8v { background-color: #F0F4F8; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-header">📐 Distribuciones de Probabilidad</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["Variables Aleatorias", "Binomial", "Poisson", "Normal"])

with tab1:
    st.markdown('<div class="sub-section-title">Esperanza, Varianza y Desviación Estándar</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        n_vals = st.number_input("Número de valores", min_value=2, max_value=20, value=3, key="n_vals")
        col_x, col_p = st.columns(2)
        values = []
        probs = []
        for i in range(int(n_vals)):
            c1, c2 = st.columns(2)
            v = c1.number_input(f"x{i+1}", value=float(i+1), key=f"x_{i}", format="%.2f")
            p = c2.number_input(f"P(x{i+1})", value=1.0/n_vals, key=f"p_{i}", min_value=0.0, max_value=1.0, format="%.4f")
            values.append(v)
            probs.append(p)
        if st.button("Calcular", key="calc_var_aleat"):
            total_p = sum(probs)
            if abs(total_p - 1.0) > 0.01:
                st.error(f"Las probabilidades deben sumar 1 (suman {total_p:.4f})")
            else:
                mu = expected_value(values, probs)
                var = variance(values, probs)
                std = std_deviation(values, probs)
                st.markdown(f"""
                <div class="result-box">
                    <h3>📊 Resultados</h3>
                    <div class="value">E(X) = {mu:.4f}</div>
                    <div class="label">Esperanza matemática (media ponderada)</div>
                    <div class="value" style="margin-top:0.6rem;">Var(X) = {var:.4f}</div>
                    <div class="label">Varianza</div>
                    <div class="value" style="margin-top:0.6rem;">σ = {std:.4f}</div>
                    <div class="label">Desviación estándar</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="sub-section-title">Distribución Binomial</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        n_binom = c1.number_input("n (ensayos)", min_value=1, max_value=1000, value=10, key="binom_n")
        p_binom = c2.number_input("p (probabilidad de éxito)", min_value=0.0, max_value=1.0, value=0.5, format="%.4f", key="binom_p")
        k_binom = c3.number_input("k (éxitos)", min_value=0, max_value=int(n_binom), value=5, key="binom_k")
        if st.button("Calcular", key="calc_binom"):
            prob_exacta = binomial_prob(int(n_binom), int(k_binom), p_binom) if k_binom <= n_binom else 0
            prob_acum = binomial_cumulative(int(n_binom), int(k_binom), p_binom) if k_binom <= n_binom else 0
            media_b = binomial_mean(int(n_binom), p_binom)
            var_b = binomial_variance(int(n_binom), p_binom)
            st.markdown(f"""
            <div class="result-box">
                <h3>📊 Resultados Binomial</h3>
                <div class="value">P(X = {int(k_binom)}) = {prob_exacta:.6f}</div>
                <div class="label">Probabilidad exacta de {int(k_binom)} éxitos</div>
                <div class="value" style="margin-top:0.6rem;">P(X ≤ {int(k_binom)}) = {prob_acum:.6f}</div>
                <div class="label">Probabilidad acumulada</div>
                <div class="value" style="margin-top:0.6rem;">μ = {media_b:.4f} &nbsp;|&nbsp; σ² = {var_b:.4f} &nbsp;|&nbsp; σ = {np.sqrt(var_b):.4f}</div>
                <div class="label">Media, Varianza y Desviación estándar</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="sub-section-title">Distribución de Poisson</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        lam_pois = c1.number_input("λ (tasa media)", min_value=0.0, max_value=1000.0, value=3.0, format="%.4f", key="pois_lam")
        k_pois = c2.number_input("k (ocurrencias)", min_value=0, max_value=1000, value=2, key="pois_k")
        if st.button("Calcular", key="calc_pois"):
            p_exacta = poisson_prob(lam_pois, int(k_pois))
            p_acum = poisson_cumulative(lam_pois, int(k_pois))
            st.markdown(f"""
            <div class="result-box">
                <h3>📊 Resultados Poisson</h3>
                <div class="value">P(X = {int(k_pois)}) = {p_exacta:.6f}</div>
                <div class="label">Probabilidad exacta de {int(k_pois)} ocurrencias</div>
                <div class="value" style="margin-top:0.6rem;">P(X ≤ {int(k_pois)}) = {p_acum:.6f}</div>
                <div class="label">Probabilidad acumulada</div>
                <div class="value" style="margin-top:0.6rem;">μ = {lam_pois:.4f} &nbsp;|&nbsp; σ² = {lam_pois:.4f} &nbsp;|&nbsp; σ = {np.sqrt(lam_pois):.4f}</div>
                <div class="label">Media, Varianza y Desviación estándar (λ = {lam_pois:.4f})</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="sub-section-title">Distribución Normal</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        mu_norm = c1.number_input("μ (media)", value=0.0, format="%.4f", key="norm_mu")
        sigma_norm = c2.number_input("σ (desviación estándar)", min_value=0.0001, value=1.0, format="%.4f", key="norm_sigma")
        tipo_calc = st.radio("Tipo de cálculo", ["P(X < x)", "P(a < X < b)", "Valor Z", "Percentil Inverso (dada P)"])
        if tipo_calc == "P(X < x)":
            x_val = st.number_input("x", value=1.0, format="%.4f", key="norm_x")
            if st.button("Calcular", key="calc_norm1"):
                prob = normal_prob(x_val, mu_norm, sigma_norm)
                z = normal_z_score(x_val, mu_norm, sigma_norm)
                st.markdown(f"""
                <div class="result-box">
                    <h3>📊 Resultados Normal</h3>
                    <div class="value">P(X < {x_val:.4f}) = {prob:.6f}</div>
                    <div class="label">Probabilidad acumulada</div>
                    <div class="value" style="margin-top:0.6rem;">Z = {z:.4f}</div>
                    <div class="label">Puntaje Z</div>
                </div>
                """, unsafe_allow_html=True)
        elif tipo_calc == "P(a < X < b)":
            c1, c2 = st.columns(2)
            a_val = c1.number_input("a (límite inferior)", value=-1.0, format="%.4f", key="norm_a")
            b_val = c2.number_input("b (límite superior)", value=1.0, format="%.4f", key="norm_b")
            if st.button("Calcular", key="calc_norm2"):
                prob = normal_prob_between(a_val, b_val, mu_norm, sigma_norm)
                z_a = normal_z_score(a_val, mu_norm, sigma_norm)
                z_b = normal_z_score(b_val, mu_norm, sigma_norm)
                st.markdown(f"""
                <div class="result-box">
                    <h3>📊 Resultados Normal</h3>
                    <div class="value">P({a_val:.4f} < X < {b_val:.4f}) = {prob:.6f}</div>
                    <div class="label">Probabilidad en el intervalo</div>
                    <div class="value" style="margin-top:0.6rem;">Z₁ = {z_a:.4f} &nbsp;|&nbsp; Z₂ = {z_b:.4f}</div>
                    <div class="label">Puntajes Z</div>
                </div>
                """, unsafe_allow_html=True)
        elif tipo_calc == "Valor Z":
            x_val = st.number_input("x", value=1.0, format="%.4f", key="norm_zx")
            if st.button("Calcular", key="calc_norm3"):
                z = normal_z_score(x_val, mu_norm, sigma_norm)
                st.markdown(f"""
                <div class="result-box">
                    <h3>📊 Resultados</h3>
                    <div class="value">Z = {z:.4f}</div>
                    <div class="label">Puntaje Z para X = {x_val:.4f}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            prob_perc = st.slider("Probabilidad acumulada P(X ≤ x)", 0.001, 0.999, 0.95, format="%.3f", key="norm_perc")
            if st.button("Calcular", key="calc_norm4"):
                x_inv = normal_inverse(prob_perc, mu_norm, sigma_norm)
                z_inv = normal_inverse(prob_perc, 0, 1)
                st.markdown(f"""
                <div class="result-box">
                    <h3>📊 Resultados Percentil Inverso</h3>
                    <div class="value">x = {x_inv:.4f}</div>
                    <div class="label">Valor de X tal que P(X ≤ x) = {prob_perc:.4f}</div>
                    <div class="value" style="margin-top:0.6rem;">z = {z_inv:.4f}</div>
                    <div class="label">Puntaje Z correspondiente</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
