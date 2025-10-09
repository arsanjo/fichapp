import streamlit as st
import pandas as pd
import os
from datetime import datetime
from utils.theme import aplicar_tema, rodape

# ======================================================
# Configurações iniciais
# ======================================================
aplicar_tema()
st.title("📦 Cadastro de Insumos")
st.write("Gerencie os insumos utilizados nas suas receitas e fichas técnicas.")

# Caminho para o arquivo CSV
CAMINHO_ARQUIVO = "data/insumos.csv"

# ======================================================
# Funções auxiliares
# ======================================================
def carregar_dados():
    """Carrega o CSV com os insumos, criando-o caso não exista."""
    if not os.path.exists(CAMINHO_ARQUIVO):
        colunas = ["Nome", "Unidade", "Custo", "Fornecedor", "Atualizado_em"]
        pd.DataFrame(columns=colunas).to_csv(CAMINHO_ARQUIVO, index=False)
    return pd.read_csv(CAMINHO_ARQUIVO)

def salvar_dados(df):
    """Salva o DataFrame no CSV."""
    df.to_csv(CAMINHO_ARQUIVO, index=False)

# ======================================================
# Interface principal
# ======================================================
aba = st.radio(
    "Selecione uma opção:",
    ["Cadastrar novo insumo", "Visualizar insumos"]
)

dados = carregar_dados()

# ======================================================
# Cadastrar novo insumo
# ======================================================
if aba == "Cadastrar novo insumo":
    with st.form("cadastro_insumo"):
        nome = st.text_input("Nome do insumo")
        unidade = st.selectbox("Unidade de medida", ["kg", "g", "L", "mL", "unidade"])
        custo = st.number_input("Custo (R$)", min_value=0.0, step=0.01, format="%.2f")
        fornecedor = st.text_input("Fornecedor (opcional)")
        enviar = st.form_submit_button("Salvar insumo")

    if enviar:
        if nome.strip() == "":
            st.warning("⚠️ Informe o nome do insumo.")
        elif custo <= 0:
            st.warning("⚠️ O custo deve ser maior que zero.")
        else:
            novo = pd.DataFrame([{
                "Nome": nome.strip(),
                "Unidade": unidade,
                "Custo": custo,
                "Fornecedor": fornecedor.strip(),
                "Atualizado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }])
            dados = pd.concat([dados, novo], ignore_index=True)
            salvar_dados(dados)
            st.success(f"✅ Insumo **{nome}** cadastrado com sucesso!")

# ======================================================
# Visualizar insumos
# ======================================================
elif aba == "Visualizar insumos":
    if dados.empty:
        st.info("📭 Nenhum insumo cadastrado ainda.")
    else:
        st.dataframe(dados, use_container_width=True)
        if st.button("🗑️ Limpar todos os registros"):
            os.remove(CAMINHO_ARQUIVO)
            st.warning("Todos os insumos foram excluídos.")
            st.experimental_rerun()

# ======================================================
# Rodapé
# ======================================================
rodape()
