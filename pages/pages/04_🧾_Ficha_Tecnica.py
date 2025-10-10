import streamlit as st
from utils.nav import sidebar_menu
from datetime import date

# ======================================================
# MENU LATERAL
# ======================================================
sidebar_menu(ativo="ficha_tecnica")

# ======================================================
# CONFIGURAÇÕES DA PÁGINA
# ======================================================
st.set_page_config(page_title="FichApp — Ficha Técnica", page_icon="🧾", layout="wide")

# ======================================================
# CABEÇALHO
# ======================================================
st.markdown("<h1 style='text-align:center;'>🧾 Ficha Técnica</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; opacity:.8;'>Dividida em duas partes: Cozinha e Administrativa</p>", unsafe_allow_html=True)
st.divider()

# ======================================================
# SELEÇÃO DE VISUALIZAÇÃO
# ======================================================
visualizacao = st.radio(
    "Escolha qual versão deseja visualizar:",
    ["🍳 Parte da Cozinha", "💼 Parte Administrativa", "📘 Ficha Completa"],
    horizontal=True
)
st.divider()

# ======================================================
# PARTE 1 - COZINHA
# ======================================================
if visualizacao in ["🍳 Parte da Cozinha", "📘 Ficha Completa"]:
    st.subheader("🍳 Parte da Cozinha — Informações Operacionais")

    col1, col2, col3 = st.columns(3)
    with col1:
        referencia = st.text_input("Código / Referência", placeholder="Ex: PRD-001")
    with col2:
        nome_produto = st.text_input("Nome do Produto", placeholder="Ex: Yakissoba Tradicional")
    with col3:
        rendimento = st.text_input("Rendimento", placeholder="Ex: 3 porções")

    st.text_area("Descrição resumida do prato", placeholder="Breve descrição do produto ou preparo...")

    colA, colB = st.columns(2)
    with colA:
        data_revisao = st.date_input("Data da revisão", value=date.today())
    with colB:
        revisado_por = st.text_input("Revisado por", placeholder="Ex: Chef Marnie")

    st.file_uploader("📸 Foto ilustrativa do produto (opcional)", type=["png", "jpg", "jpeg"])

    st.markdown("### Ingredientes e etapas de preparo")
    st.caption("Adicione os ingredientes conforme cada etapa da receita.")

    st.dataframe(
        {
            "Etapa": ["Preparo", "Acompanhamento", "Embalagem"],
            "Produto": ["Arroz Cozido", "Molho Shoyu", "Caixa Yakissoba"],
            "UM": ["KG", "L", "UN"],
            "Qtde": [0.300, 0.050, 1],
            "%": [60, 10, 30],
            "Observação": ["Arroz cozido base", "Molho pronto", "Embalagem plástica"]
        },
        use_container_width=True
    )

    st.text_area("Modo de Preparo", placeholder="Descreva o passo a passo da preparação...")
    st.text_area("Observações Gerais", placeholder="Notas adicionais sobre preparo, montagem ou armazenamento...")

    st.divider()

# ======================================================
# PARTE 2 - ADMINISTRATIVA
# ======================================================
if visualizacao in ["💼 Parte Administrativa", "📘 Ficha Completa"]:
    st.subheader("💼 Parte Administrativa — Análise Financeira")

    st.caption("Esta seção é restrita à área administrativa e contém cálculos de custo e margem de lucro.")

    col1, col2, col3 = st.columns(3)
    with col1:
        custo_total = st.number_input("Custo total dos insumos (R$)", min_value=0.0, step=0.01)
    with col2:
        margem_contribuicao = st.number_input("Margem de contribuição (%)", min_value=0.0, max_value=100.0, step=0.1)
    with col3:
        lucro_desejado = st.number_input("Lucro desejado (%)", min_value=0.0, max_value=100.0, step=0.1)

    st.markdown("### Despesas e percentuais adicionais")
    colA, colB, colC, colD = st.columns(4)
    with colA:
        taxa_cartao = st.number_input("Taxa cartão (%)", min_value=0.0, max_value=100.0, step=0.1)
        cashback = st.number_input("Cashback Menudino (%)", min_value=0.0, max_value=100.0, step=0.1)
    with colB:
        comissao_app = st.number_input("Comissão APP (%)", min_value=0.0, max_value=100.0, step=0.1)
        comissao_atendente = st.number_input("Comissão Atendente (%)", min_value=0.0, max_value=100.0, step=0.1)
    with colC:
        simples = st.number_input("Simples (%)", min_value=0.0, max_value=100.0, step=0.1)
        outros1 = st.number_input("Outros 1 (%)", min_value=0.0, max_value=100.0, step=0.1)
    with colD:
        outros2 = st.number_input("Outros 2 (%)", min_value=0.0, max_value=100.0, step=0.1)

    st.divider()

    st.markdown("### Exportar / Imprimir")
    st.caption("Escolha a versão da ficha técnica para exportar ou imprimir.")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("📘 Gerar PDF Completo")
    with col2:
        st.button("🍳 Imprimir versão Cozinha")
    with col3:
        st.button("💼 Imprimir versão Administrativa")

    st.divider()

# ======================================================
# RODAPÉ
# ======================================================
st.markdown(
    """
    <div style='text-align:center; font-size:0.9rem; opacity:.7; margin-top:30px;'>
        <em>“E tudo quanto fizerdes, fazei-o de todo o coração, como ao Senhor.” — Colossenses 3:23</em><br>
        © 2025 FichApp — Todos os direitos reservados.
    </div>
    """,
    unsafe_allow_html=True
)
