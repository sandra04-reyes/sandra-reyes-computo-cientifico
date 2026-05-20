#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$ROOT_DIR/config/egfr_config.env"

PROTEIN_FASTA="$ROOT_DIR/data/raw/${PROTEIN_PREFIX}_${UNIPROT_ACCESSION}.fasta"
MRNA_FASTA="$ROOT_DIR/data/raw/${MRNA_PREFIX}_${NCBI_NUCCORE_ID}.fasta"

if [[ ! -s "$PROTEIN_FASTA" || ! -s "$MRNA_FASTA" ]]; then
  echo "No se encontraron los FASTA esperados. Ejecute primero: bash scripts/01_download_egfr_fasta.sh" >&2
  exit 1
fi

python "$ROOT_DIR/scripts/analyze_fasta.py" \
  --input "$PROTEIN_FASTA" \
  --seq-type protein \
  --prefix "$PROTEIN_PREFIX" \
  --processed-dir "$ROOT_DIR/data/processed" \
  --results-dir "$ROOT_DIR/results" \
  --figures-dir "$ROOT_DIR/figures"

python "$ROOT_DIR/scripts/analyze_fasta.py" \
  --input "$MRNA_FASTA" \
  --seq-type nucleotide \
  --prefix "$MRNA_PREFIX" \
  --processed-dir "$ROOT_DIR/data/processed" \
  --results-dir "$ROOT_DIR/results" \
  --figures-dir "$ROOT_DIR/figures"
