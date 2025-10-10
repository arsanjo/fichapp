import streamlit as st
from utils.nav import sidebar_menu

# ============================================================
# CONFIGURAÇÕES INICIAIS
# ============================================================
st.set_page_config(
    page_title="FichApp - Início",
    page_icon="📘",
    layout="wide"
)

# ============================================================
# MENU LATERAL
# ============================================================
sidebar_menu(ativo="home")

# ============================================================
# CONTEÚDO PRINCIPAL DA PÁGINA
# ============================================================
st.title("🏠 Bem-vindo ao FichApp!")
st.markdown("---")

st.markdown(
    """
    ### Seu sistema inteligente para gestão de fichas técnicas e custos de produção 🍣🍔  
    O **FichApp** foi desenvolvido para integrar todas as etapas de controle de insumos, engenharia do cardápio e análise financeira em um só lugar.

    #### ⚙️ Funcionalidades principais:
    - **Cadastro de Insumos:** registre e atualize todos os ingredientes utilizados na produção.
    - **Parâmetros Financeiros:** defina margens, impostos e custos fixos.
    - **Engenharia do Cardápio:** avalie rentabilidade e popularidade de cada item.
    - **Fichas Técnicas (Cozinha e Administrativa):** mantenha padrão e controle total dos produtos.
    
    ---
    #### 💡 Dica:
    Use o menu lateral para navegar entre as seções do sistema.
    """
)

st.info("Versão atual: **v1.0.0** — Base Estável | Desenvolvido por Arsanjo")
