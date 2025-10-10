import streamlit as st
import pandas as pd
from datetime import datetime, date
import os, json, random

# =========================================================
# CONFIG / THEME
# =========================================================
st.set_page_config(page_title="FichApp — Cadastro de Insumos", page_icon="📦", layout="centered")

DARK_CSS = """
<style>
.block-container { padding-top: 2rem; padding-bottom: 2rem; }
h1, h2, h3, h4 { font-weight: 700; }
.st-expander { border: 1px solid #e5e7eb; border-radius: 10px; }
.stButton>button, .stForm form button[kind="primary"]{
  background: #0f172a; color: #fff; border: 0; border-radius: 10px; padding: .6rem 1rem;
}
.stButton>button:hover, .stForm form button[kind="primary"]{
  background: #1e293b;
}
#fichapp-footer {
  margin-top: 24px; padding: 16px 18px; border-radius: 12px;
  background: #0b1220; color: #e5e7eb; font-size: 0.92rem;
  display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap;
}
#fichapp-footer .left { font-weight: 600; }
#fichapp-footer .right { opacity: .85; }
</style>
"""
st.markdown(DARK_CSS, unsafe_allow_html=True)

# =========================================================
# Versão
# =========================================================
VERSAO_PATH = "version.json"
versao_info = {"version": "0.0.0", "released_at": "", "description": ""}
if os.path.exists(VERSAO_PATH):
    try:
        with open(VERSAO_PATH, "r", encoding="utf-8") as f:
            versao_info = json.load(f)
    except Exception:
        pass

# =========================================================
# Caminhos dos dados
# =========================================================
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

COMPRAS_CSV = os.path.join(DATA_DIR, "compras_insumos.csv")
GRUPOS_CSV  = os.path.join(DATA_DIR, "grupos_insumos.csv")
UNIDS_CSV   = os.path.join(DATA_DIR, "unidades_medida.csv")

# =========================================================
# Inicialização dos arquivos
# =========================================================
compras_cols = [
    "data_compra","grupo","insumo_resumo","insumo_completo","marca","tipo",
    "un_med","quantidade_compra","qtde_para_custos",
    "valor_total_compra","valor_frete","percentual_perda",
    "valor_unit_bruto","custo_total_com_frete","quantidade_liquida",
    "custo_real_unitario","valor_unit_para_custos",
    "fornecedor","fone_fornecedor","representante","documento","observacao",
    "atualizado_em"
]
if (not os.path.exists(COMPRAS_CSV)) or os.stat(COMPRAS_CSV).st_size == 0:
    pd.DataFrame(columns=compras_cols).to_csv(COMPRAS_CSV, index=False)

grupos_padrao = [
    "Embalagem","Peixe","Carne","Hortifruti","Bebida","Frios",
    "Molhos e Temperos","Grãos e Cereais","Higiene","Limpeza","Outros"
]
if (not os.path.exists(GRUPOS_CSV)) or os.stat(GRUPOS_CSV).st_size == 0:
    pd.DataFrame({"grupo": grupos_padrao}).to_csv(GRUPOS_CSV, index=False)

# qtde_padrao é o FATOR da unidade. Para DZ=12, CT=100, MIL=1000
unidades_padrao = [
    ("KG","Quilograma", 1),
    ("G","Grama", 1000),
    ("L","Litro", 1),
    ("ML","Mililitro", 1000),
    ("UN","Unidade", 1),
    ("DZ","Dúzia", 12),
    ("MIL","Milheiro", 1000),
    ("CT","Cento", 100),
    ("CX","Caixa", 1),
    ("FD","Fardo", 1),
    ("PAC","Pacote", 1),
    ("BAN","Bandeja", 1),
    ("PAR","Par", 2),
    ("POR","Porção", 1),
]
if (not os.path.exists(UNIDS_CSV)) or os.stat(UNIDS_CSV).st_size == 0:
    pd.DataFrame(unidades_padrao, columns=["codigo","descricao","qtde_padrao"]).to_csv(UNIDS_CSV, index=False)

# =========================================================
# Helpers
# =========================================================
@st.cache_data
def carregar_tabela(path: str) -> pd.DataFrame:
    try: return pd.read_csv(path)
    except Exception: return pd.DataFrame()

def salvar_tabela(df: pd.DataFrame, path: str):
    df.to_csv(path, index=False)
    st.cache_data.clear()

def lista_grupos() -> list[str]:
    gdf = carregar_tabela(GRUPOS_CSV)
    if "grupo" in gdf.columns:
        return sorted(gdf["grupo"].dropna().astype(str).unique().tolist())
    return grupos_padrao

def lista_unidades() -> pd.DataFrame:
    udf = carregar_tabela(UNIDS_CSV)
    cols = {"codigo","descricao","qtde_padrao"}
    if set(udf.columns) >= cols:
        return udf
    return pd.DataFrame(unidades_padrao, columns=["codigo","descricao","qtde_padrao"])

def label_unidade(row):
    return f"{row['codigo']} – {row['descricao']}"

# =========================================================
# Estado da UI
# =========================================================
defaults = {
    "nome_resumo": "",
    "nome_completo": "",
    "nome_completo_lock": True,
    "un_sel": "UN",
    "last_un_sel": None,
    "last_qtd_compra": None,
    "qtde_para_custos_value": 0.0,   # valor que exibimos no input (permite override manual)
}
for k,v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =========================================================
# Cabeçalho
# =========================================================
st.markdown("<h1>Cadastro de Insumos</h1>", unsafe_allow_html=True)
acao = st.radio("Ação:", ["➕ Cadastrar novo insumo", "✏️ Editar insumo", "📋 Visualizar insumos"], index=0)

# =========================================================
# CADASTRO
# =========================================================
if acao == "➕ Cadastrar novo insumo":
    grupos = lista_grupos()
    unidades_df = lista_unidades()
    unidades_labels = unidades_df.apply(label_unidade, axis=1).tolist()
    codigo_por_label = dict(zip(unidades_labels, unidades_df["codigo"]))
    fator_por_codigo = dict(zip(unidades_df["codigo"], unidades_df["qtde_padrao"]))

    with st.form("cadastro_insumo", clear_on_submit=False):
        c1, c2 = st.columns(2)

        # -------- coluna 1
        with c1:
            data_compra = st.date_input("Data da compra", value=date.today(), format="DD/MM/YYYY")

            grupo = st.selectbox(
                "Grupo", options=grupos,
                index=grupos.index("Embalagem") if "Embalagem" in grupos else 0
            )
            with st.expander("➕ Novo grupo / editar existentes"):
                novo_grupo = st.text_input("Adicionar novo grupo")
                add_grupo = st.form_submit_button("Adicionar grupo")
                if add_grupo:
                    if novo_grupo.strip():
                        gdf = carregar_tabela(GRUPOS_CSV)
                        if "grupo" not in gdf.columns:
                            gdf = pd.DataFrame({"grupo":[]})
                        if novo_grupo.strip() not in gdf["grupo"].values:
                            gdf.loc[len(gdf)] = [novo_grupo.strip()]
                            salvar_tabela(gdf, GRUPOS_CSV)
                            st.success(f"Grupo “{novo_grupo}” adicionado. Ele já aparece na lista.")
                            st.stop()
                    else:
                        st.warning("Digite um nome para o novo grupo.")
                        st.stop()

            # nomes com cópia automática (pode editar)
            nome_resumo = st.text_input("Nome resumido do insumo", value=st.session_state["nome_resumo"])
            if nome_resumo != st.session_state["nome_resumo"]:
                st.session_state["nome_resumo"] = nome_resumo
                if st.session_state["nome_completo_lock"]:
                    st.session_state["nome_completo"] = nome_resumo

            nome_completo = st.text_input("Nome completo do insumo", value=st.session_state["nome_completo"])
            if nome_completo != st.session_state["nome_completo"]:
                st.session_state["nome_completo"] = nome_completo
                st.session_state["nome_completo_lock"] = (nome_completo == st.session_state["nome_resumo"])

            marca = st.text_input("Marca (opcional)")
            tipo = st.selectbox("Tipo", ["Comprado", "Produzido no restaurante"])

        # -------- coluna 2
        with c2:
            un_label_sel = st.selectbox(
                "Unidade de medida", options=unidades_labels,
                index=unidades_df.index[unidades_df["codigo"]==st.session_state["un_sel"]].tolist()[0]
                      if st.session_state["un_sel"] in unidades_df["codigo"].values else 0
            )
            un_med = codigo_por_label[un_label_sel]

            quantidade_compra = st.number_input("Quantidade comprada", min_value=0.0, value=0.0, step=0.01)

            # -------- CÁLCULO AUTOMÁTICO da QTDE PARA CUSTOS (com override manual)
            fator = fator_por_codigo.get(un_med, 1)
            fator = 1 if (pd.isna(fator) or fator is None or fator<=0) else float(fator)

            # se unidade/quantidade mudaram, atualiza cálculo automático
            if st.session_state["last_un_sel"] != un_med or st.session_state["last_qtd_compra"] != quantidade_compra:
                calculado = (quantidade_compra / fator) if fator > 1 else quantidade_compra
                st.session_state["qtde_para_custos_value"] = float(calculado)

            qtde_para_custos = st.number_input(
                "Quantidade para custos",
                min_value=0.0,
                value=float(st.session_state["qtde_para_custos_value"]),
                step=0.01
            )
            # se usuário alterou manualmente, preserva
            if qtde_para_custos != st.session_state["qtde_para_custos_value"]:
                st.session_state["qtde_para_custos_value"] = qtde_para_custos

            # salva os últimos para detectar mudanças
            st.session_state["un_sel"] = un_med
            st.session_state["last_un_sel"] = un_med
            st.session_state["last_qtd_compra"] = quantidade_compra

            valor_total_compra = st.number_input("Valor total da compra (R$)", min_value=0.0, value=0.0, step=0.01)
            valor_frete = st.number_input("Frete (R$)", min_value=0.0, value=0.0, step=0.01)
            percentual_perda = st.number_input("% de perda", min_value=0.0, max_value=100.0, value=0.0, step=0.5)

            # nova unidade
            with st.expander("➕ Nova unidade / editar existentes"):
                nova_abrev = st.text_input("Abreviação (ex.: KG, UN, CT)", max_chars=6)
                nova_desc  = st.text_input("Descrição (ex.: Quilograma)")
                nova_qtd_padrao = st.number_input("Fator da unidade (p/ auto-cálculo: MIL=1000, CT=100, DZ=12)", min_value=0.0, value=0.0, step=1.0)
                add_un = st.form_submit_button("Adicionar unidade")
                if add_un:
                    if nova_abrev.strip() and nova_desc.strip():
                        udf = carregar_tabela(UNIDS_CSV)
                        if set(udf.columns) != {"codigo","descricao","qtde_padrao"}:
                            udf = pd.DataFrame(columns=["codigo","descricao","qtde_padrao"])
                        if nova_abrev.strip().upper() not in udf["codigo"].values:
                            udf.loc[len(udf)] = [nova_abrev.strip().upper(), nova_desc.strip(), (nova_qtd_padrao or 1.0)]
                            salvar_tabela(udf, UNIDS_CSV)
                            st.success(f"Unidade “{nova_abrev.upper()} – {nova_desc}” adicionada.")
                            st.stop()
                    else:
                        st.warning("Preencha abreviação e descrição.")
                        st.stop()

        # =========================================================
        # Cálculos automáticos (com perda e frete)
        # =========================================================
        valor_unit_bruto = (valor_total_compra / quantidade_compra) if quantidade_compra > 0 else 0.0
        custo_total_com_frete = valor_total_compra + valor_frete
        quantidade_liquida = quantidade_compra * (1 - percentual_perda/100.0) if quantidade_compra > 0 else 0.0
        custo_real_unitario = (custo_total_com_frete / quantidade_liquida) if quantidade_liquida > 0 else 0.0
        valor_unit_para_custos = (custo_real_unitario / qtde_para_custos) if qtde_para_custos > 0 else 0.0

        st.markdown("### 💰 Pré-visualização dos cálculos")
        left, right = st.columns(2)
        with left:
            st.write(f"**Valor unitário bruto:** R$ {valor_unit_bruto:.4f}")
            st.write(f"**Custo total com frete:** R$ {custo_total_com_frete:.2f}")
            st.write(f"**Quantidade líquida (após perda):** {quantidade_liquida:.4f} {un_med}")
        with right:
            st.write(f"**Custo real unitário:** R$ {custo_real_unitario:.4f}")
            st.write(f"**Custo unitário p/ custos:** R$ {valor_unit_para_custos:.6f}")

        # =========================================================
        # Fornecedor / Observações
        # =========================================================
        st.markdown("### 🧾 Fornecedor e contato (opcional)")
        c3, c4 = st.columns(2)
        with c3:
            fornecedor = st.text_input("Fornecedor")
            fone_fornecedor = st.text_input("Fone do fornecedor")
            documento = st.text_input("Documento / Nota Fiscal")
        with c4:
            representante = st.text_input("Representante")
            observacao = st.text_area("Observação")

        enviado = st.form_submit_button("💾 Salvar Insumo")

    # Persistência
    if 'enviado' in locals() and enviado:
        df = carregar_tabela(COMPRAS_CSV)
        novo = {
            "data_compra": data_compra.strftime("%d/%m/%Y"),
            "grupo": grupo,
            "insumo_resumo": st.session_state["nome_resumo"],
            "insumo_completo": st.session_state["nome_completo"] or st.session_state["nome_resumo"],
            "marca": marca,
            "tipo": tipo,
            "un_med": st.session_state["un_sel"],
            "quantidade_compra": quantidade_compra,
            "qtde_para_custos": st.session_state["qtde_para_custos_value"],
            "valor_total_compra": valor_total_compra,
            "valor_frete": valor_frete,
            "percentual_perda": percentual_perda,
            "valor_unit_bruto": round(valor_unit_bruto,4),
            "custo_total_com_frete": round(custo_total_com_frete,2),
            "quantidade_liquida": round(quantidade_liquida,4),
            "custo_real_unitario": round(custo_real_unitario,6),
            "valor_unit_para_custos": round(valor_unit_para_custos,6),
            "fornecedor": fornecedor,
            "fone_fornecedor": fone_fornecedor,
            "representante": representante,
            "documento": documento,
            "observacao": observacao,
            "atualizado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
        salvar_tabela(df, COMPRAS_CSV)

        # limpa campos principais e pronto para novo cadastro
        st.session_state["nome_resumo"] = ""
        st.session_state["nome_completo"] = ""
        st.session_state["nome_completo_lock"] = True
        st.session_state["qtde_para_custos_value"] = 0.0
        st.success(f"Insumo **{novo['insumo_resumo']}** salvo com sucesso!")
        st.rerun()

# =========================================================
# EDITAR (placeholder — manteremos a aba)
# =========================================================
elif acao == "✏️ Editar insumo":
    st.info("A edição será adicionada logo após estabilizarmos o cadastro. 🙂")

# =========================================================
# LISTA
# =========================================================
elif acao == "📋 Visualizar insumos":
    st.markdown("### 📋 Lista de Insumos Cadastrados")
    lista_df = carregar_tabela(COMPRAS_CSV)
    if lista_df.empty:
        st.info("Nenhum insumo cadastrado ainda.")
    else:
        st.dataframe(lista_df, use_container_width=True)

# =========================================================
# Rodapé com versão + versículo
# =========================================================
versiculos = [
    ("E tudo quanto fizerdes, fazei-o de todo o coração, como ao Senhor.", "Colossenses 3:23"),
    ("O Senhor é meu pastor; nada me faltará.", "Salmo 23:1"),
    ("Confia no Senhor de todo o teu coração.", "Provérbios 3:5"),
    ("Tudo posso naquele que me fortalece.", "Filipenses 4:13"),
    ("Sede fortes e corajosos, o Senhor está convosco.", "Josué 1:9"),
    ("O amor jamais acaba.", "1 Coríntios 13:8"),
    ("O Senhor é a minha luz e a minha salvação.", "Salmo 27:1"),
    ("Lâmpada para os meus pés é a tua palavra.", "Salmo 119:105"),
    ("O choro pode durar uma noite, mas a alegria vem pela manhã.", "Salmo 30:5"),
    ("Entrega o teu caminho ao Senhor; confia nele, e ele o fará.", "Salmo 37:5")
]
v_texto, v_ref = random.choice(versiculos)
st.markdown(
    f"""
    <div id="fichapp-footer">
      <div class="left">🧩 FichApp v{versao_info.get('version','0.0.0')} — última atualização: {versao_info.get('released_at','')}</div>
      <div class="right"><em>“{v_texto}”</em> — <strong>{v_ref}</strong></div>
    </div>
    """,
    unsafe_allow_html=True
)
