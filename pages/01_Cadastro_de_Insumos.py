import streamlit as st
import pandas as pd
from datetime import date, datetime
from pathlib import Path

# ============================================================
# CONFIGURAÇÃO INICIAL
# ============================================================
st.set_page_config(page_title="FichApp — Cadastro de Insumos", page_icon="📦", layout="wide")

APP_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = APP_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

COMPRAS_CSV = DATA_DIR / "compras_insumos.csv"
GRUPOS_CSV  = DATA_DIR / "grupos_insumos.csv"
UNIDS_CSV   = DATA_DIR / "unidades_medida.csv"

# Campos padrão do CSV
COLS_COMPRAS = [
    "data_compra","grupo","insumo_resumo","insumo_completo","marca","tipo",
    "un_med","quantidade_compra","qtde_para_custos","valor_total_compra","valor_frete",
    "percentual_perda","valor_unit_bruto","custo_total_com_frete","quantidade_liquida",
    "custo_real_unitario","valor_unit_para_custos","fornecedor","fone_fornecedor",
    "representante","documento","observacao","Atualizado_em"
]

# Grupos e unidades padrão
DEFAULT_GRUPOS = [
    "Embalagem","Peixe","Carne","Hortifruti","Bebida","Frios",
    "Molhos e Temperos","Grãos e Cereais","Higiene","Limpeza","Outros"
]

DEFAULT_UNIDADES = [
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

# Inicializa arquivos
if not COMPRAS_CSV.exists():
    pd.DataFrame(columns=COLS_COMPRAS).to_csv(COMPRAS_CSV, index=False)
if not GRUPOS_CSV.exists():
    pd.DataFrame({"grupo": DEFAULT_GRUPOS}).to_csv(GRUPOS_CSV, index=False)
if not UNIDS_CSV.exists():
    pd.DataFrame(DEFAULT_UNIDADES, columns=["codigo","descricao","qtde_padrao"]).to_csv(UNIDS_CSV, index=False)

# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================
@st.cache_data
def load_df(path: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()

def save_df(df: pd.DataFrame, path: Path):
    df.to_csv(path, index=False)
    st.cache_data.clear()

def get_grupos():
    g = load_df(GRUPOS_CSV)
    if "grupo" in g.columns:
        return sorted(g["grupo"].dropna().astype(str).unique().tolist())
    return DEFAULT_GRUPOS

def get_unidades():
    u = load_df(UNIDS_CSV)
    if {"codigo","descricao","qtde_padrao"}.issubset(u.columns):
        return u
    return pd.DataFrame(DEFAULT_UNIDADES, columns=["codigo","descricao","qtde_padrao"])

def label_unidade(row):
    return f"{row['codigo']} – {row['descricao']}"

def calc_preview(qtd_compra, total, frete, perda, qtd_custo):
    valor_unit_bruto = (total / qtd_compra) if qtd_compra > 0 else 0
    custo_total_com_frete = total + frete
    fator_apr = (100 - perda) / 100
    qtd_liquida = qtd_compra * fator_apr if qtd_compra > 0 else 0
    custo_real_unit = (custo_total_com_frete / qtd_liquida) if qtd_liquida > 0 else 0
    valor_unit_para_custos = (custo_real_unit / qtd_custo) if qtd_custo > 0 else 0
    return valor_unit_bruto, custo_total_com_frete, qtd_liquida, custo_real_unit, valor_unit_para_custos

# ============================================================
# GERENCIAR GRUPOS / UNIDADES
# ============================================================
with st.expander("🧩 Gerenciar listas auxiliares"):
    gcol, ucol = st.columns(2)
    with gcol:
        st.subheader("➕ Grupos de insumo")
        novo_grupo = st.text_input("Novo grupo")
        if st.button("Adicionar grupo"):
            if novo_grupo.strip():
                g = load_df(GRUPOS_CSV)
                if "grupo" not in g.columns:
                    g = pd.DataFrame({"grupo":[]})
                if novo_grupo not in g["grupo"].values:
                    g.loc[len(g)] = [novo_grupo]
                    save_df(g, GRUPOS_CSV)
                    st.success(f"Grupo “{novo_grupo}” adicionado com sucesso.")
                    st.rerun()
            else:
                st.warning("Digite o nome do grupo antes de adicionar.")

    with ucol:
        st.subheader("➕ Unidades de medida")
        abrev = st.text_input("Abreviação (ex.: KG, UN, CT)")
        desc = st.text_input("Descrição (ex.: Quilograma)")
        qtd_padrao = st.number_input("Qtde padrão (opcional)", min_value=0.0, step=1.0, value=0.0)
        if st.button("Adicionar unidade"):
            if abrev.strip() and desc.strip():
                u = load_df(UNIDS_CSV)
                if "codigo" not in u.columns:
                    u = pd.DataFrame(columns=["codigo","descricao","qtde_padrao"])
                if abrev.upper() not in u["codigo"].values:
                    qtd_val = qtd_padrao if qtd_padrao > 0 else None
                    u.loc[len(u)] = [abrev.upper(), desc.strip(), qtd_val]
                    save_df(u, UNIDS_CSV)
                    st.success(f"Unidade “{abrev.upper()} – {desc}” adicionada.")
                    st.rerun()
            else:
                st.warning("Informe abreviação e descrição.")

# ============================================================
# INTERFACE PRINCIPAL
# ============================================================
st.markdown("## 📦 Cadastro de Insumos")
st.write("Cadastre insumos com **grupos**, **unidades dinâmicas**, **frete**, **perda** e cálculos automáticos de custo.")

modo = st.radio("Ação:", ["➕ Cadastrar novo insumo", "✏️ Editar insumo", "📋 Visualizar insumos"])

grupos = get_grupos()
unidades_df = get_unidades()
unidades_labels = unidades_df.apply(label_unidade, axis=1).tolist()
map_label_to_code = dict(zip(unidades_labels, unidades_df["codigo"]))
map_code_to_qpad = dict(zip(unidades_df["codigo"], unidades_df["qtde_padrao"]))
df_compras = load_df(COMPRAS_CSV)

# ============================================================
# FORMULÁRIO BASE
# ============================================================
def form_insumo(initial: dict | None, is_edit: bool):
    dat = initial.copy() if initial else {}
    dat.setdefault("data_compra", date.today().strftime("%d/%m/%Y"))
    dat.setdefault("grupo", grupos[0] if grupos else "Outros")
    dat.setdefault("insumo_resumo", "")
    dat.setdefault("insumo_completo", "")
    dat.setdefault("marca", "")
    dat.setdefault("tipo", "Comprado")
    dat.setdefault("un_med", "UN")
    dat.setdefault("quantidade_compra", 0.0)
    dat.setdefault("qtde_para_custos", 1.0)
    dat.setdefault("valor_total_compra", 0.0)
    dat.setdefault("valor_frete", 0.0)
    dat.setdefault("percentual_perda", 0.0)
    dat.setdefault("fornecedor", "")
    dat.setdefault("fone_fornecedor", "")
    dat.setdefault("representante", "")
    dat.setdefault("documento", "")
    dat.setdefault("observacao", "")

    with st.form("form_edit" if is_edit else "form_new", clear_on_submit=False):
        c1, c2 = st.columns(2)
        with c1:
            data_compra = st.date_input(
                "Data da compra",
                value=datetime.strptime(dat["data_compra"], "%d/%m/%Y").date() if dat["data_compra"] else date.today(),
                format="DD/MM/YYYY"
            )
            grupo = st.selectbox("Grupo", options=grupos, index=grupos.index(dat["grupo"]) if dat["grupo"] in grupos else 0)
            insumo_resumo = st.text_input("Nome resumido do insumo", value=dat["insumo_resumo"])
            insumo_completo = st.text_input(
                "Nome completo do insumo",
                value=dat["insumo_completo"] or dat["insumo_resumo"]
            )
            if insumo_resumo and (dat["insumo_completo"] == "" or dat["insumo_completo"] == dat["insumo_resumo"]):
                insumo_completo = insumo_resumo
            marca = st.text_input("Marca", value=dat["marca"])
            tipo = st.selectbox("Tipo", ["Comprado", "Produzido no restaurante"], index=0 if dat["tipo"] != "Produzido no restaurante" else 1)

        with c2:
            un_label_sel = st.selectbox(
                "Unidade de medida",
                options=unidades_labels,
                index=unidades_df.index[unidades_df["codigo"]==dat["un_med"]].tolist()[0]
                if dat["un_med"] in unidades_df["codigo"].tolist() else 0
            )
            un_med = map_label_to_code[un_label_sel]

            quantidade_compra = st.number_input("Quantidade comprada", value=float(dat["quantidade_compra"]), min_value=0.0, step=0.01)

            # Quantidade para custos automática
            if un_med in ["MIL", "CT", "DZ"]:
                auto_valor = {"MIL": 1000, "CT": 100, "DZ": 12}[un_med]
            else:
                auto_valor = 1.0
            qtde_para_custos = st.number_input(
                "Quantidade para custos",
                value=float(dat.get("qtde_para_custos", auto_valor) or auto_valor),
                min_value=0.0,
                step=1.0,
                help="Preenchida automaticamente conforme unidade padrão (MIL=1000, CT=100, DZ=12)."
            )

        st.markdown("---")
        st.subheader("💰 Custos e ajustes")

        c3, c4, c5 = st.columns(3)
        with c3:
            valor_total_compra = st.number_input("Valor total da compra (R$)", value=float(dat["valor_total_compra"]), min_value=0.0, step=0.01)
        with c4:
            valor_frete = st.number_input("Frete (R$)", value=float(dat["valor_frete"]), min_value=0.0, step=0.01)
        with c5:
            percentual_perda = st.number_input(
                "% de perda", value=float(dat["percentual_perda"]),
                min_value=0.0, max_value=100.0, step=0.5,
                help="Perda (limpeza, aparas, evaporação, etc.)"
            )

        # cálculos
        valor_unit_bruto, custo_total_com_frete, qtd_liq, custo_real_unit, valor_unit_custos = calc_preview(
            quantidade_compra, valor_total_compra, valor_frete, percentual_perda, qtde_para_custos
        )

        st.markdown("#### 📊 Pré-visualização")
        lcol, rcol = st.columns(2)
        with lcol:
            st.write(f"• Valor unitário bruto: **R$ {valor_unit_bruto:.4f}**")
            st.write(f"• Custo total com frete: **R$ {custo_total_com_frete:.2f}**")
            st.write(f"• Quantidade líquida (após perda): **{qtd_liq:.4f} {un_med}**")
        with rcol:
            st.write(f"• Custo real unitário: **R$ {custo_real_unit:.6f}**")
            st.write(f"• Custo unitário p/ custos: **R$ {valor_unit_custos:.6f}**")

        st.markdown("---")
        st.subheader("📇 Fornecedor e contato")
        f1, f2 = st.columns(2)
        with f1:
            fornecedor = st.text_input("Fornecedor", value=dat["fornecedor"])
            representante = st.text_input("Representante", value=dat["representante"])
        with f2:
            fone_fornecedor = st.text_input("Fone do fornecedor", value=dat["fone_fornecedor"])
            documento = st.text_input("Documento / Nota Fiscal", value=dat["documento"])
        observacao = st.text_area("Observação", value=dat["observacao"])

        enviado = st.form_submit_button("💾 Salvar alterações" if is_edit else "💾 Salvar insumo")

    payload = {
        "data_compra": data_compra.strftime("%d/%m/%Y"),
        "grupo": grupo,
        "insumo_resumo": insumo_resumo,
        "insumo_completo": insumo_completo,
        "marca": marca,
        "tipo": tipo,
        "un_med": un_med,
        "quantidade_compra": quantidade_compra,
        "qtde_para_custos": qtde_para_custos,
        "valor_total_compra": valor_total_compra,
        "valor_frete": valor_frete,
        "percentual_perda": percentual_perda,
        "valor_unit_bruto": round(valor_unit_bruto,4),
        "custo_total_com_frete": round(custo_total_com_frete,4),
        "quantidade_liquida": round(qtd_liq,4),
        "custo_real_unitario": round(custo_real_unit,6),
        "valor_unit_para_custos": round(valor_unit_custos,6),
        "fornecedor": fornecedor,
        "fone_fornecedor": fone_fornecedor,
        "representante": representante,
        "documento": documento,
        "observacao": observacao,
        "Atualizado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return enviado, payload

# ============================================================
# ➊ CADASTRAR
# ============================================================
if modo == "➕ Cadastrar novo insumo":
    enviado, novo = form_insumo(None, False)
    if enviado:
        df = load_df(COMPRAS_CSV)
        df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
        save_df(df, COMPRAS_CSV)
        st.success(f"Insumo **{novo['insumo_resumo']}** salvo com sucesso!")
        st.rerun()

# ============================================================
# ➋ EDITAR
# ============================================================
elif modo == "✏️ Editar insumo":
    df = load_df(COMPRAS_CSV)
    if df.empty:
        st.info("Nenhum insumo cadastrado ainda.")
    else:
        idx = st.selectbox(
            "Selecione o insumo para editar:",
            options=df.index.tolist(),
            format_func=lambda i: f"{df.loc[i,'insumo_resumo']} • {df.loc[i,'grupo']} ({df.loc[i,'data_compra']})"
        )
        dados = df.loc[idx].to_dict()
        enviado, atualizado = form_insumo(dados, True)
        if enviado:
            df.loc[idx] = atualizado
            save_df(df, COMPRAS_CSV)
            st.success("Alterações salvas com sucesso.")
            st.rerun()

# ============================================================
# ➌ VISUALIZAR
# ============================================================
else:
    df = load_df(COMPRAS_CSV)
    if df.empty:
        st.info("Nenhum insumo cadastrado ainda.")
    else:
        df_show = df.copy()
        for c in ["valor_total_compra","valor_frete","valor_unit_bruto","custo_total_com_frete","custo_real_unitario","valor_unit_para_custos"]:
            if c in df_show.columns:
                df_show[c] = df_show[c].apply(lambda x: f"R$ {x:,.4f}".replace(",", "X").replace(".", ",").replace("X","."))
        st.dataframe(df_show, use_container_width=True)
