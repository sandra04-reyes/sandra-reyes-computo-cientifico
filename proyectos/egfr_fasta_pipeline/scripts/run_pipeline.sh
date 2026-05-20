#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$ROOT_DIR/logs"

{
  echo "Inicio del pipeline: $(date)"
  bash "$ROOT_DIR/scripts/01_download_egfr_fasta.sh"
  bash "$ROOT_DIR/scripts/02_analyze_egfr.sh"
  echo "Fin del pipeline: $(date)"
} 2>&1 | tee "$ROOT_DIR/logs/pipeline.log"
