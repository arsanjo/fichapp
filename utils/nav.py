# utils/nav.py - CORRIGIDO PARA EXIBIR A LOGO FICHAPP

import streamlit as st

# Mapeamento do Rótulo do Menu -> Nome do Arquivo (na raiz do projeto)
MENU_PAGES = {
    "Cadastro de Insumos": "01_Cadastro_de_Insumos.py",
    "Parâmetros Financeiros": "02_Parametros_Financeiros.py",
    "Engenharia do Cardápio": "03_Engenharia_do_Cardapio.py",
    "Ficha Técnica - Cozinha": "04_Ficha_Tecnica_Cozinha.py",
    "Ficha Técnica - Admin": "05_Ficha_Tecnica_Admin.py"
}

def sidebar_menu(ativo="home"):
    """
    Cria o menu lateral e usa o estado de sessão para controlar a página ativa.
    """
    
    # 1. Inicializa o estado da página se ainda não existir
    if 'current_page' not in st.session_state:
        st.session_state.current_page = ativo
    
    # === ADICIONA A LOGOMARCA FichApp NO TOPO DO MENU LATERAL ===
    # CORREÇÃO: Usando o nome do arquivo que está na pasta assets/
    st.sidebar.image("assets/logo_fichapp.png", use_column_width="always")
    # =============================================================

    st.sidebar.markdown("---")
    
    # 2. Botão da Página Inicial (Home)
    if st.sidebar.button("🏠 Início", key="nav_home"):
        st.session_state.current_page = "home"
        st.rerun()

    st.sidebar.markdown("---") 

    # 3. Botões das Páginas Secundárias
    for label, filename in MENU_PAGES.items():
        page_key = filename
        
        # Cria o botão e verifica o clique
        if st.sidebar.button(label, key=f"nav_{page_key}"):
            st.session_state.current_page = page_key
            st.rerun() 
            
    st.sidebar.markdown("---") 
    st.sidebar.markdown("Desenvolvido por Arsanjo")

# FIM do arquivo utils/nav.py
