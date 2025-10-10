import streamlit as st
from PIL import Image
import json
import os
from datetime import date

# ==============================
# CONFIGURAÇÕES INICIAIS
# ==============================
st.set_page_config(page_title="FichApp — Início", page_icon="📘", layout="wide")

# ==============================
# LOGO CENTRAL E CABEÇALHO
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

# ==============================
# MENSAGEM DE BOAS-VINDAS
# ==============================
st.info(
    "💡 **O FichApp** é o seu assistente de gestão gastronômica. "
    "Cadastre seus insumos, defina parâmetros financeiros e, em breve, monte fichas técnicas completas com cálculo de custo e preço sugerido."
)

# ==============================
# INSTRUÇÕES BÁSICAS
# ==============================
st.markdown("### 🧭 Primeiros passos")
st.markdown(
    """
1️⃣ **Acesse “Cadastro de Insumos”** para registrar todos os produtos e ingredientes utilizados nas suas receitas.  
2️⃣ **Preencha os “Parâmetros Financeiros”** com as margens e percentuais aplicáveis.  
3️⃣ Aguarde a próxima atualização com o módulo de **Fichas Técnicas** e cálculo automático de custo de produção.
"""
)

# ==============================
# RODAPÉ COM VERSÃO
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
