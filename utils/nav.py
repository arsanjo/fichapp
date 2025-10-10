# utils/nav.py
import streamlit as st

def _css_sidebar():
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"]{min-width:270px; background:#f5f6fa;}
        [data-testid="stSidebar"] h3{margin-top:.5rem; margin-bottom:.2rem;}
        [data-testid="stSidebar"] .subtle{color:#6b7280; font-size:12px; margin:6px 0 10px;}
        </style>
        """,
        unsafe_allow_html=True,
    )

def sidebar_menu(ativo: str = ""):
    """Desenha o menu lateral único do FichApp.
    Parâmetro `ativo` é apenas informativo (se quiser realçar algo no futuro)."""
    _css_sidebar()

    st.sidebar.markdown("### FichApp")
    st.sidebar.markdown("<div class='subtle'>Menu</div>", unsafe_allow_html=True)

    st.sidebar.page_link("streamlit_app.py", label="Início", icon="🏠")
    st.sidebar.page_link("pages/01_Cadastro_de_Insumos.py", label="Cadastro de Insumos", icon="📦")
    st.sidebar.page_link("pages/02_💰_Parametros_Financeiros.py", label="Parâmetros Financeiros", icon="💰")
