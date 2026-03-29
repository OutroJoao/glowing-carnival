# Arquitetura - Agente de Gestão Condominial

## Visão Geral

```
┌─────────────────────────────────────────────────────────────────┐
│                   Claude Agent (Anthropic)                       │
│  - Raciocínio e decisões autónomas                              │
│  - Orquestração de ferramentas                                  │
│  - Linguagem natural (Português)                                │
└──────────────────────┬──────────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
   ┌────────────┐ ┌──────────────┐ ┌──────────────┐
   │   Gmail    │ │Google Sheets │ │  (Future)    │
   │    MCP     │ │     MCP      │ │ WhatsApp MCP │
   └────────────┘ └──────────────┘ └──────────────┘
        │              │              │
        ▼              ▼              ▼
   ┌────────────┐ ┌──────────────┐ ┌──────────────┐
   │ Gmail API  │ │ Sheets API   │ │  WhatsApp-   │
   │ (Google)   │ │  (Google)    │ │  web.js      │
   └────────────┘ └──────────────┘ └──────────────┘
        │              │              │
        ▼              ▼              ▼
   ┌────────────┐ ┌──────────────┐ ┌──────────────┐
   │Condominium │ │Residents DB  │ │ WhatsApp     │
   │Email Box   │ │Incidents DB  │ │ Service      │
   │            │ │Quotas DB     │ │              │
   └────────────┘ └──────────────┘ └──────────────┘
```

## Componentes Principais

### 1. Agente Principal (`src/agent/main.py`)

**Responsabilidades:**
- Gerenciar conversas com utilizadores
- Orquestrar chamadas de ferramentas (MCP)
- Processar respostas da API Claude
- Executar tarefas proativas

**Métodos Principais:**
- `run_conversation()`: Executa uma volta de conversa
- `run_interactive()`: Interface interativa
- `process_tool_call()`: Delegação de ferramentas
- `check_overdue_quotas()`: Tarefa proativa
- `check_open_incidents()`: Tarefa proativa
- `process_emails()`: Tarefa proativa

### 2. MCP Servers

#### Gmail MCP (`src/mcp_servers/gmail_server.py`)

**Ferramentas Disponíveis:**
- `send_email`: Enviar email
- `read_emails`: Ler emails (com filtros)
- `reply_to_email`: Responder em thread
- `mark_as_read`: Marcar como lido

**Cliente Subjacente:** `src/tools/gmail_tools.py`

#### Google Sheets MCP (`src/mcp_servers/sheets_server.py`)

**Ferramentas Disponíveis:**
- `read_sheet`: Ler dados de uma sheet
- `write_sheet`: Escrever dados numa sheet
- `append_row`: Adicionar linha
- `get_residents`: Obter lista de residentes
- `get_overdue_quotas`: Quotas atrasadas
- `log_incident`: Registar incidente
- `get_incidents`: Obter incidentes com filtro

**Cliente Subjacente:** `src/tools/sheets_tools.py`

### 3. Ferramentas de Integração

#### Gmail Tools (`src/tools/gmail_tools.py`)

Classe `GmailClient`:
- Autenticação OAuth 2.0
- Gestão de credenciais (token.json)
- Métodos para operações Gmail
- Parsing de mensagens

#### Sheets Tools (`src/tools/sheets_tools.py`)

Classe `SheetsClient`:
- Autenticação OAuth 2.0
- Leitura/escrita de dados
- Métodos de negócio (residentes, quotas, incidentes)
- Parsing de estruturas de dados

### 4. Configuração (`src/config/settings.py`)

**Gerencia:**
- Variáveis de ambiente (.env)
- Caminhos de ficheiros
- IDs de Google Sheets
- Informações de autenticação

**Usa:** `pydantic-settings`

### 5. System Prompt (`src/agent/system_prompt.py`)

Define a personalidade e comportamento do agente:
- Restrições críticas (não apagar dados, etc.)
- Responsabilidades principais
- Padrões de comunicação
- Comportamento proativo

## Fluxo de Execução

### Conversa Típica

```
1. Utilizador digita mensagem
   ↓
2. Agent.run_conversation(mensagem)
   ↓
3. Claude analisa mensagem + context
   ↓
4. Claude identifica ferramentas necessárias
   ↓
5. Agent.process_tool_call() para cada ferramenta
   ↓
6. Gmail/Sheets executam ações
   ↓
7. Resultados devolvidos ao Claude
   ↓
8. Claude formula resposta final
   ↓
9. Resposta exibida ao utilizador
```

### Tarefa Proativa Típica

```
1. Agendador (cron job) dispara
   ↓
2. Agent.check_overdue_quotas()
   ↓
3. Conversa interna com Claude:
   - "Verifica quotas atrasadas"
   ↓
4. Claude chama get_overdue_quotas
   ↓
5. Sheets API retorna dados
   ↓
6. Claude analisa e processa:
   - Identifica pendências
   - Formata emails
   ↓
7. Claude chama send_email para cada
   ↓
8. Gmail API envia emails
   ↓
9. Log gravado em Sheets
```

## Fluxos de Dados

### Leitura de Dados

```
Agent → MCP Server → Google API Client → Google Cloud → Sheet
                                        ↓
                                    Response (JSON)
                                        ↓
Google API Client → Parser → MCP Server → Agent → Claude
```

### Escrita de Dados

```
Claude → Agent → MCP Server → Google API Client → Google Cloud → Sheet
                                                       ↓
                                                    Confirmation
                                                       ↓
Google API Client → MCP Server → Agent → Claude
```

## Segurança

### Autenticação
- OAuth 2.0 para Google APIs
- Tokens armazenados localmente (token.json)
- Credenciais em variáveis de ambiente

### Autorização
- Agente restringido por system prompt
- Não pode fazer ações financeiras
- Não pode contactar fornecedores sem aprovação
- Não pode apagar dados

### Auditoria
- Todas as ações registadas em Sheets
- Logs estruturados
- Rastreabilidade completa

## Escalabilidade Futura

### Fase 2: WhatsApp Privado
- Novo MCP: `whatsapp_server.py`
- Cliente: `whatsapp_tools.py` (whatsapp-web.js)
- Interface: Conversas diretas com residentes

### Fase 3: WhatsApp Grupo
- Agente como membro silencioso
- Detecção de incidentes
- Intervenção inteligente

### Fase 4: Produção
- Meta Cloud API (substituir whatsapp-web.js)
- Dashboard administrativo
- Google Calendar API
- Votações interativas
- Relatórios automáticos

## Tecnologias

| Componente | Tecnologia | Versão |
|-----------|-----------|--------|
| Agent SDK | claude-agent-sdk | 0.1.0+ |
| LLM | Claude (API) | Opus 4.6 |
| Email | Gmail API | v1 |
| Sheets | Google Sheets API | v4 |
| Auth | OAuth 2.0 | Google |
| Config | pydantic | 2.0+ |
| Logging | Python logging | Built-in |

## Performance Considerada

- Chamadas de API são síncronas (pode paralelizar em V2)
- Cache de dados (residentes, quotas) pode reduzir latência
- Agendamento de tarefas proativas fora de pico
- Batch processing para múltiplos emails
