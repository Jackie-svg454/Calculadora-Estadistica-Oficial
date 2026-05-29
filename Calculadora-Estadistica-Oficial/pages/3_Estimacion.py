import streamlit as st
import numpy as np
from scipy import stats as sp_stats
from utils.formulas import *

st.set_page_config(page_title="Estimación", layout="wide", initial_sidebar_state="expanded")

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

st.markdown('<div class="page-header">📏 Estimación</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["Estimaciones Puntuales", "Intervalo (Media/Proporción)", "Distribución t", "Tamaño de Muestra"])

with tab1:
    st.markdown('<div class="sub-section-title">Estimaciones Puntuales</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.write("Ingrese sus datos (separados por comas):")
        datos_punt = st.text_area("Datos", "23, 25, 28, 30, 32, 35, 37, 40", height=80, key="datos_punt")
        if st.button("Calcular Estimaciones", key="calc_punt"):
            try:
                datos = np.array([float(x.strip()) for x in datos_punt.split(",")])
                media = sample_mean(datos)
                mediana = np.median(datos)
                var = sample_variance(datos)
                std = sample_std_dev(datos)
                st.markdown(f"""
                <div class="result-box">
                    <h3>📊 Estimaciones Puntuales</h3>
                    <div class="value">ẋ = {media:.4f}</div>
                    <div class="label">Media muestral (estimación de μ)</div>
                    <div class="value" style="margin-top:0.6rem;">Mediana = {mediana:.4f}</div>
                    <div class="label">Mediana muestral</div>
                    <div class="value" style="margin-top:0.6rem;">s² = {var:.4f}</div>
                    <div class="label">Varianza muestral (estimación de σ²)</div>
                    <div class="value" style="margin-top:0.6rem;">s = {std:.4f}</div>
                    <div class="label">Desviación estándar muestral (estimación de σ)</div>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="sub-section-title">Estimación de Intervalo (Media y Proporción)</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        tipo_int = st.radio("Tipo de intervalo", ["Media (σ conocida)", "Media (solo datos)", "Proporción"], key="tipo_int")
        conf = st.slider("Nivel de confianza", 0.80, 0.99, 0.95, format="%.2f", key="conf_int")
        if tipo_int == "Media (σ conocida)":
            c1, c2, c3 = st.columns(3)
            x_bar_int = c1.number_input("ẋ (media muestral)", value=50.0, format="%.4f", key="int_xbar")
            sigma_int = c2.number_input("σ (desv. poblacional)", min_value=0.0001, value=10.0, format="%.4f", key="int_sigma")
            n_int = c3.number_input("n (tamaño muestra)", min_value=2, value=100, key="int_n")
            if st.button("Calcular Intervalo", key="calc_int_z"):
                li, ls, me = confidence_interval_mean_z_from_stats(x_bar_int, sigma_int, int(n_int), conf)
                z_actual = sp_stats.norm.ppf(1 - (1 - conf) / 2)
                st.markdown(f"""
                <div class="result-box">
                    <h3>📊 Intervalo de Confianza (Media, σ conocida)</h3>
                    <div class="value">{li:.4f} ≤ μ ≤ {ls:.4f}</div>
                    <div class="label">Intervalo de confianza del {conf:.0%}</div>
                    <div class="value" style="margin-top:0.6rem;">ẋ = {x_bar_int:.4f} &nbsp;|&nbsp; Error = ±{me:.4f}</div>
                    <div class="label">z_{{α/2}} = {z_actual:.4f} &nbsp;|&nbsp; n = {int(n_int)}</div>
                </div>
                """, unsafe_allow_html=True)
        elif tipo_int == "Media (solo datos)":
            datos_int = st.text_area("Ingrese datos", "45, 48, 52, 47, 50, 49, 51, 46", height=80, key="datos_int")
            if st.button("Calcular Intervalo", key="calc_int_data"):
                try:
                    datos = np.array([float(x.strip()) for x in datos_int.split(",")])
                    x_bar_calc = sample_mean(datos)
                    s_calc = sample_std_dev(datos)
                    n_calc = len(datos)
                    li, ls, me = confidence_interval_mean_z_from_stats(x_bar_calc, s_calc, n_calc, conf)
                    z_val = sp_stats.norm.ppf(1 - (1 - conf) / 2)
                    st.markdown(f"""
                    <div class="result-box">
                        <h3>📊 Intervalo de Confianza (Muestras Grandes)</h3>
                        <div class="value">{li:.4f} ≤ μ ≤ {ls:.4f}</div>
                        <div class="label">Intervalo de confianza del {conf:.0%}</div>
                        <div class="value" style="margin-top:0.6rem;">ẋ = {x_bar_calc:.4f} &nbsp;|&nbsp; s = {s_calc:.4f} &nbsp;|&nbsp; n = {n_calc}</div>
                        <div class="label">Error = ±{me:.4f} &nbsp;|&nbsp; z_{{α/2}} = {z_val:.4f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            c1, c2 = st.columns(2)
            x_int = c1.number_input("x (número de éxitos)", min_value=0, value=45, key="int_x")
            n_int_p = c2.number_input("n (tamaño muestra)", min_value=1, value=100, key="int_n_p")
            if st.button("Calcular Intervalo", key="calc_int_prop"):
                p_hat, li, ls, me = confidence_interval_proportion(int(x_int), int(n_int_p), conf)
                z_val = sp_stats.norm.ppf(1 - (1 - conf) / 2)
                st.markdown(f"""
                <div class="result-box">
                    <h3>📊 Intervalo de Confianza (Proporción)</h3>
                    <div class="value">{li:.4f} ≤ p ≤ {ls:.4f}</div>
                    <div class="label">Intervalo de confianza del {conf:.0%}</div>
                    <div class="value" style="margin-top:0.6rem;">ṗ = {p_hat:.4f} &nbsp;|&nbsp; Error = ±{me:.4f}</div>
                    <div class="label">z_{{α/2}} = {z_val:.4f} &nbsp;|&nbsp; n = {int(n_int_p)}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="sub-section-title">Estimaciones con Distribución t (Student)</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        metodo_t = st.radio("Método", ["A partir de datos", "A partir de estadísticos"], key="metodo_t")
        conf_t = st.slider("Nivel de confianza", 0.80, 0.99, 0.95, format="%.2f", key="conf_t")
        if metodo_t == "A partir de datos":
            datos_t = st.text_area("Ingrese datos", "23, 25, 28, 30, 32, 35, 37, 40, 42, 45", height=80, key="datos_t")
            if st.button("Calcular", key="calc_t_data"):
                try:
                    datos = np.array([float(x.strip()) for x in datos_t.split(",")])
                    x_bar_t, li, ls, me = confidence_interval_t(datos, conf_t)
                    n_t = len(datos)
                    s_t = sample_std_dev(datos)
                    t_val = sp_stats.t.ppf(1 - (1 - conf_t) / 2, n_t - 1)
                    st.markdown(f"""
                    <div class="result-box">
                        <h3>📊 Intervalo con Distribución t</h3>
                        <div class="value">{li:.4f} ≤ μ ≤ {ls:.4f}</div>
                        <div class="label">Intervalo de confianza del {conf_t:.0%}</div>
                        <div class="value" style="margin-top:0.6rem;">ẋ = {x_bar_t:.4f} &nbsp;|&nbsp; s = {s_t:.4f} &nbsp;|&nbsp; n = {n_t}</div>
                        <div class="label">t_{{α/2, {n_t-1}}} = {t_val:.4f} &nbsp;|&nbsp; Error = ±{me:.4f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            c1, c2, c3 = st.columns(3)
            x_bar_ts = c1.number_input("ẋ (media muestral)", value=50.0, format="%.4f", key="t_xbar")
            s_ts = c2.number_input("s (desv. muestral)", min_value=0.0001, value=8.0, format="%.4f", key="t_s")
            n_ts = c3.number_input("n (tamaño muestra)", min_value=2, value=20, key="t_n")
            if st.button("Calcular", key="calc_t_stats"):
                li, ls, me = confidence_interval_t_from_stats(x_bar_ts, s_ts, int(n_ts), conf_t)
                t_val = sp_stats.t.ppf(1 - (1 - conf_t) / 2, int(n_ts) - 1)
                st.markdown(f"""
                <div class="result-box">
                    <h3>📊 Intervalo con Distribución t</h3>
                    <div class="value">{li:.4f} ≤ μ ≤ {ls:.4f}</div>
                    <div class="label">Intervalo de confianza del {conf_t:.0%}</div>
                    <div class="value" style="margin-top:0.6rem;">ẋ = {x_bar_ts:.4f} &nbsp;|&nbsp; s = {s_ts:.4f} &nbsp;|&nbsp; n = {int(n_ts)}</div>
                    <div class="label">t_{{α/2, {int(n_ts)-1}}} = {t_val:.4f} &nbsp;|&nbsp; Error = ±{me:.4f}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="sub-section-title">Determinación del Tamaño de Muestra</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        tipo_n = st.radio("Para", ["Media", "Proporción"], key="tipo_n")
        conf_n = st.slider("Nivel de confianza", 0.80, 0.99, 0.95, format="%.2f", key="conf_n")
        if tipo_n == "Media":
            c1, c2 = st.columns(2)
            sigma_n = c1.number_input("σ (desviación estándar)", min_value=0.0001, value=15.0, format="%.4f", key="n_sigma")
            e_n = c2.number_input("E (error máximo deseado)", min_value=0.0001, value=3.0, format="%.4f", key="n_e")
            if st.button("Calcular n", key="calc_n_mean"):
                n_req = sample_size_mean(sigma_n, e_n, conf_n)
                z_n = sp_stats.norm.ppf(1 - (1 - conf_n) / 2)
                st.markdown(f"""
                <div class="result-box">
                    <h3>📊 Tamaño de Muestra Requerido</h3>
                    <div class="value">n = {n_req}</div>
                    <div class="label">Tamaño mínimo de muestra para estimar μ</div>
                    <div class="value" style="margin-top:0.6rem;">z_{{α/2}} = {z_n:.4f} &nbsp;|&nbsp; σ = {sigma_n:.4f} &nbsp;|&nbsp; E = {e_n:.4f}</div>
                    <div class="label">n = (z_{{α/2}} · σ / E)²</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            c1, c2 = st.columns(2)
            p_n = c1.number_input("p* (proporción estimada)", min_value=0.001, max_value=0.999, value=0.5, format="%.4f", key="n_p")
            e_n_p = c2.number_input("E (error máximo deseado)", min_value=0.0001, max_value=0.5, value=0.05, format="%.4f", key="n_e_p")
            if st.button("Calcular n", key="calc_n_prop"):
                n_req = sample_size_proportion(p_n, e_n_p, conf_n)
                z_n = sp_stats.norm.ppf(1 - (1 - conf_n) / 2)
                st.markdown(f"""
                <div class="result-box">
                    <h3>📊 Tamaño de Muestra Requerido</h3>
                    <div class="value">n = {n_req}</div>
                    <div class="label">Tamaño mínimo de muestra para estimar p</div>
                    <div class="value" style="margin-top:0.6rem;">z_{{α/2}} = {z_n:.4f} &nbsp;|&nbsp; p* = {p_n:.4f} &nbsp;|&nbsp; E = {e_n_p:.4f}</div>
                    <div class="label">n = (z_{{α/2}})² · p*(1-p*) / E²</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
