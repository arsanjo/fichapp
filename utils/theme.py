import streamlit as st
from datetime import date
import json
import random
from pathlib import Path

# ------------------------------
# Tema escuro e estilo global
# ------------------------------
DARK_CSS = """
<style>
  body { background-color: #0E1117; color: #FAFAFA; }
  h1, h2, h3 { color: #58A6FF; font-weight: 700; }
  .stButton>button { background-color: #0078D7; color: white; border-radius: 10px; }
  .stPageLink { font-weight: 600; }
  .footer-box {
    background:#0D1117; border:1px solid #1F2A44; border-radius:12px; padding:16px; margin-top:24px;
  }
</style>
"""

def aplicar_tema():
    """Configura o tema escuro padrão do FichApp"""
    st.set_page_config(page_title="FichApp — Gestão Gastronômica", page_icon="📘", layout="wide")
    st.markdown(DARK_CSS, unsafe_allow_html=True)

def carregar_versao(caminho="versao.json"):
    """Lê a versão atual do arquivo versao.json"""
    p = Path(caminho)
    if not p.exists():
        return {"versao": "0.0.0", "data_lancamento": str(date.today()), "descricao": ""}
    return json.loads(p.read_text(encoding="utf-8"))

VERSOS = [
    ("“Tudo posso naquele que me fortalece.”", "Filipenses 4:13"),
    ("“Confia no Senhor de todo o teu coração.”", "Provérbios 3:5"),
    ("“Sede fortes e corajosos.”", "Josué 1:9")
]

def rodape(versao_info: dict):
    """Cria o rodapé padrão do FichApp"""
    verso, ref = random.choice(VERSOS)
    st.markdown(
        f"""
        <div class="footer-box">
          <strong>FichApp v{versao_info.get("versao", "0.0.0")}</strong> — última atualização: {versao_info.get("data_lancamento")}
          <br><br>
          <em>{verso}</em> — <strong>{ref}</strong><br><br>
          <span style="opacity:.8">Criado por Arsanjo • Todos os direitos reservados • Proibida reprodução</span>
        </div>
        """,
        unsafe_allow_html=True
    )
