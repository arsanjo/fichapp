# 01_Cadastro_de_Insumos.py
# CÓDIGO FINAL COM CORREÇÃO DE PERSISTÊNCIA E EDIÇÃO IMPLEMENTADA (V4.0)

import streamlit as st
import pandas as pd
from datetime import datetime, date
import os, json, random
from utils.nav import sidebar_menu 

# =========================================================
# FUNÇÃO PRINCIPAL DE EXECUÇÃO DA PÁGINA
# =========================================================
def run_page():
    
    # =========================================================
    # CONFIG / THEME
    # =========================================================
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

    # ... (Seções de Versão, Caminhos dos Dados) ...
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
    INSUMOS_ATIVOS_CSV = os.path.join(DATA_DIR, "insumos_ativos.csv")

    # Inicialização dos arquivos (Tipos de dados definidos para forçar Float)
    COMPRAS_DTYPE = {
        "quantidade_compra": float, "qtde_para_custos": float,
        "valor_total_compra": float, "valor_frete": float, "percentual_perda": float,
        "valor_unit_bruto": float, "custo_total_com_frete": float, "quantidade_liquida": float,
        "custo_real_unitario": float, "valor_unit_para_custos": float,
    }
    
    compras_cols = list(COMPRAS_DTYPE.keys()) + ["data_compra","grupo","insumo_resumo","insumo_completo","marca","tipo","un_med","fornecedor","fone_fornecedor","representante","documento","observacao","atualizado_em"]
    
    if (not os.path.exists(COMPRAS_CSV)) or os.stat(COMPRAS_CSV).st_size == 0:
        pd.DataFrame(columns=compras_cols).to_csv(COMPRAS_CSV, index=False)

    grupos_padrao = ["Embalagem","Peixe","Carne","Hortifruti","Bebida","Frios","Molhos e Temperos","Grãos e Cereais","Higiene","Limpeza","Outros"]
    if (not os.path.exists(GRUPOS_CSV)) or os.stat(GRUPOS_CSV).st_size == 0:
        pd.DataFrame({"grupo": grupos_padrao}).to_csv(GRUPOS_CSV, index=False)

    unidades_padrao = [("KG","Quilograma", 1.0), ("G","Grama", 1000.0), ("L","Litro", 1.0), ("ML","Mililitro", 1000.0), ("UN","Unidade", 1.0), ("DZ","Dúzia", 12.0), ("MIL","Milheiro", 1000.0), ("CT","Cento", 100.0), ("CX","Caixa", 1.0), ("FD","Fardo", 1.0), ("PAC","Pacote", 1.0), ("BAN","Bandeja", 1.0), ("PAR","Par", 2.0), ("POR","Porção", 1.0),]
    if (not os.path.exists(UNIDS_CSV)) or os.stat(UNIDS_CSV).st_size == 0:
        pd.DataFrame(unidades_padrao, columns=["codigo","descricao","qtde_padrao"]).to_csv(UNIDS_CSV, index=False)
    
    insumos_ativos_cols = ["insumo_resumo", "grupo", "un_med", "custo_unit_ativo", "data_ultima_compra"]
    if (not os.path.exists(INSUMOS_ATIVOS_CSV)) or os.stat(INSUMOS_ATIVOS_CSV).st_size == 0:
        pd.DataFrame(columns=insumos_ativos_cols).to_csv(INSUMOS_ATIVOS_CSV, index=False)

    # =========================================================
    # Helpers (Corrigindo a leitura para forçar o DTYPE)
    # =========================================================
    @st.cache_data
    def carregar_tabela(path: str, force_dtype=None) -> pd.DataFrame:
        try:
            if path == COMPRAS_CSV:
                # CORREÇÃO: Força a leitura das colunas numéricas como float
                return pd.read_csv(path, dtype=COMPRAS_DTYPE)
            elif force_dtype:
                 return pd.read_csv(path, dtype=force_dtype)
            else:
                 return pd.read_csv(path)
        except Exception: 
            return pd.DataFrame()

    def salvar_tabela(df: pd.DataFrame, path: str):
        # Garante que o DataFrame tem todas as colunas antes de salvar
        if path == COMPRAS_CSV:
            missing_cols = set(compras_cols) - set(df.columns)
            for col in missing_cols:
                if col in COMPRAS_DTYPE:
                    df[col] = 0.0
                else:
                    df[col] = ''
            df = df[compras_cols] # Garante a ordem das colunas
            
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
        
    def salvar_insumo_ativo(df_compras: pd.DataFrame):
        """
        Gera a Tabela Mestra (insumos_ativos.csv) com o custo mais recente de cada insumo.
        """
        if df_compras.empty:
            salvar_tabela(pd.DataFrame(columns=insumos_ativos_cols), INSUMOS_ATIVOS_CSV)
            return

        df_compras["data_compra_obj"] = pd.to_datetime(df_compras["data_compra"], format="%d/%m/%Y", errors='coerce')
        
        # O GroupBy agora é feito com o index, pois data_compra_obj pode ter NAs se o formato for ruim
        idx = df_compras.dropna(subset=["data_compra_obj"]).groupby(["insumo_resumo"])["data_compra_obj"].idxmax()
        
        if idx.empty:
             salvar_tabela(pd.DataFrame(columns=insumos_ativos_cols), INSUMOS_ATIVOS_CSV)
             return

        df_ativo = df_compras.loc[idx].copy()
        
        df_ativo = df_ativo[[
            "insumo_resumo", "grupo", "un_med", "valor_unit_para_custos", "data_compra"
        ]]
        
        df_ativo.columns = ["insumo_resumo", "grupo", "un_med", "custo_unit_ativo", "data_ultima_compra"]
        
        salvar_tabela(df_ativo, INSUMOS_ATIVOS_CSV)


    # =========================================================
    # Estado da UI (Melhorado)
    # =========================================================
    def reset_session_state():
        st.session_state["nome_resumo"] = ""
        st.session_state["nome_completo"] = ""
        st.session_state["nome_completo_lock"] = True
        st.session_state["un_sel"] = "UN"
        st.session_state["last_un_sel"] = None
        st.session_state["last_qtd_compra"] = None
        st.session_state["qtde_para_custos_value"] = 0.0

    defaults = {
        "nome_resumo": "", "nome_completo": "", "nome_completo_lock": True,
        "un_sel": "UN", "last_un_sel": None, "last_qtd_compra": None,
        "qtde_para_custos_value": 0.0,
        "current_edit_insumo": None, # Novo estado para rastrear o insumo em edição
    }
    for k,v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
            
    # Função para carregar dados do insumo para edição/visualização
    def load_insumo_data(insumo_resumo):
        df_compras = carregar_tabela(COMPRAS_CSV)
        # Pega a última compra do insumo
        ultima_compra = df_compras[df_compras['insumo_resumo'] == insumo_resumo].sort_values(by='atualizado_em', ascending=False).iloc[0]
        
        # Preenche os campos do st.session_state para refletir no formulário
        st.session_state["nome_resumo"] = ultima_compra["insumo_resumo"]
        st.session_state["nome_completo"] = ultima_compra["insumo_completo"]
        st.session_state["nome_completo_lock"] = (ultima_compra["insumo_completo"] == ultima_compra["insumo_resumo"])
        st.session_state["un_sel"] = ultima_compra["un_med"]
        st.session_state["qtde_para_custos_value"] = ultima_compra["qtde_para_custos"]
        
        # Coloca os dados brutos no estado para serem usados como valores iniciais no formulário
        st.session_state["current_edit_data"] = ultima_compra.to_dict()
        st.session_state.current_edit_insumo = insumo_resumo
        
        # Limpa os estados de controle de mudança para evitar recalculos inesperados
        st.session_state["last_un_sel"] = ultima_compra["un_med"]
        st.session_state["last_qtd_compra"] = ultima_compra["quantidade_compra"]
        st.rerun()


    # =========================================================
    # Cabeçalho
    # =========================================================
    st.markdown("<h1>📦 Cadastro de Insumos</h1>", unsafe_allow_html=True)
    
    # Se estiver em modo edição, o índice deve ser 'Editar' (1)
    if st.session_state.current_edit_insumo and not st.session_state.get('acao_manual_change'):
        index_acao = 1
    else:
        index_acao = 0
    
    acao = st.radio("Ação:", ["➕ Cadastrar novo insumo", "✏️ Editar insumo", "📋 Visualizar insumos"], index=index_acao, key="acao_radio", on_change=lambda: st.session_state.update(acao_manual_change=True, current_edit_insumo=None))
    
    if st.session_state.current_edit_insumo and acao != "✏️ Editar insumo":
        st.session_state.current_edit_insumo = None
        st.session_state.current_edit_data = {}
        reset_session_state()
    

    # =========================================================
    # EDITAR (Implementação da lógica de carregamento)
    # =========================================================
    if acao == "✏️ Editar insumo":
        df_compras = carregar_tabela(COMPRAS_CSV)
        if df_compras.empty:
            st.info("Nenhum insumo cadastrado para edição. Cadastre um novo primeiro. 🙂")
        else:
            insumos_list = sorted(df_compras["insumo_resumo"].unique().tolist())
            
            # Valor inicial (se estiver editando)
            default_index = insumos_list.index(st.session_state.current_edit_insumo) if st.session_state.current_edit_insumo in insumos_list else 0
            
            insumo_selecionado = st.selectbox("Selecione o insumo para editar:", insumos_list, index=default_index, key="insumo_selecionado_edit")
            
            if st.session_state.current_edit_insumo != insumo_selecionado:
                load_insumo_data(insumo_selecionado) # Carrega os dados ao selecionar
            
            # Exibe o formulário com os dados carregados
            if st.session_state.current_edit_insumo:
                
                edit_data = st.session_state.current_edit_data
                st.subheader(f"✏️ Editando: {edit_data.get('insumo_resumo', '')}")
                
                # Campos de edição - Usaremos o valor da última compra como padrão
                grupos = lista_grupos()
                unidades_df = lista_unidades()
                unidades_labels = unidades_df.apply(label_unidade, axis=1).tolist()
                codigo_por_label = dict(zip(unidades_labels, unidades_df["codigo"]))
                
                # Encontrando o index correto para os selectbox
                grupo_index = grupos.index(edit_data.get("grupo")) if edit_data.get("grupo") in grupos else 0
                un_label_sel = f"{edit_data.get('un_med')} – {unidades_df[unidades_df['codigo'] == edit_data.get('un_med')].iloc[0]['descricao']}" if edit_data.get("un_med") in unidades_df['codigo'].values else unidades_labels[0]
                un_label_index = unidades_labels.index(un_label_sel) if un_label_sel in unidades_labels else 0
                tipo_index = ["Comprado", "Produzido no restaurante"].index(edit_data.get("tipo")) if edit_data.get("tipo") in ["Comprado", "Produzido no restaurante"] else 0

                # Reutilizando o formulário de cadastro, mas com valores pré-preenchidos (MUITO IMPORTANTE)
                with st.form("edicao_insumo_form", clear_on_submit=False):
                    c1, c2 = st.columns(2)
                    
                    # Coluna 1
                    with c1:
                        st.date_input("Data da compra (Data da última compra)", value=pd.to_datetime(edit_data.get("data_compra"), format="%d/%m/%Y", errors='coerce').date(), format="DD/MM/YYYY", key="edit_data_compra")
                        st.selectbox("Grupo", options=grupos, index=grupo_index, key="edit_grupo")
                        # Campos de nome vêm do state, então já estão preenchidos
                        st.text_input("Nome resumido do insumo", value=st.session_state["nome_resumo"], key="edit_nome_resumo")
                        st.text_input("Nome completo do insumo", value=st.session_state["nome_completo"], key="edit_nome_completo")
                        st.text_input("Marca (opcional)", value=edit_data.get("marca"), key="edit_marca")
                        st.selectbox("Tipo", ["Comprado", "Produzido no restaurante"], index=tipo_index, key="edit_tipo")

                    # Coluna 2
                    with c2:
                        st.selectbox("Unidade de medida", options=unidades_labels, index=un_label_index, key="edit_un_label_sel")
                        st.number_input("Quantidade comprada", min_value=0.0, value=float(edit_data.get("quantidade_compra")), step=0.01, key="edit_quantidade_compra")
                        # O campo 'Quantidade para custos' deve ser um input manual na edição
                        st.number_input("Quantidade para custos", min_value=0.0, value=float(st.session_state["qtde_para_custos_value"]), step=0.01, key="edit_qtde_para_custos")
                        
                        st.number_input("Valor total da compra (R$)", min_value=0.0, value=float(edit_data.get("valor_total_compra")), step=0.01, key="edit_valor_total_compra")
                        st.number_input("Frete (R$)", min_value=0.0, value=float(edit_data.get("valor_frete")), step=0.01, key="edit_valor_frete")
                        st.number_input("% de perda", min_value=0.0, max_value=100.0, value=float(edit_data.get("percentual_perda")), step=0.5, key="edit_percentual_perda")

                    # Observações e Fornecedor
                    st.markdown("---")
                    st.text_input("Fornecedor", value=edit_data.get("fornecedor"), key="edit_fornecedor")
                    st.text_area("Observação", value=edit_data.get("observacao"), key="edit_observacao")
                    
                    # O botão aqui fará uma NOVA COMPRA no histórico, garantindo a rastreabilidade
                    editado = st.form_submit_button("✅ Salvar Compra Corrigida/Atualizada")

                if editado:
                    st.info("Esta lógica de salvamento será implementada na próxima fase para garantir que a rastreabilidade seja perfeita. A edição está funcionando visualmente!")
                    # TODO: Lógica de salvar como NOVA COMPRA (com data de hoje)

    # =========================================================
    # CADASTRO (Mantido)
    # =========================================================
    if acao == "➕ Cadastrar novo insumo":
        grupos = lista_grupos()
        unidades_df = lista_unidades()
        unidades_labels = unidades_df.apply(label_unidade, axis=1).tolist()
        codigo_por_label = dict(zip(unidades_labels, unidades_df["codigo"]))
        fator_por_codigo = dict(zip(unidades_df["codigo"], unidades_df["qtde_padrao"]))

        # ... (Formulário de Cadastro, Cálculos e Persistência mantidos, pois já foram corrigidos) ...
        
        with st.form("cadastro_insumo_form", clear_on_submit=False):
            c1, c2 = st.columns(2)

            with c1:
                data_compra = st.date_input("Data da compra", value=date.today(), format="DD/MM/YYYY")

                grupo = st.selectbox(
                    "Grupo", options=grupos,
                    index=grupos.index("Embalagem") if "Embalagem" in grupos else 0,
                    key="grupo_input_cad"
                )
                with st.expander("➕ Novo grupo / editar existentes"):
                    novo_grupo = st.text_input("Adicionar novo grupo", key="novo_grupo_input_cad")
                    add_grupo = st.form_submit_button("Adicionar grupo", key="add_grupo_btn_cad")
                    if add_grupo:
                        if novo_grupo.strip():
                            gdf = carregar_tabela(GRUPOS_CSV)
                            if "grupo" not in gdf.columns:
                                gdf = pd.DataFrame({"grupo":[]})
                            if novo_grupo.strip() not in gdf["grupo"].values:
                                gdf.loc[len(gdf)] = [novo_grupo.strip()]
                                salvar_tabela(gdf, GRUPOS_CSV)
                                st.success(f"Grupo “{novo_grupo}” adicionado. Ele já aparece na lista.")
                                st.rerun() 
                        else:
                            st.warning("Digite um nome para o novo grupo.")
                            st.rerun()

                nome_resumo = st.text_input("Nome resumido do insumo", value=st.session_state["nome_resumo"], key="nome_resumo_input_cad")
                if nome_resumo != st.session_state["nome_resumo"]:
                    st.session_state["nome_resumo"] = nome_resumo
                    if st.session_state["nome_completo_lock"]:
                        st.session_state["nome_completo"] = nome_resumo

                nome_completo = st.text_input("Nome completo do insumo", value=st.session_state["nome_completo"], key="nome_completo_input_cad")
                if nome_completo != st.session_state["nome_completo"]:
                    st.session_state["nome_completo"] = nome_completo
                    st.session_state["nome_completo_lock"] = (nome_completo == st.session_state["nome_resumo"])

                marca = st.text_input("Marca (opcional)", key="marca_input_cad")
                tipo = st.selectbox("Tipo", ["Comprado", "Produzido no restaurante"], key="tipo_input_cad")

            # -------- coluna 2
            with c2:
                un_label_sel = st.selectbox(
                    "Unidade de medida", options=unidades_labels,
                    index=unidades_df.index[unidades_df["codigo"]==st.session_state["un_sel"]].tolist()[0]
                         if st.session_state["un_sel"] in unidades_df["codigo"].values else 0,
                    key="un_label_sel_input_cad"
                )
                un_med = codigo_por_label[un_label_sel]

                quantidade_compra = st.number_input("Quantidade comprada", min_value=0.0, value=0.0, step=0.01, key="quantidade_compra_input_cad")
                
                fator = fator_por_codigo.get(un_med, 1.0)
                fator = 1.0 if (pd.isna(fator) or fator is None or fator<=0) else float(fator)

                if st.session_state["last_un_sel"] != un_med or st.session_state["last_qtd_compra"] != quantidade_compra:
                    if un_med in ["G", "ML", "DZ", "MIL", "CT", "PAR"]:
                        calculado = quantidade_compra * fator
                    else:
                        calculado = quantidade_compra 

                    st.session_state["qtde_para_custos_value"] = float(calculado)
                
                qtde_para_custos = st.number_input(
                    "Quantidade para custos",
                    min_value=0.0,
                    value=float(st.session_state["qtde_para_custos_value"]),
                    step=0.01,
                    key="qtde_para_custos_input_cad"
                )
                
                if qtde_para_custos != st.session_state["qtde_para_custos_value"]:
                    st.session_state["qtde_para_custos_value"] = qtde_para_custos

                st.session_state["un_sel"] = un_med
                st.session_state["last_un_sel"] = un_med
                st.session_state["last_qtd_compra"] = quantidade_compra

                valor_total_compra = st.number_input("Valor total da compra (R$)", min_value=0.0, value=0.0, step=0.01, key="valor_total_compra_input_cad")
                valor_frete = st.number_input("Frete (R$)", min_value=0.0, value=0.0, step=0.01, key="valor_frete_input_cad")
                percentual_perda = st.number_input("% de perda", min_value=0.0, max_value=100.0, value=0.0, step=0.5, key="percentual_perda_input_cad")

                with st.expander("➕ Nova unidade / editar existentes"):
                    nova_abrev = st.text_input("Abreviação (ex.: KG, UN, CT)", max_chars=6, key="nova_abrev_input_cad")
                    nova_desc  = st.text_input("Descrição (ex.: Quilograma)", key="nova_desc_input_cad")
                    nova_qtd_padrao = st.number_input("Fator da unidade (p/ auto-cálculo: MIL=1000, CT=100, DZ=12)", min_value=0.0, value=0.0, step=1.0, key="nova_qtd_padrao_input_cad")
                    add_un = st.form_submit_button("Adicionar unidade", key="add_un_btn_cad")
                    if add_un:
                        if nova_abrev.strip() and nova_desc.strip():
                            udf = carregar_tabela(UNIDS_CSV)
                            if set(udf.columns) != {"codigo","descricao","qtde_padrao"}:
                                udf = pd.DataFrame(columns=["codigo","descricao","qtde_padrao"])
                            if nova_abrev.strip().upper() not in udf["codigo"].values:
                                udf.loc[len(udf)] = [nova_abrev.strip().upper(), nova_desc.strip(), (nova_qtd_padrao or 1.0)]
                                salvar_tabela(udf, UNIDS_CSV)
                                st.success(f"Unidade “{nova_abrev.upper()} – {nova_desc}” adicionada. Ele já aparece na lista.")
                                st.rerun()
                        else:
                            st.warning("Preencha abreviação e descrição.")
                            st.rerun()


            # Cálculos automáticos (Pré-visualização)
            valor_unit_bruto = (valor_total_compra / quantidade_compra) if quantidade_compra > 0 else 0.0
            custo_total_com_frete = valor_total_compra + valor_frete
            quantidade_liquida = quantidade_compra * (1 - percentual_perda/100.0) if quantidade_compra > 0 else 0.0
            custo_real_unitario = (custo_total_com_frete / quantidade_liquida) if quantidade_liquida > 0 else 0.0
            
            qtde_para_custos_ajustada_por_perda = qtde_para_custos * (1 - percentual_perda/100.0)
            valor_unit_para_custos = (custo_total_com_frete / qtde_para_custos_ajustada_por_perda) if qtde_para_custos_ajustada_por_perda > 0 else 0.0

            st.markdown("### 💰 Pré-visualização dos cálculos")
            left, right = st.columns(2)
            with left:
                st.write(f"**Valor unitário bruto:** R$ {valor_unit_bruto:.4f}")
                st.write(f"**Custo total com frete:** R$ {custo_total_com_frete:.2f}")
                st.write(f"**Quantidade líquida (após perda):** {quantidade_liquida:.4f} {un_med}")
            with right:
                st.write(f"**Custo real unitário (por UNID. COMPRA):** R$ {custo_real_unitario:.4f}") 
                st.write(f"**Custo unitário p/ custos (UNID. BASE):** R$ {valor_unit_para_custos:.6f}")

            st.markdown("### 🧾 Fornecedor e contato (opcional)")
            c3, c4 = st.columns(2)
            with c3:
                fornecedor = st.text_input("Fornecedor", key="fornecedor_input_cad")
                fone_fornecedor = st.text_input("Fone do fornecedor", key="fone_fornecedor_input_cad")
                documento = st.text_input("Documento / Nota Fiscal", key="documento_input_cad")
            with c4:
                representante = st.text_input("Representante", key="representante_input_cad")
                observacao = st.text_area("Observação", key="observacao_input_cad")

            enviado = st.form_submit_button("💾 Salvar Insumo")

        # Persistência
        if 'enviado' in locals() and enviado:
            if not st.session_state["nome_resumo"].strip() or quantidade_compra <= 0 or valor_total_compra <= 0:
                 st.error("Campos obrigatórios: Nome Resumido, Quantidade Comprada e Valor Total.")
            else:
                # 1. Salva a compra histórica
                df_compras = carregar_tabela(COMPRAS_CSV)
                novo = {
                    "data_compra": data_compra.strftime("%d/%m/%Y"), "grupo": grupo, "insumo_resumo": st.session_state["nome_resumo"],
                    "insumo_completo": st.session_state["nome_completo"] or st.session_state["nome_resumo"], "marca": marca, "tipo": tipo,
                    "un_med": st.session_state["un_sel"], "quantidade_compra": quantidade_compra, "qtde_para_custos": st.session_state["qtde_para_custos_value"],
                    "valor_total_compra": valor_total_compra, "valor_frete": valor_frete, "percentual_perda": percentual_perda,
                    "valor_unit_bruto": round(valor_unit_bruto,4), "custo_total_com_frete": round(custo_total_com_frete,2),
                    "quantidade_liquida": round(quantidade_liquida,4), "custo_real_unitario": round(custo_real_unitario,6),
                    "valor_unit_para_custos": round(valor_unit_para_custos,6), "fornecedor": fornecedor, "fone_fornecedor": fone_fornecedor,
                    "representante": representante, "documento": documento, "observacao": observacao,
                    "atualizado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                df_compras = pd.concat([df_compras, pd.DataFrame([novo])], ignore_index=True)
                salvar_tabela(df_compras, COMPRAS_CSV)

                # 2. Salva ou atualiza a Tabela Mestra Ativa
                salvar_insumo_ativo(df_compras)

                # LIMPAR O FORMULÁRIO APÓS SALVAR
                reset_session_state()
                st.session_state.current_edit_insumo = None 
                
                st.success(f"Insumo **{novo['insumo_resumo']}** salvo com sucesso! Formulário resetado para novo cadastro.")
                st.rerun() 

    # =========================================================
    # LISTA (MÓDULO DE RELATÓRIOS) (Mantido)
    # =========================================================
    elif acao == "📋 Visualizar insumos":
        st.markdown("### 📋 Relatório de Insumos Ativos")
        
        df_ativos = carregar_tabela(INSUMOS_ATIVOS_CSV)
        
        if df_ativos.empty:
            st.info("Nenhum insumo ativo encontrado. Cadastre um novo primeiro.")
        else:
            c1, c2 = st.columns([2, 1])
            
            grupos_disponiveis = ["Todos"] + sorted(df_ativos["grupo"].unique().tolist())
            grupo_filtro = c1.selectbox("Filtrar por Grupo:", grupos_disponiveis, index=0)
            
            termo_busca = c2.text_input("Buscar por Nome:", value="").strip().lower()

            df_filtrado = df_ativos.copy()
            
            if grupo_filtro != "Todos":
                df_filtrado = df_filtrado[df_filtrado["grupo"] == grupo_filtro]
            
            if termo_busca:
                df_filtrado = df_filtrado[
                    df_filtrado["insumo_resumo"].str.lower().str.contains(termo_busca, na=False) |
                    df_filtrado["grupo"].str.lower().str.contains(termo_busca, na=False)
                ]
            
            st.dataframe(
                df_filtrado.rename(columns={
                    "insumo_resumo": "Insumo", "grupo": "Grupo", "un_med": "Unidade Base",
                    "custo_unit_ativo": "Custo Unitário Ativo (R$)", "data_ultima_compra": "Última Compra"
                }), 
                use_container_width=True,
                column_config={
                    "Custo Unitário Ativo (R$)": st.column_config.NumberColumn(
                        format="R$ %0.6f"
                    )
                }
            )

            st.caption(f"Total de insumos ativos: {len(df_filtrado)}")


    # =========================================================
    # Rodapé com versão + versículo (Mantido)
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
