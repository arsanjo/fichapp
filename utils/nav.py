import streamlit as st

# ============================================================
# FUNÇÃO DE LINK PERSONALIZADO (USADA NO MENU LATERAL)
# ============================================================
def link(path: str, label: str, emoji: str = ""):
    """
    Cria um link lateral com ícone e texto para cada página.
    """
    st.sidebar.page_link(
        path,
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
        # CABEÇALHO
        st.markdown("### 📘 FichApp")
        st.markdown("#### Menu principal")

        # LINKS DE NAVEGAÇÃO
        link("00_Home.py", "Início", "🏠")
        link("01_Cadastro_de_Insumos.py", "Cadastro de Insumos", "📦")
        link("02_Parametros_Financeiros.py", "Parâmetros Financeiros", "💰")
        link("03_Engenharia_do_Cardapio.py", "Engenharia do Cardápio", "📊")
        link("04_Ficha_Tecnica_Cozinha.py", "Ficha Técnica (Cozinha)", "👨‍🍳")
        link("05_Ficha_Tecnica_Admin.py", "Ficha Técnica (Administrativa)", "📑")

        # RODAPÉ
        st.markdown("---")
        st.markdown("##### FichApp v1.0.0")
        st.caption("Desenvolvido por Arsanjo")
