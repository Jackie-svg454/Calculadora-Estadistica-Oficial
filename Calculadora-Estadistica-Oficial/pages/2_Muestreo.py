import streamlit as st
import numpy as np
import pandas as pd
from utils.formulas import *

st.set_page_config(page_title="Muestreo y Distribuciones de Muestreo", layout="wide", initial_sidebar_state="expanded")

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

st.markdown('<div class="page-header">🎯 Muestreo y Distribuciones de Muestreo</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Muestreo Aleatorio", "Error Estándar"])

with tab1:
    st.markdown('<div class="sub-section-title">Generación de Muestra Aleatoria</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.write("Ingrese su población (separada por comas):")
        poblacion_input = st.text_area("Población", "10, 12, 15, 18, 20, 22, 25, 28, 30, 35", height=80, key="pob_input")
        c1, c2 = st.columns(2)
        n_muestra = c1.number_input("Tamaño de muestra (n)", min_value=1, max_value=500, value=5, key="n_muestra")
        semilla = c2.number_input("Semilla (opcional)", min_value=0, max_value=9999, value=42, key="semilla")
        if st.button("Generar Muestra", key="calc_muestreo"):
            try:
                poblacion = [float(x.strip()) for x in poblacion_input.split(",")]
                np.random.seed(int(semilla))
                muestra = np.random.choice(poblacion, size=int(n_muestra), replace=False)
                media_muestral = np.mean(muestra)
                media_poblacional = np.mean(poblacion)
                st.markdown(f"""
                <div class="result-box">
                    <h3>📊 Resultados del Muestreo</h3>
                    <div class="value">Muestra: {', '.join(f'{v:.2f}' for v in muestra)}</div>
                    <div class="label">Elementos seleccionados aleatoriamente</div>
                    <div class="value" style="margin-top:0.6rem;">Media muestral (ẋ) = {media_muestral:.4f}</div>
                    <div class="label">Promedio de la muestra</div>
                    <div class="value" style="margin-top:0.6rem;">Media poblacional (μ) = {media_poblacional:.4f}</div>
                    <div class="label">Promedio de la población original</div>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="sub-section-title">Relación entre Tamaño de Muestra y Error Estándar</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        tipo_error = st.radio("Tipo de error estándar", ["Media (σ conocida)", "Proporción"])
        if tipo_error == "Media (σ conocida)":
            c1, c2 = st.columns(2)
            sigma_pob = c1.number_input("σ (desviación poblacional)", min_value=0.0001, value=15.0, format="%.4f", key="se_sigma")
            n_se = c2.number_input("n (tamaño de muestra)", min_value=1, max_value=10000, value=100, key="se_n")
            if st.button("Calcular Error Estándar", key="calc_se_media"):
                se = standard_error_mean(sigma_pob, int(n_se))
                st.markdown(f"""
                <div class="result-box">
                    <h3>📊 Error Estándar de la Media</h3>
                    <div class="value">σ_ẋ = {se:.4f}</div>
                    <div class="label">σ / √n = {sigma_pob:.4f} / √{int(n_se)}</div>
                    <div class="value" style="margin-top:0.6rem;">
                        σ_ẋ × √n = {sigma_pob:.4f}
                    </div>
                    <div class="label">Verificación: σ_ẋ · √n = σ</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            c1, c2 = st.columns(2)
            p_se = c1.number_input("p (proporción estimada)", min_value=0.0001, max_value=0.9999, value=0.5, format="%.4f", key="se_p")
            n_se_p = c2.number_input("n (tamaño de muestra)", min_value=1, max_value=10000, value=100, key="se_n_p")
            if st.button("Calcular Error Estándar", key="calc_se_prop"):
                se = standard_error_proportion(p_se, int(n_se_p))
                st.markdown(f"""
                <div class="result-box">
                    <h3>📊 Error Estándar de la Proporción</h3>
                    <div class="value">σ_ṗ = {se:.4f}</div>
                    <div class="label">√(p(1-p)/n) = √({p_se:.4f}·{1-p_se:.4f}/{int(n_se_p)})</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sub-section-title">Análisis: Error Estándar vs Tamaño de Muestra</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        sigma_analisis = st.number_input("σ para análisis", min_value=0.0001, value=15.0, format="%.2f", key="se_analisis")
        tamanos = [10, 20, 30, 50, 75, 100, 150, 200, 300, 500]
        errores = [standard_error_mean(sigma_analisis, n) for n in tamanos]
        df_se = pd.DataFrame({"n": tamanos, "Error Estándar": errores})
        import plotly.express as px
        fig = px.line(df_se, x="n", y="Error Estándar",
                      title="Error Estándar vs Tamaño de Muestra",
                      markers=True,
                      color_discrete_sequence=["#1A3A5C"])
        fig.update_traces(line_width=3, marker=dict(size=8, color="#D4AF37"))
        fig.update_layout(
            plot_bgcolor="#F0F4F8",
            paper_bgcolor="#FFFFFF",
            font=dict(color="#1A3A5C"),
            xaxis_title="Tamaño de muestra (n)",
            yaxis_title="Error Estándar (σ_ẋ)",
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            '<p style="color:#4A6A8A; font-style:italic; text-align:center;">'
            'A mayor tamaño de muestra, menor es el error estándar (relación inversa con √n)</p>',
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)
