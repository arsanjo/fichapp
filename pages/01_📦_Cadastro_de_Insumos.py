import streamlit as st
import pandas as pd
from datetime import datetime
import sys, os

# ---------------------------------------------------
# Corrige caminho absoluto para importações
# ---------------------------------------------------
# Adiciona o diretório raiz do app ao path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_dir not in sys.path:
    sys.path.append(root_dir)

# Agora importa normalmente o módulo utils
from utils.theme import aplicar_tema, rodape

# ===================================================
# Configurações iniciais
# ===================================================
aplicar_tema()
st.title("📦 Cadastro de Insumos")
st.write("Gerencie os insumos utilizados nas suas receitas e fichas técnicas.")

# Caminho do arquivo CSV para salvar os insumos
CAMINHO_ARQUIVO = os.path.join("dados", "insumos.csv")

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

if aba == "➕ Cadastrar novo insumo":
    st.subheader("Cadastrar novo insumo")
    nome = st.text_input("Nome do insumo:")
    unidade = st.selectbox("Unidade de medida:", ["kg", "g", "L", "ml", "un"])
    custo = st.number_input("Custo (R$):", min_value=0.0, format="%.2f")
    fornecedor = st.text_input("Fornecedor:")
    
    if st.button("Salvar insumo"):
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
            st.success(f"Insumo '{nome}' cadastrado com sucesso!")
        else:
            st.warning("Preencha pelo menos o nome do insumo.")

elif aba == "📋 Visualizar insumos":
    st.subheader("Lista de Insumos Cadastrados")
    if not dados.empty:
        st.dataframe(dados)
    else:
        st.info("Nenhum insumo cadastrado ainda.")

# ===================================================
# Rodapé
# ===================================================
rodape()
