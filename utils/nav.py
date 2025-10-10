import streamlit as st

# ============================================================
# MENU LATERAL FIXO - FichApp
# ============================================================
def sidebar_menu(ativo="inicio"):
    with st.sidebar:
        # LOGO E TÍTULO
        st.markdown("## 🧾 FichApp")
        st.markdown("### Menu")
        st.markdown("---")

        # =========================
        # LINKS DE NAVEGAÇÃO
        # =========================
        st.page_link(
            "streamlit_app.py",
            label="🏠 Início",
            disabled=(ativo == "inicio")
        )

        st.page_link(
            "pages/01_Cadastro_de_Insumos.py",
            label="📦 Cadastro de Insumos",
            disabled=(ativo == "insumos")
        )

        st.page_link(
            "pages/02_💰_Parametros_Financeiros.py",
            label="💰 Parâmetros Financeiros",
            disabled=(ativo == "parametros")
        )

        st.page_link(
            "pages/03_📊_Engenharia_do_Cardapio.py",
            label="📊 Engenharia do Cardápio",
            disabled=(ativo == "engenharia")
        )

        st.markdown("---")
        st.caption("Navegação fixa • FichApp v1.0.0")
