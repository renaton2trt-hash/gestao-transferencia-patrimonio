# 🚀 Guia Passo a Passo: Do Zero ao Portfólio no GitHub (Gestão Patrimonial)

Este guia ensina como rodar seu novo projeto real de **Controle de Transferências de Bens Patrimoniais** no **DBeaver**, testar as consultas SQL e publicá-lo no seu **GitHub**!

---

## 📌 Passo 1: Conectar o DBeaver ao Novo Banco de Dados

1. Abra o **DBeaver Community**.
2. Clique no ícone da tomada com o **`+` colorido** (Nova Conexão) no canto superior esquerdo (ou pressione `Ctrl + Shift + N`).
3. Escolha **SQLite** e clique em **Avançar**.
4. No campo **Caminho do Arquivo (Path)**, clique em **Navegar...** e selecione o arquivo:
   `C:\Users\rpereira.sup.TRTRIO\.gemini\antigravity\scratch\portfolio-patrimonio\data\bens_patrimoniais.db`
5. Clique em **Testar Conexão...** e depois em **Concluir**.

---

## 📌 Passo 2: Executar as Consultas SQL no DBeaver

1. Clique com o botão direito na nova conexão `bens_patrimoniais.db` no DBeaver e selecione **Criar ➔ Editor SQL** (`Ctrl + ]`).
2. Abra o arquivo de queries localizado em:
   [scripts/queries_analiticas.sql](file:///C:/Users/rpereira.sup.TRTRIO/.gemini/antigravity/scratch/portfolio-patrimonio/scripts/queries_analiticas.sql)
3. Copie as consultas para a tela do DBeaver e pressione **`Ctrl + Enter`** para executar.

---

## 📌 Passo 3: Criar o Repositório no GitHub e Publicar

1. Acesse o seu [GitHub](https://github.com) e clique no botão verde **New** para criar um novo repositório.
2. Nomeie o repositório como: `gestao-transferencia-patrimonio`.
3. Mantenha a opção **Public** marcada e clique em **Create repository**.
4. No terminal da pasta do seu projeto (`C:\Users\rpereira.sup.TRTRIO\.gemini\antigravity\scratch\portfolio-patrimonio`), execute os comandos:

```bash
git init
git add .
git commit -m "feat: projeto inicial de controle de transferencias patrimoniais"
git branch -M main
git remote add origin https://github.com/seu-usuario/gestao-transferencia-patrimonio.git
git push -u origin main
```

*(Ou suba os arquivos diretamente clicando em **Upload files** na página do repositório no GitHub).*
