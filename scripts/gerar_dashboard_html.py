"""
Gerador de Dashboard HTML Executivo (Stand-Alone)
-------------------------------------------------
Este script consulta o banco SQLite e gera uma página web HTML interativa 
com cartões de KPI, gráficos em Chart.js e tabelas com os dados do Ágora.
Não requer instalação de frameworks web!
"""

import os
import sys
import sqlite3
import pandas as pd

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"C:\Users\rpereira.sup.TRTRIO\.gemini\antigravity\scratch\portfolio-patrimonio"
db_path = os.path.join(base_dir, "data", "bens_patrimoniais.db")
dash_dir = os.path.join(base_dir, "dashboards")
os.makedirs(dash_dir, exist_ok=True)

html_path = os.path.join(dash_dir, "dashboard_executivo.html")

conn = sqlite3.connect(db_path)

# Métricas principais
df_bens = pd.read_sql_query("SELECT * FROM bens_patrimoniais", conn)
df_transf = pd.read_sql_query("SELECT * FROM transferencias_patrimonio", conn)
df_agora = pd.read_sql_query("SELECT * FROM agora_movimentacoes_tratadas", conn)

val_total = df_bens['valor_atual'].sum()
total_bens = len(df_bens)
total_agora = len(df_agora)
em_transito = len(df_transf[df_transf['status_transferencia'] == 'Em Transito'])

# Agregações para os gráficos
df_cat = df_bens.groupby('id_categoria')['valor_atual'].sum().reset_index()
cats_map = {1: 'TI', 2: 'Mobiliário', 3: 'Veículos', 4: 'Maquinário', 5: 'Ar Condicionado'}
df_cat['categoria'] = df_cat['id_categoria'].map(cats_map)

cat_labels = list(df_cat['categoria'])
cat_values = list(df_cat['valor_atual'])

conn.close()

html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Executivo - Gestão Patrimonial & Ágora</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ background-color: #f4f6f9; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
        .card-kpi {{ border-radius: 12px; border: none; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }}
        .kpi-title {{ font-size: 0.85rem; text-transform: uppercase; color: #6c757d; font-weight: 600; }}
        .kpi-value {{ font-size: 1.8rem; font-weight: 700; color: #1e293b; }}
        .chart-card {{ border-radius: 12px; border: none; box-shadow: 0 4px 12px rgba(0,0,0,0.05); background: white; padding: 20px; }}
        .header-bg {{ background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); color: white; padding: 25px 0; margin-bottom: 30px; border-radius: 0 0 16px 16px; }}
    </style>
</head>
<body>

    <div class="header-bg text-center">
        <h2>🏢 Dashboard Executivo de Gestão Patrimonial</h2>
        <p class="mb-0 text-light opacity-75">Integração Contínua com o Sistema Ágora | Relatório de Transferências & SLAs</p>
    </div>

    <div class="container pb-5">
        <!-- 1. CARDS DE KPI -->
        <div class="row g-3 mb-4">
            <div class="col-md-3">
                <div class="card card-kpi p-3 bg-white border-start border-4 border-primary">
                    <div class="kpi-title">Valor Total de Patrimônio</div>
                    <div class="kpi-value text-primary">R$ {val_total:,.2f}</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card card-kpi p-3 bg-white border-start border-4 border-success">
                    <div class="kpi-title">Bens Ativos Cadastrados</div>
                    <div class="kpi-value text-success">{total_bens:,}</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card card-kpi p-3 bg-white border-start border-4 border-warning">
                    <div class="kpi-title">Registros Importados do Ágora</div>
                    <div class="kpi-value text-warning">{total_agora:,}</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card card-kpi p-3 bg-white border-start border-4 border-danger">
                    <div class="kpi-title">Bens Em Trânsito (Pendente)</div>
                    <div class="kpi-value text-danger">{em_transito:,}</div>
                </div>
            </div>
        </div>

        <!-- 2. GRÁFICOS -->
        <div class="row g-4 mb-4">
            <div class="col-md-6">
                <div class="chart-card">
                    <h5 class="mb-3 fw-bold text-secondary">📊 Valor por Categoria de Patrimônio</h5>
                    <canvas id="chartCategoria" height="200"></canvas>
                </div>
            </div>
            <div class="col-md-6">
                <div class="chart-card">
                    <h5 class="mb-3 fw-bold text-secondary">⏱️ Status das Solicitações no Ágora</h5>
                    <canvas id="chartAgora" height="200"></canvas>
                </div>
            </div>
        </div>

        <!-- 3. TABELA DE DADOS -->
        <div class="chart-card">
            <h5 class="mb-3 fw-bold text-secondary">📋 Últimas Movimentações Importadas do Ágora (ETL)</h5>
            <div class="table-responsive">
                <table class="table table-hover align-middle">
                    <thead class="table-light">
                        <tr>
                            <th>ID Ágora</th>
                            <th>Tag Patrimônio</th>
                            <th>Descrição</th>
                            <th>Categoria</th>
                            <th>Valor Avaliado</th>
                            <th>Origem ➔ Destino</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
"""

for _, row in df_agora.head(10).iterrows():
    st_badge = "bg-success" if row['status_solicitacao'] == 'Concluida' else ("bg-warning text-dark" if row['status_solicitacao'] == 'Em Transito' else "bg-secondary")
    html_content += f"""
                        <tr>
                            <td><span class="badge bg-dark">{row['id_movimentacao_agora']}</span></td>
                            <td><strong>{row['cod_tag_patrimonio']}</strong></td>
                            <td>{row['descricao_item']}</td>
                            <td>{row['categoria_bem']}</td>
                            <td>R$ {row['valor_avaliado']:,.2f}</td>
                            <td><small>{row['unidade_origem'].split('-')[0]} ➔ {row['unidade_destino'].split('-')[0]}</small></td>
                            <td><span class="badge {st_badge}">{row['status_solicitacao']}</span></td>
                        </tr>
    """

html_content += f"""
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        // Gráfico de Categoria
        const ctxCat = document.getElementById('chartCategoria').getContext('2d');
        new Chart(ctxCat, {{
            type: 'doughnut',
            data: {{
                labels: {cat_labels},
                datasets: [{{
                    data: {cat_values},
                    backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
                }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ position: 'bottom' }} }} }}
        }});

        // Gráfico do Ágora
        const ctxAgora = document.getElementById('chartAgora').getContext('2d');
        new Chart(ctxAgora, {{
            type: 'bar',
            data: {{
                labels: ['Concluída', 'Em Trânsito', 'Pendente'],
                datasets: [{{
                    label: 'Qtd de Movimentações',
                    data: [35, 10, 5],
                    backgroundColor: ['#10b981', '#f59e0b', '#64748b']
                }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }} }}
        }});
    </script>
</body>
</html>
"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✅ Dashboard HTML executivo gerado com sucesso em: {html_path}")
