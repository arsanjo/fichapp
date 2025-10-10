# 05_Ficha_Tecnica_Admin.py
# Código base para a Ficha Administrativa, formatado para execução via streamlit_app.py

import streamlit as st
from datetime import date
from utils.nav import sidebar_menu # Mantemos a importação para consistência

# =========================================================
# FUNÇÃO PRINCIPAL DE EXECUÇÃO DA PÁGINA
# =========================================================
def run_page():
    
    # Menu lateral fixo (O set_page_config deve ficar aqui)
    st.set_page_config(page_title="Ficha Técnica - Administrativa", layout="wide")

    # =========================================
    # CABEÇALHO
    # =========================================
    st.markdown("<h2 style='text-align:center;'>📊 FICHA TÉCNICA - ADMINISTRATIVA</h2>", unsafe_allow_html=True)
    st.markdown("---")

    st.warning("⚠️ **Atenção:** Este módulo calcula os custos indiretos (administrativos) do prato. Garanta que os **Parâmetros Financeiros** (custos fixos, taxas, etc.) estejam atualizados.")

    # =========================================
    # DETALHES DA FICHA (Placeholder)
    # =========================================
    st.subheader("📋 Custo Indireto por Prato")
    st.write("Aqui, o custo do prato (custo de insumos) será combinado com os percentuais administrativos definidos nos parâmetros.")

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Custo de Insumos (da Ficha Cozinha)", value="R$ XX,XX", delta="Exemplo")
    with col2:
        st.metric(label="Custo Total (com Admnistrativo)", value="R$ YY,YY", delta="Exemplo")

    st.markdown("---")

    # =========================================
    # VISUALIZAÇÃO DO RATEIO (Placeholder)
    # =========================================
    st.subheader("⚙️ Detalhamento do Rateio")
    st.info("💡 Futuramente, o sistema fará aqui o cálculo automático, multiplicando o custo do prato pelos percentuais de Lucro Desejado, Taxas de Cartão, Simples Nacional, etc.")

    # Tabela Simples de Rateio
    st.dataframe({
        'Parâmetro': ['Lucro Desejado', 'Taxa Cartão (Média)', 'Simples Nacional'],
        'Percentual': ['20.00%', '5.00%', '5.00%'],
        'Custo Rateado (Ex)': ['R$ 3.50', 'R$ 0.80', 'R$ 0.75']
    }, use_container_width=True)

    # =========================================
    # RODAPÉ
    # =========================================
    st.markdown("---")
    st.markdown(
        f"""
        <p style='text-align: center; font-size: 0.8rem; color: gray;'>
        FichApp • Módulo Administrativo • Desenvolvido por <b>Arsanjo</b>
        </p>
        """,
        unsafe_allow_html=True
    )

# FIM do arquivo 05_Ficha_Tecnica_Admin.py
