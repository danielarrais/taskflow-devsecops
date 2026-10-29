# DAST — ZAP Baseline

## Estratégia

O workflow [`dast.yml`](../.github/workflows/dast.yml) builda `Dockerfile.dast`, sobe a
TaskFlow corrigida no próprio runner, aguarda `/healthz` responder e só então executa o
ZAP Baseline. Em seguida, cria uma fixture XSS autenticada e roda um active scan
direcionado a `/tasks`. Isso mantém o Baseline exigido e permite demonstrar que remover
o autoescape realmente reprova o PR com as regras `40012` e `40014`. Os exit codes são
preservados, os relatórios saem mesmo em falha e qualquer alerta não aceito deixa o job
vermelho.

Não usamos `continue-on-error`, `-I` ou `--exit-zero`. As exceções ficam em
[`rules.tsv`](../.zap/rules.tsv), são específicas por plugin e trazem a justificativa
junto à regra. Elas cobrem limitações do alvo HTTP local e falsos positivos verificados,
sem ignorar as regras de XSS `40012` e `40014` usadas no gate.

## Antes × depois e OWASP Top 10

| Achado original | Categoria OWASP Top 10 (2021) | Correção | Resultado esperado |
|---|---|---|---|
| XSS armazenado no título/descrição | A03 — Injection | Renderização em Jinja2 com autoescape, sem `safe` | payload exibido como texto |
| XSS refletido no parâmetro `q` | A03 — Injection | variável de template com autoescape | nenhum script executado |
| Mensagem de login como sink HTML | A03 — Injection | mensagem fixa renderizada pelo template | nenhum HTML não confiável |
| `/debug/info` público | A05 — Security Misconfiguration | rota removida | resposta 404 |
| Debug ligado | A05 — Security Misconfiguration | `FLASK_DEBUG=0` e Gunicorn | debugger indisponível |
| Cabeçalhos ausentes | A05 — Security Misconfiguration | CSP, X-Frame-Options, nosniff e Referrer-Policy | alertas eliminados |

HSTS permanece fora da aplicação porque TLS termina no proxy reverso em produção. O
runner acessa a aplicação por HTTP em loopback; aplicar HSTS ali produziria uma evidência
enganosa. A exceção é documentada, limitada ao plugin `10035` e não desativa o gate.

### Evidência executada

Em 29/10/2026, o ZAP foi executado nas duas versões:

| Versão | PASS | WARN | FAIL | Exit code |
|---|---:|---:|---:|---:|
| Linha de base (`origin/main` anterior à Atividade 2) | 60 | 8 | 0 | 2 |
| Aplicação corrigida | 64 | 0 | 0 | 0 |

- [Console e relatório da linha de base](evidencias/atividade2/zap-antes.txt)
- [Console e relatório depois das correções](evidencias/atividade2/zap-depois.txt)
- [Active scan com XSS reintroduzido: regras 40012/40014, exit code 2](evidencias/atividade2/zap-active-xss.txt)
- [Active scan corrigido: 0 WARN/FAIL, exit code 0](evidencias/atividade2/zap-active-depois.txt)

## Como executar

```bash
gh workflow run dast.yml
gh run list --workflow dast.yml
```

No run, baixe o artefato `zap-reports`, que contém os relatórios HTML, JSON e Markdown
do Baseline e do active scan autenticado.

## Demonstração de bloqueio

Em uma branch de demonstração, troque no template `{{ task.description }}` por
`{{ task.description | safe }}`, abra um PR e mostre o check `DAST - ZAP Baseline`
vermelho pelas regras **40012 (Reflected XSS)** e **40014 (Persistent XSS)**. Reaplique
o autoescape, faça push e aguarde o gate verde. Não faça merge da versão vulnerável.
