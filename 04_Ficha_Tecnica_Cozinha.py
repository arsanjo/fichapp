# 04_Ficha_Tecnica_Cozinha.py
# Código completo e formatado para ser executado via streamlit_app.py

import streamlit as st
from datetime import date
from utils.nav import sidebar_menu

# =========================================================
# FUNÇÃO PRINCIPAL DE EXECUÇÃO DA PÁGINA
# =========================================================
def run_page():
    
    # Menu lateral fixo (O set_page_config deve ficar aqui)
    st.set_page_config(page_title="Ficha Técnica - Cozinha", layout="wide")

    # =========================================
    # CABEÇALHO
    # =========================================
    st.markdown("<h2 style='text-align:center;'>📘 FICHA TÉCNICA - COZINHA</h2>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        referencia = st.text_input("Referência", value="")
        derivacao = st.text_input("Derivação", value="")
    with col2:
        produto = st.text_input("Produto", value="")
        eng_cardapio = st.text_input("Engenharia de Cardápio", value="")
    with col3:
        cod_sistema = st.text_input("Código Sistema", value="")
        rendimento = st.text_input("Rendimento (ex: 8 peças)", value="")

    st.text_area("Descrição do Produto", placeholder="Descreva brevemente o produto e seu preparo...")

    # Upload da foto do produto
    foto = st.file_uploader("📸 Foto do Produto", type=["jpg", "png", "jpeg"])
    if foto:
        st.image(foto, use_container_width=True)

    st.markdown("---")

    # =========================================
    # MODO DE PREPARO
    # =========================================
    st.subheader("🧑‍🍳 Modo de Preparo")
    modo_preparo = st.text_area(
        "Descreva detalhadamente o modo de preparo:",
        height=200,
        placeholder="Ex: Colocar o arroz na alga; espalhar o cream cheese; adicionar o salmão..."
    )

    video = st.text_input("🎥 Link de vídeo explicativo (opcional)", placeholder="Cole aqui o link do vídeo")

    st.markdown("---")

    # =========================================
    # DETALHAMENTO DO PREPARO
    # =========================================
    st.subheader("📋 Detalhamento do Preparo")

    with st.expander("Adicionar Ingredientes"):
        st.markdown("Preencha os campos abaixo para cada item utilizado no preparo:")

        col1, col2, col3, col4, col5 = st.columns([1.5, 2.5, 1, 1, 2])
        col1.text_input("Etapa", placeholder="Ex: Preparo")
        col2.text_input("Produto", placeholder="Ex: Arroz japonês")
        col3.text_input("Unidade", placeholder="Kg / Un / Pc")
        col4.number_input("Qtd.", min_value=0.0, step=0.001, format="%.3f")
        col5.text_input("Observação", placeholder="Opcional")

    st.info("💡 Em versões futuras, esta tabela será preenchida automaticamente a partir dos insumos cadastrados.")

    st.markdown("---")

    # =========================================
    # OBSERVAÇÕES
    # =========================================
    st.subheader("🗒️ Observações Gerais")
    st.text_area("Anotações, dicas ou cuidados importantes", height=120)

    st.markdown("---")

    # =========================================
    # RODAPÉ
    # =========================================
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("**Revisado por:** Arsanjo Paul Colaço")
    with col2:
        st.write(f"**Data:** {date.today().strftime('%d/%m/%Y')}")

    st.markdown(
        "<p style='font-size: 0.8rem; color: red;'>Siga sempre a Ficha Técnica para a padronização dos preparos.</p>",
        unsafe_allow_html=True
    )

# FIM do arquivo 04_Ficha_Tecnica_Cozinha.py
