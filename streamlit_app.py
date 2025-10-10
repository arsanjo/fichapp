import streamlit as st
from PIL import Image
import json, os
from datetime import date
from utils.nav import sidebar_menu

# ==============================
# CONFIG GLOBAL
# ==============================
st.set_page_config(
    page_title="FichApp",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)

# nosso menu único
sidebar_menu(ativo="inicio")

# ==============================
# CONTEÚDO DA HOME
# ==============================
col1, col2, col3 = st.columns([1, 2, 1])

logo_path = os.path.join("assets", "logo_fichapp.png")
with col2:
    if os.path.exists(logo_path):
        st.image(Image.open(logo_path), use_container_width=True)

    st.markdown(
        """
        <h1 style='text-align:center;margin-top:-8px;'>FichApp</h1>
        <p style='text-align:center;color:#6b7280;font-size:18px;margin-top:-8px'>
          Sistema de controle de fichas técnicas e insumos
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style='margin-top:36px;text-align:center;font-style:italic;color:#374151;font-size:17px;'>
          “E tudo quanto fizerdes, fazei-o de todo o coração, como ao Senhor, e não aos homens.”<br>
          <b>Colossenses 3:23</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ==============================
# RODAPÉ COM VERSÃO
# ==============================
def rodape():
    versao, data = "1.0.0", str(date.today())
    try:
        with open("version.json","r",encoding="utf-8") as f:
            info = json.load(f)
        versao = info.get("version", versao)
        data   = info.get("last_update", data)
    except Exception:
        pass

    st.markdown(
        f"""
        <div style='margin-top:60px;padding:12px;background:#0b1220;color:#fff;text-align:center;border-radius:10px;'>
            <b>FichApp v{versao}</b> — atualizado em {data}<br>
            Desenvolvido por <b>Arsanjo</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

rodape()
