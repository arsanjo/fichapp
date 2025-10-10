import streamlit as st
from datetime import date

# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================
st.set_page_config(
    page_title="FichApp - Início",
    page_icon="📘",
    layout="wide"
)

# =========================================================
# CABEÇALHO COM LOGO
# =========================================================
col_logo, col_titulo = st.columns([1, 6])
with col_logo:
    # 🔹 caminho da logomarca oficial (já está na pasta assets/)
    st.image("assets/logo_fichapp.png", width=120)
with col_titulo:
    st.markdown("""
        <h1 style="margin-bottom: 0px;">FichApp</h1>
        <h4 style="color: gray; margin-top: 0;">Sistema de Controle de Fichas Técnicas e Insumos</h4>
    """, unsafe_allow_html=True)

st.divider()

# =========================================================
# MENSAGEM DE BOAS-VINDAS
# =========================================================
st.markdown("""
🧾 **Bem-vindo ao FichApp!**

Aqui você poderá **cadastrar insumos**, **criar fichas técnicas completas** e **acompanhar custos em tempo real**, de forma simples, precisa e integrada ao seu controle financeiro.
""")

st.info("🚀 O FichApp está em constante evolução. Em breve novas funções de cálculo de receitas e relatórios dinâmicos serão ativadas!")

# =========================================================
# RODAPÉ / INFORMAÇÕES
# =========================================================
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: gray;'>
        <b>FichApp</b> v1.1.0 — atualizado em {date.today().strftime("%Y-%m-%d")}<br>
        Desenvolvido por <b>Arsanjo</b>
    </div>
    """,
    unsafe_allow_html=True
)
