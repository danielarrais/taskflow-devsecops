#!/usr/bin/env bash
set -euo pipefail

target="${1:-http://127.0.0.1:5000/login}"
attempts="${2:-20}"
username="${3:-admin}"

echo "Simulando $attempts tentativas inválidas para $username em $target"
cookie_jar="$(mktemp)"
login_page="$(mktemp)"
trap 'rm -f "$cookie_jar" "$login_page"' EXIT

curl --fail --silent --show-error --cookie-jar "$cookie_jar" "$target" > "$login_page"
csrf_token="$(sed -n 's/.*name="csrf_token" value="\([^"]*\)".*/\1/p' "$login_page")"
if [[ -z "$csrf_token" ]]; then
  echo "Não foi possível obter o token CSRF da tela de login." >&2
  exit 1
fi

for attempt in $(seq 1 "$attempts"); do
  curl --fail --silent --show-error \
    --cookie "$cookie_jar" \
    --data-urlencode "username=$username" \
    --data-urlencode "password=incorreta-$attempt" \
    --data-urlencode "csrf_token=$csrf_token" \
    "$target" >/dev/null
done
echo "Simulação concluída. Execute a query do runbook no Grafana."
