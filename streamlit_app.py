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
# ESCONDER MENUS PADRÕES DO STREAMLIT
# ==============================
hide_default_elements = """
    <style>
        /* Oculta o menu automático "streamlit app" e suas páginas */
        section[data-testid="stSidebarNav"] {display: none !important;}
        /* Oculta também o texto "Navegação fixa • FichApp" no final */
        div[data-testid="stSidebarFooter"] {display: none !important;}
        footer {visibility: hidden;}
        /* Garante o tamanho do menu lateral customizado */
        [data-testid="stSidebar"] {
            min-width: 270px;
        }
    </style>
"""
st.markdown(hide_default_elements, unsafe_allow_html=True)

# ==============================
# MENU FIXO DO FICHAPP
# ==============================
menu_lateral()

# ==============================
# CONTEÚDO PRINCIPAL
# ==============================
col1, col2, col3 = st.columns([1, 2, 1])

logo_path = os.path.join("assets", "logo_fichapp.png")
with col2:
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
        st.image(logo, use_container_width=True)
    
    # Nome e subtítulo
    st.markdown(
        """
        <h1 style='text-align:center; margin-top:-10px;'>📘 FichApp</h1>
        <p style='text-align:center; color:gray; font-size:18px;'>Sistema de controle de fichas técnicas e insumos</p>
        """,
        unsafe_allow_html=True
    )

    # Versículo bíblico
    st.markdown(
        """
        <div style='margin-top:40px; text-align:center; font-style:italic; color:#333; font-size:17px; animation: fadeIn 2s ease-in-out;'>
            “E tudo quanto fizerdes, fazei-o de todo o coração, como ao Senhor, e não aos homens.”<br>
            <b>Colossenses 3:23</b>
        </div>
        <style>
            @keyframes fadeIn {
                from {opacity: 0;}
                to {opacity: 1;}
            }
        </style>
        """,
        unsafe_allow_html=True
    )

# ==============================
# RODAPÉ
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
        <div style='margin-top:70px; padding:12px; background-color:#0b1220; color:white; text-align:center; border-radius:10px;'>
        <b>FichApp v{versao}</b> — atualizado em {data}<br>
        Desenvolvido por <b>Arsanjo</b>
        </div>
        """,
        unsafe_allow_html=True
    )

rodape()
