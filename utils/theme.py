import streamlit as st
import json
from datetime import date
from pathlib import Path

# ======================================================
# CONFIGURAÇÃO DE TEMA E ESTILO
# ======================================================

DARK_CSS = """
<style>
body { background-color: #0E1117; color: #FAFAFA; }
h1, h2, h3 { color: #58A6FF; font-weight: 700; }
.stButton>button { background-color: #0078D7; color: white; border-radius: 8px; }
footer { text-align: center; font-size: 13px; color: #AAA; margin-top: 40px; }
</style>
"""

def aplicar_tema():
    """Aplica o tema escuro e configura o layout da página principal."""
    st.set_page_config(page_title="FichApp", page_icon="📘", layout="wide")
    st.markdown(DARK_CSS, unsafe_allow_html=True)


# ======================================================
# CONTROLE DE VERSÃO E RODAPÉ
# ======================================================

def carregar_versao(caminho="version.json"):
    """Carrega o número da versão e data de atualização."""
    p = Path(caminho)
    if not p.exists():
        return {"versao": "0.0.0", "data_lancamento": str(date.today())}
    return json.loads(p.read_text(encoding="utf-8"))

def rodape():
    """Exibe rodapé com versão e créditos."""
    v = carregar_versao()
    st.markdown(
        f"<footer>FichApp v{v['versao']} — atualizado em {v['data_lancamento']}<br>Desenvolvido por Arsanjo</footer>",
        unsafe_allow_html=True,
    )
