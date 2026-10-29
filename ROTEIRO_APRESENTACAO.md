# Roteiro de Apresentação — Atividade 2
> DAST, IaC e Observabilidade · ~10 minutos cronometrados

---

## ⏱️ Cronômetro geral

| Bloco | Tempo | Duração |
|---|---|---|
| 1 — Contexto | 0:00 – 0:40 | 40s |
| 2 — Módulo 4: DAST | 0:40 – 3:10 | 2min30 |
| 3 — Módulo 5: IaC | 3:10 – 5:40 | 2min30 |
| 4 — Módulo 6: Observabilidade | 5:40 – 8:10 | 2min30 |
| 5 — Workflows ao vivo | 8:10 – 9:20 | 1min10 |
| 6 — Fechamento e trade-off | 9:20 – 10:00 | 40s |

---

## 1) Contexto — 40s

**Abrir:** [`README_ATIVIDADE2.md`](./README_ATIVIDADE2.md)

**Falar:**
> "A Atividade 1 fechou o ciclo estático: SAST, SCA e hardening de container.
> Agora fechamos o ciclo dinâmico: a aplicação sobe dentro do pipeline e é atacada pelo ZAP,
> a infraestrutura passa pelo mesmo rigor do código, e um ataque real é detectado nos logs
> e tratado por um runbook."

---

## 2) Módulo 4 — DAST e Pipeline (2min30)

### Correção de XSS e sinks

| O que mostrar | Arquivo e linha |
|---|---|
| Parâmetro `q` da busca seguro | [`app_fixed_dast.py:142`](./app_fixed_dast.py#L142) |
| Mensagem de erro do login renderizada com autoescape | [`app_fixed_dast.py:126`](./app_fixed_dast.py#L126) |
| Template sem uso de `\| safe` | [`templates/tasks.html:16`](./templates/tasks.html#L16) |

### Endpoint de debug removido

| O que mostrar | Arquivo e linha |
|---|---|
| `/debug/info` inexistente (removido) | [`app_fixed_dast.py:182`](./app_fixed_dast.py#L182) |

### DAST no pipeline

| O que mostrar | Arquivo e linha |
|---|---|
| Build da imagem | [`.github/workflows/dast.yml:22`](./.github/workflows/dast.yml#L22) |
| Subida do container | [`.github/workflows/dast.yml:25`](./.github/workflows/dast.yml#L25) |
| Espera ativa pelo `/login` | [`.github/workflows/dast.yml:27`](./.github/workflows/dast.yml#L27) |
| Execução do ZAP Baseline | [`.github/workflows/dast.yml:41`](./.github/workflows/dast.yml#L41) |
| Upload do relatório como artefato | [`.github/workflows/dast.yml:50`](./.github/workflows/dast.yml#L50) |

### Regras e mapeamento

| O que mostrar | Arquivo e linha |
|---|---|
| Regras ZAP justificadas | [`.zap/rules.tsv:1`](./.zap/rules.tsv#L1) |
| Achados antes × depois + OWASP Top 10 | [`docs/dast.md:14`](./docs/dast.md#L14) |

**Falar:**
> "Mostramos prevenção de XSS no código e validação automática no pipeline,
> com evidência de relatório e regras justificadas."

---

## 3) Módulo 5 — Segurança em IaC (2min30)

### Docker Compose seguro

| O que mostrar | Arquivo e linha |
|---|---|
| Redes `frontend` e `backend` isoladas | [`docker-compose.yml:16`](./docker-compose.yml#L16) |
| `read_only: true` | [`docker-compose.yml:18`](./docker-compose.yml#L18) |
| `no-new-privileges` | [`docker-compose.yml:22`](./docker-compose.yml#L22) |
| Healthcheck | [`docker-compose.yml:23`](./docker-compose.yml#L23) |
| Limites de CPU e memória | [`docker-compose.yml:31`](./docker-compose.yml#L31) |
| Segredos versionados só como exemplo | [`.env.example`](./.env.example) |

### Terraform corrigido

| O que mostrar | Arquivo e linha |
|---|---|
| Versionamento do bucket | [`infra/main.tf:52`](./infra/main.tf#L52) |
| Criptografia | [`infra/main.tf:59`](./infra/main.tf#L59) |
| Bloqueio de acesso público | [`infra/main.tf:69`](./infra/main.tf#L69) |
| Logging | [`infra/main.tf:78`](./infra/main.tf#L78) |
| Security Group restrito por `allowed_ip_cidr` | [`infra/main.tf:93`](./infra/main.tf#L93) |
| Justificativas dos `#checkov:skip` | [`infra/main.tf:15`](./infra/main.tf#L15) |

### Gates Checkov + Trivy

| O que mostrar | Arquivo e linha |
|---|---|
| Job Checkov | [`.github/workflows/iac-scan.yml:21`](./.github/workflows/iac-scan.yml#L21) |
| Trivy config com `exit-code 1` | [`.github/workflows/iac-scan.yml:39`](./.github/workflows/iac-scan.yml#L39) |

**Falar:**
> "IaC recebeu o mesmo rigor do código, com endurecimento da configuração
> e bloqueio automático no CI."

---

## 4) Módulo 6 — Observabilidade e Resposta a Incidente (2min30)

### Logging estruturado e `request_id`

| O que mostrar | Arquivo e linha |
|---|---|
| `request_id` gerado por requisição | [`app_instrumented.py:33`](./app_instrumented.py#L33) |
| Evento `login_failed` (sem senha nos logs) | [`app_instrumented.py:146`](./app_instrumented.py#L146) |
| Evento `tasks_list` | [`app_instrumented.py:178`](./app_instrumented.py#L178) |
| Evento `task_created` | [`app_instrumented.py:198`](./app_instrumented.py#L198) |
| Middleware `http_response` | [`app_instrumented.py:61`](./app_instrumented.py#L61) |

### Stack Grafana + Loki + Promtail

| O que mostrar | Arquivo e linha |
|---|---|
| Serviço Loki | [`docker-compose.observabilidade.yml:14`](./docker-compose.observabilidade.yml#L14) |
| Serviço Promtail | [`docker-compose.observabilidade.yml:24`](./docker-compose.observabilidade.yml#L24) |
| Serviço Grafana | [`docker-compose.observabilidade.yml:37`](./docker-compose.observabilidade.yml#L37) |

### Consultas LogQL e runbook

| O que mostrar | Arquivo e linha |
|---|---|
| Queries LogQL documentadas | [`docs/observabilidade.md:15`](./docs/observabilidade.md#L15) |
| Runbook — Preparação | [`docs/runbook-login-bruteforce.md:10`](./docs/runbook-login-bruteforce.md#L10) |
| Runbook — Detecção/Análise | [`docs/runbook-login-bruteforce.md:14`](./docs/runbook-login-bruteforce.md#L14) |
| Runbook — Contenção | [`docs/runbook-login-bruteforce.md:19`](./docs/runbook-login-bruteforce.md#L19) |
| Runbook — Erradicação/Recuperação | [`docs/runbook-login-bruteforce.md:24`](./docs/runbook-login-bruteforce.md#L24) |
| Evidência da simulação + query usada | [`docs/observabilidade.md:30`](./docs/observabilidade.md#L30) |

**Falar:**
> "A esteira valida higiene dos logs e a demo mostra a detecção real do ataque
> via query do runbook."

---

## 5) Execução das esteiras ao vivo (1min10)

**Abrir GitHub Actions:** https://github.com/danielarrais/taskflow-devsecops/actions

| Workflow | Arquivo |
|---|---|
| DAST | [`.github/workflows/dast.yml`](./.github/workflows/dast.yml) |
| IaC Scan | [`.github/workflows/iac-scan.yml`](./.github/workflows/iac-scan.yml) |
| Observability Smoke | [`.github/workflows/observability-smoke.yml`](./.github/workflows/observability-smoke.yml) |

**Mostrar:**
- Runs verdes nos três workflows
- Artefato do relatório ZAP (baixar ao vivo)
- Log do smoke de observabilidade

---

## 6) Fechamento e trade-off (40s)

**Falar:**
> "Nossa decisão foi manter gates estritos em segurança e justificar exceções no código —
> nunca silenciar com `continue-on-error` ou `--exit-zero`.
> O trade-off é claro: mais segurança e rastreabilidade versus maior esforço de manutenção
> de regras e evidências. Custo que vale pela garantia de que nenhum PR inseguro entra na main."

### Se o professor perguntar sobre brute force no CI

> "O CI valida a qualidade e higiene dos logs.
> A simulação de incidente é executada como cenário operacional guiado por runbook,
> evidenciada em documentação e prints.
> Isso separa validação automática de pipeline da resposta operacional de incidente."

---

## ✅ Checklist pré-apresentação

- [ ] Pipeline verde no último commit da `main`
- [ ] Relatório ZAP baixado e aberto localmente (plano B)
- [ ] Stack de observabilidade subindo: `docker compose -f docker-compose.observabilidade.yml up -d`
- [ ] Grafana acessível em http://localhost:3000
- [ ] Query de brute force retornando resultado no Grafana
- [ ] Screenshot da detecção no Grafana salvo em `docs/evidencias/`
- [ ] `terraform validate` passando em `infra/`
- [ ] Todos os membros sabem qual bloco apresentam

---

## 🗂️ Mapa completo de arquivos

```
taskflow-devsecops/
├── app_fixed_dast.py                        # Módulo 4: XSS corrigido, sem /debug/info
├── app_instrumented.py                      # Módulo 6: logging JSON + request_id
├── docker-compose.yml                       # Módulo 5: compose seguro (app)
├── docker-compose.observabilidade.yml       # Módulo 6: Grafana + Loki + Promtail
├── .env.example                             # Módulo 5: template de variáveis (sem valores reais)
├── .zap/
│   └── rules.tsv                            # Módulo 4: regras ZAP justificadas
├── infra/
│   └── main.tf                              # Módulo 5: Terraform corrigido
├── .github/workflows/
│   ├── ci.yml                               # Atividade 1: lint + testes
│   ├── sast.yml                             # Atividade 1: Semgrep + Gitleaks
│   ├── sca.yml                              # Atividade 1: pip-audit + Trivy fs
│   ├── container.yml                        # Atividade 1: build + Trivy image
│   ├── dast.yml                             # Módulo 4: ZAP Baseline
│   ├── iac-scan.yml                         # Módulo 5: Checkov + Trivy config
│   └── observability-smoke.yml              # Módulo 6: smoke da stack
└── docs/
    ├── dast.md                              # Módulo 4: antes × depois + OWASP Top 10
    ├── observabilidade.md                   # Módulo 6: queries LogQL + evidência simulação
    ├── runbook-login-bruteforce.md          # Módulo 6: 4 fases NIST SP 800-61
    └── hardening.md                         # Atividade 1: Trivy/docker history antes × depois
```

---

## ⚠️ Armadilhas a evitar (do PDF)

| Risco | Como evitar |
|---|---|
| ZAP atacando o nada (app não subiu ainda) | Espera ativa com `curl --retry` antes do scan |
| Gate de DAST desligado (`continue-on-error: true`) | Nunca suprimir — corrigir ou justificar no `rules.tsv` |
| `iac-scan.yml` com `paths:` travando PRs sem `.tf` | Rodar sempre, sem filtro de path, documentar no README |
| Senha nos logs (`request.form` inteiro) | Logar apenas `username`, nunca `password` |
| Runbook genérico sem query real | A query do runbook deve ser a mesma usada no Grafana durante a simulação |
| `.env` commitado com valores reais | Confirmar `.env` no `.gitignore` antes de qualquer push |
