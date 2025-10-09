import streamlit as st
from utils.theme import aplicar_tema, carregar_versao, rodape

# ============================
# Configuração e layout base
# ============================

# Aplica o tema escuro global
aplicar_tema()

# Carrega a versão atual
versao = carregar_versao("versao.json")

# Barra lateral (menu principal)
st.sidebar.title("📋 Menu Principal")
menu = st.sidebar.radio("Selecione uma categoria:", ["🏠 Início", "📦 Cadastros", "📊 Relatórios"])

# ============================
# Páginas principais
# ============================

if menu == "🏠 Início":
    st.title("FichApp")
    st.markdown("### Gestão inteligente de fichas técnicas e custos gastronômicos")
    st.write("---")

    st.subheader("Bem-vindo ao FichApp 👋")
    st.markdown("""
    O **FichApp** é um sistema profissional de gestão gastronômica que permite:
    - Cadastrar e gerenciar insumos
    - Montar fichas técnicas completas
    - Calcular custos e rendimentos
    - Gerar relatórios inteligentes de desempenho e margem  
      
    Use o menu lateral para navegar entre as seções.
    """)

elif menu == "📦 Cadastros":
    st.title("📦 Cadastros")
    st.markdown("Selecione o módulo desejado na barra superior:")
    st.markdown("- [Cadastro de Insumos](pages/01_📦_Cadastro_de_Insumos.py)")
    st.markdown("- [Ficha Técnica](pages/02_🧪_Ficha_Tecnica.py) *(em breve)*")

elif menu == "📊 Relatórios":
    st.title("📊 Relatórios")
    st.info("Em desenvolvimento...")

# ============================
# Rodapé e versão
# ============================
st.write("---")
st.markdown(
    f"**FichApp v{versao['versao']}** — última atualização: {versao['data_lancamento']}"
)
st.markdown("> _“Sede fortes e corajosos.” — Josué 1:9_")

rodape()
