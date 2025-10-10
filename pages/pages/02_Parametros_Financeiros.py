import streamlit as st
import pandas as pd
from datetime import datetime, date
import os, json, random
from utils.nav import sidebar_menu

# ativa o menu lateral fixo padronizado
sidebar_menu(ativo="insumos")

# =========================================================
# CONFIGURAÇÃO E ESTILO
# =========================================================
st.set_page_config(page_title="FichApp — Parâmetros Financeiros", page_icon="💰", layout="centered")

st.markdown("""
<style>
.block-container { padding-top: 2rem; padding-bottom: 2rem; }
h1, h2, h3 { font-weight: 700; }
.stButton>button, .stForm form button[kind="primary"]{
  background: #0f172a; color: #fff; border: 0; border-radius: 10px; padding: .6rem 1rem;
}
.stButton>button:hover{ background: #1e293b; }
</style>
""", unsafe_allow_html=True)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
PARAMS_CSV = os.path.join(DATA_DIR, "parametros_financeiros.csv")

# =========================================================
# CAMPOS PADRÃO
# =========================================================
parametros_iniciais = [
    {"parametro": "Margem de Contribuição", "valor": 50.43, "observacao": "Cálculo: Faturamento - Custo Produção - Taxa Cartão - Simples - Comissão"},
    {"parametro": "Lucro Desejado", "valor": 20.0, "observacao": "Percentual de lucro desejado sobre o custo final."},
    {"parametro": "Comissão APP", "valor": 0.0, "observacao": "Percentual de comissão do aplicativo de delivery."},
    {"parametro": "Simples", "valor": 5.0, "observacao": "Percentual de imposto Simples Nacional."},
    {"parametro": "Cashback Menudino", "valor": 1.0, "observacao": "Percentual destinado a cashback em campanhas do Menudino."},
    {"parametro": "Comissão Atendente", "valor": 1.0, "observacao": "Percentual de comissão repassado ao atendente."},
    {"parametro": "Taxa Cartão", "valor": 5.0, "observacao": "Taxa média cobrada pelas operadoras de cartão."},
    {"parametro": "Outros (1)", "valor": 1.0, "observacao": "Outros custos eventuais."},
    {"parametro": "Outros (2)", "valor": 1.0, "observacao": "Outros custos adicionais."}
]

# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================
def carregar_parametros():
    if os.path.exists(PARAMS_CSV):
        return pd.read_csv(PARAMS_CSV)
    else:
        df = pd.DataFrame(parametros_iniciais)
        df.to_csv(PARAMS_CSV, index=False)
        return df

def salvar_parametros(df):
    df.to_csv(PARAMS_CSV, index=False)

# =========================================================
# INTERFACE
# =========================================================
st.title("💰 Parâmetros Financeiros")
st.caption("Defina percentuais e valores base que serão utilizados futuramente nos cálculos de custo e precificação.")

acao = st.radio("Ação:", ["➕ Cadastrar / Atualizar parâmetros", "📋 Visualizar parâmetros"], index=0)

# =========================================================
# CADASTRAR / ATUALIZAR
# =========================================================
if acao == "➕ Cadastrar / Atualizar parâmetros":
    df = carregar_parametros()

    with st.form("parametros_financeiros"):
        for i, row in df.iterrows():
            st.markdown(f"#### {row['parametro']}")
            col1, col2 = st.columns([1, 3])
            with col1:
                df.at[i, "valor"] = st.number_input(f"Valor (%) — {row['parametro']}", min_value=0.0, max_value=100.0, value=float(row['valor']), step=0.1, key=f"valor_{i}")
            with col2:
                df.at[i, "observacao"] = st.text_input(f"Observação — {row['parametro']}", value=row['observacao'], key=f"obs_{i}")
            st.divider()

        enviado = st.form_submit_button("💾 Salvar parâmetros")

    if enviado:
        salvar_parametros(df)
        st.success("✅ Parâmetros financeiros atualizados com sucesso!")

# =========================================================
# VISUALIZAR
# =========================================================
elif acao == "📋 Visualizar parâmetros":
    df = carregar_parametros()
    if df.empty:
        st.info("Nenhum parâmetro cadastrado ainda.")
    else:
        st.dataframe(df, use_container_width=True)

# =========================================================
# RODAPÉ
# =========================================================
st.markdown("""
---
<div style='text-align:center; color:gray; font-size:0.9em'>
FichApp • Módulo de Parâmetros Financeiros • Versão 1.0.0<br>
<em>"Tudo deve ser feito com ordem e decência." — 1 Coríntios 14:40</em>
</div>
""", unsafe_allow_html=True)
