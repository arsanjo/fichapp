# pages/04_Ficha_Tecnica.py
import streamlit as st
from utils.nav import sidebar_menu

# Página: Ficha Técnica
st.set_page_config(page_title="FichApp — Ficha Técnica", page_icon="🧾", layout="centered")

# Menu lateral fixo
sidebar_menu(ativo="ficha_tecnica")

# ====== Estilo (leve) ======
CSS = """
h1,h2,h3{ font-weight:700; }
.card{
  border:1px solid #e9eef5; border-radius:14px; padding:18px 18px; background:#fff; 
  box-shadow:0 1px 0 rgba(0,0,0,.02); margin-bottom:16px;
}
.badge{ 
  background:#0f172a; color:#fff; font-size:.80rem; border-radius:6px; padding:.2rem .45rem; 
}
.note{
  font-size:.92rem; color:#475569;
}
.grid{
  display:grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
@media (max-width: 900px){
  .grid{ grid-template-columns: 1fr; }
}
"""
st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

# ====== Cabeçalho ======
st.title("Ficha Técnica")
st.caption("Estrutura dividida em duas partes: **Cozinha** e **Administrativa (Cálculos)**.")

st.markdown(
    """
**Objetivo:** a ficha técnica será separada para atender públicos diferentes:

- **Parte da Cozinha:** preparo, rendimento, utensílios, modo de fazer, fotos e observações técnicas.  
- **Parte Administrativa:** custos, percentuais, impostos, margem, preço sugerido, etc.

Na hora de **imprimir** ou **exportar para PDF**, o sistema permitirá escolher:
- **Ficha Completa**
- **Somente Cozinha**
- **Somente Administrativa**
"""
)

# ====== Cartões explicativos ======
st.markdown("### O que vai em cada parte")
st.markdown("<div class='grid'>", unsafe_allow_html=True)

with st.container():
    st.markdown(
        """
        <div class='card'>
          <h3>🍳 Parte da Cozinha <span class='badge'>produção</span></h3>
          <ul>
            <li>Nome da receita e categoria</li>
            <li>Rendimento e porcionamento</li>
            <li>Lista de insumos (com unidades e quantidades)</li>
            <li>Equipamentos/utensílios utilizados</li>
            <li>Passo a passo do preparo</li>
            <li>Tempo de preparo e tempo total</li>
            <li>Observações técnicas (armazenagem, cocção, etc.)</li>
            <li>Fotos (opcional)</li>
          </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

with st.container():
    st.markdown(
        """
        <div class='card'>
          <h3>📈 Parte Administrativa <span class='badge'>cálculos</span></h3>
          <ul>
            <li>Custo por insumo e custo total</li>
            <li>Perdas, frete, taxas, impostos</li>
            <li>Margem, markup e preço sugerido</li>
            <li>Indicadores (contribuição, CMV, etc.)</li>
            <li>Parâmetros financeiros vinculados (comissão, taxas, etc.)</li>
          </ul>
          <p class='note'>
            <strong>Observação:</strong> Esta seção é sensível e não será exibida para a equipe da cozinha.
          </p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)

st.info(
    "🧪 **Status:** protótipo funcional da página. Na próxima etapa, "
    "vamos criar os formulários, persistência e a exportação seletiva (completa / cozinha / administrativa)."
)
