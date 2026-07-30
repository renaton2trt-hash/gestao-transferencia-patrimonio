"""
Pipeline de Ingestão de Dados do Sistema Ágora (ETL)
----------------------------------------------------
Este script realiza o processo completo de ETL (Extract, Transform, Load):
1. Extrai os relatórios exportados em CSV/Excel do sistema Ágora.
2. Transforma e limpa os dados (padronização de datas, colunas e valores).
3. Carrega os dados atualizados no banco analítico SQLite (bens_patrimoniais.db).
"""

import os
import sys
import sqlite3
import pandas as pd
import numpy as np

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Caminhos de diretórios
base_dir = r"C:\Users\rpereira.sup.TRTRIO\.gemini\antigravity\scratch\portfolio-patrimonio"
export_dir = os.path.join(base_dir, "exportacoes_agora")
data_dir = os.path.join(base_dir, "data")

os.makedirs(export_dir, exist_ok=True)
os.makedirs(data_dir, exist_ok=True)

csv_agora_path = os.path.join(export_dir, "movimentacoes_agora_export.csv")
db_path = os.path.join(data_dir, "bens_patrimoniais.db")

def gerar_exportacao_simulada_agora():
    """Simula a geração semanal de um relatório exportado pelo sistema Ágora em CSV"""
    np.random.seed(99)
    registros = 50
    
    unidades = ['Matriz - São Paulo', 'Filial - Rio de Janeiro', 'Filial - Belo Horizonte', 
                'Centro de Distribuição - Campinas', 'Filial - Curitiba', 'Filial - Salvador']
    categorias = ['Equipamentos de TI', 'Mobiliário e Escritório', 'Veículos Corporativos', 'Maquinário e Ferramentas']
    responsaveis = ['Ana Paula (Patrimônio)', 'Marcos Viana (Logística)', 'Juliana Paes (TI)']
    
    data = []
    for i in range(1, registros + 1):
        tag = f"PAT-{200100 + i}"
        origem = np.random.choice(unidades)
        destino = np.random.choice([u for u in unidades if u != origem])
        cat = np.random.choice(categorias)
        desc = f"Item Ágora {cat} #{i}"
        val = round(float(np.random.uniform(500.0, 25000.0)), 2)
        resp = np.random.choice(responsaveis)
        st = np.random.choice(['Concluida', 'Em Transito', 'Pendente'], p=[0.7, 0.2, 0.1])
        dt_mov = f"2026-07-{np.random.randint(1, 28):02d} {np.random.randint(8, 18):02d}:30:00"
        
        data.append({
            'ID_MOVIMENTACAO_AGORA': f"AGORA-{1000 + i}",
            'COD_TAG_PATRIMONIO': tag,
            'DESCRICAO_ITEM': desc,
            'CATEGORIA_BEM': cat,
            'VALOR_AVALIADO': val,
            'UNIDADE_ORIGEM': origem,
            'UNIDADE_DESTINO': destino,
            'STATUS_SOLICITACAO': st,
            'DATA_REGISTRO_AGORA': dt_mov,
            'OPERADOR_RESPONSAVEL': resp
        })
    
    df_export = pd.DataFrame(data)
    df_export.to_csv(csv_agora_path, index=False, sep=';', encoding='utf-8-sig')
    print(f"📄 Relatório simulado do Ágora exportado para: {csv_agora_path}")

def executar_pipeline_etl():
    """Processo ETL: Lê o CSV do Ágora, trata e insere no Banco SQLite"""
    print("\n=======================================================")
    print("🚀 INICIANDO PIPELINE DE INGESTÃO DO SISTEMA ÁGORA")
    print("=======================================================\n")
    
    # 1. EXTRAÇÃO (Extract)
    if not os.path.exists(csv_agora_path):
        print("Arquivo de exportação não encontrado. Gerando arquivo simulado...")
        gerar_exportacao_simulada_agora()
        
    print(f"1. Lendo arquivo de exportação do Ágora: {os.path.basename(csv_agora_path)}...")
    df_raw = pd.read_csv(csv_agora_path, sep=';', encoding='utf-8-sig')
    print(f"   --> {len(df_raw)} registros encontrados no CSV.")

    # 2. TRANSFORMAÇÃO (Transform)
    print("2. Aplicando regras de limpeza e transformação de dados...")
    df_transformed = df_raw.copy()
    
    # Padronizar nomes de colunas para minúsculas e padrão SQL
    df_transformed.columns = [col.lower() for col in df_transformed.columns]
    
    # Converter datas para formato DATETIME
    df_transformed['data_registro_agora'] = pd.to_datetime(df_transformed['data_registro_agora'])
    
    # Adicionar coluna com data de ingestão no Data Lake / DW
    df_transformed['data_ingestao_pipeline'] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')

    # 3. CARGA (Load)
    print("3. Carregando dados na tabela 'agora_movimentacoes_tratadas' do SQLite...")
    conn = sqlite3.connect(db_path)
    
    # Salvar / Atualizar tabela no SQLite
    df_transformed.to_sql("agora_movimentacoes_tratadas", conn, if_exists="replace", index=False)
    
    # Verificar inserção
    total_banco = pd.read_sql_query("SELECT COUNT(*) AS total FROM agora_movimentacoes_tratadas", conn).iloc[0]['total']
    conn.close()
    
    print(f"   --> Carga concluída com sucesso! Total de linhas salvas na tabela: {total_banco}")
    print("\n=======================================================")
    print("✅ PIPELINE CONCLUÍDO COM SUCESSO!")
    print("=======================================================\n")

if __name__ == "__main__":
    gerar_exportacao_simulada_agora()
    executar_pipeline_etl()
