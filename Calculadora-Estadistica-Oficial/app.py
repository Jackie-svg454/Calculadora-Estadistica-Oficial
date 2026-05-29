import streamlit as st

st.set_page_config(
    page_title="Calculadora Estadística - Proyecto Final",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;400;600&display=swap');

    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 3.2rem;
        color: #1A3A5C;
        text-align: center;
        padding: 1.2rem 0 0.3rem 0;
        letter-spacing: 2px;
        border-bottom: 3px solid #D4AF37;
        margin-bottom: 0.5rem;
    }

    .sub-title {
        text-align: center;
        color: #4A6A8A;
        font-size: 1.1rem;
        font-weight: 300;
        margin-bottom: 2rem;
    }

    .section-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        color: #1A3A5C;
        border-left: 5px solid #D4AF37;
        padding-left: 1rem;
        margin: 2rem 0 1.2rem 0;
    }

    .member-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F0F4F8 100%);
        border: 1px solid #D4AF37;
        border-radius: 12px;
        padding: 0.9rem 1.2rem;
        margin: 0.4rem 0;
        box-shadow: 0 2px 8px rgba(26, 58, 92, 0.08);
        transition: transform 0.2s;
        font-weight: 500;
        color: #1A3A5C;
    }

    .member-card:hover {
        transform: translateX(6px);
        box-shadow: 0 4px 16px rgba(212, 175, 55, 0.2);
        border-color: #C4A030;
    }

    .category-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 0.8rem 1.2rem;
        margin: 0.4rem 0;
        border-left: 4px solid #D4AF37;
        box-shadow: 0 2px 6px rgba(26, 58, 92, 0.06);
        color: #2A4A6A;
        font-weight: 500;
        font-size: 0.95rem;
    }

    .category-card:hover {
        background: #F8FAFC;
        border-left-color: #1A3A5C;
    }

    .gold-accent {
        color: #D4AF37;
        font-weight: 600;
    }

    .footer-text {
        text-align: center;
        color: #8A9AAA;
        font-size: 0.85rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #E0E6EC;
    }

    .stApp {
        background-color: #F0F4F8;
    }
</style>
""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        "<h2 style='text-align: center; color: #D4AF37; font-family: Playfair Display; font-size: 1.6rem;'>📊 NAVEGACIÓN</h2>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown(
        "<p style='color: #4A6A8A; font-size: 0.9rem; text-align: center;'>Seleccione una categoría del menú superior</p>",
        unsafe_allow_html=True,
    )
    st.image(
        "https://img.icons8.com/fluency/96/statistics.png",
        width=80,
        use_container_width=True,
    )
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #1A3A5C; font-weight: 600;'>🎓 Estadística II</p>",
        unsafe_allow_html=True,
    )

st.markdown('<div class="main-title">PROYECTO FINAL DE ESTADÍSTICA II</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Calculadora Estadística · Análisis y Probabilidad · Mayo 2026</div>',
    unsafe_allow_html=True,
)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="section-title">👥 INTEGRANTES</div>', unsafe_allow_html=True)
    miembros = [
        "Jackeline Yaretzy Monterroso Pérez",
        "Marcos Anthony López Pérez",
        "Luz Elena de León Méndez",
        "Hainer Yohandri Pérez Coronado",
        "Erickson Samuel Pérez Gómez",
        "Andrea Alexandra Margarita Salazar de León",
        "Abner Edilzar Florencio Velásquez",
        "Magdiel Jonathan Roblero Roblero",
    ]
    for m in miembros:
        st.markdown(f'<div class="member-card">✦ {m}</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-title">📚 CATEGORÍAS</div>', unsafe_allow_html=True)
    categorias = [
        "Distribuciones de Probabilidad",
        "Muestreo y Distribuciones de Muestreo",
        "Estimación",
        "Prueba de Hipótesis (Una Muestra)",
        "Prueba de Hipótesis (Dos Muestras)",
        "Regresión Simple y Correlación",
    ]
    for c in categorias:
        st.markdown(f'<div class="category-card">▸ {c}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title" style="margin-top:2rem;">⚙️ SUBTEMAS</div>', unsafe_allow_html=True)
    subtemas = [
        "Variables aleatorias · Binomial · Poisson · Normal",
        "Muestreo aleatorio · Error estándar",
        "Puntual · Intervalo (media, proporción) · t · Tamaño muestra",
        "Medias (σ conocida) · Proporciones · Medias (σ desconocida)",
        "Diferencias entre medias (grandes, pequeñas, dependientes)",
        "Recta de regresión · Correlación · Inferencias",
    ]
    for s in subtemas:
        st.markdown(f'<div class="category-card" style="font-size:0.85rem; color:#4A6A8A;">▹ {s}</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="footer-text">Seleccione una categoría en el menú superior (📄) para comenzar sus cálculos estadísticos</div>',
    unsafe_allow_html=True,
)
