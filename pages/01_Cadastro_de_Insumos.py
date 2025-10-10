import streamlit as st
import pandas as pd
import os
from datetime import date, datetime

# =========================================================
# CONFIGURAÇÕES INICIAIS
# =========================================================
st.set_page_config(page_title="Cadastro de Insumos - FichApp", page_icon="📦", layout="centered")

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
INSUMOS_CSV = os.path.join(DATA_DIR, "insumos.csv")

# =========================================================
# UNIDADES PADRÃO
# =========================================================
unidades_padrao = {
    "KG": ("Quilograma", 1),
    "G": ("Grama", 1000),
    "L": ("Litro", 1),
    "ML": ("Mililitro", 1000),
    "UN": ("Unidade", 1),
    "DZ": ("Dúzia", 12),
    "CT": ("Cento", 100),
    "MIL": ("Milheiro", 1000),
}

# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================
def carregar_insumos():
    if os.path.exists(INSUMOS_CSV):
        return pd.read_csv(INSUMOS_CSV)
    else:
        return pd.DataFrame(columns=[
            "data_compra", "grupo", "insumo_resumo", "insumo_completo", "marca", "tipo",
            "un_med", "quantidade_compra", "qtde_para_custos", "valor_total_compra", 
            "valor_frete", "percentual_perda", "valor_unit_bruto", "custo_total_com_frete", 
            "quantidade_liquida", "custo_real_unitario", "valor_unit_para_custos", 
            "fornecedor", "fone_fornecedor", "representante", "documento", "observacao",
            "atualizado_em"
        ])

def salvar_insumo(df):
    df.to_csv(INSUMOS_CSV, index=False)

# =========================================================
# INTERFACE
# =========================================================
st.title("📦 Cadastro de Insumos")
st.caption("Cadastre insumos com grupos, unidades dinâmicas, frete, perda e cálculos automáticos de custo.")

acao = st.radio("Ação:", ["➕ Cadastrar novo insumo", "✏️ Editar insumo", "📋 Visualizar insumos"], index=0)

# =========================================================
# CADASTRAR NOVO INSUMO
# =========================================================
if acao == "➕ Cadastrar novo insumo":
    st.markdown("### 🧾 Dados do insumo")

    with st.form("cadastro_insumo", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            data_compra = st.date_input("Data da compra", value=date.today(), format="DD/MM/YYYY")
            grupo = st.text_input("Grupo")
            nome_resumo = st.text_input("Nome resumido do insumo")
            nome_completo = st.text_input("Nome completo do insumo", value=nome_resumo if nome_resumo else "")
            marca = st.text_input("Marca (opcional)")
            tipo = st.selectbox("Tipo", ["Comprado", "Produzido no restaurante"])
        with col2:
            un_med = st.selectbox("Unidade de medida", list(unidades_padrao.keys()), index=0)
            quantidade_compra = st.number_input("Quantidade comprada", min_value=0.0, value=0.0, step=0.01)

            # cálculo automático da quantidade para custos
            multiplicador = unidades_padrao.get(un_med, ("", 1))[1]
            qtde_para_custos_auto = quantidade_compra / multiplicador if multiplicador > 1 else quantidade_compra
            qtde_para_custos = st.number_input("Quantidade para custos", min_value=0.0, value=float(qtde_para_custos_auto), step=0.01)

            valor_total_compra = st.number_input("Valor total da compra (R$)", min_value=0.0, value=0.0, step=0.01)
            valor_frete = st.number_input("Frete (R$)", min_value=0.0, value=0.0, step=0.01)
            percentual_perda = st.number_input("% de perda", min_value=0.0, max_value=100.0, value=0.0, step=0.1)

        st.markdown("### 💰 Pré-visualização dos cálculos")

        # cálculos automáticos
        valor_unit_bruto = valor_total_compra / quantidade_compra if quantidade_compra > 0 else 0
        custo_total_com_frete = valor_total_compra + valor_frete
        quantidade_liquida = quantidade_compra * (1 - percentual_perda / 100)
        custo_real_unitario = custo_total_com_frete / quantidade_liquida if quantidade_liquida > 0 else 0
        valor_unit_para_custos = custo_real_unitario / qtde_para_custos if qtde_para_custos > 0 else 0

        c1, c2 = st.columns(2)
        with c1:
            st.write(f"**Valor unitário bruto:** R$ {valor_unit_bruto:.4f}")
            st.write(f"**Custo total com frete:** R$ {custo_total_com_frete:.2f}")
            st.write(f"**Quantidade líquida (após perda):** {quantidade_liquida:.4f} {un_med}")
        with c2:
            st.write(f"**Custo real unitário:** R$ {custo_real_unitario:.4f}")
            st.write(f"**Custo unitário p/ custos:** R$ {valor_unit_para_custos:.6f}")

        st.markdown("### 🧾 Fornecedor e contato (opcional)")
        col3, col4 = st.columns(2)
        with col3:
            fornecedor = st.text_input("Fornecedor")
            fone_fornecedor = st.text_input("Telefone do fornecedor")
            documento = st.text_input("Documento / Nota Fiscal")
        with col4:
            representante = st.text_input("Representante")
            observacao = st.text_area("Observação")

        enviado = st.form_submit_button("💾 Salvar insumo")

        if enviado:
            df = carregar_insumos()
            novo = {
                "data_compra": data_compra.strftime("%d/%m/%Y"),
                "grupo": grupo,
                "insumo_resumo": nome_resumo,
                "insumo_completo": nome_completo,
                "marca": marca,
                "tipo": tipo,
                "un_med": un_med,
                "quantidade_compra": quantidade_compra,
                "qtde_para_custos": qtde_para_custos,
                "valor_total_compra": valor_total_compra,
                "valor_frete": valor_frete,
                "percentual_perda": percentual_perda,
                "valor_unit_bruto": valor_unit_bruto,
                "custo_total_com_frete": custo_total_com_frete,
                "quantidade_liquida": quantidade_liquida,
                "custo_real_unitario": custo_real_unitario,
                "valor_unit_para_custos": valor_unit_para_custos,
                "fornecedor": fornecedor,
                "fone_fornecedor": fone_fornecedor,
                "representante": representante,
                "documento": documento,
                "observacao": observacao,
                "atualizado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
            salvar_insumo(df)
            st.success(f"Insumo **{nome_resumo}** salvo com sucesso!")
            st.experimental_rerun()

# =========================================================
# VISUALIZAR INSUMOS
# =========================================================
elif acao == "📋 Visualizar insumos":
    st.markdown("### 📋 Lista de Insumos Cadastrados")
    df = carregar_insumos()
    if df.empty:
        st.info("Nenhum insumo cadastrado ainda.")
    else:
        st.dataframe(df, use_container_width=True)

# =========================================================
# EDITAR INSUMO (placeholder futuro)
# =========================================================
elif acao == "✏️ Editar insumo":
    st.info("✏️ Função de edição de insumos será implementada em breve.")
