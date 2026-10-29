# Runbook — Tentativas de login por força bruta

**Referência:** NIST SP 800-61 Rev. 2  
**Severidade inicial:** média; elevar para alta se houver login bem-sucedido após as falhas.  
**Responsável:** pessoa de plantão; o líder do incidente coordena comunicação e evidências.

## Condição de disparo

Mais de **10 eventos `login_failed` do mesmo IP em 5 minutos**. A detecção usa:

```logql
sum by (remote_addr) (count_over_time({job="taskflow"} | json | event="login_failed" [5m])) > 10
```

## 1. Preparação

- Manter contatos, acesso ao Grafana e mecanismo de bloqueio de IP testados.
- Sincronizar relógios e preservar logs do Loki por sete dias.
- Nunca copiar senha, cookie ou token para chamado, chat ou relatório.
- Deixar o script `scripts/simular-forca-bruta.sh` restrito ao laboratório.

## 2. Detecção e análise

1. Executar a query da condição de disparo e registrar IP, janela e contagem.
2. Correlacionar pelo `request_id` e procurar `login_succeeded` após as falhas.
3. Verificar erros HTTP e comportamento de tarefas no mesmo período.
4. Classificar: sem sucesso = tentativa; sucesso posterior = possível comprometimento.
5. Preservar query, horário UTC, resultado JSON e captura do Grafana.

## 3. Contenção, erradicação e recuperação

**Contenção imediata:** bloquear temporariamente o IP no proxy/firewall, aplicar rate
limit no `/login` e monitorar IPs relacionados. Evitar apagar containers ou logs antes
de preservar evidências.

**Erradicação:** se houver sucesso suspeito, encerrar sessões, redefinir a senha da conta,
revisar tarefas criadas e identificar a origem da credencial. Corrigir a causa (senha
fraca, ausência de rate limit ou credencial reutilizada), não apenas o indicador.

**Recuperação:** remover o bloqueio somente após a janela de observação, validar login
legítimo, confirmar métricas normais e manter monitoramento reforçado por 24 horas.

## 4. Atividades pós-incidente

- Registrar linha do tempo, impacto, decisões, responsáveis e evidências.
- Comparar tempo de detecção, contenção e recuperação com os objetivos do grupo.
- Criar ações para rate limiting, MFA e melhoria de alertas, com responsável e prazo.
- Atualizar este runbook e repetir a simulação para comprovar a melhoria.

## Encerramento da simulação acadêmica

A simulação termina quando a query detecta o limiar, o grupo percorre as quatro fases,
confirma que nenhum dado sensível foi registrado e salva a evidência descrita em
[`observabilidade.md`](observabilidade.md).
