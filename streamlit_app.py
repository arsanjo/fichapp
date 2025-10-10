# streamlit_app.py - COM CORREÇÃO DA LOGO NO DASHBOARD

# =========================================================
# FichApp - Sistema de controle de fichas técnicas e insumos
# =========================================================
import streamlit as st
from utils.nav import sidebar_menu, MENU_PAGES 
import datetime
import os

# =========================================================
# FUNÇÃO PARA CARREGAR O CONTEÚDO DA PÁGINA ATIVA
# =========================================================
def load_page_content(page_key):
    filename = page_key 

    if page_key == "home":
        # === CONTEÚDO MELHORADO DA HOME (DASHBOARD) ===
        
        # Centraliza a logomarca no cabeçalho
        col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
        with col_img2:
            # CORREÇÃO: Exibe a logomarca do FichApp no centro da página
            st.image("assets/logo_fichapp.png", use_column_width=True)

        st.markdown("<h1 style='text-align: center;'>FichApp Dashboard</h1>", unsafe_allow_html=True)
        st.markdown(
            "<h4 style='text-align: center; color: gray;'>Visão Geral do Sistema de Gestão Interna</h4>",
            unsafe_allow_html=True
        )
        st.markdown("---")
        
        # --- LINHA DE KPIs (INDICADORES CHAVE) ---
        st.subheader("🚀 Indicadores de Produção")
        
        col1, col2, col3 = st.columns(3)
        
        # Nota: Estes valores são fixos para demonstração. Serão ligados aos dados na próxima fase.
        with col1:
            st.metric(label="Total de Fichas Criadas", value="24", delta="🚀 +2 Fichas")
        with col2:
            st.metric(label="Custo Médio dos Insumos", value="R$ 12,50", delta="🔻 -0.15 R$")
        with col3:
            st.metric(label="Próxima Reavaliação", value="30 dias", delta="📅 Urgente")

        st.markdown("<br>", unsafe_allow_html=True)
        
        # --- ACESSO RÁPIDO ---
        st.subheader("⚡ Acesso Rápido")
        st.info("Use o menu lateral ou os botões abaixo para ir para os módulos principais.")

        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        # Botões de navegação rápida
        with col_btn1:
            if st.button("📦 Ir para Cadastro de Insumos", use_container_width=True):
                st.session_state.current_page = "01_Cadastro_de_Insumos.py"
                st.rerun()

        with col_btn2:
            if st.button("🧑‍🍳 Criar Nova Ficha", use_container_width=True):
                st.session_state.current_page = "04_Ficha_Tecnica_Cozinha.py"
                st.rerun()
                
        with col_btn3:
            if st.button("📊 Analisar Cardápio", use_container_width=True):
                st.session_state.current_page = "03_Engenharia_do_Cardapio.py"
                st.rerun()
        
        st.markdown("---")

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
    
    # === TENTATIVA DE CARREGAMENTO DO ARQUIVO DA PÁGINA (Lógica mantida) ===
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
# CONFIGURAÇÕES INICIAIS (st.set_page_config)
# =========================================================
st.set_page_config(
    page_title="FichApp",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="collapsed", 
    menu_items=None 
)

# =========================================================
# EXECUÇÃO
# =========================================================
sidebar_menu(ativo="home") 

if 'current_page' in st.session_state:
    load_page_content(st.session_state.current_page)
else:
    load_page_content("home")
