# utils/nav.py - CÓDIGO CORRIGIDO PARA NAVEGAÇÃO INTERNA

import streamlit as st

# Mapeamento do Rótulo do Menu -> Chave de Estado (Identificador único)
MENU_PAGES = {
    "Cadastro de Insumos": "insumos",
    "Parâmetros Financeiros": "parametros",
    "Engenharia do Cardápio": "engenharia",
    "Ficha Técnica - Cozinha": "ficha_cozinha",
    "Ficha Técnica - Admin": "ficha_admin",
}

def sidebar_menu(ativo="home"):
    """
    Cria o menu lateral e usa o estado de sessão para controlar a página ativa.
    """
    
    # 1. Inicializa o estado da página se ainda não existir
    if 'current_page' not in st.session_state:
        st.session_state.current_page = ativo

    st.sidebar.markdown("---")
    
    # 2. Botão da Página Inicial (Home)
    if st.sidebar.button("🏠 Início", key="nav_home"):
        st.session_state.current_page = "home"
        st.rerun()

    st.sidebar.markdown("---") 

    # 3. Botões das Páginas Secundárias
    for label, page_key in MENU_PAGES.items():
        # Usa um ícone genérico para não precisar de um ícone para cada página
        icon = "⚫"
        
        # Cria o botão e verifica o clique
        if st.sidebar.button(label, key=f"nav_{page_key}"):
            st.session_state.current_page = page_key
            st.rerun() # Recarrega a página para exibir o novo conteúdo
            
    st.sidebar.markdown("---") 
    st.sidebar.markdown("Desenvolvido por Arsanjo")

# FIM do arquivo utils/nav.py
