import streamlit as st

# ============================================================
# MENU LATERAL FIXO - PADRÃO FICHAPP
# ============================================================

def sidebar_menu(ativo="Início"):
    """
    Cria o menu lateral fixo do FichApp com navegação funcional entre páginas.
    """

    with st.sidebar:
        # Cabeçalho
        st.markdown("### 📘 FichApp")
        st.markdown("#### Menu principal")
        st.markdown("---")

        # Navegação entre páginas usando o novo recurso do Streamlit
        st.sidebar.page_link("01_Cadastro_de_Insumos.py", label="Cadastro de Insumos", icon="📦")
        st.sidebar.page_link("02_Parametros_Financeiros.py", label="Parâmetros Financeiros", icon="💰")
        st.sidebar.page_link("03_Engenharia_do_Cardapio.py", label="Engenharia do Cardápio", icon="📊")
        st.sidebar.page_link("04_Ficha_Tecnica_Cozinha.py", label="Ficha Técnica - Cozinha", icon="👨‍🍳")
        st.sidebar.page_link("05_Ficha_Tecnica_Admin.py", label="Ficha Técnica - Admin", icon="📑")

        # Rodapé
        st.markdown("---")
        st.caption("Desenvolvido por Arsanjo")
