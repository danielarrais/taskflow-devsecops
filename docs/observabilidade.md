# Observabilidade da TaskFlow

## Arquitetura

A aplicação escreve um objeto JSON por linha em `stdout`. Promtail descobre apenas o
container TaskFlow, interpreta o envelope `json-file` do Docker, extrai `event`,
`request_id` e `remote_addr` e envia os registros ao Loki. O Grafana consulta o Loki
pela rede interna `backend`; somente Grafana, TaskFlow e Loki ficam publicados em
loopback para a demonstração local.

Nenhum evento registra senha, token, cookie, cabeçalho Authorization ou o conteúdo
integral de `request.form`. O `request_id` também é devolvido no cabeçalho
`X-Request-ID`, permitindo correlacionar a resposta com o log.

## Consultas LogQL usadas pelo grupo

### 1. Falhas de login por IP nos últimos cinco minutos

```logql
sum by (remote_addr) (count_over_time({job="taskflow"} | json | event="login_failed" [5m]))
```

Pergunta respondida: **qual IP está tentando autenticar repetidamente?** O runbook é
disparado quando um IP supera 10 falhas em cinco minutos.

### 2. Linha do tempo de uma requisição

```logql
{job="taskflow"} | json | request_id="COLE_O_REQUEST_ID"
```

Pergunta respondida: **quais eventos pertencem à mesma requisição?**

### 3. Criação e listagem de tarefas

```logql
{job="taskflow"} | json | event=~"task_created|tasks_list"
```

Pergunta respondida: **a aplicação continuou operando normalmente durante o incidente?**

### 4. Respostas HTTP com erro

```logql
{job="taskflow"} | json | event="http_response" | status >= 400
```

Pergunta respondida: **houve aumento de erros HTTP no mesmo intervalo?**

## Simulação de força bruta

1. Suba a stack: `docker compose up -d --build --wait`.
2. Execute: `scripts/simular-forca-bruta.sh http://127.0.0.1:5000/login 20 admin`.
3. Abra `http://127.0.0.1:3000`, acesse **Explore → Loki** e execute a consulta 1.
4. Confirme valor maior que 10 para o IP do cliente.
5. Percorra as quatro fases em [`runbook-login-bruteforce.md`](runbook-login-bruteforce.md).
6. Salve a captura em `docs/evidencias/atividade2/grafana-login-bruteforce.png`.

### Evidência executada

Em 29/10/2026, o grupo executou 20 tentativas inválidas. A consulta do runbook
retornou 20 eventos para `172.23.0.1`, sem senha nos logs. Evidências:

- [Captura real do painel Grafana](evidencias/atividade2/grafana-login-bruteforce.png)
- [Resultado JSON consultado no Loki](evidencias/atividade2/observabilidade-login-failed.json)
- [Logs da stack usados na verificação de higiene](evidencias/atividade2/observabilidade-stack.log)

O workflow `observability-smoke.yml` também gera 12 falhas, confirma que
`login_failed` chegou ao Loki e reprova se a senha usada no teste aparecer nos logs.
O artefato `observability-smoke` preserva o JSON consultado e os logs da stack.

## Checklist de evidência

- [x] Stack com TaskFlow, Promtail, Loki e Grafana saudável
- [x] Script de simulação executado
- [x] Query de detecção retornando mais de 10 falhas por IP
- [x] `request_id` presente nos registros
- [x] Senha, token e cookie ausentes
- [x] Captura do Grafana armazenada como plano B
- [ ] Runbook percorrido pelo grupo durante o ensaio da apresentação
