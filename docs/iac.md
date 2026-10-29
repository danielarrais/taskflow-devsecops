# Segurança em Infraestrutura como Código

## Terraform antes × depois

O arquivo [`main.insecure.tf.example`](../infra/main.insecure.tf.example) preserva a
linha de base sem extensão `.tf`, para não contaminar `terraform validate` nem os gates.

| Scanner | Antes | Depois |
|---|---:|---:|
| Checkov | 15 falhas, exit code 1 | 0 falhas; 37 aprovações; 7 exceções justificadas |
| Trivy config | 8 HIGH/CRITICAL, exit code 1 | 0 HIGH/CRITICAL, exit code 0 |
| Terraform validate | não aplicável à linha insegura isolada | configuração válida |

Os achados originais incluíam bucket público, ausência de public access block,
criptografia sem chave gerenciada e Security Group aberto. A correção implementa:

- bucket privado, versionado e com access logging em bucket dedicado;
- SSE-KMS com rotação para os dados da aplicação;
- SSE-S3 no destino de access logs, limitação documentada do serviço AWS;
- lifecycle para versões e uploads incompletos;
- Security Group com ingresso HTTPS limitado por `allowed_ip_cidr` e sem egress aberto;
- validação que recusa `0.0.0.0/0` na variável de ingresso.

## Exceções do Checkov

Cada `# checkov:skip` está junto ao recurso e informa a razão. As exceções são:

- não provisionar notificações S3, fora do escopo do laboratório;
- não provisionar replicação multi-região, que adicionaria custo sem requisito de DR;
- não fazer logging do bucket terminal de access logs nele próprio, evitando recursão;
- usar SSE-S3 no destino de server access logs, que não suporta SSE-KMS;
- deixar o SG desacoplado porque o laboratório não provisiona compute.

Nenhuma exceção desliga o scanner ou usa `soft-fail`.

## Docker Compose

O Compose separa `frontend` e `backend`, mantém o SQLite sem porta, executa a aplicação
como UID 65532, remove capabilities, usa `no-new-privileges`, filesystem read-only,
healthcheck e limites de CPU/memória. Promtail lê apenas o volume de logs da TaskFlow;
ele não recebe acesso ao socket Docker nem a logs de outros projetos.

## Evidências reais

- [Checkov antes](evidencias/atividade2/checkov-antes.txt)
- [Checkov depois](evidencias/atividade2/checkov-depois.txt)
- [Trivy config antes](evidencias/atividade2/trivy-config-antes.txt)
- [Trivy config depois](evidencias/atividade2/trivy-config-depois.txt)
- [Terraform validate](evidencias/atividade2/terraform-validate.txt)
