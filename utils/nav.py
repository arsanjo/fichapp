import streamlit as st
import os

# ============================================================
# FUNÇÃO DE LINK PERSONALIZADO (USADA NO MENU LATERAL)
# ============================================================
def link(filename: str, label: str, emoji: str = ""):
    """
    Cria um link lateral com ícone e texto para cada página.
    O caminho é resolvido dinamicamente para evitar erros no Streamlit Cloud.
    """
    base_path = os.path.dirname(__file__)  # utils/
    app_root = os.path.abspath(os.path.join(base_path, ".."))  # volta para raiz (fichapp)
    page_path = os.path.join(app_root, filename)  # ex: fichapp/00_Home.py

    # Remove ./ e converte para formato compatível
    rel_path = os.path.relpath(page_path, app_root)

    st.sidebar.page_link(
        rel_path,
        label=f"{emoji} {label}" if emoji else label
    )

# ============================================================
# MENU LATERAL FIXO - PADRÃO FICHAPP
# ============================================================
def sidebar_menu(ativo: str = "home"):
    """
    Renderiza o menu lateral fixo do FichApp.
    Essa função deve ser chamada no início de cada página.
    """
    with st.sidebar:
        st.markdown("### 📘 FichApp")
        st.markdown("#### Menu principal")

        link("00_Home.py", "Início", "🏠")
        link("01_Cadastro_de_Insumos.py", "Cadastro de Insumos", "📦")
        link("02_Parametros_Financeiros.py", "Parâmetros Financeiros", "💰")
        link("03_Engenharia_do_Cardapio.py", "Engenharia do Cardápio", "📊")
        link("04_Ficha_Tecnica_Cozinha.py", "Ficha Técnica (Cozinha)", "👨‍🍳")
        link("05_Ficha_Tecnica_Admin.py", "Ficha Técnica (Administrativa)", "📑")

        st.markdown("---")
        st.caption("FichApp v1.0.0 | Desenvolvido por Arsanjo")
