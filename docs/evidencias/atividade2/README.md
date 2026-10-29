# Evidências reais — Atividade 2

Arquivos produzidos por execuções locais em 29/10/2026.

| Evidência | Resultado |
|---|---|
| `zap-antes.txt` / `zap-antes.md` | linha de base da `origin/main`: 8 WARN, exit code 2 |
| `zap-depois.txt` / `zap-depois.md` | aplicação corrigida: 0 WARN, 0 FAIL, exit code 0 |
| `zap-active-xss.txt` / `.html` | XSS reintroduzido: regras 40012/40014, exit code 2 |
| `zap-active-depois.txt` / `.md` | active scan corrigido: 0 WARN/FAIL, exit code 0 |
| `terraform-validate.txt` | saída real do `terraform validate` |
| `checkov-depois.txt` | 37 checks aprovados, 0 falhas e exceções justificadas |
| `trivy-config-depois.txt` | 0 HIGH/CRITICAL em Dockerfiles e Terraform |
| `checkov-antes.txt` | linha insegura: 15 falhas e exit code 1 |
| `trivy-config-antes.txt` | linha insegura: 8 HIGH/CRITICAL e exit code 1 |
| `observabilidade-login-failed.json` | consulta real ao Loki após 20 tentativas inválidas |
| `observabilidade-stack.log` | logs da stack usados para verificar higiene |
| `grafana-login-bruteforce.png` | painel real mostrando 20 falhas por IP em cinco minutos |

Nenhum resultado foi fabricado: todos os arquivos acima vieram das execuções descritas na documentação.
