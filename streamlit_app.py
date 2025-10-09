import streamlit as st
import os
from utils.theme import aplicar_tema, carregar_versao, rodape

# ============================
# CONFIGURAÇÃO GLOBAL
# ============================
aplicar_tema()
versao = carregar_versao("versao.json")

# ============================
# MENU PRINCIPAL
# ============================
st.sidebar.title("📋 Menu Principal")
menu = st.sidebar.radio("Selecione uma categoria:", ["🏠 Início", "📦 Cadastros", "📊 Relatórios"])

# ============================
# FUNÇÃO PARA LISTAR PÁGINAS
# ============================
def listar_paginas():
    """Lista todos os arquivos .py dentro da pasta /pages e retorna seus nomes formatados."""
    paginas = []
    if os.path.exists("pages"):
        for arquivo in sorted(os.listdir("pages")):
            if arquivo.endswith(".py"):
                nome_formatado = arquivo.replace("_", " ").replace(".py", "")
                paginas.append(nome_formatado)
    return paginas

# ============================
# CONTEÚDO PRINCIPAL
# ============================
if menu == "🏠 Início":
    st.title("FichApp")
    st.markdown("### Gestão inteligente de fichas técnicas e custos gastronômicos")
    st.write("---")

    st.subheader("Bem-vindo ao FichApp 👋")
    st.markdown("""
    O **FichApp** é um sistema profissional de gestão gastronômica que permite:
    - 📦 Cadastrar e gerenciar insumos
    - 🧪 Montar fichas técnicas completas
    - 💰 Calcular custos e rendimentos
    - 📊 Gerar relatórios de desempenho e margem  
    
    Use o menu lateral para navegar entre as seções.
    """)

elif menu == "📦 Cadastros":
    st.title("📦 Módulos de Cadastro")
    st.write("Selecione um módulo disponível:")

    paginas = listar_paginas()
    for p in paginas:
        st.markdown(f"- [{p}](pages/{p.replace(' ', '_')}.py)")

elif menu == "📊 Relatórios":
    st.title("📊 Relatórios")
    st.info("Módulo de relatórios em desenvolvimento...")

# ============================
# RODAPÉ
# ============================
st.write("---")
st.markdown(
    f"**FichApp v{versao['versao']}** — última atualização: {versao['data_lancamento']}"
)
st.markdown("> _“Sede fortes e corajosos.” — Josué 1:9_")

rodape()
