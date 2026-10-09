#!/usr/bin/env bash
# Atualiza os docs importados de data/docs.yaml para a última release (@upgrade do Go).
# @upgrade e não @latest: um projeto fixado num commit depois da última tag (pseudo-versão)
# não volta para essa tag; a próxima tag passa na frente do commit normalmente.
# Roda no deploy, não no CI de PRs; localmente: scripts/docs-latest.sh && hugo server
# GOPRIVATE busca direto do GitHub, sem esperar o cache do proxy do Go depois de uma tag nova.
set -euo pipefail
cd "$(dirname "$0")/.."
export GOPRIVATE="github.com/rogeriojunior31/*,github.com/sp-night/*"

repos=$(sed -nE 's/^[[:space:]]*repo:[[:space:]]*"?([A-Za-z0-9._-]+\/[A-Za-z0-9._-]+)"?[[:space:]]*$/\1/p' data/docs.yaml)
modules=$(hugo mod graph | awk '{ sub(/@.*/, "", $2); print $2 }')
for repo in $repos; do
  # Docs externos não precisam de um Hugo Module nem de atualização local.
  if ! printf '%s\n' "$modules" | grep -Fxq "github.com/$repo"; then continue; fi
  echo "docs: github.com/$repo@upgrade"
  hugo mod get "github.com/$repo@upgrade"
done
