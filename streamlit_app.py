import streamlit as st
from utilitários.theme import aplicar_tema, carregar_versao, rodape

# ========================
# CONFIGURAÇÕES E TEMA
# ========================
aplicar_tema()
versao = carregar_versao()

# ========================
# MENU LATERAL
# ========================
with st.sidebar:
    st.header("📋 Menu Principal")
    st.radio("Selecione uma categoria:", ["🏠 Início", "📦 Cadastros", "📊 Relatórios"], index=0)

# ========================
# CONTEÚDO PRINCIPAL
# ========================
st.title("FichApp")
st.caption("Gestão inteligente de fichas técnicas e custos gastronômicos")

st.divider()
st.subheader("📂 Módulos disponíveis")

col1, col2 = st.columns(2)

with col1:
    st.page_link("páginas/01_📦_Cadastro_de_Insumos.py", label="📦 Cadastro de Insumos")
    st.page_link("páginas/02_🧪_Ficha_Técnica.py", label="🧪 Ficha Técnica")

with col2:
    st.markdown("**📊 Relatórios (em breve)**")
    st.markdown("**⚙️ Configurações (em breve)**")

st.divider()

# ========================
# RODAPÉ
# ========================
rodape(versao)
