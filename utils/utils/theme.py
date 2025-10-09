import streamlit as st
from datetime import date
import json
import random
from pathlib import Path

# -------------------------------
# Tema escuro e estilo global
# -------------------------------
DARK_CSS = """
<style>
body { background-color: #0E1117; color: #FAFAFA; }
h1, h2, h3 { color: #58A6FF; font-weight: 700; }
.stButton>button { background-color: #0078D7; color: white; border-radius: 8px; }
.stButton>button:hover { background-color: #1E90FF; }
.footer-box {
    border-top: 1px solid #444;
    margin-top: 32px;
    padding-top: 12px;
    font-size: 0.9em;
    color: #AAA;
}
</style>
"""

def aplicar_tema():
    """Configura o tema visual padrão do FichApp"""
    st.set_page_config(
        page_title="FichApp – Gestão Gastronômica",
        page_icon="📘",
        layout="wide"
    )
    st.markdown(DARK_CSS, unsafe_allow_html=True)

def carregar_versao(caminho="versao.json"):
    """Lê a versão atual do arquivo versao.json"""
    p = Path(caminho)
    if not p.exists():
        return {"versao": "0.0.0", "data_lancamento": str(date.today()), "descricao": ""}
    return json.loads(p.read_text(encoding="utf-8"))

def rodape():
    """Exibe o rodapé padrão do app"""
    st.markdown(
        """
        <div class='footer-box'>
            <p><b>Criado por Arsanjo</b> • Todos os direitos reservados • Proibida reprodução</p>
        </div>
        """,
        unsafe_allow_html=True
    )
