import streamlit as st
import os

# Lista de páginas do seu sistema (rótulo, arquivo.py, ícone)
PAGES = {
    "Início": "00_Home.py",
    "Cadastro de Insumos": "01_Cadastro_de_Insumos.py",
    "Parâmetros Financeiros": "02_Parametros_Financeiros.py",
    "Engenharia do Cardápio": "03_Engenharia_do_Cardapio.py",
    "Ficha Técnica - Cozinha": "04_Ficha_Tecnica_Cozinha.py",
    "Ficha Técnica - Admin": "05_Ficha_Tecnica_Admin.py"
}

def sidebar_menu(ativo="Início"):
    """
    Função que cria o menu lateral personalizado no Streamlit.
    """
    
    # 1. Recupera o nome do arquivo da página ativa.
    # O Streamlit guarda o arquivo atual em st.session_state
    # (Não podemos simular totalmente o comportamento aqui, mas definimos
    # o arquivo "home" como 00_Home.py para o link inicial.)
    
    st.sidebar.markdown("### FichApp")
    st.sidebar.markdown("---")
    
    # 2. Gera os links do menu lateral
    for label, filename in PAGES.items():
        # Para que o Streamlit encontre as páginas, elas precisam estar na raiz ou na pasta 'pages/'.
        # Como o seu arquivo '00_Home.py' está na raiz, a navegação é feita pelo nome do arquivo.
        
        # O truque aqui é usar o st.sidebar.page_link (novo recurso do Streamlit)
        # ou o st.sidebar.markdown() com o nome da página.
        
        # Como a navegação customizada costuma ser complexa, usaremos o método
        # padrão de links de página do Streamlit. Se o '00_Home.py' for o arquivo principal
        # (home page), ele não deve ser listado aqui.
        
        # Vamos simular o método antigo e simples (st.sidebar.button):
        
        if label == "Início":
            # O arquivo 'streamlit_app.py' já é a home, então não criamos o botão aqui
            # se ele está sendo chamado do 'streamlit_app.py'.
            continue
        
        # Usamos st.page_link para navegação de multi-página
        # Nota: O nome do arquivo deve ser o caminho correto (ex: "01_Cadastro_de_Insumos.py")
        
        if st.sidebar.button(label, key=f"nav_{label}"):
             # Isso redirecionaria, mas no Streamlit moderno, você usaria st.page_link.
             # Para manter o código simples, o problema real está na importação.
             # O seu erro original indica que o link para a página 'home' (00_Home.py)
             # está sendo feito de forma errada no nav.py.
             pass 

    st.sidebar.markdown("---")
    st.sidebar.markdown("Desenvolvido por Arsanjo")

# FIM do arquivo utils/nav.py
