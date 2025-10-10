import streamlit as st
from PIL import Image
import json
import os
from datetime import date
from utils.nav import menu_lateral

# ==============================
# CONFIGURAÇÃO GERAL DA PÁGINA
# ==============================
st.set_page_config(
    page_title="FichApp",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# ESCONDER MENU PADRÃO (antes de tudo)
# ==============================
hide_default_menu = """
    <style>
        /* Remove completamente o menu padrão de navegação */
        section[data-testid="stSidebarNav"] {display: none !important;}
        /* Garante que a sidebar permaneça aberta e limpa */
        [data-testid="stSidebar"] {
            min-width: 270px;
        }
    </style>
"""
st.markdown(hide_default_menu, unsafe_allow_html=True)

# ==============================
# MENU FIXO DO FICHAPP
# ==============================
menu_lateral()

# ==============================
# CONTEÚDO DA PÁGINA INICIAL
# ==============================
col1, col2, col3 = st.columns([1, 2, 1])

logo_path = os.path.join("assets", "logo_fichapp.png")
with col2:
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
        st.image(logo, use_container_width=True)
    st.markdown("<h1 style='text-align:center; margin-top:-10px;'>📘 FichApp</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:gray;'>Sistema de controle de fichas técnicas e insumos</p>", unsafe_allow_html=True)

st.divider()

st.info(
    "🚀 O **FichApp** está em construção. Em breve você poderá cadastrar insumos, "
    "criar fichas técnicas e acompanhar custos em tempo real."
)

st.markdown(
    """
    ### 🧭 Primeiros passos

    1️⃣ **Cadastre seus insumos** em “Cadastro de Insumos”.  
    2️⃣ **Defina parâmetros financeiros** na aba “Parâmetros Financeiros”.  
    3️⃣ Aguarde o próximo módulo com **Fichas Técnicas e Cálculo de Custos**.
    """
)

# ==============================
# RODAPÉ COM VERSÃO E AUTOR
# ==============================
def rodape():
    if os.path.exists("version.json"):
        with open("version.json", "r", encoding="utf-8") as f:
            versao_info = json.load(f)
        versao = versao_info.get("version", "1.0.0")
        data = versao_info.get("last_update", str(date.today()))
    else:
        versao, data = "1.0.0", str(date.today())

    st.markdown(
        f"""
        <div style='margin-top:50px; padding:12px; background-color:#0b1220; color:white; text-align:center; border-radius:10px;'>
        <b>FichApp v{versao}</b> — atualizado em {data}<br>
        Desenvolvido por <b>Arsanjo</b>
        </div>
        """,
        unsafe_allow_html=True
    )

rodape()
