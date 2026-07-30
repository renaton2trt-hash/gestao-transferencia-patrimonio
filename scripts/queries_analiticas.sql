-- ====================================================================
-- PROJETO: Controle de Transferências de Bens Patrimoniais
-- OBJETIVO: Consultas Analíticas para Diagnóstico Operacional e Logístico
-- INTEGRADO COM O SISTEMA ÁGORA
-- ====================================================================

-- 1. DADOS IMPORTADOS DO SISTEMA ÁGORA (ETL AUTOMÁTICO VIA CSV/EXCEL)
-- Consulta a tabela de dados brutos e tratados vindos do relatório do Ágora.
SELECT 
    id_movimentacao_agora AS id_agora,
    cod_tag_patrimonio AS tag,
    descricao_item,
    categoria_bem,
    valor_avaliado,
    unidade_origem,
    unidade_destino,
    status_solicitacao,
    data_registro_agora,
    data_ingestao_pipeline
FROM agora_movimentacoes_tratadas
ORDER BY data_registro_agora DESC
LIMIT 20;


-- 2. VISÃO GERAL DE TODAS AS TRANSFERÊNCIAS (HISTÓRICO INTERNO)
SELECT 
    t.id_transferencia,
    b.tombamento_tag AS tag,
    b.descricao_bem,
    u1.nome_unidade AS origem,
    u2.nome_unidade AS destino,
    t.status_transferencia,
    t.data_solicitacao
FROM transferencias_patrimonio t
JOIN bens_patrimoniais b ON t.id_bem = b.id_bem
JOIN filiais_unidades u1 ON t.id_unidade_origem = u1.id_unidade
JOIN filiais_unidades u2 ON t.id_unidade_destino = u2.id_unidade
ORDER BY t.id_transferencia DESC
LIMIT 20;


-- 3. VALOR TOTAL E QUANTIDADE DE BENS POR FILIAL/UNIDADE
SELECT 
    u.nome_unidade,
    u.estado AS uf,
    u.centro_custo,
    COUNT(b.id_bem) AS qtd_bens,
    ROUND(SUM(b.valor_aquisicao), 2) AS valor_total_aquisicao,
    ROUND(SUM(b.valor_atual), 2) AS valor_total_atual
FROM bens_patrimoniais b
JOIN filiais_unidades u ON b.id_unidade_atual = u.id_unidade
GROUP BY u.nome_unidade, u.estado, u.centro_custo
ORDER BY valor_total_atual DESC;


-- 4. TEMPO MÉDIO DE TRÂNSITO (SLA DE LOGÍSTICA) POR ROTA
SELECT 
    u1.nome_unidade AS origem,
    u2.nome_unidade AS destino,
    COUNT(t.id_transferencia) AS qtd_transferencias,
    ROUND(AVG(t.tempo_transito_dias), 1) AS media_dias_transito,
    MAX(t.tempo_transito_dias) AS max_dias_transito
FROM transferencias_patrimonio t
JOIN filiais_unidades u1 ON t.id_unidade_origem = u1.id_unidade
JOIN filiais_unidades u2 ON t.id_unidade_destino = u2.id_unidade
WHERE t.status_transferencia = 'Concluida'
GROUP BY u1.nome_unidade, u2.nome_unidade
ORDER BY media_dias_transito DESC;


-- 5. BENS EM TRÂNSITO (PENDÊNCIAS DE ENTREGA)
SELECT 
    t.id_transferencia,
    b.tombamento_tag AS tag,
    b.descricao_bem,
    c.nome_categoria,
    b.valor_atual,
    u1.nome_unidade AS origem,
    u2.nome_unidade AS destino,
    t.data_envio,
    t.tempo_transito_dias AS dias_em_transito,
    t.status_transferencia
FROM transferencias_patrimonio t
JOIN bens_patrimoniais b ON t.id_bem = b.id_bem
JOIN categorias_bens c ON b.id_categoria = c.id_categoria
JOIN filiais_unidades u1 ON t.id_unidade_origem = u1.id_unidade
JOIN filiais_unidades u2 ON t.id_unidade_destino = u2.id_unidade
WHERE t.status_transferencia = 'Em Transito' OR t.status_transferencia LIKE '%Transito%'
ORDER BY t.tempo_transito_dias DESC;
