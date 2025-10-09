import streamlit as st
import pandas as pd
from datetime import datetime
import sys, os

# ---------------------------------------------------
# Corrige o caminho do módulo utils para o ambiente Streamlit Cloud
# ---------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.theme import aplicar_tema, rodape

# ===================================================
# Configurações iniciais
# ===================================================
aplicar_tema()
st.title("📦 Cadastro de Insumos")
st.write("Gerencie os insumos utilizados nas suas receitas e fichas técnicas.")

# Caminho do arquivo CSV para salvar os insumos
CAMINHO_ARQUIVO = "dados/insumos.csv"

# ===================================================
# Funções auxiliares
# ===================================================
def carregar_dados():
    """Carrega o arquivo CSV de insumos"""
    try:
        return pd.read_csv(CAMINHO_ARQUIVO)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Nome", "Unidade", "Custo", "Fornecedor", "Atualizado_em"])

def salvar_dados(df):
    """Salva os dados no CSV"""
    df.to_csv(CAMINHO_ARQUIVO, index=False)

# ===================================================
# Interface principal
# ===================================================
aba = st.radio("Selecione a ação:", ["➕ Cadastrar novo insumo", "📋 Visualizar insumos"])

dados = carregar_dados()

# ===================================================
# Aba 1 - Cadastro de insumos
# ===================================================
if aba == "➕ Cadastrar novo insumo":
    st.subheader("Novo insumo")

    with st.form("form_insumo"):
        nome = st.text_input("Nome do insumo")
        unidade = st.selectbox("Unidade de medida", ["kg", "g", "L", "ml", "un"])
        custo = st.number_input("Custo unitário (R$)", min_value=0.0, step=0.01, format="%.2f")
        fornecedor = st.text_input("Fornecedor (opcional)")

        enviado = st.form_submit_button("Salvar insumo")

        if enviado:
            if nome.strip() == "":
                st.warning("⚠️ O nome do insumo é obrigatório.")
            else:
                novo = pd.DataFrame([{
                    "Nome": nome,
                    "Unidade": unidade,
                    "Custo": custo,
                    "Fornecedor": fornecedor,
                    "Atualizado_em": datetime.now().strftime("%d/%m/%Y %H:%M")
                }])
                dados = pd.concat([dados, novo], ignore_index=True)
                salvar_dados(dados)
                st.success(f"Insumo **{nome}** salvo com sucesso! ✅")

# ===================================================
# Aba 2 - Visualização de insumos
# ===================================================
elif aba == "📋 Visualizar insumos":
    st.subheader("Lista de insumos cadastrados")

    if dados.empty:
        st.info("Nenhum insumo cadastrado ainda.")
    else:
        st.dataframe(
            dados.style.format({"Custo": "R$ {:.2f}"}),
            use_container_width=True
        )

# ===================================================
# Rodapé
# ===================================================
rodape()
