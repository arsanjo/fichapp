import streamlit as st

# ======================================================
# MENU LATERAL PRINCIPAL — FichApp
# ======================================================

def sidebar_menu(ativo="inicio"):
    st.sidebar.markdown("<h3 style='margin-bottom: 0;'>📘 FichApp</h3>", unsafe_allow_html=True)
    st.sidebar.markdown("<small>Menu principal</small>", unsafe_allow_html=True)
    st.sidebar.markdown("---")

    # Lista de itens do menu (sem emojis nos links)
    menu_itens = {
        "inicio": {"icon": "🏠", "label": "Início", "link": "/Inicio"},
        "insumos": {"icon": "📦", "label": "Cadastro de Insumos", "link": "/Cadastro_de_Insumos"},
        "parametros": {"icon": "💰", "label": "Parâmetros Financeiros", "link": "/Parametros_Financeiros"},
        "engenharia": {"icon": "📊", "label": "Engenharia do Cardápio", "link": "/Engenharia_do_Cardapio"},
        "ficha_tecnica": {"icon": "🧾", "label": "Ficha Técnica", "link": "/Ficha_Tecnica"},
    }

    # Renderização do menu
    for chave, item in menu_itens.items():
        estilo = (
            "background-color:#0f172a; color:white; border-radius:8px; padding:6px 12px;"
            if chave == ativo
            else "padding:6px 12px; color:#333;"
        )
        st.sidebar.markdown(
            f"""
            <a href="{item['link']}" target="_self" style="text-decoration:none;">
                <div style="{estilo}">{item['icon']} {item['label']}</div>
            </a>
            """,
            unsafe_allow_html=True,
        )

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "<p style='text-align:center; font-size:0.8rem; opacity:.7;'>FichApp v1.0.0</p>",
        unsafe_allow_html=True,
    )
