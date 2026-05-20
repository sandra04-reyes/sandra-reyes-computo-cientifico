#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$ROOT_DIR/config/egfr_config.env"

mkdir -p "$ROOT_DIR/data/raw" "$ROOT_DIR/logs"

PROTEIN_URL="https://rest.uniprot.org/uniprotkb/${UNIPROT_ACCESSION}.fasta"
MRNA_URL="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=${NCBI_NUCCORE_ID}&rettype=fasta&retmode=text"

PROTEIN_OUT="$ROOT_DIR/data/raw/${PROTEIN_PREFIX}_${UNIPROT_ACCESSION}.fasta"
MRNA_OUT="$ROOT_DIR/data/raw/${MRNA_PREFIX}_${NCBI_NUCCORE_ID}.fasta"

printf "Descargando proteina EGFR desde UniProt: %s\n" "$PROTEIN_URL"
curl -fL --retry 3 --retry-delay 2 "$PROTEIN_URL" -o "$PROTEIN_OUT"

printf "Descargando mRNA EGFR desde NCBI EFetch: %s\n" "$MRNA_URL"
curl -fL --retry 3 --retry-delay 2 "$MRNA_URL" -o "$MRNA_OUT"

printf "\nArchivos descargados:\n"
printf "  %s\n" "$PROTEIN_OUT"
printf "  %s\n" "$MRNA_OUT"

printf "\nVista rapida de la proteina:\n"
head -n 5 "$PROTEIN_OUT"
printf "\nVista rapida del mRNA:\n"
head -n 5 "$MRNA_OUT"
