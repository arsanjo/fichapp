import streamlit as st

# ==============================
# Menu lateral unificado (fixo)
# ==============================
def menu_lateral():
    """
    Desenha o menu lateral do FichApp, igual em todas as páginas, e
    esconde o menu padrão do multipage do Streamlit.
    """

    # 1) Esconde completamente o nav padrão do Streamlit (seções "streamlit app" etc.)
    HIDE_DEFAULT_NAV = """
    <style>
      /* Esconde o container do menu padrão */
      section[data-testid="stSidebarNav"] { display: none !important; }
      /* Garante a sidebar aberta por padrão */
      [data-testid="stSidebar"] { min-width: 270px; }
    </style>
    """
    st.markdown(HIDE_DEFAULT_NAV, unsafe_allow_html=True)

    # 2) Força a sidebar expandida para o usuário
    st.set_page_config(initial_sidebar_state="expanded")

    # 3) Render do menu próprio
    with st.sidebar:
        # Logo (usa sua imagem enviada em assets)
        try:
            st.logo("assets/logo_fichapp.png")
        except Exception:
            st.markdown("### FichApp")

        st.markdown("#### Menu")

        # Links estáticos para as páginas
        # (st.page_link precisa do caminho relativo ao repo)
        st.page_link("streamlit_app.py", label="Início", icon=":material/home:")
        st.page_link(
            "pages/01_Cadastro_de_Insumos.py",
            label="Cadastro de Insumos",
            icon="📦",
        )
        st.page_link(
            "pages/02_💰_Parametros_Financeiros.py",
            label="Parâmetros Financeiros",
            icon="💰",
        )

        st.markdown("---")
        st.caption("Navegação fixa • FichApp")
