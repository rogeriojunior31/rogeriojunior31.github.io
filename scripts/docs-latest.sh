#!/usr/bin/env bash
# Atualiza o docs/ de cada projeto de data/docs.yaml para a última release (maior tag vX.Y.Z).
# Roda em todo build do CI; localmente: scripts/docs-latest.sh && hugo server
# GOPRIVATE busca direto do GitHub, sem esperar o cache do proxy do Go depois de uma tag nova.
set -euo pipefail
cd "$(dirname "$0")/.."
export GOPRIVATE="github.com/rogeriojunior31/*"

repos=$(sed -nE 's/^[[:space:]]*repo:[[:space:]]*"?([A-Za-z0-9._-]+\/[A-Za-z0-9._-]+)"?[[:space:]]*$/\1/p' data/docs.yaml)
for repo in $repos; do
  echo "docs: github.com/$repo@latest"
  hugo mod get "github.com/$repo@latest"
done
