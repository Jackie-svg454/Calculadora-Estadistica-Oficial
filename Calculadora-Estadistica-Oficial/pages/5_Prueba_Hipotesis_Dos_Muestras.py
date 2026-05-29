import streamlit as st
import numpy as np
from scipy import stats as sp_stats
from utils.formulas import *

st.set_page_config(page_title="Prueba de Hipótesis - Dos Muestras", layout="wide", initial_sidebar_state="expanded")

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

st.markdown('<div class="page-header">🔬 Prueba de Hipótesis (Dos Muestras)</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Diferencias entre Medias (Muestras Grandes)", "Diferencias entre Medias (Muestras Pequeñas)", "Muestras Dependientes (Pareadas)"])

with tab1:
    st.markdown('<div class="sub-section-title">Diferencia entre Medias — Muestras Grandes (Z)</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Muestra 1**")
            x1_bar = st.number_input("ẋ₁", value=105.0, format="%.4f", key="tz_x1")
            sigma1 = st.number_input("σ₁", min_value=0.0001, value=15.0, format="%.4f", key="tz_s1")
            n1 = st.number_input("n₁", min_value=1, value=100, key="tz_n1")
        with c2:
            st.markdown("**Muestra 2**")
            x2_bar = st.number_input("ẋ₂", value=100.0, format="%.4f", key="tz_x2")
            sigma2 = st.number_input("σ₂", min_value=0.0001, value=15.0, format="%.4f", key="tz_s2")
            n2 = st.number_input("n₂", min_value=1, value=100, key="tz_n2")
        tail_z2 = st.selectbox("Tipo de prueba", ["two (bilateral)", "left (unilateral izq)", "right (unilateral der)"], key="tz_tail")
        alpha_z2 = st.slider("Nivel de significancia (α)", 0.01, 0.10, 0.05, format="%.2f", key="tz_alpha")
        if st.button("Realizar Prueba Z (2 muestras)", key="calc_tz"):
            tail_map = {"two (bilateral)": "two", "left (unilateral izq)": "left", "right (unilateral der)": "right"}
            z_stat, p_value = two_sample_z_test(x1_bar, x2_bar, sigma1, sigma2, int(n1), int(n2), tail_map[tail_z2])
            z_crit = sp_stats.norm.ppf(1 - alpha_z2 / 2) if tail_map[tail_z2] == "two" else sp_stats.norm.ppf(alpha_z2) if tail_map[tail_z2] == "left" else sp_stats.norm.ppf(1 - alpha_z2)
            decision = "RECHAZAR H₀" if p_value < alpha_z2 else "NO RECHAZAR H₀"
            st.markdown(f"""
            <div class="result-box">
                <h3>📊 Prueba Z — Dos Muestras</h3>
                <div class="value">ẋ₁ − ẋ₂ = {x1_bar - x2_bar:.4f}</div>
                <div class="label">Diferencia observada entre medias</div>
                <div class="value" style="margin-top:0.6rem;">Z<sub>calc</sub> = {z_stat:.4f}</div>
                <div class="label">Estadístico de prueba</div>
                <div class="value" style="margin-top:0.6rem;">p-valor = {p_value:.6f}</div>
                <div class="label">Significancia observada</div>
                <div class="value" style="margin-top:0.6rem;">Z<sub>crítico</sub> = {z_crit:.4f}</div>
                <div class="value" style="margin-top:0.6rem; font-size:1.6rem;">{decision}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="sub-section-title">Diferencia entre Medias — Muestras Pequeñas (t)</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        metodo_tt = st.radio("Método", ["A partir de datos", "A partir de estadísticos"], key="tt_metodo")
        if metodo_tt == "A partir de datos":
            c1, c2 = st.columns(2)
            with c1:
                datos_tt1 = st.text_area("Muestra 1 (separados por coma)", "45, 47, 50, 52, 48, 51, 49", height=100, key="tt_d1")
            with c2:
                datos_tt2 = st.text_area("Muestra 2 (separados por coma)", "42, 44, 43, 46, 45, 44, 47", height=100, key="tt_d2")
            tail_tt = st.selectbox("Tipo de prueba", ["two (bilateral)", "left (unilateral izq)", "right (unilateral der)"], key="tt_tail")
            alpha_tt = st.slider("Nivel de significancia (α)", 0.01, 0.10, 0.05, format="%.2f", key="tt_alpha")
            if st.button("Realizar Prueba t (2 muestras)", key="calc_tt_data"):
                try:
                    m1 = np.array([float(x.strip()) for x in datos_tt1.split(",")])
                    m2 = np.array([float(x.strip()) for x in datos_tt2.split(",")])
                    x1_bar = np.mean(m1); x2_bar = np.mean(m2)
                    s1 = np.std(m1, ddof=1); s2 = np.std(m2, ddof=1)
                    n1 = len(m1); n2 = len(m2)
                    tail_map = {"two (bilateral)": "two", "left (unilateral izq)": "left", "right (unilateral der)": "right"}
                    t_stat, p_value, df, sp = two_sample_t_test(x1_bar, x2_bar, s1, s2, n1, n2, tail_map[tail_tt])
                    t_crit = sp_stats.t.ppf(1 - alpha_tt / 2, df) if tail_map[tail_tt] == "two" else sp_stats.t.ppf(alpha_tt, df) if tail_map[tail_tt] == "left" else sp_stats.t.ppf(1 - alpha_tt, df)
                    decision = "RECHAZAR H₀" if p_value < alpha_tt else "NO RECHAZAR H₀"
                    st.markdown(f"""
                    <div class="result-box">
                        <h3>📊 Prueba t — Dos Muestras Independientes</h3>
                        <div class="value">ẋ₁ = {x1_bar:.4f} &nbsp;|&nbsp; ẋ₂ = {x2_bar:.4f} &nbsp;|&nbsp; Diferencia = {x1_bar - x2_bar:.4f}</div>
                        <div class="label">Medias muestrales</div>
                        <div class="value" style="margin-top:0.6rem;">s₁ = {s1:.4f} &nbsp;|&nbsp; s₂ = {s2:.4f} &nbsp;|&nbsp; s<sub>p</sub> = {sp:.4f}</div>
                        <div class="label">Desviaciones y desviación pooled</div>
                        <div class="value" style="margin-top:0.6rem;">t<sub>calc</sub> = {t_stat:.4f} &nbsp;|&nbsp; gl = {df}</div>
                        <div class="label">Estadístico de prueba</div>
                        <div class="value" style="margin-top:0.6rem;">p-valor = {p_value:.6f}</div>
                        <div class="value" style="margin-top:0.6rem;">t<sub>crítico</sub> = {t_crit:.4f}</div>
                        <div class="value" style="margin-top:0.6rem; font-size:1.6rem;">{decision}</div>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Muestra 1**")
                x1_ts = st.number_input("ẋ₁", value=50.0, format="%.4f", key="tt_x1")
                s1_ts = st.number_input("s₁", min_value=0.0001, value=5.0, format="%.4f", key="tt_s1")
                n1_ts = st.number_input("n₁", min_value=2, value=15, key="tt_n1")
            with c2:
                st.markdown("**Muestra 2**")
                x2_ts = st.number_input("ẋ₂", value=45.0, format="%.4f", key="tt_x2")
                s2_ts = st.number_input("s₂", min_value=0.0001, value=5.0, format="%.4f", key="tt_s2")
                n2_ts = st.number_input("n₂", min_value=2, value=15, key="tt_n2")
            tail_ts = st.selectbox("Tipo de prueba", ["two (bilateral)", "left (unilateral izq)", "right (unilateral der)"], key="tt_tail_s")
            alpha_ts = st.slider("Nivel de significancia (α)", 0.01, 0.10, 0.05, format="%.2f", key="tt_alpha_s")
            if st.button("Realizar Prueba t", key="calc_tt_stats"):
                tail_map = {"two (bilateral)": "two", "left (unilateral izq)": "left", "right (unilateral der)": "right"}
                t_stat, p_value, df, sp = two_sample_t_test(x1_ts, x2_ts, s1_ts, s2_ts, int(n1_ts), int(n2_ts), tail_map[tail_ts])
                t_crit = sp_stats.t.ppf(1 - alpha_ts / 2, df) if tail_map[tail_ts] == "two" else sp_stats.t.ppf(alpha_ts, df) if tail_map[tail_ts] == "left" else sp_stats.t.ppf(1 - alpha_ts, df)
                decision = "RECHAZAR H₀" if p_value < alpha_ts else "NO RECHAZAR H₀"
                st.markdown(f"""
                <div class="result-box">
                    <h3>📊 Prueba t — Dos Muestras</h3>
                    <div class="value">ẋ₁ − ẋ₂ = {x1_ts - x2_ts:.4f}</div>
                    <div class="label">Diferencia observada</div>
                    <div class="value" style="margin-top:0.6rem;">s<sub>p</sub> = {sp:.4f} &nbsp;|&nbsp; gl = {df}</div>
                    <div class="label">Desviación pooled y grados de libertad</div>
                    <div class="value" style="margin-top:0.6rem;">t<sub>calc</sub> = {t_stat:.4f}</div>
                    <div class="value" style="margin-top:0.6rem;">p-valor = {p_value:.6f}</div>
                    <div class="value" style="margin-top:0.6rem;">t<sub>crítico</sub> = {t_crit:.4f}</div>
                    <div class="value" style="margin-top:0.6rem; font-size:1.6rem;">{decision}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="sub-section-title">Muestras Dependientes (Pareadas) — Prueba t</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            antes = st.text_area("Antes (separados por coma)", "85, 88, 90, 82, 86, 89, 84, 87", height=100, key="paired_antes")
        with c2:
            despues = st.text_area("Después (separados por coma)", "90, 92, 95, 88, 91, 93, 89, 91", height=100, key="paired_despues")
        tail_paired = st.selectbox("Tipo de prueba", ["two (bilateral)", "left (unilateral izq)", "right (unilateral der)"], key="paired_tail")
        alpha_paired = st.slider("Nivel de significancia (α)", 0.01, 0.10, 0.05, format="%.2f", key="paired_alpha")
        if st.button("Realizar Prueba t Pareada", key="calc_paired"):
            try:
                antes_arr = np.array([float(x.strip()) for x in antes.split(",")])
                despues_arr = np.array([float(x.strip()) for x in despues.split(",")])
                if len(antes_arr) != len(despues_arr):
                    st.error("Ambas muestras deben tener el mismo número de elementos")
                else:
                    tail_map = {"two (bilateral)": "two", "left (unilateral izq)": "left", "right (unilateral der)": "right"}
                    t_stat, p_value, df, d_bar, s_d = paired_t_test(antes_arr, despues_arr, tail_map[tail_paired])
                    t_crit = sp_stats.t.ppf(1 - alpha_paired / 2, df) if tail_map[tail_paired] == "two" else sp_stats.t.ppf(alpha_paired, df) if tail_map[tail_paired] == "left" else sp_stats.t.ppf(1 - alpha_paired, df)
                    decision = "RECHAZAR H₀" if p_value < alpha_paired else "NO RECHAZAR H₀"
                    diferencias = despues_arr - antes_arr
                    st.markdown(f"""
                    <div class="result-box">
                        <h3>📊 Prueba t Pareada</h3>
                        <div class="value">d̄ = {d_bar:.4f} &nbsp;|&nbsp; s<sub>d</sub> = {s_d:.4f}</div>
                        <div class="label">Media y desviación de las diferencias</div>
                        <div class="value" style="margin-top:0.6rem;">Diferencias: {', '.join(f'{d:+.2f}' for d in diferencias)}</div>
                        <div class="label">Diferencias individuales (Después − Antes)</div>
                        <div class="value" style="margin-top:0.6rem;">t<sub>calc</sub> = {t_stat:.4f} &nbsp;|&nbsp; gl = {df}</div>
                        <div class="label">Estadístico de prueba</div>
                        <div class="value" style="margin-top:0.6rem;">p-valor = {p_value:.6f}</div>
                        <div class="value" style="margin-top:0.6rem;">t<sub>crítico</sub> = {t_crit:.4f}</div>
                        <div class="value" style="margin-top:0.6rem; font-size:1.6rem;">{decision}</div>
                        <div class="label">p-valor {'<' if p_value < alpha_paired else '≥'} α</div>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
