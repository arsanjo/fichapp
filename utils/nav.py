import streamlit as st

# =========================================================
# MENU LATERAL — versão otimizada com cache
# =========================================================
@st.cache_resource
def sidebar_menu(ativo: str = None):
    """
    Renderiza o menu lateral fixo do FichApp com cache.
    O parâmetro 'ativo' serve para destacar a página atual.
    """

    # Define estilo personalizado do menu
    st.markdown("""
        <style>
            /* Remove barra superior automática do Streamlit */
            header {visibility: hidden;}
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}

            /* Estilo do menu lateral */
            section[data-testid="stSidebar"] {
                background-color: #f7f8fa;
                border-right: 1px solid #e0e0e0;
            }

            .menu-item {
                padding: 0.5rem 0.75rem;
                border-radius: 8px;
                display: flex;
                align-items: center;
                font-size: 0.95rem;
                font-weight: 500;
                margin-bottom: 0.3rem;
                color: #333;
                text-decoration: none;
            }
            .menu-item:hover {
                background-color: #e8f0fe;
                color: #0b57d0;
            }
            .menu-item.active {
                background-color: #0b57d0;
                color: white !important;
                font-weight: 600;
            }

            .menu-icon {
                margin-right: 8px;
                font-size: 1.1rem;
            }

            .menu-footer {
                margin-top: 1rem;
                font-size: 0.75rem;
                color: #999;
                text-align: center;
            }
        </style>
    """, unsafe_allow_html=True)

    # =========================================================
    # CONTEÚDO DO MENU
    # =========================================================
    with st.sidebar:
        st.markdown("### 📘 FichApp")
        st.markdown("Menu principal")
        st.write("")

        # Itens do menu
        menu_itens = {
            "home": {"nome": "Início", "icone": "🏠", "link": "Home"},
            "insumos": {"nome": "Cadastro de Insumos", "icone": "📦", "link": "Cadastro_de_Insumos"},
            "financeiros": {"nome": "Parâmetros Financeiros", "icone": "💰", "link": "Parametros_Financeiros"},
            "engenharia": {"nome": "Engenharia do Cardápio", "icone": "📊", "link": "Engenharia_do_Cardapio"},
            "ficha_tecnica_cozinha": {"nome": "Ficha Técnica (Cozinha)", "icone": "👨‍🍳", "link": "Ficha_Tecnica_Cozinha"},
            "ficha_tecnica_admin": {"nome": "Ficha Técnica (Administrativa)", "icone": "📈", "link": "Ficha_Tecnica_Administrativa"},
        }

        # Renderização dos links com destaque dinâmico
        for chave, item in menu_itens.items():
            classe = "menu-item"
            if ativo == chave:
                classe += " active"

            st.markdown(
                f"<a href='/{item['link']}' target='_self' class='{classe}'>"
                f"<span class='menu-icon'>{item['icone']}</span>{item['nome']}</a>",
                unsafe_allow_html=True
            )

        # Rodapé do menu
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div class='menu-footer'>FichApp v1.0.0</div>", unsafe_allow_html=True)
