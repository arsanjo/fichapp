# utils/nav.py
# ---------------------------------------------------------
# Menu lateral fixo do FichApp (não desenha nada no corpo)
# ---------------------------------------------------------
import os
import streamlit as st
from PIL import Image

def sidebar_menu(ativo: str = "home"):
    """
    Desenha somente o menu lateral do FichApp.
    NÃO renderiza atalhos/menus no corpo da página.
    """
    # Ajustes de espaçamento do sidebar
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] {padding-top: 0.25rem !important;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    sb = st.sidebar

    # Logo (opcional)
    logo_path = os.path.join("assets", "logo_fichapp.png")
    if os.path.exists(logo_path):
        try:
            sb.image(Image.open(logo_path), use_container_width=True)
        except Exception:
            sb.image(logo_path, use_container_width=True)

    sb.markdown("### 📘 FichApp")
    sb.caption("Menu principal")
    sb.write("")

    # Helper para links
    def link(path: str, label: str, emoji: str):
        # st.page_link garante navegação entre as páginas (Streamlit 1.31+)
        sb.page_link(path, label=f"{emoji} {label}")

    # Navegação
    link("streamlit_app.py", "Início", "🏠")
    link("pages/01_Cadastro_de_Insumos.py", "Cadastro de Insumos", "📦")
    link("pages/02_Parametros_Financeiros.py", "Parâmetros Financeiros", "💰")
    link("pages/03_Engenharia_do_Cardapio.py", "Engenharia do Cardápio", "📊")
    link("pages/04_Ficha_Tecnica.py", "Ficha Técnica", "🧾")

    sb.markdown("---")
    sb.caption("FichApp v1.0.0")
