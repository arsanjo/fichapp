# streamlit_app.py - CÓDIGO CORRIGIDO PARA NAVEGAÇÃO

# =========================================================
# FichApp - Sistema de controle de fichas técnicas e insumos
# =========================================================
import streamlit as st
from utils.nav import sidebar_menu, MENU_PAGES # Importa a função e o dicionário de páginas
import datetime
import os
import importlib.util

# =========================================================
# FUNÇÃO PARA CARREGAR O CONTEÚDO DA PÁGINA ATIVA
# =========================================================
def load_page_content(page_key):
    # Mapeia a chave de estado para o nome do arquivo (ex: 'insumos' -> '01_Cadastro_de_Insumos.py')
    # O StreamlitApp.py cuida da HOME.
    
    if page_key == "home":
        # Se for HOME, carregamos o conteúdo padrão da HOME que você já tinha no 00_Home.py
        # NOTA: O código da HOME será movido para baixo para evitar a importação circular!
        return 
    
    # Busca o nome do arquivo baseado na chave
    filename = next((file for label, file in MENU_PAGES.items() if MENU_PAGES[label] == page_key), None)
    
    if filename:
        # Tenta carregar o módulo da página (os arquivos de página estão na raiz, como você indicou)
        # Atenção: Este método exige que você mova as funções de execução para dentro de um bloco
        # ou use uma função para o conteúdo de cada arquivo de página.
        try:
            # Caminho relativo ao arquivo principal (que está na raiz)
            module_name = filename.replace(".py", "")
            
            # CRÍTICO: Vamos usar a convenção de que o arquivo 'filename' tem uma função 'run_page()'
            # que deve ser executada.
            
            spec = importlib.util.spec_from_file_location(module_name, filename)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Se o arquivo de página tiver uma função 'run_page()', ele a executa.
            # Caso contrário, ele executa o código do arquivo como um script.
            if hasattr(module, 'run_page'):
                module.run_page()
            
        except Exception as e:
            st.error(f"Erro ao carregar a página {filename}: {e}")
            st.warning("Verifique se o arquivo da página existe na raiz e se não tem erros de sintaxe.")
    else:
        st.error(f"Página não encontrada para a chave: {page_key}")


# =========================================================
# CONFIGURAÇÕES INICIAIS DA APLICAÇÃO
# =========================================================
st.set_page_config(
    page_title="FichApp",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None  # 🚫 remove o menu automático do Streamlit
)

# =========================================================
# MENU LATERAL
# =========================================================
# Esta chamada agora inicia o st.session_state.current_page
sidebar_menu(ativo="home") 


# =========================================================
# EXECUÇÃO DO CONTEÚDO
# =========================================================
# Executa a função que carrega o conteúdo da página ativa
load_page_content(st.session_state.current_page)


# =========================================================
# HOME (Apenas se for a página inicial)
# =========================================================
if st.session_state.current_page == "home":
    st.markdown("<h1 style='text-align: center;'>FichApp</h1>", unsafe_allow_html=True)
    st.markdown(
        "<h4 style='text-align: center; color: gray;'>Sistema de controle de fichas técnicas e insumos</h4>",
        unsafe_allow_html=True
    )
    # Conteúdo da HOME (Versículo e Rodapé que já estavam no código original)
    st.write("")
    st.markdown("---")
    st.markdown(
        """
        <p style="text-align: center; font-style: italic; color: #555;">
        “E tudo quanto fizerdes, fazei-o de todo o coração, como ao Senhor, e não aos homens.”<br>
        <b>Colossenses 3:23</b>
        </p>
        """,
        unsafe_allow_html=True
    )

    # RODAPÉ - INFORMAÇÕES DE VERSÃO
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="background-color: #0b132b; color: white; border-radius: 10px; padding: 1.5rem; text-align: center;">
            <b>FichApp v1.0.0</b> — atualizado em {datetime.date.today().strftime("%Y-%m-%d")}<br>
            Desenvolvido por <b>Arsanjo</b>
        </div>
        """,
        unsafe_allow_html=True
    )

# FIM do arquivo streamlit_app.py
