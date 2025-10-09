import streamlit as st

st.set_page_config(
    page_title="FichApp — Controle de Fichas Técnicas",
    page_icon="📘",
    layout="wide"
)

# 👇 muda o título do item lateral (que hoje aparece como "streamlit app")
st.sidebar.title("📋 Menu")

st.markdown("# 📘 FichApp")
st.write("Bem-vindo ao sistema de controle de fichas técnicas e insumos!")

st.info("🚀 O FichApp está em construção. Em breve você poderá cadastrar insumos, criar fichas técnicas e acompanhar custos em tempo real.")

st.markdown(
    """
    <div style='margin-top: 24px; padding: 16px 18px; border-radius: 12px; background: #0b1220; color: #e5e7eb; font-size: 0.92rem; text-align:center;'>
    <b>FichApp v0.1.0</b> — atualizado em 2025-10-09<br>
    Desenvolvido por Arsanjo
    </div>
    """,
    unsafe_allow_html=True
)
