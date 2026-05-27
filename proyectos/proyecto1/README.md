# EGFR FASTA Pipeline

Pipeline reproducible para descargar secuencias FASTA de EGFR humano, calcular estadisticas basicas y generar graficas sencillas.

## Objetivo

Este repositorio sirve como practica introductoria de computo cientifico/bioinformatica:

1. Descargar secuencias FASTA desde terminal.
2. Organizar un proyecto reproducible.
3. Analizar secuencias con Python.
4. Generar tablas y figuras simples.
5. Versionar el proyecto con Git y subirlo a un repositorio privado en GitHub.

## Estructura

```text
egfr_fasta_pipeline/
├── config/                 # Parametros editables del pipeline
├── scripts/                # Scripts Bash y Python
├── data/
│   ├── raw/                # FASTA descargados
│   └── processed/          # Tablas CSV generadas
├── results/                # Resumenes de texto
├── figures/                # Graficas PNG
├── docs/                   # Instrucciones en PDF y Markdown
├── logs/                   # Bitacoras de ejecucion
├── requirements.txt
├── environment.yml
└── README.md
```

## Instalacion rapida con conda

```bash
conda env create -f environment.yml
conda activate egfr-fasta-pipeline
```

Alternativa con `venv`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecucion completa

Desde la raiz del repositorio:

```bash
bash scripts/run_pipeline.sh
```

## Ejecucion paso a paso

```bash
bash scripts/01_download_egfr_fasta.sh
bash scripts/02_analyze_egfr.sh
```

## Salidas esperadas

- `data/raw/EGFR_protein_P00533.fasta`
- `data/raw/EGFR_mRNA_NM_005228.fasta`
- `data/processed/EGFR_protein_sequence_stats.csv`
- `data/processed/EGFR_protein_composition.csv`
- `data/processed/EGFR_mRNA_sequence_stats.csv`
- `data/processed/EGFR_mRNA_composition.csv`
- `results/EGFR_protein_summary.txt`
- `results/EGFR_mRNA_summary.txt`
- `figures/EGFR_protein_lengths.png`
- `figures/EGFR_protein_composition.png`
- `figures/EGFR_mRNA_lengths.png`
- `figures/EGFR_mRNA_composition.png`

## Cambiar a otro gen o proteina

Edite `config/egfr_config.env` y cambie:

```bash
GENE_SYMBOL="EGFR"
UNIPROT_ACCESSION="P00533"
NCBI_NUCCORE_ID="NM_005228"
```

Para otro objetivo, use un accession valido de UniProt para proteina y un identificador valido de NCBI Nucleotide para FASTA nucleotidico.
