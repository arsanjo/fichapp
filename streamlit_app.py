import streamlit as st
from utils.theme import aplicar_tema, rodape

# ======================================================
# CONFIGURAÇÃO INICIAL
# ======================================================

# Aplica o tema escuro e define o layout da página
aplicar_tema()

# Título principal
st.title("📘 FichApp")
st.write("Bem-vindo ao sistema de controle de fichas técnicas e insumos!")

# ======================================================
# CONTEÚDO PRINCIPAL TEMPORÁRIO
# ======================================================

st.info(
    "🚀 O FichApp está em construção. Em breve você poderá cadastrar insumos, "
    "criar fichas técnicas e acompanhar custos em tempo real."
)

# ======================================================
# RODAPÉ
# ======================================================
rodape()
