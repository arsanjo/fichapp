# 01_Cadastro_de_Insumos.py
# CÓDIGO FINAL COM ESTRUTURA DE 2 ABAS E CORREÇÃO DE ERRO DE ÍNDICE (V8.3)

import streamlit as st
import pandas as pd
from datetime import datetime, date
import os, json, random
# from utils.nav import sidebar_menu # Comentado porque não é usado no script principal

# =========================================================
# FUNÇÃO PRINCIPAL DE EXECUÇÃO DA PÁGINA
# =========================================================
def run_page():

    # =========================================================
    # CONFIG / THEME (Mantido)
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
    /* Estilo para o botão de edição na tabela */
    .edit-button-style { background-color: #f7a81b; color: #000; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer; }

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

    # =========================================================
    # Paths e Inicialização (Mantido)
    # =========================================================
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
    # Helpers (Mantidos)
    # =========================================================
    @st.cache_data
    def carregar_tabela(path: str, force_dtype=None) -> pd.DataFrame:
        try:
            if path == COMPRAS_CSV:
                return pd.read_csv(path, dtype=COMPRAS_DTYPE)
            elif force_dtype:
                 return pd.read_csv(path, dtype=force_dtype)
            else:
                 return pd.read_csv(path)
        except Exception: 
            return pd.DataFrame()

    def salvar_tabela(df: pd.DataFrame, path: str):
        if path == COMPRAS_CSV:
            missing_cols = set(compras_cols) - set(df.columns)
            for col in missing_cols:
                if col in COMPRAS_DTYPE:
                    df[col] = 0.0
                else:
                    df[col] = ''
            df = df[compras_cols] 
            
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
        if df_compras.empty:
            salvar_tabela(pd.DataFrame(columns=insumos_ativos_cols), INSUMOS_ATIVOS_CSV)
            return

        df_compras["data_compra_obj"] = pd.to_datetime(df_compras["data_compra"], format="%d/%m/%Y", errors='coerce')
        idx = df_compras.dropna(subset=["data_compra_obj"]).groupby(["insumo_resumo"])["data_compra_obj"].idxmax()
        
        if idx.empty:
             salvar_tabela(pd.DataFrame(columns=insumos_ativos_cols), INSUMOS_ATIVOS_CSV)
             return

        df_ativo = df_compras.loc[idx].copy()
        
        df_ativo = df_ativo[[
            "insumo_resumo", "grupo", "un_med", "valor_unit_para_custos", "data_compra"
        ]]
        
        df_ativo.columns = ["insumo_resumo", "grupo", "un_med", "custo_unit_ativo", "data_ultima_compra"]
        
        df_ativo['custo_unit_ativo'] = pd.to_numeric(df_ativo['custo_unit_ativo'], errors='coerce').fillna(0.0)
        
        salvar_tabela(df_ativo, INSUMOS_ATIVOS_CSV)

    # =========================================================
    # Estado da UI & Funções de Edição/Reset
    # =========================================================
    def reset_session_state():
        st.session_state["nome_resumo"] = ""
        st.session_state["nome_completo"] = ""
        st.session_state["nome_completo_lock"] = True
        st.session_state.current_edit_insumo = None
        st.session_state.current_edit_data = {}
        # Reseta os inputs que ficaram fora do form
        st.session_state.qtde_compra_key = 0.0
        st.session_state.valor_total_compra_key = 0.0
        st.session_state.valor_frete_key = 0.0
        st.session_state.percentual_perda_key = 0.0
        st.session_state.un_med_select_key = "UN"
        st.session_state["qtde_para_custos_value"] = 0.0
        st.session_state.acao_radio = "➕ Cadastrar novo insumo" # Garante o radio button no estado inicial

    defaults = {
        "nome_resumo": "", "nome_completo": "", "nome_completo_lock": True,
        "current_edit_insumo": None, "current_edit_data": {}, 
        "acao_manual_change": False, 
        "qtde_compra_key": 0.0, "valor_total_compra_key": 0.0, "valor_frete_key": 0.0, "percentual_perda_key": 0.0,
        "un_med_select_key": "UN", "qtde_para_custos_value": 0.0,
        "current_page_action": "Cadastro",
        "acao_radio": "➕ Cadastrar novo insumo"
    }
    for k,v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    def load_insumo_data(insumo_resumo):
        df_compras = carregar_tabela(COMPRAS_CSV)
        # Tenta encontrar a última compra
        try:
             ultima_compra = df_compras[df_compras['insumo_resumo'] == insumo_resumo].sort_values(by='atualizado_em', ascending=False).iloc[0]
        except IndexError:
             st.error(f"Erro: Insumo '{insumo_resumo}' não encontrado ou sem histórico de compras.")
             st.session_state.current_page_action = "Visualizar"
             st.rerun()
             return

        st.session_state["nome_resumo"] = ultima_compra["insumo_resumo"]
        st.session_state["nome_completo"] = ultima_compra["insumo_completo"]
        st.session_state.qtde_compra_key = float(ultima_compra["quantidade_compra"])
        st.session_state.valor_total_compra_key = float(ultima_compra["valor_total_compra"])
        st.session_state.valor_frete_key = float(ultima_compra["valor_frete"])
        st.session_state.percentual_perda_key = float(ultima_compra["percentual_perda"])
        st.session_state.un_med_select_key = ultima_compra["un_med"]
        st.session_state["qtde_para_custos_value"] = float(ultima_compra["qtde_para_custos"]) 
        
        st.session_state["current_edit_data"] = ultima_compra.to_dict()
        st.session_state.current_edit_insumo = insumo_resumo
        st.session_state.current_page_action = "Edição" 
        st.session_state.acao_radio = "📋 Visualizar insumos (e Editar)" # Altera o rádio para Edição
        
        st.rerun()

    # Callback para o botão de Edição na tabela
    if 'edit_insumo_trigger' in st.session_state and st.session_state.edit_insumo_trigger:
        insumo_a_editar = st.session_state.edit_insumo_trigger
        st.session_state.edit_insumo_trigger = None 
        load_insumo_data(insumo_a_editar)


    # =========================================================
    # INICIALIZAÇÃO E CÁLCULO
    # =========================================================
    
    grupos = lista_grupos()
    unidades_df = lista_unidades()
    unidades_labels = unidades_df.apply(label_unidade, axis=1).tolist()
    codigo_por_label = dict(zip(unidades_labels, unidades_df["codigo"]))
    fator_por_codigo = dict(zip(unidades_df["codigo"], unidades_df["qtde_padrao"])) 
    
    # 1. Pega os valores atuais do estado (as chaves dos inputs fora do form)
    current_un_med = st.session_state.get('un_med_select_key', "UN")
    current_qtde_compra = st.session_state.get('qtde_compra_key', 0.0)

    fator = fator_por_codigo.get(current_un_med, 1.0)
    fator = 1.0 if (pd.isna(fator) or fator is None or fator<=0) else float(fator)

    # LÓGICA DE CÁLCULO (Quantidade comprada * Fator)
    if current_un_med in ["G", "ML", "DZ", "MIL", "CT", "PAR"]:
        calculated_qtde_custos = current_qtde_compra * fator
    else:
        calculated_qtde_custos = current_qtde_compra
    
    # 2. Se o cálculo mudou E não for edição, atualiza o state (força a automação)
    if st.session_state.current_page_action == "Cadastro":
        if st.session_state["qtde_para_custos_value"] != float(calculated_qtde_custos):
            st.session_state["qtde_para_custos_value"] = float(calculated_qtde_custos)
    
    # Garante que as variáveis de cálculo tenham os valores mais recentes para uso posterior
    qtde_compra_final = st.session_state.qtde_compra_key
    qtde_custos_final = st.session_state["qtde_para_custos_value"]
    valor_total_compra = st.session_state.valor_total_compra_key
    valor_frete = st.session_state.valor_frete_key
    percentual_perda = st.session_state.percentual_perda_key
    un_med_final = st.session_state.un_med_select_key
    
    # =========================================================
    # Cabeçalho da Página
    # =========================================================
    st.markdown("<h1>📦 Cadastro de Insumos</h1>", unsafe_allow_html=True)
    
    # --- RADIO BUTTON (Removendo a opção de 3, forçando o novo fluxo) ---
    
    # Determina o índice ativo
    index_acao = 0 if st.session_state.current_page_action in ["Cadastro", "Edição"] else 1
    
    # Handler para o reset e troca de aba
    def set_page_action_and_reset(new_action):
        st.session_state.acao_manual_change = True
        st.session_state.current_edit_insumo = None 
        if new_action != st.session_state.current_page_action:
            reset_session_state()
            st.session_state.current_page_action = new_action
            st.rerun()

    # Callback para o Radio Button
    def handle_radio_change():
        if st.session_state.acao_radio_key == "➕ Cadastrar novo insumo":
            set_page_action_and_reset("Cadastro")
        elif st.session_state.acao_radio_key == "📋 Visualizar insumos (e Editar)":
            set_page_action_and_reset("Visualizar")

    acao = st.radio("Ação:", ["➕ Cadastrar novo insumo", "📋 Visualizar insumos (e Editar)"], 
                    index=index_acao,
                    key="acao_radio_key", # Alterado para evitar conflito
                    on_change=handle_radio_change)
    

    # =========================================================
    # MODO EDIÇÃO (Formulário Carregado)
    # =========================================================
    if st.session_state.current_page_action == "Edição":
        
        edit_data = st.session_state.current_edit_data
        st.subheader(f"✏️ Editando: {edit_data.get('insumo_resumo', 'Insumo')}")
        
        # --- INPUTS INTERATIVOS NA EDIÇÃO (Fora do Form) ---
        col_compra_data, col_compra_qtde = st.columns(2)
        
        # Encontra o índice correto do selectbox
        try:
             grupo_index = grupos.index(edit_data.get("grupo"))
        except ValueError:
             grupo_index = 0
             
        un_codes_list = unidades_df["codigo"].to_list()
        un_default_index_for_edit = 0
        try:
             # Correção de inicialização: busca o índice do código de unidade (seguro)
             un_default_index_for_edit = un_codes_list.index(edit_data.get("un_med", "UN"))
        except ValueError:
             un_default_index_for_edit = 0

        data_compra_val = pd.to_datetime(edit_data.get("data_compra"), format="%d/%m/%Y", errors='coerce').date() if edit_data.get("data_compra") else date.today()

        with col_compra_data:
            st.date_input("Data da compra (Última Compra)", value=data_compra_val, format="DD/MM/YYYY", key="edit_data_compra")
            st.selectbox("Unidade de medida", options=unidades_labels, index=un_default_index_for_edit, key="edit_un_label_sel")
            st.number_input("Quantidade comprada", min_value=0.0, value=qtde_compra_final, step=0.01, key="edit_quantidade_compra")
            st.selectbox("Grupo", options=grupos, index=grupo_index, key="edit_grupo")
            
        with col_compra_qtde:
            st.number_input("Valor total da compra (R$)", min_value=0.0, value=valor_total_compra, step=0.01, key="edit_valor_total_compra")
            st.number_input("Frete (R$)", min_value=0.0, value=valor_frete, step=0.01, key="edit_valor_frete")
            st.number_input("Quantidade para custos", min_value=0.0, value=qtde_custos_final, step=0.01, key="edit_qtde_para_custos")
            st.number_input("% de perda", min_value=0.0, max_value=100.0, value=percentual_perda, step=0.5, key="edit_percentual_perda")
            
        st.markdown("---")
        
        # --- PRÉ-VISUALIZAÇÃO (Recalcula com os inputs de Edição) ---
        edit_valor_unit_bruto = (st.session_state.edit_valor_total_compra / st.session_state.edit_quantidade_compra) if st.session_state.edit_quantidade_compra > 0 else 0.0
        edit_custo_total_com_frete = st.session_state.edit_valor_total_compra + st.session_state.edit_valor_frete
        edit_qtde_para_custos_ajustada_perda = st.session_state.edit_qtde_para_custos * (1 - st.session_state.edit_percentual_perda/100.0)
        edit_valor_unit_para_custos = (edit_custo_total_com_frete / edit_qtde_para_custos_ajustada_perda) if edit_qtde_para_custos_ajustada_perda > 0 else 0.0
        
        st.markdown("### 💰 Pré-visualização dos cálculos")
        left, right = st.columns(2)
        with left:
            st.write(f"**Custo total c/ frete (Atual):** R$ {edit_custo_total_com_frete:.2f}")
        with right:
            st.write(f"**Novo Custo Unitário p/ Custos (UNID. BASE):** R$ {edit_valor_unit_para_custos:.6f}")


        # --- FORMULÁRIO DE EDIÇÃO (Dados não interativos) ---
        with st.form("edicao_insumo_form", clear_on_submit=False):
            st.subheader("2. Detalhes do Insumo e Fornecedor")
            c1, c2 = st.columns(2)
            
            with c1:
                st.text_input("Nome resumido do insumo", value=st.session_state["nome_resumo"], key="edit_nome_resumo")
                st.text_input("Nome completo do insumo", value=st.session_state["nome_completo"], key="edit_nome_completo")
                st.text_input("Marca (opcional)", value=edit_data.get("marca"), key="edit_marca")
                st.selectbox("Tipo", ["Comprado", "Produzido no restaurante"], index=["Comprado", "Produzido no restaurante"].index(edit_data.get("tipo")) if edit_data.get("tipo") in ["Comprado", "Produzido no restaurante"] else 0, key="edit_tipo")

            with c2:
                st.text_input("Fornecedor", value=edit_data.get("fornecedor"), key="edit_fornecedor")
                st.text_input("Fone do fornecedor", value=edit_data.get("fone_fornecedor"), key="edit_fone_fornecedor")
                st.text_input("Documento / Nota Fiscal", value=edit_data.get("documento"), key="edit_documento")
                st.text_input("Representante", value=edit_data.get("representante"), key="edit_representante")

            observacao = st.text_area("Observação", value=edit_data.get("observacao"), key="edit_observacao")
            
            editado = st.form_submit_button("✅ Salvar Compra Corrigida/Atualizada")

            if editado:
                # TODO: Lógica de salvar como NOVA COMPRA (com data de hoje)
                st.info("A lógica de salvamento da edição (que gera uma nova compra no histórico) será implementada na próxima fase. A edição está funcionando visualmente!")
                st.rerun()


    # =========================================================
    # MODO CADASTRO
    # =========================================================
    elif st.session_state.current_page_action == "Cadastro":
        
        st.subheader("1. Dados Essenciais de Compra")
        
        # --- BLOCO DE INPUTS INTERATIVOS (FORA DO FORM) ---
        col_compra_data, col_compra_qtde = st.columns(2)
        
        # Encontra o índice correto do selectbox (usando a lógica mais segura)
        un_codes_list = unidades_df["codigo"].to_list()
        un_default_index_for_cad = 0
        try:
             un_default_index_for_cad = un_codes_list.index(st.session_state.un_med_select_key)
        except ValueError:
             un_default_index_for_cad = 0

        try:
             grupo_default_index = grupos.index(st.session_state.get('grupo_input_cad', grupos[0]))
        except ValueError:
             grupo_default_index = 0


        with col_compra_data:
            data_compra = st.date_input("Data da compra", value=date.today(), format="DD/MM/YYYY")
            
            un_label_sel = st.selectbox(
                "Unidade de medida", options=unidades_labels,
                index=un_default_index_for_cad,
                key="un_med_select_key" 
            )
            un_med_current = codigo_por_label[un_label_sel]
            
            # Sincroniza o estado. Quando o valor for diferente, o código de cálculo acima rodará
            if st.session_state.un_med_select_key != un_med_current:
                 st.session_state.un_med_select_key = un_med_current
                 st.rerun() 
            
            quantidade_compra = st.number_input(
                "Quantidade comprada", min_value=0.0, value=st.session_state.qtde_compra_key, step=0.01, key="qtde_compra_key"
            )
            
            grupo = st.selectbox(
                "Grupo", options=grupos,
                index=grupo_default_index,
                key="grupo_input_cad"
            )
            
        with col_compra_qtde:
            valor_total_compra_input = st.number_input("Valor total da compra (R$)", min_value=0.0, value=st.session_state.valor_total_compra_key, step=0.01, key="valor_total_compra_key")
            valor_frete_input = st.number_input("Frete (R$)", min_value=0.0, value=st.session_state.valor_frete_key, step=0.01, key="valor_frete_key")
            
            # Quantidade para Custos (AGORA FUNCIONAL)
            qtde_para_custos = st.number_input(
                "Quantidade para custos",
                min_value=0.0,
                value=qtde_custos_final, # Usa o valor calculado automaticamente
                step=0.01,
                key="qtde_para_custos_final_key"
            )
            
            percentual_perda_input = st.number_input("% de perda", min_value=0.0, max_value=100.0, value=st.session_state.percentual_perda_key, step=0.5, key="percentual_perda_key")
            
            # Expander Nova Unidade (Precisa ficar fora do form para o rerun funcionar no add)
            with st.expander("➕ Nova unidade / editar existentes"):
                nova_abrev = st.text_input("Abreviação (ex.: KG, UN, CT)", max_chars=6, key="nova_abrev_input_cad")
                nova_desc  = st.text_input("Descrição (ex.: Quilograma)", key="nova_desc_input_cad")
                nova_qtd_padrao = st.number_input("Fator da unidade (p/ auto-cálculo: MIL=1000, CT=100, DZ=12)", min_value=0.0, value=0.0, step=1.0, key="nova_qtd_padrao_input_cad")
                add_un = st.button("Adicionar unidade", key="add_un_btn_cad") 
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
        
        st.markdown("---")
        
        # Pré-visualização dos cálculos
        st.markdown("### 💰 Pré-visualização dos cálculos")
        left, right = st.columns(2)
        with left:
            st.write(f"**Valor unitário bruto:** R$ {valor_unit_bruto:.4f}")
            st.write(f"**Custo total com frete:** R$ {custo_total_com_frete:.2f}")
            st.write(f"**Quantidade líquida (após perda):** {quantidade_liquida:.4f} {un_med_final}")
        with right:
            st.write(f"**Custo real unitário (por UNID. COMPRA):** R$ {custo_real_unitario:.4f}") 
            st.write(f"**Custo unitário p/ custos (UNID. BASE):** R$ {valor_unit_para_custos:.6f}")

        # --- BLOCO DE DADOS NÃO INTERATIVOS (DENTRO DO FORM) ---
        st.markdown("---")
        with st.form("cadastro_insumo_form", clear_on_submit=False):
            st.subheader("2. Detalhes do Insumo e Fornecedor")
            c1, c2 = st.columns(2)

            # -------- coluna 1
            with c1:
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
                
            # -------- coluna 2 (Fornecedor)
            with c2:
                fornecedor = st.text_input("Fornecedor", key="fornecedor_input_cad")
                fone_fornecedor = st.text_input("Fone do fornecedor", key="fone_fornecedor_input_cad")
                documento = st.text_input("Documento / Nota Fiscal", key="documento_input_cad")
                representante = st.text_input("Representante", key="representante_input_cad")
                observacao = st.text_area("Observação", key="observacao_input_cad")

            enviado = st.form_submit_button("💾 Salvar Insumo")

        # Persistência
        if 'enviado' in locals() and enviado:
            
            if not st.session_state["nome_resumo"].strip() or qtde_compra_final <= 0 or valor_total_compra_input <= 0:
                 st.error("Campos obrigatórios: Nome Resumido, Quantidade Comprada e Valor Total.")
            else:
                # 1. Salva a compra histórica
                df_compras = carregar_tabela(COMPRAS_CSV)
                novo = {
                    "data_compra": data_compra.strftime("%d/%m/%Y"), "grupo": grupo, "insumo_resumo": st.session_state["nome_resumo"],
                    "insumo_completo": st.session_state["nome_completo"] or st.session_state["nome_resumo"], "marca": marca, "tipo": tipo,
                    "un_med": un_med_final, "quantidade_compra": qtde_compra_final, "qtde_para_custos": qtde_custos_final,
                    "valor_total_compra": valor_total_compra_input, "valor_frete": valor_frete_input, "percentual_perda": percentual_perda_input,
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
                st.session_state.acao_manual_change = False
                st.session_state.current_page_action = "Visualizar" # Manda o usuário para o relatório
                st.session_state.acao_radio_key = "📋 Visualizar insumos (e Editar)" # Atualiza o radio
                
                st.success(f"Insumo **{novo['insumo_resumo']}** salvo com sucesso! Formulário resetado para novo cadastro.")
                st.rerun() 

    # =========================================================
    # MODO VISUALIZAR (RELATÓRIO COM FILTROS E EDIÇÃO)
    # =========================================================
    elif st.session_state.current_page_action in ["Visualizar", "Edição"]:
        st.markdown("### 📋 Relatório de Insumos Ativos")
        
        # Carrega as tabelas para busca e relatório
        df_ativos = carregar_tabela(INSUMOS_ATIVOS_CSV, force_dtype={"custo_unit_ativo": float})
        df_compras_full = carregar_tabela(COMPRAS_CSV) # Para extrair todos os fornecedores/representantes
        
        if df_ativos.empty:
            st.info("Nenhum insumo ativo encontrado. Cadastre um novo primeiro.")
        else:
            # === FILTROS AVANÇADOS ===
            col_grupo, col_forn, col_busca = st.columns([1, 1, 1])
            
            # Filtro 1: Grupo
            grupos_disponiveis = ["Todos"] + sorted(df_ativos["grupo"].unique().tolist())
            grupo_filtro = col_grupo.selectbox("Filtrar por Grupo:", grupos_disponiveis, index=0)
            
            # Filtro 2: Fornecedor
            fornecedores = ["Todos"] + sorted(df_compras_full["fornecedor"].dropna().astype(str).unique().tolist())
            fornecedor_filtro = col_forn.selectbox("Filtrar por Fornecedor:", fornecedores, index=0)
            
            # Filtro 3: Busca (Nome ou Representante)
            termo_busca = col_busca.text_input("Buscar (Insumo ou Representante):", value="").strip().lower()

            df_filtrado = df_ativos.copy()
            
            # Aplica os Filtros
            if grupo_filtro != "Todos":
                df_filtrado = df_filtrado[df_filtrado["grupo"] == grupo_filtro]
            
            if fornecedor_filtro != "Todos":
                # Cruza com a tabela de compras para encontrar o insumo associado ao fornecedor
                insumos_por_fornecedor = df_compras_full[df_compras_full["fornecedor"] == fornecedor_filtro]["insumo_resumo"].unique()
                df_filtrado = df_filtrado[df_filtrado["insumo_resumo"].isin(insumos_por_fornecedor)]
            
            if termo_busca:
                # Busca por nome resumido, nome completo OU representante
                df_compras_busca = df_compras_full[['insumo_resumo', 'insumo_completo', 'representante']].drop_duplicates(subset=['insumo_resumo'])
                
                insumos_por_busca = df_compras_busca[
                    df_compras_busca["insumo_resumo"].str.lower().str.contains(termo_busca, na=False) |
                    df_compras_busca["insumo_completo"].str.lower().str.contains(termo_busca, na=False) |
                    df_compras_busca["representante"].str.lower().str.contains(termo_busca, na=False)
                ]["insumo_resumo"].unique()
                
                df_filtrado = df_filtrado[df_filtrado["insumo_resumo"].isin(insumos_por_busca)]
            
            
            # --- INTEGRAÇÃO COM EDIÇÃO ---
            st.markdown("---")
            st.caption("A tabela abaixo mostra o custo ativo de cada insumo. Use o seletor abaixo para editar a última compra.")

            # Adiciona a coluna de Ações
            df_display = df_filtrado.copy()
            df_display['Ações'] = 'Editar'
            
            # Colunas para exibição no DataFrame
            cols_map = {
                "insumo_resumo": "Insumo", "grupo": "Grupo", "un_med": "Unidade Base",
                "custo_unit_ativo": "Custo Unitário Ativo (R$)", "data_ultima_compra": "Última Compra",
                "Ações": "Ações"
            }
            
            insumos_com_acao = df_filtrado['insumo_resumo'].tolist()

            st.dataframe(
                df_display.rename(columns=cols_map)[list(cols_map.values())],
                use_container_width=True,
                column_config={
                    "Custo Unitário Ativo (R$)": st.column_config.NumberColumn(
                        format="R$ %0.6f"
                    ),
                    "Ações": st.column_config.Column(
                        # A coluna de ações agora é apenas um texto estático
                    )
                }
            )
            
            st.caption(f"Total de insumos ativos: {len(df_filtrado)}")
            
            # --- CAPTURA DE CLIQUE NO BOTÃO DE EDIÇÃO ---
            st.markdown("---")
            st.markdown("Selecione o insumo para editar a última compra:")
            
            if insumos_com_acao:
                insumo_selecionado = st.selectbox("Insumo:", insumos_com_acao, key="selectbox_edicao_insumo")
                
                if st.button(f"✏️ Editar última compra de: {insumo_selecionado}", key="trigger_edit_btn"):
                    st.session_state.edit_insumo_trigger = insumo_selecionado
                    st.rerun()
            else:
                st.info("Nenhum insumo corresponde aos filtros para edição.")


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
