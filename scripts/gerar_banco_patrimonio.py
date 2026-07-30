import sys
import sqlite3
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


# Diretórios
base_dir = r"C:\Users\rpereira.sup.TRTRIO\.gemini\antigravity\scratch\portfolio-patrimonio"
data_dir = os.path.join(base_dir, "data")
os.makedirs(data_dir, exist_ok=True)

db_path = os.path.join(data_dir, "bens_patrimoniais.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Tabela Unidades / Filiais
cursor.execute('''
CREATE TABLE IF NOT EXISTS filiais_unidades (
    id_unidade INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_unidade TEXT NOT NULL,
    cidade TEXT NOT NULL,
    estado TEXT NOT NULL,
    centro_custo TEXT NOT NULL
)
''')

# 2. Tabela Categorias de Bens
cursor.execute('''
CREATE TABLE IF NOT EXISTS categorias_bens (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_categoria TEXT NOT NULL,
    vida_util_anos INTEGER,
    taxa_depreciacao_anual DECIMAL(5,2)
)
''')

# 3. Tabela Bens Patrimoniais
cursor.execute('''
CREATE TABLE IF NOT EXISTS bens_patrimoniais (
    id_bem INTEGER PRIMARY KEY AUTOINCREMENT,
    tombamento_tag TEXT UNIQUE NOT NULL,
    descricao_bem TEXT NOT NULL,
    id_categoria INTEGER,
    data_aquisicao DATE,
    valor_aquisicao DECIMAL(12,2),
    valor_atual DECIMAL(12,2),
    id_unidade_atual INTEGER,
    status_bem TEXT,
    FOREIGN KEY (id_categoria) REFERENCES categorias_bens(id_categoria),
    FOREIGN KEY (id_unidade_atual) REFERENCES filiais_unidades(id_unidade)
)
''')

# 4. Tabela Transferências de Patrimônio
cursor.execute('''
CREATE TABLE IF NOT EXISTS transferencias_patrimonio (
    id_transferencia INTEGER PRIMARY KEY AUTOINCREMENT,
    id_bem INTEGER,
    id_unidade_origem INTEGER,
    id_unidade_destino INTEGER,
    data_solicitacao DATETIME,
    data_envio DATETIME,
    data_recebimento DATETIME,
    tempo_transito_dias INTEGER,
    status_transferencia TEXT,
    motivo_transferencia TEXT,
    responsavel_solicitacao TEXT,
    FOREIGN KEY (id_bem) REFERENCES bens_patrimoniais(id_bem),
    FOREIGN KEY (id_unidade_origem) REFERENCES filiais_unidades(id_unidade),
    FOREIGN KEY (id_unidade_destino) REFERENCES filiais_unidades(id_unidade)
)
''')

# Popular Dados Fictícios de Produção
cursor.execute("SELECT COUNT(*) FROM filiais_unidades")
if cursor.fetchone()[0] == 0:
    unidades = [
        ('Matriz - São Paulo', 'São Paulo', 'SP', 'CC-1001'),
        ('Filial - Rio de Janeiro', 'Rio de Janeiro', 'RJ', 'CC-2001'),
        ('Filial - Belo Horizonte', 'Belo Horizonte', 'MG', 'CC-3001'),
        ('Centro de Distribuição - Campinas', 'Campinas', 'SP', 'CC-4001'),
        ('Filial - Curitiba', 'Curitiba', 'PR', 'CC-5001'),
        ('Filial - Salvador', 'Salvador', 'BA', 'CC-6001')
    ]
    cursor.executemany("INSERT INTO filiais_unidades (nome_unidade, cidade, estado, centro_custo) VALUES (?, ?, ?, ?)", unidades)

cursor.execute("SELECT COUNT(*) FROM categorias_bens")
if cursor.fetchone()[0] == 0:
    categorias = [
        ('Equipamentos de TI', 5, 20.00),
        ('Mobiliário e Escritório', 10, 10.00),
        ('Veículos Corporativos', 5, 20.00),
        ('Maquinário e Ferramentas', 10, 10.00),
        ('Aparelhos de Ar Condicionado', 8, 12.50)
    ]
    cursor.executemany("INSERT INTO categorias_bens (nome_categoria, vida_util_anos, taxa_depreciacao_anual) VALUES (?, ?, ?)", categorias)

# Gerar Bens Patrimoniais
cursor.execute("SELECT COUNT(*) FROM bens_patrimoniais")
if cursor.fetchone()[0] == 0:
    np.random.seed(42)
    bens_exemplos = [
        ('Notebook Dell Latitude 5420', 1, 4800.00),
        ('MacBook Pro 16"', 1, 14500.00),
        ('Monitor Dell 27" 4K', 1, 2200.00),
        ('Servidor Rack PowerEdge', 1, 35000.00),
        ('Cadeira Ergonômica Herman Miller', 2, 6500.00),
        ('Mesa Reunião Oval 8 Lugares', 2, 4200.00),
        ('Furgão Renault Kangoo', 3, 85000.00),
        ('Veículo Fiat Strada Hard Working', 3, 72000.00),
        ('Gerador de Energia 50kVA', 4, 45000.00),
        ('Sistema de Ar Condicionado VRF 60k BTU', 5, 18000.00)
    ]
    
    bens_list = []
    for i in range(1, 201):
        tag = f"PAT-{200000 + i}"
        item, cat_id, val_orig = bens_exemplos[i % len(bens_exemplos)]
        # Idade aleatória entre 1 e 4 anos
        anos_uso = np.random.randint(1, 5)
        dt_aquisicao = (datetime.now() - timedelta(days=anos_uso*365)).strftime('%Y-%m-%d')
        # Calcular depreciação simples
        val_atual = max(val_orig * (1 - (anos_uso * 0.15)), val_orig * 0.2)
        unidade_atual = np.random.randint(1, 7)
        status = np.random.choice(['Em Uso', 'Em Uso', 'Em Uso', 'Em Trânsito', 'Manutenção'])
        bens_list.append((tag, f"{item} #{i}", cat_id, dt_aquisicao, round(val_orig, 2), round(val_atual, 2), unidade_atual, status))
    
    cursor.executemany('''
    INSERT INTO bens_patrimoniais 
    (tombamento_tag, descricao_bem, id_categoria, data_aquisicao, valor_aquisicao, valor_atual, id_unidade_atual, status_bem) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', bens_list)

# Gerar Histórico de Transferências
cursor.execute("SELECT COUNT(*) FROM transferencias_patrimonio")
if cursor.fetchone()[0] == 0:
    motivos = [
        'Reorganização Departamental', 
        'Substituição de Equipamento', 
        'Abertura de Nova Filial', 
        'Manutenção Centralizada', 
        'Redistribuição de Frota'
    ]
    responsaveis = ['Carlos Eduardo (Patrimônio)', 'Mariana Souza (Logística)', 'Roberto Alves (TI)', 'Fernanda Lima (Facilities)']
    status_transf = ['Concluida', 'Concluida', 'Concluida', 'Em Transito', 'Cancelada', 'Pendente']
    
    transf_list = []
    for i in range(1, 151):
        id_bem = np.random.randint(1, 201)
        origem = np.random.randint(1, 7)
        destino = np.random.choice([u for u in range(1, 7) if u != origem])
        
        # Datas nos últimos 12 meses
        dias_atras = np.random.randint(5, 360)
        dt_sol = datetime.now() - timedelta(days=dias_atras)
        st = np.random.choice(status_transf, p=[0.70, 0.05, 0.05, 0.10, 0.05, 0.05])
        
        if st == 'Concluida':
            dias_envio = np.random.randint(1, 3)
            dias_transito = np.random.randint(1, 10)
            dt_env = dt_sol + timedelta(days=dias_envio)
            dt_rec = dt_env + timedelta(days=dias_transito)
            t_transito = dias_transito
        elif st == 'Em Transito':
            dt_env = dt_sol + timedelta(days=1)
            dt_rec = None
            t_transito = (datetime.now() - dt_env).days

        else:
            dt_env = None
            dt_rec = None
            t_transito = None
            
        transf_list.append((
            id_bem, origem, destino, 
            dt_sol.strftime('%Y-%m-%d %H:%M:%S'),
            dt_env.strftime('%Y-%m-%d %H:%M:%S') if dt_env else None,
            dt_rec.strftime('%Y-%m-%d %H:%M:%S') if dt_rec else None,
            t_transito, st, np.random.choice(motivos), np.random.choice(responsaveis)
        ))
        
    cursor.executemany('''
    INSERT INTO transferencias_patrimonio 
    (id_bem, id_unidade_origem, id_unidade_destino, data_solicitacao, data_envio, data_recebimento, tempo_transito_dias, status_transferencia, motivo_transferencia, responsavel_solicitacao)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', transf_list)

conn.commit()

# Exportar também uma visão tratada em CSV para fácil importação no Power BI / Excel
df_relatorio = pd.read_sql_query('''
SELECT 
    t.id_transferencia,
    b.tombamento_tag AS tag_patrimonio,
    b.descricao_bem,
    c.nome_categoria AS categoria,
    b.valor_aquisicao,
    b.valor_atual,
    u1.nome_unidade AS unidade_origem,
    u1.estado AS uf_origem,
    u2.nome_unidade AS unidade_destino,
    u2.estado AS uf_destino,
    t.data_solicitacao,
    t.data_envio,
    t.data_recebimento,
    t.tempo_transito_dias,
    t.status_transferencia,
    t.motivo_transferencia,
    t.responsavel_solicitacao
FROM transferencias_patrimonio t
JOIN bens_patrimoniais b ON t.id_bem = b.id_bem
JOIN categorias_bens c ON b.id_categoria = c.id_categoria
JOIN filiais_unidades u1 ON t.id_unidade_origem = u1.id_unidade
JOIN filiais_unidades u2 ON t.id_unidade_destino = u2.id_unidade
''', conn)

csv_path = os.path.join(data_dir, "relatorio_transferencias_patrimonio.csv")
df_relatorio.to_csv(csv_path, index=False, encoding='utf-8-sig')

conn.close()
print("✅ Banco SQLite e Relatório CSV de Gestão Patrimonial criados com sucesso!")
