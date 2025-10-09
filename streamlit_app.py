import streamlit as st
import sys, os
from datetime import datetime

# ---------------------------------------------------
# Corrige o caminho do módulo utils (importações locais)
# ---------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from utils.theme import aplicar_tema, carregar_versao, rodape

# ===================================================
# Inicialização do aplicativo principal
# ===================================================
aplicar_tema()
versao = carregar_versao("versao.json")

st.title("🍣 FichApp — Gestão Gastronômica")
st.markdown(f"**Versão atual:** {versao['versao']} — lançada em {versao['data_lancamento']}")

st.write("Bem-vindo ao FichApp! Selecione uma opção no menu lateral para começar.")
st.info("📦 Use o menu à esquerda para cadastrar ou visualizar insumos.")

# ===================================================
# Rodapé
# ===================================================
rodape()
