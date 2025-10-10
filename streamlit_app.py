import streamlit as st
from PIL import Image
import json
import os
from datetime import date

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
# LOGO E CABEÇALHO PERSONALIZADO
# ==============================
logo_path = os.path.join("assets", "logo_fichapp.png")
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    st.sidebar.image(logo, use_container_width=True)
else:
    st.sidebar.markdown("### 📘 FichApp")

st.sidebar.markdown("---")
st.sidebar.markdown("## 📋 Menu")

# ==============================
# RODAPÉ FIXO
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
        <div style='margin-top:60px; padding:12px; background-color:#0b1220; color:white; text-align:center; border-radius:10px;'>
        <b>FichApp v{versao}</b> — atualizado em {data}<br>
        Desenvolvido por <b>Arsanjo</b>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==============================
# PÁGINA INICIAL (HOME)
# ==============================
st.markdown("<h1 style='text-align:center;'>📘 FichApp</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Bem-vindo ao sistema de controle de fichas técnicas e insumos!</p>", unsafe_allow_html=True)

st.info("🚀 O FichApp está em construção. Em breve você poderá cadastrar insumos, criar fichas técnicas e acompanhar custos em tempo real.")

rodape()
