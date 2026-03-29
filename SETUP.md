# Guia de Configuração - Fase 1

## Pré-requisitos

- Python 3.11+
- Conta Google (para Gmail e Google Sheets)
- Projeto criado no Google Cloud Console

## Passo 1: Instalação de Dependências

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Passo 2: Configurar Google Cloud Project

### 2.1 Criar Projeto
1. Aceda a [Google Cloud Console](https://console.cloud.google.com)
2. Crie um novo projeto (ex: "Condomínio Gestão")

### 2.2 Ativar APIs
1. No painel de pesquisa, procure **Gmail API**
   - Clique em "Ativar"
2. Procure **Google Sheets API**
   - Clique em "Ativar"
3. Procure **Google Calendar API** (para futuras fases)
   - Clique em "Ativar"

### 2.3 Criar Credenciais OAuth
1. Vá a **Credenciais** no menu esquerdo
2. Clique em **Criar Credenciais** → **ID de Cliente OAuth**
3. Selecione **Aplicação de Desktop**
4. Clique em "Criar"
5. Clique no botão de download para descarregar o JSON
6. Renomeie o ficheiro para `credentials.json` e coloque na raiz do projeto

## Passo 3: Configurar Variáveis de Ambiente

```bash
cp .env.example .env
```

Edite `.env` e preencha:
- `ANTHROPIC_API_KEY`: Sua chave da API Anthropic
- `GMAIL_SENDER_ADDRESS`: Email do condomínio
- `RESIDENTS_SHEET_ID`: ID da sheet de residentes
- `INCIDENTS_SHEET_ID`: ID da sheet de incidentes
- `QUOTAS_SHEET_ID`: ID da sheet de quotas

### Como Obter IDs de Sheets

1. Abra a sheet no Google Sheets
2. O ID está na URL: `https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit`
3. Copie apenas a parte entre `/d/` e `/edit`

## Passo 4: Criar as Google Sheets

### 4.1 Sheet de Residentes

Crie uma nova sheet com as colunas:
- `Nome`
- `Apartamento`
- `Email`
- `Telefone`
- `Data Inscrição`

### 4.2 Sheet de Incidentes

Colunas:
- `Data`
- `Residente`
- `Descrição`
- `Prioridade` (Baixa, Normal, Alta)
- `Status` (Aberta, Em Progresso, Fechada)
- `Notas`

### 4.3 Sheet de Quotas

Colunas:
- `Residente`
- `Apartamento`
- `Valor` (€)
- `Data Vencimento`
- `Status` (Paga, Pendente, Atrasada)
- `Mês/Ano`

## Passo 5: Autenticação Inicial

Execute o agente pela primeira vez:

```bash
python -m src.agent.main
```

Na primeira execução:
- Uma janela do navegador abrirá
- Inicie sessão com sua conta Google
- Conceda as permissões solicitadas
- Um token será guardado em `token.json`

## Passo 6: Primeiro Teste

No modo interativo, experimente:

```
Você: Quantos residentes temos na base de dados?
```

O agente deverá:
1. Ler a sheet de residentes
2. Contar os registos
3. Responder com o número

## Troubleshooting

### Erro: "Credentials file not found"
- Verifique se `credentials.json` está na raiz do projeto
- Certifique-se de que descarregou o ficheiro correto do Google Cloud Console

### Erro: "Invalid spreadsheet ID"
- Verifique se copiou o ID completo e correto da URL
- Certifique-se de que compartilhou a sheet com o email do OAuth

### Erro: "The caller does not have permission"
- Vá ao Google Cloud Console
- Verifique se as APIs estão ativadas
- Tente criar novas credenciais OAuth

### Erro de autenticação Gmail
- Elimine `token.json`
- Execute o agente novamente para reauthenticar
- Se usar 2FA, verifique se criou uma "app password"

## Próximos Passos

Após validar que tudo funciona:
1. Configurar cron jobs para execução periódica
2. Implementar logging persistente
3. Preparar Phase 2 (WhatsApp)

## Recursos Úteis

- [Gmail API Docs](https://developers.google.com/gmail/api)
- [Google Sheets API Docs](https://developers.google.com/sheets/api)
- [Claude Agent SDK Docs](https://github.com/anthropics/claude-agent-sdk)
