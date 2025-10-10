# =========================================================
# FichApp - Sistema de controle de fichas técnicas e insumos
# =========================================================
import streamlit as st
# CORRIGIDO: O nome da importação estava errado, deve ser o nome do arquivo (nav)
# e o nome da função (sidebar_menu).
from utils.nav import sidebar_menu 
import datetime

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
# MENU LATERAL (IMPORTADO DE utils/nav.py)
# =========================================================
# O erro estava na chamada do nav.py, mas a função 'sidebar_menu' precisa estar
# definida em nav.py, o que não estava no seu código.
# Agora que definimos 'sidebar_menu' em utils/nav.py, esta chamada está correta.
sidebar_menu(ativo="Início") # Mudado "home" para "Início"

# =========================================================
# CONTEÚDO PRINCIPAL DA PÁGINA INICIAL
# =========================================================
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

# =========================================================
# RODAPÉ - INFORMAÇÕES DE VERSÃO
# =========================================================
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
