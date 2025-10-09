import streamlit as st
import pandas as pd
from datetime import datetime
from utils.theme import aplicar_tema, rodape

# ===============================
# Configurações iniciais
# ===============================
aplicar_tema()
st.title("📦 Cadastro de Insumos")
st.write("Gerencie os insumos utilizados nas suas receitas e fichas técnicas.")

# Caminho do arquivo CSV para salvar os insumos
CAMINHO_ARQUIVO = "dados/insumos.csv"

# ===============================
# Funções auxiliares
# ===============================
def carregar_dados():
    """Carrega o arquivo CSV de insumos"""
    try:
        return pd.read_csv(CAMINHO_ARQUIVO)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Nome", "Unidade", "Custo", "Fornecedor", "Atualizado_em"])

def salvar_dados(df):
    """Salva os dados no CSV"""
    df.to_csv(CAMINHO_ARQUIVO, index=False)

# ===============================
# Interface principal
# ===============================
aba = st.radio("Selecione a ação:", ["➕ Cadastrar novo insumo", "📋 Visualizar insumos"])

dados = carregar_dados()

if aba == "➕ Cadastrar novo insumo":
    with st.form("cadastro_insumo"):
        nome = st.text_input("Nome do insumo")
        unidade = st.selectbox("Unidade de medida", ["Kg", "g", "L", "ml", "un", "cx", "pct"])
        custo = st.number_input("Custo por unidade (R$)", min_value=0.0, step=0.01)
        fornecedor = st.text_input("Fornecedor")
        enviar = st.form_submit_button("Salvar insumo")

        if enviar:
            if nome:
                novo = pd.DataFrame([{
                    "Nome": nome,
                    "Unidade": unidade,
                    "Custo": custo,
                    "Fornecedor": fornecedor,
                    "Atualizado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }])
                dados = pd.concat([dados, novo], ignore_index=True)
                salvar_dados(dados)
                st.success(f"Insumo **{nome}** cadastrado com sucesso!")
            else:
                st.warning("Por favor, preencha o nome do insumo.")

elif aba == "📋 Visualizar insumos":
    st.dataframe(dados, use_container_width=True)
    if not dados.empty:
        custo_medio = dados["Custo"].mean()
        st.info(f"💰 Custo médio dos insumos: R$ {custo_medio:.2f}")

# ===============================
# Rodapé
# ===============================
st.write("---")
rodape()
