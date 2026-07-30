"""
Dashboard Interativo de Gestão Patrimonial e Sistema Ágora
-----------------------------------------------------------
Este script utiliza Python com Streamlit e Plotly para criar um dashboard 
interativo completo com KPIs, gráficos de SLA por rota e tabela de busca.

Para executar:
pip install streamlit plotly pandas
streamlit run dashboards/app_dashboard.py
"""

import os
import sqlite3
import pandas as pd

# Verificar se streamlit está instalado
try:
    import streamlit as st
    import plotly.express as px
    import plotly.graph_objects as go
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

if HAS_STREAMLIT:
    st.set_page_config(page_title="Dashboard Patrimonial - Ágora", page_icon="🏢", layout="wide")
    
    st.title("🏢 Dashboard de Gestão Patrimonial & Ingestão Ágora")
    st.markdown("Monitoramento de transferências interdepartamentais de bens e conformidade de SLA logístico.")
    
    # Carregar dados do banco SQLite
    db_path = os.path.join(os.path.dirname(__file__), "..", "data", "bens_patrimoniais.db")
    
    @st.cache_data
    def carregar_dados():
        conn = sqlite3.connect(db_path)
        df_bens = pd.read_sql_query("SELECT * FROM bens_patrimoniais", conn)
        df_transf = pd.read_sql_query("""
            SELECT t.*, u1.nome_unidade AS origem, u2.nome_unidade AS destino, b.descricao_bem, b.valor_atual
            FROM transferencias_patrimonio t
            JOIN filiais_unidades u1 ON t.id_unidade_origem = u1.id_unidade
            JOIN filiais_unidades u2 ON t.id_unidade_destino = u2.id_unidade
            JOIN bens_patrimoniais b ON t.id_bem = b.id_bem
        """, conn)
        df_agora = pd.read_sql_query("SELECT * FROM agora_movimentacoes_tratadas", conn)
        conn.close()
        return df_bens, df_transf, df_agora
        
    try:
        df_bens, df_transf, df_agora = carregar_dados()
        
        # 1. KPIs no topo
        col1, col2, col3, col4 = st.columns(4)
        val_total = df_bens['valor_atual'].sum()
        col1.metric("Valor Total Patrimônio (R$)", f"R$ {val_total:,.2f}")
        col2.metric("Total de Bens Cadastrados", f"{len(df_bens):,}")
        col3.metric("Movimentações no Ágora", f"{len(df_agora):,}")
        col4.metric("Itens Em Trânsito", f"{len(df_transf[df_transf['status_transferencia'] == 'Em Transito']):,}")
        
        st.divider()
        
        # 2. Gráficos principais
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            st.subheader("📊 Valor do Patrimônio por Filial")
            df_unidade = df_transf.groupby('destino')['valor_atual'].sum().reset_index()
            fig_unidade = px.bar(df_unidade, x='destino', y='valor_atual', 
                                 title="Patrimônio por Filial Destino",
                                 labels={'destino': 'Filial', 'valor_atual': 'Valor Atual (R$)'},
                                 color='valor_atual', color_continuous_scale='Viridis')
            st.plotly_chart(fig_unidade, use_container_width=True)
            
        with col_g2:
            st.subheader("⏱️ Tempo Médio de Trânsito (SLA) por Rota")
            df_sla = df_transf[df_transf['status_transferencia'] == 'Concluida'].groupby(['origem', 'destino'])['tempo_transito_dias'].mean().reset_index()
            df_sla['rota'] = df_sla['origem'].str.split('-').str[0] + " ➔ " + df_sla['destino'].str.split('-').str[0]
            fig_sla = px.bar(df_sla.sort_values(by='tempo_transito_dias', ascending=False).head(8), 
                             x='rota', y='tempo_transito_dias', 
                             title="Maiores Prazos de Entrega entre Filiais (Dias)",
                             labels={'rota': 'Rota', 'tempo_transito_dias': 'Média de Dias'},
                             color='tempo_transito_dias', color_continuous_scale='Reds')
            st.plotly_chart(fig_sla, use_container_width=True)
            
        st.divider()
        
        # 3. Tabela de Ingestão do Ágora
        st.subheader("📋 Últimos Registros Ingeridos do Sistema Ágora")
        st.dataframe(df_agora[['id_movimentacao_agora', 'cod_tag_patrimonio', 'descricao_item', 'categoria_bem', 'valor_avaliado', 'unidade_origem', 'unidade_destino', 'status_solicitacao']], use_container_width=True)
        
    except Exception as e:
        st.error(f"Erro ao carregar dados do banco SQLite: {e}")
else:
    print("Streamlit não instalado nesta máquina. Para rodar o dashboard interativo, instale com: pip install streamlit plotly")
