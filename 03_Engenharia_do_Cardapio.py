# 03_Engenharia_do_Cardapio.py
# Código completo e formatado para ser executado via streamlit_app.py

import streamlit as st
from utils.nav import sidebar_menu # Mantemos a importação para consistência

# =========================================================
# FUNÇÃO PRINCIPAL DE EXECUÇÃO DA PÁGINA
# =========================================================
def run_page():
    
    # ==============================
    # CONFIGURAÇÃO GERAL DA PÁGINA
    # ==============================
    st.set_page_config(
        page_title="FichApp – Engenharia do Cardápio",
        page_icon="📊",
        layout="wide"
    )

    # ==============================
    # CONTEÚDO PRINCIPAL
    # ==============================

    st.title("📊 Engenharia do Cardápio")
    st.markdown("### Estratégia para equilibrar **lucro e popularidade** dos produtos.")

    st.markdown(
        """
    A **Engenharia do Cardápio** é uma ferramenta de gestão estratégica que analisa o desempenho de cada item do cardápio com base em dois fatores principais:
    - **Popularidade** (quantidade vendida)  
    - **Lucratividade** (margem de contribuição)

    O objetivo é ajudar o gestor a tomar **decisões inteligentes** sobre quais produtos devem ser **mantidos, ajustados, promovidos ou removidos**, garantindo um cardápio rentável e atrativo.
        """
    )

    st.divider()

    # ==============================
    # TABELA DE CATEGORIAS
    # ==============================

    st.subheader("📘 Classificação e Estratégias")

    st.markdown(
        """
    | 🏷️ **Categoria** | 📊 **Análise** | 🎯 **Ação Recomendada** |
    |:-----------------|:--------------|:------------------------|
    | 🐶 **Cão** | Itens que raramente são pedidos e têm pouco retorno financeiro. | Avaliar **remoção** ou **reformulação** desses itens. Se ocupam espaço que poderia ser usado para produtos mais rentáveis, considere substituí-los. Caso sejam ingredientes de outros pratos, reavalie sua **realocação**. |
    | 🌟 **Estrela** | Itens que são tanto populares quanto lucrativos. | **Manter e promover** esses itens. Garanta a qualidade e consistência. Destaque-os em materiais de marketing e no cardápio físico/digital. São os pratos que mais **atraem e fidelizam** clientes. |
    | 🧩 **Desafio** | Itens com boa margem de lucro, mas pouca saída. | Investir em **marketing e apresentação**. Revise nome, descrição e fotos. Ofereça degustações, descontos ou combos para aumentar a popularidade. Treine a equipe para sugerir esses pratos. |
    | 🐴 **Burro de Carga** | Itens populares, mas com baixa margem de lucro. | Buscar **melhorar a rentabilidade**: ajustar preços, otimizar preparo ou reduzir custos sem afetar qualidade. Combine com itens de maior margem (ex: bebidas ou acompanhamentos). |
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # ==============================
    # MENSAGEM FINAL
    # ==============================
    st.info(
        """
    💡 *Em breve este módulo permitirá importar dados de vendas do seu sistema (como o Consumer ou outro controle),
    realizando automaticamente os cálculos de popularidade e margem de contribuição de cada item.*
        """
    )

    # Rodapé
    st.markdown(
        """
    <div style='text-align: center; margin-top: 40px; font-size: 0.9em; color: gray;'>
    <b>FichApp</b> v1.0.0 — atualizado em 2025-10-10<br>
    Desenvolvido por <b>Arsanjo</b>
    </div>
    """,
        unsafe_allow_html=True
    )
