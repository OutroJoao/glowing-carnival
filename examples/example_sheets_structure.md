# Estrutura de Exemplo das Google Sheets

## Sheet: Residentes

| Nome | Apartamento | Email | Telefone | Data Inscrição |
|------|-------------|-------|----------|------------------|
| João Silva | 101 | joao@email.com | 918888888 | 2024-01-15 |
| Maria Santos | 102 | maria@email.com | 919999999 | 2024-01-15 |
| Carlos Oliveira | 201 | carlos@email.com | 916666666 | 2024-02-01 |
| Ana Costa | 202 | ana@email.com | 917777777 | 2024-02-01 |
| Pedro Ferreira | 301 | pedro@email.com | 915555555 | 2024-03-01 |

## Sheet: Incidentes

| Data | Residente | Descrição | Prioridade | Status | Notas |
|------|-----------|-----------|-----------|--------|-------|
| 2024-03-25 | João Silva | Torneira com fuga na cozinha | Normal | Aberta | Contactado encanador, aguardando resposta |
| 2024-03-20 | Maria Santos | Infiltração no teto da sala | Alta | Em Progresso | Obra já iniciada pelo pedreiro João |
| 2024-03-10 | Carlos Oliveira | Luz da escada com avaria | Baixa | Aberta | Registado, agendado para próxima semana |
| 2024-03-15 | Ana Costa | Campainha não funciona | Normal | Fechada | Reparado em 2024-03-22 |

## Sheet: Quotas

| Residente | Apartamento | Valor (€) | Data Vencimento | Status | Mês/Ano |
|-----------|-------------|-----------|-----------------|--------|---------|
| João Silva | 101 | 150.00 | 2024-03-10 | Paga | Março 2024 |
| Maria Santos | 102 | 150.00 | 2024-03-10 | Atrasada | Março 2024 |
| Carlos Oliveira | 201 | 150.00 | 2024-03-10 | Pendente | Março 2024 |
| Ana Costa | 202 | 150.00 | 2024-03-10 | Paga | Março 2024 |
| Pedro Ferreira | 301 | 150.00 | 2024-03-10 | Atrasada | Março 2024 |
| João Silva | 101 | 150.00 | 2024-04-10 | Pendente | Abril 2024 |
| Maria Santos | 102 | 150.00 | 2024-04-10 | Pendente | Abril 2024 |

## Notas Importantes

- Mantenha o cabeçalho (primeira linha) consistente
- Use datas no formato ISO: YYYY-MM-DD
- Use valores numéricos para o campo Valor
- Status devem ser exatamente: "Paga", "Pendente", "Atrasada"
- Prioridades: "Baixa", "Normal", "Alta"
- Status de incidentes: "Aberta", "Em Progresso", "Fechada"
