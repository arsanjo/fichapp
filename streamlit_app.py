# streamlit_app.py - CÓDIGO FINAL COM CORREÇÃO DE RESPONSIVIDADE

# =========================================================
# FichApp - Sistema de controle de fichas técnicas e insumos
# =========================================================
import streamlit as st
from utils.nav import sidebar_menu, MENU_PAGES 
import datetime
import os

# =========================================================
# FUNÇÃO PARA CARREGAR O CONTEÚDO DA PÁGINA ATIVA
# (Mantida a mesma lógica funcional)
# =========================================================
def load_page_content(page_key):
    filename = page_key 

    if page_key == "home":
        # Conteúdo da Home (FichApp)
        st.markdown("<h1 style='text-align: center;'>FichApp</h1>", unsafe_allow_html=True)
        st.markdown(
            "<h4 style='text-align: center; color: gray;'>Sistema de controle de fichas técnicas e insumos</h4>",
            unsafe_allow_html=True
        )
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
        return
    
    # === TENTATIVA DE CARREGAMENTO DO ARQUIVO DA PÁGINA ===
    if filename in MENU_PAGES.values():
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                code = file.read()
            
            exec(code, globals())
            
            if 'run_page' in globals():
                globals()['run_page']()
            else:
                st.error("Erro: A função 'run_page()' não foi encontrada no arquivo da página.")

        except FileNotFoundError:
            st.error(f"Erro ao carregar a página: Arquivo '{filename}' não encontrado.")
        except Exception as e:
            st.error(f"Erro ao executar a página {filename}: {e}")
    else:
        st.error(f"Página '{page_key}' não mapeada. Verifique o dicionário de páginas no nav.py.")


# =========================================================
# CONFIGURAÇÕES INICIAIS (AQUI ESTÁ A CORREÇÃO CRÍTICA)
# =========================================================
st.set_page_config(
    page_title="FichApp",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="collapsed", # <--- CORREÇÃO: Colapsada por padrão
    menu_items=None 
)

# =========================================================
# MENU LATERAL
# =========================================================
sidebar_menu(ativo="home") 


# =========================================================
# EXECUÇÃO DO CONTEÚDO
# =========================================================
if 'current_page' in st.session_state:
    load_page_content(st.session_state.current_page)
else:
    load_page_content("home")
