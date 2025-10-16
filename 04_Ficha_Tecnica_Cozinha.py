import streamlit as st
import pandas as pd
import json, os, random
from datetime import datetime

# =========================================================
# CONFIG / THEME
# =========================================================
st.set_page_config(page_title="FichApp — Ficha Técnica (Cozinha)", page_icon="🍣", layout="centered")

DARK_CSS = """
<style>
.block-container { padding-top: 2rem; padding-bottom: 2rem; }
h1, h2, h3, h4 { font-weight: 700; }
.st-expander { border: 1px solid #1f2937; border-radius: 10px; background:#0f172a22;}
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
.small { font-size: .85rem; color: #94a3b8; }
</style>
"""
st.markdown(DARK_CSS, unsafe_allow_html=True)

# =========================================================
# MENU (protegido)
# =========================================================
try:
    from utils.nav import sidebar_menu
    sidebar_menu(ativo="ficha_tecnica")
except Exception:
    pass

# =========================================================
# Caminhos / dados
# =========================================================
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
COMPRAS_CSV = os.path.join(DATA_DIR, "compras_insumos.csv")
FICHAS_CSV = os.path.join(DATA_DIR, "fichas_tecnicas.csv")

if not os.path.exists(FICHAS_CSV):
    pd.DataFrame(columns=[
        "nome_prato","codigo_interno","codigo_sistema","codigo_pdv","categoria",
        "rendimento_total","peso_por_porcao","responsavel","modo_preparo","obs_tecnicas",
        "tempo_preparo","temperatura","equipamentos","armazenamento","foto_path",
        "ingredientes_json","atualizado_em"
    ]).to_csv(FICHAS_CSV, index=False)

@st.cache_data
def carregar_tabela(path: str) -> pd.DataFrame:
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()

def salvar_tabela(df: pd.DataFrame, path: str):
    df.to_csv(path, index=False)
    st.cache_data.clear()

# =========================================================
# Prefixos (pode editar conforme sua lógica)
# =========================================================
PREFIXOS = {
    "Hossomaki": 13,
    "Uramaki": 14,
    "Hot Roll": 15,
    "Porção": 21,
    "Burger": 31,
    "Risoto": 41,
    "Yakissoba": 51,
}

def proximo_codigo_interno(categoria: str) -> str:
    fichas = carregar_tabela(FICHAS_CSV)
    prefixo = PREFIXOS.get(categoria, 99)
    prefixo_str = str(prefixo)
    if not fichas.empty and "codigo_interno" in fichas.columns:
        same_cat = fichas[fichas["categoria"].astype(str) == str(categoria)]
        existentes = same_cat["codigo_interno"].dropna().astype(str).tolist()
        ultimos = []
        for c in existentes:
            if c.startswith(prefixo_str):
                try:
                    ultimos.append(int(c[len(prefixo_str):]))
                except Exception:
                    pass
        prox = (max(ultimos) + 1) if ultimos else 1
    else:
        prox = 1
    return f"{prefixo}{prox:02d}"

# =========================================================
# Estado inicial
# =========================================================
if "ingredientes" not in st.session_state:
    st.session_state["ingredientes"] = []

# Carregar insumos
insumos_df = carregar_tabela(COMPRAS_CSV)
insumos_opcoes = []
insumo_para_un = {}
if not insumos_df.empty:
    for _, row in insumos_df.iterrows():
        nome = str(row.get("insumo_resumo", "")).strip()
        un = str(row.get("un_med", "")).strip()
        if nome:
            insumos_opcoes.append(nome)
            insumo_para_un[nome] = un

# =========================================================
# UI — Cabeçalho
# =========================================================
st.markdown("<h1>Ficha Técnica — Parte da Cozinha</h1>", unsafe_allow_html=True)

with st.form("ficha_cozinha"):
    cab1, cab2 = st.columns(2)
    with cab1:
        nome_prato = st.text_input("Nome do prato", placeholder="Ex.: Uramaki Salmão Filadélfia")
        categoria = st.selectbox("Categoria / Grupo", options=["— selecione —"] + list(PREFIXOS.keys()), index=0)
        rendimento_total = st.number_input("Rendimento total (nº de porções)", min_value=0.0, value=0.0)
        peso_por_porcao = st.number_input("Peso médio por porção (g/ml)", min_value=0.0, value=0.0)
        responsavel = st.text_input("Responsável pela elaboração", placeholder="Nome do colaborador")
    with cab2:
        # Gera o código somente se a categoria for escolhida
        codigo_interno = ""
        if categoria != "— selecione —":
            codigo_interno = proximo_codigo_interno(categoria)
        codigo_interno = st.text_input("Código Interno (FT)", value=codigo_interno, placeholder="Gerado após escolher categoria")
        codigo_sistema = st.text_input("Código Sistema (opcional)")
        codigo_pdv = st.text_input("Código PDV (opcional)")
        st.caption(f"Atualização: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    st.divider()

    # =========================================================
    # Ingredientes
    # =========================================================
    st.markdown("### 🧾 Ingredientes (vinculados ao cadastro de insumos)")

    if not st.session_state["ingredientes"]:
        st.info("Nenhum ingrediente adicionado ainda.")
    else:
        for idx, item in enumerate(st.session_state["ingredientes"]):
            with st.expander(f"Ingrediente #{idx+1}", expanded=True):
                c1, c2, c3, c4 = st.columns([3, 1.2, 1.2, 2])
                with c1:
                    item["insumo"] = st.selectbox(
                        "Insumo",
                        options=["— selecione —"] + insumos_opcoes,
                        index=0 if not item.get("insumo") else insumos_opcoes.index(item.get("insumo")) + 1,
                        key=f"ins_{idx}"
                    )
                with c2:
                    item["quantidade"] = st.number_input("Quantidade", min_value=0.0, value=float(item.get("quantidade", 0.0)), step=0.01, key=f"qt_{idx}")
                with c3:
                    unidade_auto = insumo_para_un.get(item.get("insumo", ""), "")
                    st.text_input("Unidade", value=unidade_auto, disabled=True, key=f"un_{idx}")
                    item["unidade"] = unidade_auto
                with c4:
                    item["obs"] = st.text_input("Observação (opcional)", value=item.get("obs", ""), key=f"obs_{idx}")
                if st.button(f"🗑️ Remover ingrediente #{idx+1}", key=f"rm_{idx}"):
                    st.session_state["ingredientes"].pop(idx)
                    st.rerun()

    st.divider()
    if st.form_submit_button("💾 Salvar Ficha Técnica", use_container_width=True):
        if not nome_prato.strip():
            st.error("Informe o nome do prato.")
            st.stop()
        if categoria == "— selecione —":
            st.error("Selecione uma categoria válida.")
            st.stop()
        ingredientes_validos = [i for i in st.session_state["ingredientes"] if i.get("insumo") and float(i.get("quantidade", 0)) > 0]
        if not ingredientes_validos:
            st.error("Adicione ao menos um ingrediente com quantidade.")
            st.stop()

        fichas = carregar_tabela(FICHAS_CSV)
        novo = {
            "nome_prato": nome_prato.strip(),
            "codigo_interno": codigo_interno.strip(),
            "codigo_sistema": codigo_sistema.strip(),
            "codigo_pdv": codigo_pdv.strip(),
            "categoria": categoria,
            "rendimento_total": rendimento_total,
            "peso_por_porcao": peso_por_porcao,
            "responsavel": responsavel.strip(),
            "modo_preparo": "",
            "obs_tecnicas": "",
            "tempo_preparo": 0,
            "temperatura": "",
            "equipamentos": "",
            "armazenamento": "",
            "foto_path": "",
            "ingredientes_json": json.dumps(ingredientes_validos, ensure_ascii=False),
            "atualizado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        fichas = pd.concat([fichas, pd.DataFrame([novo])], ignore_index=True)
        salvar_tabela(fichas, FICHAS_CSV)
        st.success(f"Ficha técnica de **{novo['nome_prato']}** salva com sucesso! (FT {novo['codigo_interno']})")

# =========================================================
# Botão adicionar ingrediente (fora do form)
# =========================================================
if st.button("➕ Adicionar ingrediente", use_container_width=True):
    st.session_state["ingredientes"].append({"insumo": "", "quantidade": 0.0, "unidade": "", "obs": ""})
    st.rerun()

# =========================================================
# Rodapé
# =========================================================
versiculos = [
    ("E tudo quanto fizerdes, fazei-o de todo o coração, como ao Senhor.", "Colossenses 3:23"),
    ("O Senhor é meu pastor; nada me faltará.", "Salmo 23:1"),
    ("Confia no Senhor de todo o teu coração.", "Provérbios 3:5"),
    ("Tudo posso naquele que me fortalece.", "Filipenses 4:13"),
    ("Sede fortes e corajosos, o Senhor está convosco.", "Josué 1:9"),
]
v_texto, v_ref = random.choice(versiculos)
st.markdown(
    f"""
    <div id='fichapp-footer'>
      <div class='left'>🧩 FichApp v1.2.0 — última atualização: {datetime.now().strftime('%Y-%m-%d')}</div>
      <div class='right'><em>“{v_texto}”</em> — <strong>{v_ref}</strong></div>
    </div>
    """,
    unsafe_allow_html=True,
)
