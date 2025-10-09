import streamlit as st
from datetime import date
import json
from pathlib import Path

# -------------------------------
# Tema escuro + estilo global
# -------------------------------
DARK_CSS = """
<style>
  body { background-color: #0E1117; color: #FAFAFA; }
  h1, h2, h3 { color: #58A6FF; font-weight: 700; }
  .stButton>button { background-color: #0078D7; color: white; border-radius: 10px; padding: 10px 16px; }
  .stButton>button:hover { background-color: #1e293b; }
  .stPageLink { font-weight: 600; }
  .footer-box {
    background:#0D1117; border:1px solid #1F2A44; border-radius:12px; margin-top:24px;
    padding:14px; text-align:center; color:#9aa5b1; font-size:0.9rem;
  }
</style>
"""

def aplicar_tema():
    """Aplica o tema padrão do FichApp."""
    st.set_page_config(page_title="FichApp — Gestão Gastronômica", page_icon="📘", layout="wide")
    st.markdown(DARK_CSS, unsafe_allow_html=True)

# -------------------------------
# Leitura de versão
# -------------------------------
def ler_versao(caminho="version.json"):
    """
    Lê a versão do arquivo version.json.
    Se não existir, retorna uma versão neutra.
    """
    p = Path(caminho)
    if not p.exists():
        return {"version": "0.0.0", "release_date": str(date.today()), "notes": ""}
    return json.loads(p.read_text(encoding="utf-8"))

# -------------------------------
# Rodapé padrão
# -------------------------------
def rodape():
    """Exibe rodapé com versão e autoria."""
    v = ler_versao()
    st.markdown(
        f"""
        <div class="footer-box">
          <strong>FichApp v{v.get('version','0.0.0')}</strong> — atualizado em {v.get('release_date','')}
          <br>
          <span>Desenvolvido por Arsanjo</span>
        </div>
        """,
        unsafe_allow_html=True
    )
