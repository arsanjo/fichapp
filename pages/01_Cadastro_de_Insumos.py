import streamlit as st
import pandas as pd
from datetime import date, datetime
from pathlib import Path

# Utilidades de tema/rodapé (você já tem isso em utils/theme.py)
try:
    from utils.theme import aplicar_tema, carregar_versao, rodape
except Exception:
    # fallback simples caso ainda não exista utils/theme.py
    def aplicar_tema(): 
        st.set_page_config(page_title="FichApp — Cadastro de Insumos", page_icon="📦", layout="wide")
    def carregar_versao(_="versao.json"):
        return {"versao": "v0.1.0", "data_lancamento": date.today().isoformat()}
    def rodape(_): 
        st.markdown("""<div style="margin-top:24px;color:#94a3b8;">FichApp — rodapé</div>""", unsafe_allow_html=True)

# ============================================================
# Setup / paths
# ============================================================
aplicar_tema()
VERSAO = carregar_versao("versao.json")

APP_DIR = Path(__file__).resolve().parents[1]  # raiz do repo
DATA_DIR = APP_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

COMPRAS_CSV = DATA_DIR / "compras_insumos.csv"
GRUPOS_CSV  = DATA_DIR / "grupos_insumos.csv"
UNIDS_CSV   = DATA_DIR / "unidades_medida.csv"

# tabelas padrão
COLS_COMPRAS = [
    "data_compra","grupo","insumo_resumo","insumo_completo","marca","tipo",
    "un_med","quantidade_compra","qtde_para_custos","valor_total_compra",
    "valor_frete","percentual_perda","valor_unit_bruto","custo_total_com_frete",
    "quantidade_liquida","custo_real_unitario","valor_unit_para_custos",
    "fornecedor","fone_fornecedor","representante","documento","observacao"
]

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

# cria arquivos vazios se necessário
if not COMPRAS_CSV.exists():
    pd.DataFrame(columns=COLS_COMPRAS).to_csv(COMPRAS_CSV, index=False)

if not GRUPOS_CSV.exists():
    pd.DataFrame({"grupo": DEFAULT_GRUPOS}).to_csv(GRUPOS_CSV, index=False)

if not UNIDS_CSV.exists():
    pd.DataFrame(DEFAULT_UNIDADES, columns=["codigo","descricao","qtde_padrao"]).to_csv(UNIDS_CSV, index=False)

# ============================================================
# Helpers
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

def get_grupos() -> list:
    g = load_df(GRUPOS_CSV)
    if "grupo" in g.columns:
        return sorted(g["grupo"].dropna().astype(str).unique().tolist())
    return DEFAULT_GRUPOS

def get_unidades() -> pd.DataFrame:
    u = load_df(UNIDS_CSV)
    if {"codigo","descricao","qtde_padrao"}.issubset(u.columns):
        return u
    return pd.DataFrame(DEFAULT_UNIDADES, columns=["codigo","descricao","qtde_padrao"])

def unit_label(row):
    return f"{row['codigo']} – {row['descricao']}"

def calc_preview(quantidade_compra, valor_total_compra, valor_frete, percentual_perda, qtde_para_custos):
    valor_unit_bruto = (valor_total_compra / quantidade_compra) if quantidade_compra > 0 else 0.0
    custo_total_com_frete = valor_total_compra + valor_frete
    fator_apr = (100.0 - percentual_perda) / 100.0
    quantidade_liquida = quantidade_compra * fator_apr if quantidade_compra > 0 else 0.0
    custo_real_unitario = (custo_total_com_frete / quantidade_liquida) if quantidade_liquida > 0 else 0.0
    base = qtde_para_custos if qtde_para_custos and qtde_para_custos > 0 else 1.0
    valor_unit_para_custos = custo_real_unitario / base
    return (
        valor_unit_bruto, custo_total_com_frete, quantidade_liquida,
        custo_real_unitario, valor_unit_para_custos
    )

# ============================================================
# Gerenciar grupos/unidades (fora do form)
# ============================================================
with st.expander("🧩 Gerenciar listas auxiliares (grupos e unidades)"):
    gcol, ucol = st.columns(2)

    with gcol:
        st.subheader("➕ Grupos de insumo")
        novo_grupo = st.text_input("Novo grupo")
        if st.button("Adicionar grupo", key="add_grupo_now"):
            novo_grupo2 = (novo_grupo or "").strip()
            if not novo_grupo2:
                st.warning("Digite um nome para o grupo.")
            else:
                g = load_df(GRUPOS_CSV)
                if "grupo" not in g.columns:
                    g = pd.DataFrame({"grupo": []})
                if novo_grupo2 not in set(g["grupo"].astype(str)):
                    g.loc[len(g)] = [novo_grupo2]
                    save_df(g, GRUPOS_CSV)
                    st.success(f"Grupo “{novo_grupo2}” adicionado.")
                    st.rerun()
                else:
                    st.info("Esse grupo já existe.")

    with ucol:
        st.subheader("➕ Unidades de medida")
        nova_abrev = st.text_input("Abreviação (ex.: KG, UN, CT)", key="nova_abrev")
        nova_desc  = st.text_input("Descrição (ex.: Quilograma)", key="nova_desc")
        nova_qtd_padrao = st.number_input("Qtde padrão p/ custos (opcional)", min_value=0.0, step=1.0, value=0.0, key="nova_qtd_padrao")
        if st.button("Adicionar unidade", key="add_un_now"):
            ab = (nova_abrev or "").strip().upper()
            ds = (nova_desc or "").strip()
            if not ab or not ds:
                st.warning("Informe abreviação e descrição.")
            else:
                u = load_df(UNIDS_CSV)
                if {"codigo","descricao","qtde_padrao"}.issubset(u.columns) is False:
                    u = pd.DataFrame(columns=["codigo","descricao","qtde_padrao"])
                if ab not in set(u["codigo"].astype(str)):
                    qtdp = nova_qtd_padrao if nova_qtd_padrao > 0 else None
                    u.loc[len(u)] = [ab, ds, qtdp]
                    save_df(u, UNIDS_CSV)
                    st.success(f"Unidade “{ab} – {ds}” adicionada.")
                    st.rerun()
                else:
                    st.info("Essa unidade já existe.")

# ============================================================
# Cabeçalho e modo (Cadastrar / Editar / Visualizar)
# ============================================================
st.markdown("## 📦 Cadastro de Insumos")
st.write("Cadastre insumos com **grupos**, **unidades dinâmicas**, **frete**, **perda** e cálculos automáticos de custo.")

modo = st.radio("Ação:", ["➕ Cadastrar novo insumo", "✏️ Editar insumo", "📋 Visualizar insumos"], horizontal=False)

grupos = get_grupos()
unidades_df = get_unidades()
unidades_labels = unidades_df.apply(unit_label, axis=1).tolist()
map_label_to_code = dict(zip(unidades_labels, unidades_df["codigo"]))
map_code_to_qpad = dict(zip(unidades_df["codigo"], unidades_df["qtde_padrao"]))

df_compras = load_df(COMPRAS_CSV)

# ============================================================
# Formulário base (função para reaproveitar no cadastrar/editar)
# ============================================================
def form_insumo(initial: dict | None, is_edit: bool):
    """
    Renderiza o formulário e retorna (dados_salvos_boolean, dict_dados)
    """
    # valores padrão/seeding
    dat = initial.copy() if initial else {}
    dat.setdefault("data_compra", date.today().strftime("%d/%m/%Y"))
    dat.setdefault("grupo", grupos[0] if grupos else "Outros")
    dat.setdefault("insumo_resumo", "")
    dat.setdefault("insumo_completo", "")
    dat.setdefault("marca", "")
    dat.setdefault("tipo", "Comprado")
    dat.setdefault("un_med", "UN")
    dat.setdefault("quantidade_compra", 0.0)
    dat.setdefault("qtde_para_custos", map_code_to_qpad.get(dat["un_med"], 1) or 1)
    dat.setdefault("valor_total_compra", 0.0)
    dat.setdefault("valor_frete", 0.0)
    dat.setdefault("percentual_perda", 0.0)
    dat.setdefault("fornecedor", "")
    dat.setdefault("fone_fornecedor", "")
    dat.setdefault("representante", "")
    dat.setdefault("documento", "")
    dat.setdefault("observacao", "")

    with st.form("f_insumo_edit" if is_edit else "f_insumo_new", clear_on_submit=False):
        c1, c2 = st.columns([1,1])
        with c1:
            data_compra = st.date_input(
                "Data da compra",
                value=datetime.strptime(dat["data_compra"], "%d/%m/%Y").date() if dat["data_compra"] else date.today(),
                format="DD/MM/YYYY"
            )
            grupo = st.selectbox("Grupo", options=grupos, index=grupos.index(dat["grupo"]) if dat["grupo"] in grupos else 0)

            # nome resumido / completo com cópia automática
            insumo_resumo = st.text_input("Nome resumido do insumo", value=dat["insumo_resumo"])
            default_completo = dat["insumo_completo"] or dat["insumo_resumo"]
            insumo_completo = st.text_input("Nome completo do insumo", value=default_completo)
            if insumo_resumo and (dat["insumo_completo"] == "" or dat["insumo_completo"] == dat["insumo_resumo"]):
                insumo_completo = insumo_resumo  # copia automática

            marca = st.text_input("Marca (opcional)", value=dat["marca"])
            tipo = st.selectbox("Tipo", options=["Comprado","Produzido no restaurante"], index=0 if dat["tipo"]!="Produzido no restaurante" else 1)

        with c2:
            # medidas
            un_label_sel = st.selectbox(
                "Unidade de medida",
                options=unidades_labels,
                index=unidades_df.index[unidades_df["codigo"]==dat["un_med"]].tolist()[0]
                if dat["un_med"] in unidades_df["codigo"].tolist() else 0
            )
            un_med = map_label_to_code[un_label_sel]

            quantidade_compra = st.number_input("Quantidade comprada", value=float(dat["quantidade_compra"]), min_value=0.0, step=0.01)
            # padrão de custos para unidade
            padrao_un = map_code_to_qpad.get(un_med)
            default_qc = dat["qtde_para_custos"] or (padrao_un if padrao_un and pd.notna(padrao_un) else 1)
            qtde_para_custos = st.number_input("Quantidade para custos", value=float(default_qc), min_value=0.0, step=1.0)

        st.markdown("---")
        st.subheader("💵 Custos")
        c3, c4, c5 = st.columns([1,1,1])

        with c3:
            valor_total_compra = st.number_input("Valor total da compra (R$)", value=float(dat["valor_total_compra"]), min_value=0.0, step=0.01)
        with c4:
            valor_frete = st.number_input("Frete (R$)", value=float(dat["valor_frete"]), min_value=0.0, step=0.01)
        with c5:
            percentual_perda = st.number_input("% de perda", value=float(dat["percentual_perda"]), min_value=0.0, max_value=100.0, step=0.5,
                                               help="Perda por limpeza/aparas/evaporação etc.")

        # cálculo em tempo real
        (valor_unit_bruto, custo_total_com_frete, quantidade_liquida,
         custo_real_unitario, valor_unit_para_custos) = calc_preview(
            quantidade_compra, valor_total_compra, valor_frete, percentual_perda, qtde_para_custos
        )

        st.markdown("#### 🧮 Pré-visualização dos cálculos")
        lcol, rcol = st.columns(2)
        with lcol:
            st.write(f"• **Valor unitário bruto:** R$ {valor_unit_bruto:.4f}")
            st.write(f"• **Custo total com frete:** R$ {custo_total_com_frete:.2f}")
            st.write(f"• **Quantidade líquida (após perda):** {quantidade_liquida:.4f} {un_med}")
        with rcol:
            st.write(f"• **Custo real unitário:** R$ {custo_real_unitario:.6f}")
            st.write(f"• **Custo unitário p/ custos:** R$ {valor_unit_para_custos:.6f}")

        st.markdown("---")
        st.subheader("📇 Fornecedor e contato (opcional)")
        f1, f2 = st.columns(2)
        with f1:
            fornecedor = st.text_input("Fornecedor", value=dat["fornecedor"])
            representante = st.text_input("Representante", value=dat["representante"])
        with f2:
            fone_fornecedor = st.text_input("Fone do fornecedor", value=dat["fone_fornecedor"])
            documento = st.text_input("Documento / Nota Fiscal", value=dat["documento"])
        observacao = st.text_area("Observação", value=dat["observacao"])

        enviado = st.form_submit_button("💾 Salvar alterações" if is_edit else "💾 Salvar insumo")

    # monta o dicionário pronto para salvar
    payload = {
        "data_compra": data_compra.strftime("%d/%m/%Y"),
        "grupo": grupo,
        "insumo_resumo": insumo_resumo,
        "insumo_completo": insumo_completo or insumo_resumo,
        "marca": marca,
        "tipo": tipo,
        "un_med": un_med,
        "quantidade_compra": quantidade_compra,
        "qtde_para_custos": qtde_para_custos,
        "valor_total_compra": valor_total_compra,
        "valor_frete": valor_frete,
        "percentual_perda": percentual_perda,
        "valor_unit_bruto": round(valor_unit_bruto, 4),
        "custo_total_com_frete": round(custo_total_com_frete, 4),
        "quantidade_liquida": round(quantidade_liquida, 4),
        "custo_real_unitario": round(custo_real_unitario, 6),
        "valor_unit_para_custos": round(valor_unit_para_custos, 6),
        "fornecedor": fornecedor,
        "fone_fornecedor": fone_fornecedor,
        "representante": representante,
        "documento": documento,
        "observacao": observacao
    }
    return enviado, payload

# ============================================================
# ➊ Cadastrar novo
# ============================================================
if modo == "➕ Cadastrar novo insumo":
    enviado, novo = form_insumo(initial=None, is_edit=False)
    if enviado:
        df = load_df(COMPRAS_CSV)
        df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
        save_df(df, COMPRAS_CSV)
        st.success(f"Insumo **{novo['insumo_resumo']}** salvo com sucesso!")
        st.rerun()

# ============================================================
# ➋ Editar existente
# ============================================================
elif modo == "✏️ Editar insumo":
    if df_compras.empty:
        st.info("Não há insumos para editar ainda.")
    else:
        # escolha do registro
        idx = st.selectbox(
            "Selecione o insumo para editar:",
            options=df_compras.index.tolist(),
            format_func=lambda i: f"{df_compras.loc[i,'insumo_resumo']} • {df_compras.loc[i,'grupo']} ({df_compras.loc[i,'data_compra']})"
        )
        dados_idx = df_compras.loc[idx].to_dict()
        enviado, editado = form_insumo(initial=dados_idx, is_edit=True)
        if enviado:
            df_compras.loc[idx] = editado
            save_df(df_compras, COMPRAS_CSV)
            st.success("Alterações salvas com sucesso.")
            st.rerun()

# ============================================================
# ➌ Visualizar
# ============================================================
else:
    st.markdown("### 📋 Lista de Insumos Cadastrados")
    if df_compras.empty:
        st.info("Nenhum insumo cadastrado ainda.")
    else:
        # formata valores monetários
        df_show = df_compras.copy()
        for col in ["valor_total_compra","valor_frete","valor_unit_bruto","custo_total_com_frete","custo_real_unitario","valor_unit_para_custos"]:
            if col in df_show.columns:
                df_show[col] = df_show[col].apply(lambda x: f"R$ {x:,.4f}".replace(",", "X").replace(".", ",").replace("X","."))
        st.dataframe(df_show, use_container_width=True)

# Rodapé
rodape(VERSAO)
