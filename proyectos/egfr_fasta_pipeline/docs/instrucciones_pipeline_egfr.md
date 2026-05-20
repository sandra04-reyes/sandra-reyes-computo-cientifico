# Instrucciones del pipeline EGFR FASTA

## 1. Requisitos

Instalar:

- Git
- Python 3.10 o superior
- conda o venv
- curl
- GitHub CLI (`gh`), recomendado para crear repositorios privados desde terminal

## 2. Crear el ambiente

Opcion con conda:

```bash
conda env create -f environment.yml
conda activate egfr-fasta-pipeline
```

Opcion con venv:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3. Ejecutar el pipeline

Desde la raiz del repositorio:

```bash
bash scripts/run_pipeline.sh
```

Tambien puede ejecutarse por pasos:

```bash
bash scripts/01_download_egfr_fasta.sh
bash scripts/02_analyze_egfr.sh
```

## 4. Revisar resultados

Tablas:

```bash
ls data/processed
```

Resumenes:

```bash
cat results/EGFR_protein_summary.txt
cat results/EGFR_mRNA_summary.txt
```

Figuras:

```bash
ls figures
```

## 5. Inicializar Git

```bash
git init
git branch -M main
git status
git add .
git commit -m "Initial EGFR FASTA pipeline"
```

## 6. Crear repositorio privado en GitHub con GitHub CLI

Primero autenticarse:

```bash
gh auth login
```

Crear el repositorio privado y subir el codigo:

```bash
gh repo create egfr-fasta-pipeline --private --source=. --remote=origin --push
```

## 7. Alternativa sin GitHub CLI

1. Crear un repositorio privado desde la interfaz web de GitHub.
2. Copiar la URL HTTPS o SSH del repositorio.
3. Ejecutar:

```bash
git remote add origin URL_DEL_REPOSITORIO
git push -u origin main
```

## 8. Ciclo de trabajo recomendado

Despues de modificar codigo o resultados:

```bash
git status
git add scripts README.md docs config
git commit -m "Describe el cambio realizado"
git push
```

Si desea versionar resultados pequenos tambien puede usar:

```bash
git add results figures data/processed
git commit -m "Add updated EGFR analysis outputs"
git push
```

## 9. Buenas practicas

- No subir datos grandes o sensibles al repositorio.
- Mantener `scripts/` para codigo, `results/` para reportes y `figures/` para graficas.
- Documentar cambios importantes en el README.
- Usar mensajes de commit descriptivos.
- Revisar `git status` antes de cada commit.
