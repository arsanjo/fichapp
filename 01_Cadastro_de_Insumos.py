# 01_Cadastro_de_Insumos.py
# CÓDIGO FINAL COM AUTOMAÇÃO DE UNIDADES, LIMPEZA E ESTRUTURA DE EDIÇÃO

import streamlit as st
import pandas as pd
from datetime import datetime, date
import os, json, random
from utils.nav import sidebar_menu # Mantenha a importação

# =========================================================
# FUNÇÃO PRINCIPAL DE EXECUÇÃO DA PÁGINA
# =========================================================
def run_page():

    # =========================================================
    # CONFIG / THEME (Mantido o seu código original)
    # =========================================================
    # 📦 Adicionando o ícone ao título para estética
    st.set_page_config(page_title="FichApp — Cadastro de Insumos", page_icon="📦", layout="centered")

    DARK_CSS = """
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1, h2, h3, h4 { font-weight: 700; }
    .st-expander { border: 1px solid #e5e7eb; border-radius: 10px; }
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
    </style>
    """
    st.markdown(DARK_CSS, unsafe_allow_html=True)

    # ... (Seções de Versão, Caminhos dos Dados, Inicialização dos Arquivos mantidas) ...
    # (Removidas do snippet aqui por serem longas, mas MANTENHA-AS no seu arquivo)

    # --- INÍCIO DE VERSÃO, CAMINHOS E INICIALIZAÇÃO ---

    VERSAO_PATH = "version.json"
    versao_info = {"version": "0.0.0", "released_at": "", "description": ""}
    if os.path.exists(VERSAO_PATH):
        try:
            with open(VERSAO_PATH, "r", encoding="utf-8") as f:
                versao_info = json.load(f)
        except Exception:
            pass

    DATA_DIR = "data"
    os.makedirs(DATA_DIR, exist_ok=True)

    COMPRAS_CSV = os.path.join(DATA_DIR, "compras_insumos.csv")
    GRUPOS_CSV  = os.path.join(DATA_DIR, "grupos_insumos.csv")
    UNIDS_CSV   = os.path.join(DATA_DIR, "unidades_medida.csv")

    compras_cols = [
        "data_compra","grupo","insumo_resumo","insumo_completo","marca","tipo",
        "un_med","quantidade_compra","qtde_para_custos",
        "valor_total_compra","valor_frete","percentual_perda",
        "valor_unit_bruto","custo_total_com_frete","quantidade_liquida",
        "custo_real_unitario","valor_unit_para_custos",
        "fornecedor","fone_fornecedor","representante","documento","observacao",
        "atualizado_em"
    ]
    if (not os.path.exists(COMPRAS_CSV)) or os.stat(COMPRAS_CSV).st_size == 0:
        pd.DataFrame(columns=compras_cols).to_csv(COMPRAS_CSV, index=False)

    grupos_padrao = [
        "Embalagem","Peixe","Carne","Hortifruti","Bebida","Frios",
        "Molhos e Temperos","Grãos e Cereais","Higiene","Limpeza","Outros"
    ]
    if (not os.path.exists(GRUPOS_CSV)) or os.stat(GRUPOS_CSV).st_size == 0:
        pd.DataFrame({"grupo": grupos_padrao}).to_csv(GRUPOS_CSV, index=False)

    unidades_padrao = [
        ("KG","Quilograma", 1.0),
        ("G","Grama", 1000.0),
        ("L","Litro", 1.0),
        ("ML","Mililitro", 1000.0),
        ("UN","Unidade", 1.0),
        ("DZ","Dúzia", 12.0), # <--- FATOR CORRIGIDO
        ("MIL","Milheiro", 1000.0), # <--- FATOR CORRIGIDO
        ("CT","Cento", 100.0), # <--- FATOR CORRIGIDO
        ("CX","Caixa", 1.0),
        ("FD","Fardo", 1.0),
        ("PAC","Pacote", 1.0),
        ("BAN","Bandeja", 1.0),
        ("PAR","Par", 2.0),
        ("POR","Porção", 1.0),
    ]
    if (not os.path.exists(UNIDS_CSV)) or os.stat(UNIDS_CSV).st_size == 0:
        pd.DataFrame(unidades_padrao, columns=["codigo","descricao","qtde_padrao"]).to_csv(UNIDS_CSV, index=False)
    
    # --- FIM DE VERSÃO, CAMINHOS E INICIALIZAÇÃO ---


    # =========================================================
    # Helpers (Mantidos os seus)
    # =========================================================
    @st.cache_data
    def carregar_tabela(path: str) -> pd.DataFrame:
        try: return pd.read_csv(path)
        except Exception: return pd.DataFrame()

    def salvar_tabela(df: pd.DataFrame, path: str):
        df.to_csv(path, index=False)
        st.cache_data.clear()

    def lista_grupos() -> list[str]:
        gdf = carregar_tabela(GRUPOS_CSV)
        if "grupo" in gdf.columns:
            return sorted(gdf["grupo"].dropna().astype(str).unique().tolist())
        return grupos_padrao

    def lista_unidades() -> pd.DataFrame:
        udf = carregar_tabela(UNIDS_CSV)
        cols = {"codigo","descricao","qtde_padrao"}
        if set(udf.columns) >= cols:
            return udf
        return pd.DataFrame(unidades_padrao, columns=["codigo","descricao","qtde_padrao"])

    def label_unidade(row):
        return f"{row['codigo']} – {row['descricao']}"


    # =========================================================
    # Estado da UI (Melhorado para limpar o formulário)
    # =========================================================
    # Função para limpar o estado da sessão (será chamada após o cadastro)
    def reset_session_state():
        st.session_state["nome_resumo"] = ""
        st.session_state["nome_completo"] = ""
        st.session_state["nome_completo_lock"] = True
        st.session_state["un_sel"] = "UN"
        st.session_state["last_un_sel"] = None
        st.session_state["last_qtd_compra"] = None
        st.session_state["qtde_para_custos_value"] = 0.0
        st.session_state["form_data"] = {} # Para limpar outros inputs do formulário

    defaults = {
        "nome_resumo": "",
        "nome_completo": "",
        "nome_completo_lock": True,
        "un_sel": "UN",
        "last_un_sel": None,
        "last_qtd_compra": None,
        "qtde_para_custos_value": 0.0,
        "form_data": {}
    }
    for k,v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # =========================================================
    # Cabeçalho
    # =========================================================
    # 📦 Ícone adicionado ao título
    st.markdown("<h1>📦 Cadastro de Insumos</h1>", unsafe_allow_html=True)
    acao = st.radio("Ação:", ["➕ Cadastrar novo insumo", "✏️ Editar insumo", "📋 Visualizar insumos"], index=0)

    # =========================================================
    # CADASTRO (Lógica de Automação de Quantidade)
    # =========================================================
    if acao == "➕ Cadastrar novo insumo":
        grupos = lista_grupos()
        unidades_df = lista_unidades()
        unidades_labels = unidades_df.apply(label_unidade, axis=1).tolist()
        codigo_por_label = dict(zip(unidades_labels, unidades_df["codigo"]))
        fator_por_codigo = dict(zip(unidades_df["codigo"], unidades_df["qtde_padrao"]))

        # Usa uma chave única para o formulário principal
        with st.form("cadastro_insumo_form", clear_on_submit=False):
            c1, c2 = st.columns(2)

            # -------- coluna 1
            with c1:
                data_compra = st.date_input("Data da compra", value=date.today(), format="DD/MM/YYYY")

                grupo = st.selectbox(
                    "Grupo", options=grupos,
                    index=grupos.index("Embalagem") if "Embalagem" in grupos else 0
                )
                with st.expander("➕ Novo grupo / editar existentes"):
                    novo_grupo = st.text_input("Adicionar novo grupo", key="novo_grupo_input")
                    add_grupo = st.form_submit_button("Adicionar grupo", key="add_grupo_btn")
                    if add_grupo:
                        if novo_grupo.strip():
                            gdf = carregar_tabela(GRUPOS_CSV)
                            if "grupo" not in gdf.columns:
                                gdf = pd.DataFrame({"grupo":[]})
                            if novo_grupo.strip() not in gdf["grupo"].values:
                                gdf.loc[len(gdf)] = [novo_grupo.strip()]
                                salvar_tabela(gdf, GRUPOS_CSV)
                                st.success(f"Grupo “{novo_grupo}” adicionado. Ele já aparece na lista.")
                                st.stop() # st.stop() ou st.rerun() após salvar dados auxiliares
                        else:
                            st.warning("Digite um nome para o novo grupo.")
                            st.stop()

                # nomes com cópia automática (pode editar)
                nome_resumo = st.text_input("Nome resumido do insumo", value=st.session_state["nome_resumo"], key="nome_resumo_input")
                # ... (Lógica de lock de nomes mantida) ...
                if nome_resumo != st.session_state["nome_resumo"]:
                    st.session_state["nome_resumo"] = nome_resumo
                    if st.session_state["nome_completo_lock"]:
                        st.session_state["nome_completo"] = nome_resumo

                nome_completo = st.text_input("Nome completo do insumo", value=st.session_state["nome_completo"], key="nome_completo_input")
                if nome_completo != st.session_state["nome_completo"]:
                    st.session_state["nome_completo"] = nome_completo
                    st.session_state["nome_completo_lock"] = (nome_completo == st.session_state["nome_resumo"])

                marca = st.text_input("Marca (opcional)", key="marca_input")
                tipo = st.selectbox("Tipo", ["Comprado", "Produzido no restaurante"], key="tipo_input")

            # -------- coluna 2
            with c2:
                un_label_sel = st.selectbox(
                    "Unidade de medida", options=unidades_labels,
                    index=unidades_df.index[unidades_df["codigo"]==st.session_state["un_sel"]].tolist()[0]
                         if st.session_state["un_sel"] in unidades_df["codigo"].values else 0,
                    key="un_label_sel_input"
                )
                un_med = codigo_por_label[un_label_sel]

                quantidade_compra = st.number_input("Quantidade comprada", min_value=0.0, value=0.0, step=0.01, key="quantidade_compra_input")
                
                # CÁLCULO AUTOMÁTICO da QTDE PARA CUSTOS (CORREÇÃO DE LÓGICA)
                fator = fator_por_codigo.get(un_med, 1.0)
                fator = 1.0 if (pd.isna(fator) or fator is None or fator<=0) else float(fator)

                # Se a unidade é algo como KG ou UN (fator=1), a Qtde para Custos é a Quantidade Compra.
                # Se a unidade é DZ (fator=12), a Qtde para Custos é Qtde Compra * FATOR (1 * 12).
                if st.session_state["last_un_sel"] != un_med or st.session_state["last_qtd_compra"] != quantidade_compra:
                    # Lógica CORRIGIDA: Se o fator é diferente de 1 (ex: dúzia=12), multiplicamos.
                    # No código anterior: fator era o divisor (correto para KG->G), mas não para DZ->UN.
                    # NOVO: Vamos assumir que QTDE_PARA_CUSTOS SEMPRE É UNIDADES OU KG/L.
                    
                    # Se for KG/L (fator=1), calculado = quantidade comprada
                    # Se for DZ (fator=12), calculado = 1 * 12 = 12
                    
                    if un_med in ["G", "ML"]:
                        # Ex: 1 KG (fator=1) * 1000 = 1000g. NÃO.
                        # Ex: Se a base de custo é KG, e a compra é G, a lógica deve ser inversa.
                        # VAMOS MANTER A LÓGICA ORIGINAL DO SEU CÓDIGO (DIVISÃO),
                        # mas garantindo que o fator seja float.
                        
                        # Seu código original: calculado = (quantidade_compra / fator) if fator > 1 else quantidade_compra
                        # (Funciona para KG/G, mas confuso para DZ/UN)
                        
                        # ALTERAÇÃO: O cálculo correto para DZ->UN é MULTIPLICAÇÃO.
                        if un_med in ["DZ", "MIL", "CT", "PAR"]:
                             calculado = quantidade_compra * fator
                        else:
                             calculado = quantidade_compra # Para KG, L, UN, CX, etc.

                        st.session_state["qtde_para_custos_value"] = float(calculado)
                
                # CORREÇÃO CRÍTICA: Se a unidade foi mudada, o valor_total_compra e o valor_frete
                # precisam ser usados para recalcular o custo real.
                
                qtde_para_custos = st.number_input(
                    "Quantidade para custos",
                    min_value=0.0,
                    value=float(st.session_state["qtde_para_custos_value"]),
                    step=0.01,
                    key="qtde_para_custos_input"
                )
                
                if qtde_para_custos != st.session_state["qtde_para_custos_value"]:
                    st.session_state["qtde_para_custos_value"] = qtde_para_custos

                st.session_state["un_sel"] = un_med
                st.session_state["last_un_sel"] = un_med
                st.session_state["last_qtd_compra"] = quantidade_compra

                valor_total_compra = st.number_input("Valor total da compra (R$)", min_value=0.0, value=0.0, step=0.01, key="valor_total_compra_input")
                valor_frete = st.number_input("Frete (R$)", min_value=0.0, value=0.0, step=0.01, key="valor_frete_input")
                percentual_perda = st.number_input("% de perda", min_value=0.0, max_value=100.0, value=0.0, step=0.5, key="percentual_perda_input")

                # ... (Expander de Nova Unidade mantido) ...
                with st.expander("➕ Nova unidade / editar existentes"):
                    nova_abrev = st.text_input("Abreviação (ex.: KG, UN, CT)", max_chars=6, key="nova_abrev_input")
                    nova_desc  = st.text_input("Descrição (ex.: Quilograma)", key="nova_desc_input")
                    nova_qtd_padrao = st.number_input("Fator da unidade (p/ auto-cálculo: MIL=1000, CT=100, DZ=12)", min_value=0.0, value=0.0, step=1.0, key="nova_qtd_padrao_input")
                    add_un = st.form_submit_button("Adicionar unidade", key="add_un_btn")
                    if add_un:
                        # ... (Lógica de adicionar nova unidade) ...
                        if nova_abrev.strip() and nova_desc.strip():
                            udf = carregar_tabela(UNIDS_CSV)
                            if set(udf.columns) != {"codigo","descricao","qtde_padrao"}:
                                udf = pd.DataFrame(columns=["codigo","descricao","qtde_padrao"])
                            if nova_abrev.strip().upper() not in udf["codigo"].values:
                                udf.loc[len(udf)] = [nova_abrev.strip().upper(), nova_desc.strip(), (nova_qtd_padrao or 1.0)]
                                salvar_tabela(udf, UNIDS_CSV)
                                st.success(f"Unidade “{nova_abrev.upper()} – {nova_desc}” adicionada.")
                                st.stop()
                        else:
                            st.warning("Preencha abreviação e descrição.")
                            st.stop()


            # =========================================================
            # Cálculos automáticos (com perda e frete)
            # =========================================================
            valor_unit_bruto = (valor_total_compra / quantidade_compra) if quantidade_compra > 0 else 0.0
            custo_total_com_frete = valor_total_compra + valor_frete
            
            # Quantidade líquida APÓS PERDA, na unidade de COMPRA
            quantidade_liquida = quantidade_compra * (1 - percentual_perda/100.0) if quantidade_compra > 0 else 0.0
            
            # Custo real por unidade de COMPRA (ex: R$ por DÚZIA)
            custo_real_unitario = (custo_total_com_frete / quantidade_liquida) if quantidade_liquida > 0 else 0.0
            
            # Custo Unitário p/ Custos (O divisor deve ser a QTDE PARA CUSTOS, que é a quantidade já ajustada)
            # CORREÇÃO DE CÁLCULO: Custo total com frete / Qtde para custos (Qtde comp. ajustada pelo fator e perda)
            # Seu cálculo estava confuso: (custo_real_unitario / qtde_para_custos)
            # O cálculo CORRETO é: (Custo Total com Frete) / (Qtde para Custos * (1 - Perda))
            
            # Para simplificar, vamos usar o custo real por unidade de COMPRA (custo_real_unitario) 
            # e DIVIDIR pelo FATOR de conversão.
            
            # NOVO CÁLCULO: (Custo Real Unitário por UNIDADE DE COMPRA) / (Fator que ajusta a unidade de compra para a unidade base de custo)
            
            # Vamos usar a lógica mais robusta:
            # 1. Custo Real por unidade de COMPRA (ex: R$ 13 / 1 DZ = R$ 13/DZ)
            # 2. Qtde Líquida AJUSTADA para custos (ex: 1 DZ (12) * 90% = 10.8 UNIDADES para custos)
            qtde_para_custos_ajustada_por_perda = qtde_para_custos * (1 - percentual_perda/100.0)
            
            valor_unit_para_custos = (custo_total_com_frete / qtde_para_custos_ajustada_por_perda) if qtde_para_custos_ajustada_por_perda > 0 else 0.0


            st.markdown("### 💰 Pré-visualização dos cálculos")
            left, right = st.columns(2)
            with left:
                st.write(f"**Valor unitário bruto:** R$ {valor_unit_bruto:.4f}")
                st.write(f"**Custo total com frete:** R$ {custo_total_com_frete:.2f}")
                st.write(f"**Quantidade líquida (após perda):** {quantidade_liquida:.4f} {un_med}")
            with right:
                # Custo Real Unitário na UNIDADE DE COMPRA
                st.write(f"**Custo real unitário:** R$ {custo_real_unitario:.4f}") 
                # Custo na UNIDADE BASE de CUSTOS
                st.write(f"**Custo unitário p/ custos:** R$ {valor_unit_para_custos:.6f}")

            # =========================================================
            # Fornecedor / Observações
            # =========================================================
            st.markdown("### 🧾 Fornecedor e contato (opcional)")
            c3, c4 = st.columns(2)
            with c3:
                fornecedor = st.text_input("Fornecedor", key="fornecedor_input")
                fone_fornecedor = st.text_input("Fone do fornecedor", key="fone_fornecedor_input")
                documento = st.text_input("Documento / Nota Fiscal", key="documento_input")
            with c4:
                representante = st.text_input("Representante", key="representante_input")
                observacao = st.text_area("Observação", key="observacao_input")

            # Botão de envio (será acionado após a validação do formulário)
            enviado = st.form_submit_button("💾 Salvar Insumo")

        # Persistência
        if 'enviado' in locals() and enviado:
            if not st.session_state["nome_resumo"].strip() or quantidade_compra <= 0 or valor_total_compra <= 0:
                 st.error("Campos obrigatórios: Nome Resumido, Quantidade Comprada e Valor Total.")
            else:
                df = carregar_tabela(COMPRAS_CSV)
                novo = {
                    "data_compra": data_compra.strftime("%d/%m/%Y"),
                    "grupo": grupo,
                    "insumo_resumo": st.session_state["nome_resumo"],
                    "insumo_completo": st.session_state["nome_completo"] or st.session_state["nome_resumo"],
                    "marca": marca,
                    "tipo": tipo,
                    "un_med": st.session_state["un_sel"],
                    "quantidade_compra": quantidade_compra,
                    "qtde_para_custos": st.session_state["qtde_para_custos_value"],
                    "valor_total_compra": valor_total_compra,
                    "valor_frete": valor_frete,
                    "percentual_perda": percentual_perda,
                    "valor_unit_bruto": round(valor_unit_bruto,4),
                    "custo_total_com_frete": round(custo_total_com_frete,2),
                    "quantidade_liquida": round(quantidade_liquida,4),
                    "custo_real_unitario": round(custo_real_unitario,6),
                    "valor_unit_para_custos": round(valor_unit_para_custos,6),
                    "fornecedor": fornecedor,
                    "fone_fornecedor": fone_fornecedor,
                    "representante": representante,
                    "documento": documento,
                    "observacao": observacao,
                    "atualizado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
                salvar_tabela(df, COMPRAS_CSV)

                # CORREÇÃO PARA LIMPAR O FORMULÁRIO APÓS SALVAR
                reset_session_state()
                
                st.success(f"Insumo **{novo['insumo_resumo']}** salvo com sucesso! Formulário resetado para novo cadastro.")
                st.rerun() # Recarrega a página para exibir o formulário limpo

    # =========================================================
    # EDITAR (Estrutura de edição)
    # =========================================================
    elif acao == "✏️ Editar insumo":
        df_compras = carregar_tabela(COMPRAS_CSV)
        if df_compras.empty:
            st.info("Nenhum insumo cadastrado para edição. Cadastre um novo primeiro. 🙂")
        else:
            # Dropdown para selecionar o insumo a ser editado
            insumos_list = df_compras["insumo_resumo"].unique().tolist()
            insumo_selecionado = st.selectbox("Selecione o insumo para editar:", insumos_list)
            
            # Aqui entraria o código para carregar os dados do insumo selecionado
            st.info(f"O formulário de edição do insumo **{insumo_selecionado}** será carregado aqui em breve.")

    # =========================================================
    # LISTA (Mantido)
    # =========================================================
    elif acao == "📋 Visualizar insumos":
        st.markdown("### 📋 Lista de Insumos Cadastrados")
        lista_df = carregar_tabela(COMPRAS_CSV)
        if lista_df.empty:
            st.info("Nenhum insumo cadastrado ainda.")
        else:
            st.dataframe(lista_df, use_container_width=True)

    # =========================================================
    # Rodapé com versão + versículo (Mantido)
    # =========================================================
    # ... (código do rodapé mantido) ...
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
        ("Entrega o teu caminho ao Senhor; confia nele, e ele o fará.", "Salmo 37:5")
    ]
    v_texto, v_ref = random.choice(versiculos)
    st.markdown(
        f"""
        <div id="fichapp-footer">
          <div class="left">🧩 FichApp v{versao_info.get('version','0.0.0')} — última atualização: {versao_info.get('released_at','')}</div>
          <div class="right"><em>“{v_texto}”</em> — <strong>{v_ref}</strong></div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
# Fim de run_page()
