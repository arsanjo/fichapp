import streamlit as st
import pandas as pd
import json, os, random
from datetime import datetime, date

# =========================================================
# Navegação (mantém padrão visual do FichAPP)
# =========================================================
try:
    from utils.nav import sidebar_menu
    sidebar_menu(ativo="ficha_tecnica")
except Exception:
    pass

# =========================================================
# CONFIG / THEME
# =========================================================
st.set_page_config(page_title="FichApp — Ficha Técnica (Cozinha)", page_icon="🍣", layout="centered")

DARK_CSS = """
<style>
.block-container { padding-top: 2rem; padding-bottom: 2rem; }
h1, h2, h3, h4 { font-weight: 700; }
.st-expander { border: 1px solid #e5e7eb; border-radius: 10px; }
.stButton>button, .stForm form button[kind="primary"]{ background: #0f172a; color: #fff; border: 0; border-radius: 10px; padding: .6rem 1rem; }
.stButton>button:hover, .stForm form button[kind="primary"]{ background: #1e293b; }
#fichapp-footer { margin-top: 24px; padding: 16px 18px; border-radius: 12px; background: #0b1220; color: #e5e7eb; font-size: 0.92rem; display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; }
#fichapp-footer .left { font-weight: 600; }
#fichapp-footer .right { opacity: .85; }
.badge { display:inline-block; padding:.12rem .5rem; border-radius:999px; border:1px solid #334155; font-size:.75rem; color:#e2e8f0; }
.small { font-size: .85rem; color: #94a3b8; }
.table-like { width: 100%; border-collapse: collapse; }
.table-like th, .table-like td { border-bottom: 1px dashed #334155; padding: .35rem .25rem; font-size: .92rem; }
.table-like th { text-align: left; color: #93c5fd; }
.code-hint { background: #0b1220; border:1px solid #1f2937; padding:.5rem .75rem; border-radius: .5rem; }
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

COMPRAS_CSV = os.path.join(DATA_DIR, "compras_insumos.csv")      # já existente (Cadastro de Insumos)
FICHAS_CSV  = os.path.join(DATA_DIR, "fichas_tecnicas.csv")      # NOVO repositório das fichas

# =========================================================
# Inicialização dos arquivos
# =========================================================
if (not os.path.exists(FICHAS_CSV)) or os.stat(FICHAS_CSV).st_size == 0:
    cols = [
        "nome_prato","codigo_interno","codigo_sistema","codigo_pdv","categoria",
        "rendimento_total","peso_por_porcao","responsavel","modo_preparo","obs_tecnicas",
        "tempo_preparo","temperatura","equipamentos","armazenamento","foto_path",
        "ingredientes_json","atualizado_em"
    ]
    pd.DataFrame(columns=cols).to_csv(FICHAS_CSV, index=False)

# =========================================================
# Helpers
# =========================================================
@st.cache_data
def carregar_tabela(path: str) -> pd.DataFrame:
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


def salvar_tabela(df: pd.DataFrame, path: str):
    df.to_csv(path, index=False)
    st.cache_data.clear()


# Prefixos por categoria – ajustável conforme a organização interna (exemplo inicial)
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
    """Gera código sequencial por categoria, mantendo padrão PREFIXO + 2 dígitos.
    Se não houver prefixo definido, usa 99.
    """
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
# Estado da UI
# =========================================================
def _ensure_state():
    defaults = {
        "ingredientes": [  # lista de linhas: {insumo, quantidade, unidade, obs}
            {"insumo": "", "quantidade": 0.0, "unidade": "", "obs": ""},
        ],
        "categoria_sel": "Uramaki",
        "codigo_interno_lock": True,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_ensure_state()

# Dados de insumos (para popular selectbox)
insumos_df = carregar_tabela(COMPRAS_CSV)

# Mapas auxiliares
insumos_opcoes = []
insumo_para_un = {}
if not insumos_df.empty:
    # usamos a coluna "insumo_resumo" para exibir, e pegamos unidade de "un_med"
    for _, row in insumos_df.iterrows():
        nome = str(row.get("insumo_resumo", "")).strip()
        un = str(row.get("un_med", "")).strip()
        if nome:
            insumos_opcoes.append(nome)
            if nome not in insumo_para_un:
                insumo_para_un[nome] = un

# =========================================================
# Cabeçalho
# =========================================================
st.markdown("<h1>Ficha Técnica — Parte da Cozinha</h1>", unsafe_allow_html=True)

with st.form("ficha_cozinha"):
    cab1, cab2 = st.columns(2)

    with cab1:
        nome_prato = st.text_input("Nome do prato", placeholder="Ex.: Uramaki Salmão Filadélfia")
        categoria = st.selectbox("Categoria / Grupo", options=list(PREFIXOS.keys()) + ["Outros"], index=1)
        rendimento_total = st.number_input("Rendimento total (nº de porções)", min_value=0.0, value=0.0, step=0.5)
        peso_por_porcao = st.number_input("Peso médio por porção (g/ml) — opcional", min_value=0.0, value=0.0, step=1.0)
        responsavel = st.text_input("Responsável pela elaboração", placeholder="Nome de quem criou / revisou")

    with cab2:
        # Código Interno (FT) — sugerido automaticamente por categoria, mas editável
        if st.session_state.get("categoria_sel") != categoria:
            st.session_state["categoria_sel"] = categoria
        sugestao_codigo = proximo_codigo_interno(categoria)
        codigo_interno = st.text_input("Código Interno (FT)", value=sugestao_codigo, help="Gerado automaticamente por categoria; pode ajustar manualmente.")

        codigo_sistema = st.text_input("Código Sistema (opcional)")
        codigo_pdv = st.text_input("Código PDV (opcional)")
        atualizado_em = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.caption(f"Atualização: {atualizado_em}")

    st.divider()

    # =========================================================
    # Ingredientes – lista dinâmica
    # =========================================================
    st.markdown("### 🧾 Ingredientes (vinculados ao cadastro de insumos)")

    # Tabela de entrada
    for idx, item in enumerate(st.session_state["ingredientes"]):
        with st.expander(f"Ingrediente #{idx+1}", expanded=True if idx < 2 else False):
            c1, c2, c3, c4 = st.columns([3, 1.2, 1.2, 2])
            with c1:
                escolha = st.selectbox(
                    "Insumo", options=["— selecione —"] + insumos_opcoes, index=0 if not item.get("insumo") else (["— selecione —"] + insumos_opcoes).index(item.get("insumo")), key=f"ins_{idx}")
                item["insumo"] = escolha if escolha != "— selecione —" else ""
            with c2:
                item["quantidade"] = st.number_input("Quantidade", min_value=0.0, value=float(item.get("quantidade", 0.0)), step=0.01, key=f"qt_{idx}")
            with c3:
                unidade_auto = insumo_para_un.get(item.get("insumo", ""), "")
                item["unidade"] = unidade_auto
                st.text_input("Unidade", value=unidade_auto, disabled=True, key=f"un_{idx}")
            with c4:
                item["obs"] = st.text_input("Observação (opcional)", value=item.get("obs", ""), key=f"obs_{idx}")

            # Remover ingrediente
            rem_col1, rem_col2 = st.columns([1, 5])
            with rem_col1:
                if st.button("🗑️ Remover", key=f"rm_{idx}"):
                    st.session_state["ingredientes"].pop(idx)
                    st.rerun()

    # Adicionar ingrediente
    if st.button("➕ Adicionar ingrediente"):
        st.session_state["ingredientes"].append({"insumo": "", "quantidade": 0.0, "unidade": "", "obs": ""})
        st.rerun()

    st.divider()

    # =========================================================
    # Modo de preparo
    # =========================================================
    st.markdown("### 🍳 Modo de Preparo")
    st.markdown("<span class='small'>Dica: descreva por etapas (preparo, montagem, finalização).</span>", unsafe_allow_html=True)
    modo_preparo = st.text_area("Instruções", height=180, placeholder="1) ...\n2) ...\n3) ...")

    st.divider()

    # =========================================================
    # Observações técnicas
    # =========================================================
    st.markdown("### 🧪 Observações Técnicas")
    cobs1, cobs2 = st.columns(2)
    with cobs1:
        tempo_preparo = st.number_input("Tempo total de preparo (min)", min_value=0.0, value=0.0, step=5.0)
        equipamentos = st.text_input("Equipamentos / Utensílios", placeholder="Ex.: faca, tábua, chapa, forno")
    with cobs2:
        temperatura = st.text_input("Temperatura (cocção/serviço)", placeholder="Ex.: 180°C / 4°C")
        armazenamento = st.text_input("Armazenamento / Validade", placeholder="Ex.: resfriado por 24h")

    obs_tecnicas = st.text_area("Pontos de atenção (opcional)", height=100, placeholder="Ex.: não ferver o molho; finalizar na hora; conservar resfriado...")

    st.divider()

    # =========================================================
    # Ações
    # =========================================================
    left, right = st.columns([1, 1])
    salvar = left.form_submit_button("💾 Salvar Ficha Técnica", use_container_width=True)
    imprimir = right.form_submit_button("🖨️ Gerar PDF (versão cozinha)", use_container_width=True)

    if salvar:
        # validação mínima
        if not nome_prato.strip():
            st.error("Informe o nome do prato.")
            st.stop()
        if not categoria:
            st.error("Selecione a categoria.")
            st.stop()
        if not codigo_interno.strip():
            st.error("Código interno (FT) é obrigatório.")
            st.stop()

        # filtra ingredientes válidos
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
            "modo_preparo": modo_preparo,
            "obs_tecnicas": obs_tecnicas,
            "tempo_preparo": tempo_preparo,
            "temperatura": temperatura,
            "equipamentos": equipamentos,
            "armazenamento": armazenamento,
            "foto_path": "",
            "ingredientes_json": json.dumps(ingredientes_validos, ensure_ascii=False),
            "atualizado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        fichas = pd.concat([fichas, pd.DataFrame([novo])], ignore_index=True)
        salvar_tabela(fichas, FICHAS_CSV)
        st.success(f"Ficha técnica de **{novo['nome_prato']}** salva com sucesso! (FT {novo['codigo_interno']})")

    if imprimir:
        st.info("Em breve: exportação/print limpo apenas com a versão de cozinha (sem custos).")

# =========================================================
# Rodapé com versão + versículo (padrão FichAPP)
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
    ("Entrega o teu caminho ao Senhor; confia nele, e ele o fará.", "Salmo 37:5"),
]
v_texto, v_ref = random.choice(versiculos)
st.markdown(
    f"""
    <div id='fichapp-footer'>
      <div class='left'>🧩 FichApp v{versao_info.get('version','0.0.0')} — última atualização: {versao_info.get('released_at','')}</div>
      <div class='right'><em>“{v_texto}”</em> — <strong>{v_ref}</strong></div>
    </div>
    """,
    unsafe_allow_html=True,
)
