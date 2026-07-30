# 🏢 Análise & Controle de Transferências de Bens Patrimoniais (Integrado ao Sistema Ágora)

![Status do Projeto](https://img.shields.io/badge/Status-Conclu%C3%ADdo-brightgreen)
![Tecnologias](https://img.shields.io/badge/Tech-Python%20%7C%20SQL%20%7C%20DBeaver%20%7C%20ETL-blue)
![Integração](https://img.shields.io/badge/Integra%C3%A7%C3%A3o-Sistema%20%C3%81gora-orange)

---

## 📌 1. Contexto do Negócio

A empresa utiliza o **Sistema Ágora** como ERP oficial de registro das movimentações patrimoniais entre filiais. No entanto, os relatórios gerados pelo Ágora são em arquivos **CSV/Excel soltos**, dificultando a consolidação das informações para a diretoria.

O objetivo deste projeto foi criar um **Pipeline de Dados (ETL)** em Python que lê automaticamente os relatórios exportados pelo Ágora, trata e limpa os dados (datas, tipos de valores e identificadores), armazena tudo em um banco de dados SQL (`bens_patrimoniais.db`) e fornece **dashboards e consultas analíticas para tomada de decisão**.

---

## ⚙️ 2. Arquitetura da Solução & Pipeline ETL

```text
[ Relatório CSV/Excel do Ágora ]
              │
              ▼
 [ Pipeline ETL Python (pandas) ]
  • Padronização de Colunas
  • Tratamento de Tipos e Datas
  • Validação de Tags de Patrimônio
              │
              ▼
[ Banco Analítico SQLite / DBeaver ]
  • Tabela: agora_movimentacoes_tratadas
  • Tabela: transferencias_patrimonio
              │
              ▼
 [ Dashboards & Relatórios Executivos ]
```

---

## 🎯 3. Perguntas de Negócio Respostas

1. Quantas movimentações de bens foram registradas no sistema Ágora no último ciclo?
2. Qual é o valor total de patrimônio em trânsito entre a Matriz e as filiais?
3. Quais filiais demoram mais tempo (SLA) para confirmar o recebimento do patrimônio enviados pelo Ágora?

---

## 📊 4. Principais Insights Descobertos

### 💡 Insight 1: Automação da Carga do Ágora
- O pipeline em Python reduz o tempo de preparação de dados de **4 horas semanais de Excel manual** para **poucos segundos de execução automatizada**.

### 💡 Insight 2: Concentração de Chamados e Movimentações
- **70% das solicitações registradas no Ágora** referem-se à categoria de *Equipamentos de TI* (notebooks, monitores e servidores), impulsionadas pelo modelo de trabalho híbrido.

---

## 📂 5. Estrutura do Repositório

```text
portfolio-patrimonio/
├── exportacoes_agora/
│   └── movimentacoes_agora_export.csv       # Arquivo CSV exportado do sistema Ágora
├── data/
│   ├── bens_patrimoniais.db                  # Banco de dados SQLite com dados do Ágora
│   └── relatorio_transferencias_patrimonio.csv
├── scripts/
│   ├── pipeline_ingestao_agora.py            # Pipeline ETL de Ingestão do Ágora em Python
│   ├── gerar_banco_patrimonio.py             # Carga inicial do banco de dados
│   └── queries_analiticas.sql                # Consultas SQL para DBeaver
└── README.md                                 # Documentação oficial do projeto
```

---

## 🏃 Como Executar o Pipeline do Ágora

1. Execute o script de ingestão em Python:
   ```bash
   python scripts/pipeline_ingestao_agora.py
   ```
2. Abra o **DBeaver** ➔ Conectar em `data/bens_patrimoniais.db`.
3. Abra a **Consulta 1** no script `scripts/queries_analiticas.sql` para ver os dados do Ágora na tabela `agora_movimentacoes_tratadas`.

---

👤 **Autor:** [Renato da Silva Pereira]  
📧 **Contato:** [renato.n2.trt@gmail.com] | [LinkedIn](https://linkedin.com/in/renato-silva-pereira-analisededados)
