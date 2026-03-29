# Agente Autónomo de Gestão Condominial

Um agente de IA autónomo (usando Claude Agent SDK) para gerenciar um condomínio residencial em Portugal.

## Objetivo

Construir um sistema que atue proativamente para:
- Gerenciar avisos e comunicados
- Rastrear incidentes e avarias
- Monitorar quotas e pagamentos
- Gerir votações e assembleias
- Coordenar fornecedores

## Tecnologia

- **Claude Agent SDK** (Python)
- **Gmail API** para comunicação por email
- **Google Sheets** para dados de residentes, incidentes e quotas
- **Google Calendar** para eventos (Fase 4)
- **WhatsApp Business API** (Fase 2+)

## Estrutura do Projeto

```
├── src/
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── system_prompt.py
│   ├── mcp_servers/
│   │   ├── __init__.py
│   │   ├── gmail_server.py
│   │   └── sheets_server.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── gmail_tools.py
│   │   └── sheets_tools.py
│   └── config/
│       ├── __init__.py
│       └── settings.py
├── credentials.json (gitignored)
├── token.json (gitignored)
├── .env
├── requirements.txt
└── README.md
```

## Fase 1: Configuração

### 1. Dependências

```bash
pip install -r requirements.txt
```

### 2. Credenciais do Google

1. Crie um projeto no [Google Cloud Console](https://console.cloud.google.com)
2. Ative as APIs: Gmail, Google Sheets, Google Calendar
3. Crie credenciais OAuth 2.0 (Desktop App)
4. Salve as credenciais em `credentials.json`

### 3. Variáveis de Ambiente

```bash
cp .env.example .env
# Editar .env com valores reais
```

### 4. Executar o Agente

```bash
python -m src.agent.main
```

## Funcionalidades (Fase 1)

- ✅ Ler/escrever em Google Sheets (residentes, incidentes, quotas)
- ✅ Enviar e receber emails via Gmail
- ✅ Rastrear quotas atrasadas
- ✅ Responder automaticamente
- ⏳ Sistema de logs de ações

## Próximas Fases

- Fase 2: WhatsApp privado
- Fase 3: WhatsApp grupo
- Fase 4: Meta Cloud API, votações interativas, dashboard admin
