import streamlit as st
import pandas as pd
import os
from datetime import datetime
from utils.theme import aplicar_tema, rodape

# ======================================================
# CONFIGURAÇÃO INICIAL
# ======================================================
aplicar_tema()
st.title("📦 Cadastro de Insumos")
st.write("Cadastre insumos com **grupos, unidades dinâmicas, frete, perda** e cálculos automáticos de custo.")

# ======================================================
# ARQUIVOS DE DADOS
# ======================================================
DATA_DIR = "data"
COMPRAS_CSV = os.path.join(DATA_DIR, "compras_insumos.csv")
GRUPOS_CSV  = os.path.join(DATA_DIR, "grupos_insumos.csv")
UNIDS_CSV   = os.path.join(DATA_DIR, "unidades_medida.csv")

os.makedirs(DATA_DIR, exist_ok=True)

# Colunas dos arquivos
COLS_COMPRAS = [
    "data_compra","grupo","insumo_resumo","insumo_completo","marca","tipo",
    "un_med","quantidade_compra","qtde_para_custos",
    "valor_total_compra","valor_frete","percentual_perda",
    "valor_unit_bruto","custo_total_com_frete","quantidade_liquida",
    "custo_real_unitario","valor_unit_para_custos","custo_total_ajustado_ref",
    "fornecedor","fone_fornecedor","representante","documento","observacao",
    "Atualizado_em"
]

COLS_GRUPOS = ["grupo"]

COLS_UNIDS = ["codigo","descricao","qtde_padrao"]

UNIDADES_PADRAO = [
    ("KG","Quilograma", None),
    ("G","Grama", None),
    ("L","Litro", None),
    ("ML","Mililitro", None),
    ("UN","Unidade", None),
    ("DZ","Dúzia", 12),
    ("MIL","Milheiro", 1000),
    ("CT","Cento", 100),
    ("CX","Caixa", None),
    ("FD","Fardo", None),
    ("PAC","Pacote", None),
    ("BAN","Bandeja", None),
    ("PAR","Par", 2),
    ("POR","Porção", None),
]

GRUPOS_PADRAO = [
    "Embalagem","Peixe","Carne","Hortifruti","Bebida","Frios",
    "Molhos e Temperos","Grãos e Cereais","Higiene","Limpeza","Outros"
]

# ======================================================
# FUNÇÕES AUXILIARES
# ======================================================
def garantir_csv(path, cols, df_default=None):
    if not os.path.exists(path) or os.stat(path).st_size == 0:
        if df_default is None:
            pd.DataFrame(columns=cols).to_csv(path, index=False)
        else:
            df_default.to_csv(path, index=False)

def carregar_df(path):
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()

def salvar_df(df, path):
    df.to_csv(path, index=False)

# Garante arquivos base
garantir_csv(COMPRAS_CSV, COLS_COMPRAS)
garantir_csv(GRUPOS_CSV, COLS_GRUPOS, pd.DataFrame({ "grupo": GRUPOS_PADRAO }))
garantir_csv(UNIDS_CSV, COLS_UNIDS, pd.DataFrame(UNIDADES_PADRAO, columns=COLS_UNIDS))

# Carrega bases
df_compras = carregar_df(COMPRAS_CSV)
df_grupos  = carregar_df(GRUPOS_CSV)
df_unids   = carregar_df(UNIDS_CSV)

# Helpers de exibição
def label_unidade(row):
    return f"{row['codigo']} – {row['descricao']}"

unidades_labels = df_unids.apply(label_unidade, axis=1).tolist()
codigo_por_label = dict(zip(unidades_labels, df_unids["codigo"]))
padrao_por_codigo = dict(zip(df_unids["codigo"], df_unids["qtde_padrao"]))

# ======================================================
# LAYOUT PRINCIPAL
# ======================================================
aba = st.radio("Ação:", ["➕ Cadastrar novo insumo", "📋 Visualizar insumos"])

if aba == "➕ Cadastrar novo insumo":
    with st.form("f_insumo", clear_on_submit=False):
        st.subheader("🧾 Dados da compra")
        c1, c2, c3 = st.columns(3)
        with c1:
            data_compra = st.date_input("Data da compra", format="DD/MM/YYYY")
        with c2:
            documento = st.text_input("Documento / Nota Fiscal")
        with c3:
            tipo = st.selectbox("Tipo de insumo", ["Comprado", "Produzido no restaurante"])

        st.markdown("---")
        st.subheader("🏷️ Identificação")
        c4, c5 = st.columns([2,1])
        with c4:
            grupo_sel = st.selectbox("Grupo do insumo", df_grupos["grupo"].tolist() + ["➕ Adicionar novo grupo"])
            novo_grupo = ""
            if grupo_sel == "➕ Adicionar novo grupo":
                novo_grupo = st.text_input("Novo grupo (salva imediatamente)")
                if st.form_submit_button("Adicionar grupo agora"):
                    if novo_grupo.strip():
                        if novo_grupo.strip() not in df_grupos["grupo"].values:
                            df_grupos.loc[len(df_grupos)] = [novo_grupo.strip()]
                            salvar_df(df_grupos, GRUPOS_CSV)
                            st.success(f"Grupo “{novo_grupo}” adicionado. Selecione-o na lista.")
                            st.stop()
                        else:
                            st.info("Esse grupo já existe.")
                            st.stop()
                    else:
                        st.warning("Digite um nome de grupo válido.")
                        st.stop()
        with c5:
            marca = st.text_input("Marca (opcional)")

        c6, c7 = st.columns(2)
        with c6:
            insumo_resumo = st.text_input("Nome resumido do insumo")
        with c7:
            # copia automaticamente o nome resumido; o usuário pode editar
            default_completo = insumo_resumo if insumo_resumo else ""
            insumo_completo = st.text_input("Nome completo do insumo", value=default_completo)

        st.markdown("---")
        st.subheader("⚖️ Medidas e quantidades")
        c8, c9, c10 = st.columns(3)
        with c8:
            un_label = st.selectbox("Unidade de medida", options=unidades_labels)
            un_med = codigo_por_label[un_label]
        with c9:
            quantidade_compra = st.number_input("Quantidade comprada", min_value=0.0, value=0.0, step=0.01)
        with c10:
            # qtde para custos: preenche automático p/ MIL/CT/DZ (pode ser editado)
            auto_padrao = padrao_por_codigo.get(un_med)
            if pd.notna(auto_padrao) and auto_padrao:
                valor_default_qtd = float(auto_padrao)
            else:
                valor_default_qtd = 1.0
            qtde_para_custos = st.number_input("Quantidade para custos", min_value=0.0, value=valor_default_qtd, step=1.0)

        st.markdown("---")
        st.subheader("💰 Custos")
        c11, c12, c13, c14 = st.columns(4)
        with c11:
            valor_total_compra = st.number_input("Valor total da compra (R$)", min_value=0.0, value=0.0, step=0.01, format="%.2f")
        with c12:
            valor_frete = st.number_input("Frete (R$)", min_value=0.0, value=0.0, step=0.01, format="%.2f")
        with c13:
            percentual_perda = st.number_input("% de perda", min_value=0.0, max_value=100.0, value=0.0, step=0.5)
        with c14:
            st.caption("Perda: limpeza/aparas/evaporação etc.")

        # ==========================
        # PRÉVIA DE CÁLCULOS
        # ==========================
        valor_unit_bruto = (valor_total_compra / quantidade_compra) if quantidade_compra > 0 else 0.0
        custo_total_com_frete = valor_total_compra + valor_frete
        fator_aproveitamento = (100.0 - percentual_perda) / 100.0
        quantidade_liquida = quantidade_compra * fator_aproveitamento if quantidade_compra > 0 else 0.0
        custo_real_unitario = (custo_total_com_frete / quantidade_liquida) if quantidade_liquida > 0 else 0.0
        valor_unit_para_custos = (custo_real_unitario / qtde_para_custos) if qtde_para_custos > 0 else 0.0
        custo_total_ajustado_ref = custo_real_unitario * qtde_para_custos  # pedido: referência total

        st.markdown("#### 🧮 Pré-visualização dos cálculos")
        cc1, cc2 = st.columns(2)
        with cc1:
            st.write(f"• **Valor unitário bruto:** R$ {valor_unit_bruto:.4f}")
            st.write(f"• **Custo total com frete:** R$ {custo_total_com_frete:.2f}")
            st.write(f"• **Quantidade líquida (após perda):** {quantidade_liquida:.4f} {un_med}")
        with cc2:
            st.write(f"• **Custo real unitário:** R$ {custo_real_unitario:.6f}")
            st.write(f"• **Custo unitário p/ custos:** R$ {valor_unit_para_custos:.6f}")
            st.write(f"• **Custo total ajustado (ref.):** R$ {custo_total_ajustado_ref:.4f}")

        st.markdown("---")
        st.subheader("🏭 Fornecedor e contato (opcional)")
        c15, c16, c17 = st.columns(3)
        with c15:
            fornecedor = st.text_input("Fornecedor")
        with c16:
            fone_fornecedor = st.text_input("Telefone do fornecedor")
        with c17:
            representante = st.text_input("Representante")

        observacao = st.text_area("🗒️ Observações (opcional)", placeholder="Ex.: usado apenas em pratos quentes…")

        enviado = st.form_submit_button("💾 Salvar insumo")

    # Persistência
    if enviado:
        # validações essenciais
        if not insumo_resumo.strip():
            st.warning("Informe o **Nome resumido do insumo**.")
            st.stop()
        if grupo_sel == "➕ Adicionar novo grupo":
            st.warning("Selecione um **Grupo** válido (ou adicione e selecione).")
            st.stop()
        if quantidade_compra <= 0:
            st.warning("Informe uma **Quantidade comprada** válida (> 0).")
            st.stop()
        if valor_total_compra <= 0:
            st.warning("Informe um **Valor total da compra** válido (> 0).")
            st.stop()

        registro = {
            "data_compra": data_compra.strftime("%d/%m/%Y"),
            "grupo": (novo_grupo.strip() if (grupo_sel == "➕ Adicionar novo grupo" and novo_grupo.strip()) else grupo_sel),
            "insumo_resumo": insumo_resumo.strip(),
            "insumo_completo": (insumo_completo.strip() or insumo_resumo.strip()),
            "marca": (marca.strip() if marca else ""),
            "tipo": tipo,
            "un_med": un_med,
            "quantidade_compra": quantidade_compra,
            "qtde_para_custos": qtde_para_custos,
            "valor_total_compra": round(valor_total_compra, 2),
            "valor_frete": round(valor_frete, 2),
            "percentual_perda": float(percentual_perda),
            "valor_unit_bruto": round(valor_unit_bruto, 6),
            "custo_total_com_frete": round(custo_total_com_frete, 2),
            "quantidade_liquida": round(quantidade_liquida, 6),
            "custo_real_unitario": round(custo_real_unitario, 6),
            "valor_unit_para_custos": round(valor_unit_para_custos, 6),
            "custo_total_ajustado_ref": round(custo_total_ajustado_ref, 6),
            "fornecedor": (fornecedor.strip() if fornecedor else ""),
            "fone_fornecedor": (fone_fornecedor.strip() if fone_fornecedor else ""),
            "representante": (representante.strip() if representante else ""),
            "documento": (documento.strip() if documento else ""),
            "observacao": (observacao.strip() if observacao else ""),
            "Atualizado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        df_compras = pd.concat([df_compras, pd.DataFrame([registro])], ignore_index=True)
        salvar_df(df_compras, COMPRAS_CSV)
        st.success(f"Insumo **{insumo_resumo}** salvo com sucesso!")
        st.experimental_rerun()

elif aba == "📋 Visualizar insumos":
    st.subheader("📋 Lista de Insumos Cadastrados")
    if df_compras.empty:
        st.info("Nenhum insumo cadastrado ainda.")
    else:
        # formatação amigável
        df_view = df_compras.copy()
        money_cols = ["valor_total_compra","valor_frete","valor_unit_bruto",
                      "custo_total_com_frete","custo_real_unitario","valor_unit_para_custos",
                      "custo_total_ajustado_ref"]
        for col in money_cols:
            if col in df_view.columns:
                df_view[col] = df_view[col].apply(lambda x: f"R$ {x:,.4f}".replace(",", "X").replace(".", ",").replace("X", "."))

        st.dataframe(df_view, use_container_width=True)

# ======================================================
# RODAPÉ
# ======================================================
rodape()
