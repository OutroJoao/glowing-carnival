# Agente Autónomo de Gestão Condominial - Guia Completo

## 1. Introdução

O **Agente de Gestão Condominial** é um assistente de inteligência artificial que funciona como um **secretário automático** para condomínios residenciais em Portugal. Funciona 24 horas por dia, 7 dias por semana, gerando comunicação, registando problemas, controlando quotas e mantendo a organização do condomínio.

Este agente utiliza **Claude**, uma inteligência artificial avançada desenvolvida pela Anthropic, integrada com **Gmail** e **Google Sheets** para uma gestão completa e autónoma.

---

## 2. O Que o Agent Faz

### 2.1 Funcionalidades Principais

#### **A. Gestão de Comunicação**

O agent lê e responde a emails automaticamente:

**Exemplo 1: Pergunta sobre quota**
```
📧 Email recebido de: joao@example.com
Assunto: "Quando vence a quota de março?"

Agent analisa → Entende que é pergunta comum → Responde automaticamente

Resposta:
"Olá João,

A quota de março tem vencimento em 31/03/2024.

Poderá realizar o pagamento através de transferência bancária:
- IBAN: [informação condomínio]
- Referência: Apto 101 - Março 2024

Se pagar até 7 dias após o vencimento, não há multa.
Para dúvidas adicionais, contacte o administrador.

Cumprimentos,
Agente de Gestão Condominial"
```

**Exemplo 2: Aviso de incidência**
```
📧 Email recebido de: maria@example.com
Assunto: "Fuga de água no apartamento 102"

Agent analisa → Detecta incidência urgente → Registra + Responde

Resposta automática:
"Olá Maria,

Recebemos o seu relato de fuga de água no apartamento 102.

📌 Incidência registada com PRIORIDADE ALTA
📅 Data: 29/03/2024 10:30
🔧 Status: Aberta - À espera de técnico

Será contactada em breve pelo administrador para agendar reparação.
Enquanto isso, recomendamos fechar a torneira principal para evitar danos.

Cumprimentos,
Agente de Gestão Condominial"
```

#### **B. Rastreamento de Incidências**

Todas as avarias, problemas e manutenções são registadas automaticamente:

```
DATA: 29/03/2024
RESIDENTE: Maria Santos
APARTAMENTO: 102
INCIDÊNCIA: Fuga de água na cozinha
PRIORIDADE: Alta
STATUS: Aberta
NOTAS: Contactado encanador - aguardando resposta
```

O agent:
- ✅ Registra a incidência na base de dados
- ✅ Atribui prioridade (Baixa, Normal, Alta)
- ✅ Acompanha o estado (Aberta, Em Progresso, Fechada)
- ✅ Notifica o administrador
- ✅ Segue até resolução

#### **C. Controlo de Quotas**

O agent verifica automaticamente **quotas atrasadas**:

**Diariamente:**
1. Lê a folha de quotas
2. Identifica quotas atrasadas (>30 dias)
3. Prepara lembrete amável
4. Envia email ao residente
5. Registra ação na base de dados

**Exemplo de lembrete:**
```
📧 Para: pedro@example.com
Assunto: Lembrete - Quota de Fevereiro em atraso

Prezado Pedro,

Verificámos que a sua quota relativa a Fevereiro de 2024 permanece 
em atraso.

APARTAMENTO: 301
VALOR: 150,00€
VENCIMENTO: 28/02/2024
ATRASO: 30 dias

Por favor, proceda ao pagamento assim que possível.
Pode transferir para:
- IBAN: [informação]
- Referência: Apto 301 - Fevereiro 2024

Se já realizou o pagamento, ignore este aviso.

Cumprimentos,
Agente de Gestão Condominial
```

#### **D. Avisos e Circulares**

O agent distribui automaticamente avisos importantes:

```
📧 Assunto: AVISO IMPORTANTE - Manutenção de elevador

Prezados Residentes,

Informamos que será realizada manutenção preventiva do elevador nos 
próximos dias:

📅 DATA: 05 a 07 de Abril de 2024
⏰ HORÁRIO: 09h00 - 13h00
🏢 AFETADOS: Apartamentos 102-301

Durante este período, o elevador estará indisponível. Solicitamos 
a máxima compreensão.

Para emergências, contactar administrador.

Cumprimentos,
Agente de Gestão Condominial
```

---

## 3. Formas de Interação

### 3.1 Fase 1: Email (Atual)

**Residentes podem:**

#### A. Fazer Perguntas
```
Para: condominio@example.com
Assunto: Dúvida sobre a quota

Olá,

Gostaria de saber se posso pagar a quota em duas vezes.

Obrigado,
João Silva
Apto 101
```

**Agent responde em minutos** com informação precisa.

#### B. Relatar Problemas
```
Para: condominio@example.com
Assunto: Avaria - Luz da escada

A luz da escada entre o 2º e 3º andar não funciona.
Pode alguém reparar?

Obrigado,
Maria - Apto 201
```

**Agent:**
- ✅ Regista incidência
- ✅ Atribui prioridade (Baixa neste caso)
- ✅ Confirma ao morador
- ✅ Notifica técnico/administrador

#### C. Solicitar Informações
```
Para: condominio@example.com
Assunto: Informações sobre visitas

Posso receber visitantes? Há alguma regra?

Cumprimentos,
Carlos - Apto 301
```

**Agent fornece informações** do regulamento condominial.

---

### 3.2 Fase 2: WhatsApp Privado (Próximo)

Residentes poderão **conversar diretamente** com o agent:

```
👤 João Silva
💬 "Olá, qual é a data de vencimento da minha quota?"

🤖 Agent
"Olá João! 

Sua quota de Março vence em 31/03/2024.
Pode verificar o histórico de pagamentos em qualquer momento.

Tem mais alguma dúvida?"

👤 João Silva
"E se pagar atrasado, há multa?"

🤖 Agent
"Sim, há multa de 5% se pagar mais de 7 dias após o vencimento.
Mas não se preocupe - pode contactar o administrador para 
negociar em casos de dificuldade."
```

**Vantagens do WhatsApp:**
- Mais rápido que email
- Conversas informais e naturais
- Disponível 24/7
- Melhor para emergências

---

### 3.3 Fase 3: WhatsApp Grupo (Futuro)

O agent **participa silenciosamente** no grupo de residentes:

```
👥 Grupo: Condomínio - Avisos e Dúvidas

👤 Maria
"Alguém sabe quando é a próxima assembleia?"

🤖 Agent
"A próxima assembleia está marcada para 20/04/2024, às 19h00.
Local: Hall do edifício.

Será discutido: Obras de manutenção e aumento de despesas comuns.
Convocatória em anexo."

👤 Pedro
"E se não consigo ir?"

🤖 Agent
"Pode enviar procuração ou justificação para:
condominio@example.com

Prazo: até 19/04/2024"
```

**Comportamento do Agent no grupo:**
- Só responde quando **mencionado** (@agent)
- Detecta **emergências** (fogo, inundação, etc.)
- Interrompe para **avisso urgente**
- Caso contrário, **fica silencioso**

---

## 4. Base de Dados

### 4.1 Folha de Residentes

```
| Nome | Apartamento | Email | Telefone | Data Inscrição |
|------|-------------|-------|----------|----------------|
| João Silva | 101 | joao@example.com | 918888888 | 15/01/2024 |
| Maria Santos | 102 | maria@example.com | 919999999 | 15/01/2024 |
| Carlos Oliveira | 201 | carlos@example.com | 916666666 | 01/02/2024 |
```

**O que o agent faz com isto:**
- ✅ Identifica residentes
- ✅ Envia comunicações personalizadas
- ✅ Mantém histórico de contactos
- ✅ Organiza por apartamento

### 4.2 Folha de Quotas

```
| Residente | Apartamento | Valor | Vencimento | Status | Mês |
|-----------|-------------|-------|-----------|--------|-----|
| João Silva | 101 | 150€ | 31/03/2024 | Paga | Mar/2024 |
| Maria Santos | 102 | 150€ | 31/03/2024 | Atrasada | Mar/2024 |
| Carlos Oliveira | 201 | 150€ | 31/03/2024 | Pendente | Mar/2024 |
```

**Status possíveis:**
- **Paga**: Quota já foi pagada ✅
- **Pendente**: Ainda não venceu ou não foi paga ⏳
- **Atrasada**: Passou data vencimento sem pagamento ⚠️

### 4.3 Folha de Incidências

```
| Data | Residente | Descrição | Prioridade | Status | Notas |
|------|-----------|-----------|-----------|--------|-------|
| 29/03 | Maria | Fuga de água | Alta | Aberta | Encanador contactado |
| 25/03 | João | Luz avariada | Baixa | Aberta | À espera técnico |
| 20/03 | Carlos | Campainha | Normal | Fechada | Reparado em 22/03 |
```

**Estados de incidência:**
- **Aberta**: Problema registado, sem início de reparação
- **Em Progresso**: Técnico a trabalhar no problema
- **Fechada**: Problema resolvido

---

## 5. Fluxo de Trabalho Completo

### Cenário: Um Morador Relata uma Avaria

```
1️⃣ MORADOR ENVIA EMAIL
   Hora: 10:30 de quarta-feira
   
   "Olá, a minha torneira está com fuga!"

2️⃣ AGENT RECEBE E PROCESSA
   ✅ Lê o email
   ✅ Identifica o remetente (João Silva, Apto 101)
   ✅ Detecta problema: fuga de água
   ✅ Determina prioridade: ALTA (urgente!)

3️⃣ AGENT REGISTRA INCIDÊNCIA
   Cria registo na base de dados:
   - Data: 29/03/2024 10:30
   - Residente: João Silva
   - Descrição: Torneira com fuga na cozinha
   - Prioridade: Alta
   - Status: Aberta

4️⃣ AGENT RESPONDE AO MORADOR
   Envia email automático:
   "Recebemos sua avaria com prioridade ALTA.
    Será contactado em 24h.
    Enquanto isso, feche a torneira principal."

5️⃣ AGENT NOTIFICA ADMINISTRADOR
   Envia sumário do dia:
   "Nova incidência ALTA: Fuga de água, Apto 101.
    Ação necessária: Contactar encanador."

6️⃣ ACOMPANHAMENTO AUTOMÁTICO
   Agent verifica diariamente:
   - Está resolvido?
   - Passou mais de 48h?
   - Precisa de follow-up?

7️⃣ ADMIN RESOLVE
   Admin contacta técnico, problema fica resolvido.
   Admin marca como "Fechada" na base de dados.

8️⃣ CONFIRMAÇÃO AUTOMÁTICA
   Agent envia ao morador:
   "Sua avaria foi reparada. Satisfeito com o serviço?"
```

---

## 6. Comportamento e Personalidade

### 6.1 Tom de Comunicação

O agent sempre comunica:

**✅ Profissional mas amigável**
```
"Prezado João,
Recebemos sua dúvida..."
```

**❌ Não: Muito formal**
```
"Estimado Senhor Silva,
Conforme solicitação supracitada..."
```

**❌ Não: Muito casual**
```
"Oi João! Tudo bem? Sua quota é..."
```

### 6.2 Regras Éticas

O agent **NUNCA**:

1. ❌ **Apaga dados** - Tudo fica registado (auditoria)
2. ❌ **Contacta fornecedores** - Só com aprovação admin
3. ❌ **Faz decisões financeiras** - Admin decide tudo
4. ❌ **Partilha dados pessoais** - Confidencialidade rigorosa
5. ❌ **Toma decisões em votações** - Residentes decidem

O agent **SEMPRE**:

1. ✅ **Registra tudo** - Sem exceções
2. ✅ **É honesto** - Não promete o que não pode cumprir
3. ✅ **Escalona quando necessário** - Admin é sempre consultado
4. ✅ **Respeita privacidade** - Segredos seguros
5. ✅ **Confirma ações** - "Vai eu fazer isto?"

---

## 7. Exemplos de Conversas Reais

### Exemplo 1: Pergunta Simples

```
📧 De: ana@example.com
Assunto: Horário de reunião

Quando é a próxima assembleia?

---

📧 Resposta automática:
Prezada Ana,

A próxima assembleia está marcada para:
📅 20 de Abril de 2024
⏰ 19h00
📍 Hall do edifício principal

Tópicos a discutir:
- Manutenção preventiva do elevador
- Revisão do orçamento anual
- Propostas dos residentes

Participação é importante! Se não conseguir estar presente, 
pode enviar procuração.

Cumprimentos,
Agente de Gestão Condominial
```

### Exemplo 2: Incidência Urgente

```
📧 De: carlos@example.com
Assunto: URGENTE - Fogo no apartamento!

Há fogo no andar 2!

---

🚨 Agent detecta EMERGÊNCIA:

✅ IMEDIATAMENTE:
- Não responde normalmente (é emergência!)
- Envia para admin e polícia/bombeiros automaticamente
- Marca como CRÍTICA na base de dados

✅ Resposta:
"EMERGÊNCIA DETECTADA - FOGO
Contactámos automaticamente:
- Admin: [número]
- Polícia: 112
- Bombeiros: 112

SAIA DO EDIFÍCIO IMEDIATAMENTE
Aguarde ajuda no exterior."
```

### Exemplo 3: Reclamação com Feedback

```
📧 De: pedro@example.com
Assunto: Reclamação - Falta de limpeza

A escada está muito suja. Pode mandar limpar?

---

📧 Resposta automática:
Prezado Pedro,

Registámos sua reclamação sobre limpeza da escada.

📌 Incidência: Manutenção - Limpeza
👤 Responsável: Equipa de limpeza
📅 Prazo: 3 dias úteis
📌 Status: Aberta

Será verificado se já foi agendada limpeza. Caso contrário, 
solicitaremos à equipa que actue com prioridade.

Agradeço o feedback. A qualidade do condomínio depende de 
reportes como este.

Cumprimentos,
Agente de Gestão Condominial
```

---

## 8. Vantagens Para Diferentes Utilizadores

### Para o **Administrador**

```
✅ Menos emails para ler (agent filtra)
✅ Menos dúvidas repetitivas (agent responde)
✅ Tudo registado automaticamente
✅ Relatórios diários/semanais
✅ Alertas sobre situações urgentes
✅ Mais tempo para decisões importantes
```

**Exemplo de relatório diário:**
```
📊 RELATÓRIO - 29/03/2024

✉️ EMAILS: 12 recebidos
  - 7 respondidos automaticamente
  - 3 com dúvidas comuns (quotas, regras)
  - 2 incidências para revisão

🔧 INCIDÊNCIAS ABERTAS: 5
  - 2 Alta prioridade (água, eletricidade)
  - 3 Normal/Baixa

💰 QUOTAS: 2 em atraso (>30 dias)
  - Maria Santos (Apto 102)
  - Pedro Ferreira (Apto 301)
  - Lembretes já enviados

⚠️ AÇÕES PENDENTES:
  - Fuga de água (Apto 102) - contactar encanador
  - Reparação luz (Apto 201) - técnico confirmou agenda para amanhã
```

### Para o **Residente**

```
✅ Respostas em segundos, não horas
✅ Disponibilidade 24/7
✅ Sem necessidade de telefonar
✅ Confirmação automática de reclamações
✅ Acesso a informações importantes
✅ Tranquilidade que tudo está registado
```

### Para o **Técnico/Fornecedor**

```
✅ Informações de contacto claras
✅ Descrição detalha da avaria
✅ Histórico de problemas do apartamento
✅ Prioridade definida
✅ Confirmação de conclusão automática
```

---

## 9. Tecnologia Por Trás

### 9.1 Componentes

**1. Inteligência Artificial (Claude)**
- Entende português natural
- Toma decisões baseadas em contexto
- Aprende padrões de comunicação

**2. Gmail**
- Recebe emails de residentes
- Envia respostas automáticas
- Integração total

**3. Google Sheets**
- Base de dados dos residentes
- Registo de quotas
- Histórico de incidências
- Tudo sincronizado

**4. Servidor (VPS)**
- Agent roda 24/7
- Verifica emails automaticamente
- Executa tarefas agendadas
- Mantém tudo atualizado

### 9.2 Fluxo de Dados

```
📧 Gmail
  ↓
🤖 Agent (Claude AI)
  ↓
📊 Google Sheets
  ↓
📧 Gmail (resposta)
```

---

## 10. Segurança e Privacidade

### 10.1 Proteção de Dados

```
✅ Encriptação em trânsito (HTTPS)
✅ Credenciais seguras (OAuth 2.0)
✅ Sem armazenamento de senhas
✅ Acesso limitado a dados necessários
✅ Auditoria completa de ações
✅ Conformidade com GDPR
```

### 10.2 Quem Pode Ver O Quê?

```
📊 GOOGLE SHEETS (dados compartilhados)
├── Admin: Vê tudo
├── Residentes: Veem próprios dados (depois de implementar)
└── Público: Nada

📧 EMAILS (dados privados)
├── Admin: Vê resumos
├── Residentes: Veem próprios emails
└── Public: Nada
```

---

## 11. Casos de Uso Reais

### Caso 1: Condomínio Com 50 Apartamentos

**Sem Agent:**
```
- Admin gasta 3h/dia lendo emails
- Responde 30 emails por dia (manualmente)
- Muitos emails esquecidos
- Dados desorganizados em ficheiros
- Dificuldade em rastrear problemas
```

**Com Agent:**
```
- Admin gasta 30 min/dia
- Agent responde 200 emails por dia
- Nenhum email esquecido
- Base de dados automática e organizada
- Todos os problemas rastreados
- Relatórios automáticos
```

### Caso 2: Morador Precisa Resolver Problema Rápido

**Sem Agent:**
```
10:00 - Morador descobre fuga
10:05 - Tenta telefonar admin (não atende)
10:30 - Tenta novamente (atende, "pode ser amanhã?")
11:00 - Morador stressado, já há poça de água
```

**Com Agent:**
```
10:00 - Morador envia email
10:01 - Agent responde e registra como URGENTE
10:02 - Admin recebe alerta (urgência!)
10:15 - Admin contacta técnico
10:30 - Técnico chegou
```

---

## 12. Próximas Etapas

### Fase 1: Email ✅ (Atual)
- Residentes comunicam por email
- Agent responde automaticamente
- Tudo fica registado

### Fase 2: WhatsApp Privado ⏳ (1-2 semanas)
- Residentes conversam com agent no WhatsApp
- Mais rápido e intuitivo
- Mesma inteligência que email

### Fase 3: WhatsApp Grupo 📅 (3-4 semanas)
- Agent participa no grupo de residentes
- Silencioso normalmente, interrompe quando relevante
- Bloqueia emergências

### Fase 4: Dashboard Admin 📅 (Mês 2)
- Admin vê tudo em painel visual
- Gráficos de quotas
- Timeline de incidências
- Estatísticas de comunicação

---

## 13. Quanto Custa?

### Custos Estimados

```
💰 Claude API: ~10€/mês (mil emails/dia)
💰 VPS (servidor): ~5€/mês
💰 Google Sheets: Grátis (até limite generoso)
💰 Gmail: Grátis (usando conta condomínio)

TOTAL: ~15€/mês (~0,30€ por apartamento em 50 apto)
```

### ROI (Retorno do Investimento)

```
Antes:
- Admin: 3h/dia × 20€/h = 60€/dia = 1200€/mês em tempo

Depois:
- Admin: 30min/dia × 20€/h = 10€/dia = 200€/mês em tempo
- Agent: 15€/mês

ECONOMIA: 1200 - 200 - 15 = 985€/mês!
```

---

## 14. Perguntas Frequentes

**P: Agent consegue aprender com o tempo?**
R: Sim! Quanto mais interações, melhor compreende o padrão de comunicação.

**P: E se o servidor cair?**
R: Tem backup automático. Emails ficam em fila até servidor voltar.

**P: Posso usar com outro email (não Gmail)?**
R: Agora só Gmail. Mas está planeado Outlook/ProtonMail em futuro.

**P: Agent consegue fazer videochamadas?**
R: Não. Só email e WhatsApp (texto). Voz é para futuro.

**P: E se morador quer falar com pessoa real?**
R: Agent oferece opção "falar com admin" em qualquer resposta.

---

## 15. Resumo Final

O **Agente de Gestão Condominial** é uma solução moderna que:

✅ **Automatiza** comunicação repetitiva  
✅ **Organiza** dados de forma eficiente  
✅ **Acelera** respostas a residentes  
✅ **Reduz** carga administrativa  
✅ **Melhora** satisfação de residentes  
✅ **Economiza** dinheiro e tempo  

Está pronto para ser **testado com um grupo de amigos** e depois colocado em produção num condomínio real! 🚀

---

**Próximo passo:** Fornecer credenciais Google para conectar a dados reais e fazer testes práticos com amigos.

Tem dúvidas? Quer saber mais sobre alguma funcionalidade? 🤔
