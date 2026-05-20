#!/usr/bin/env python3
"""Analisis basico de archivos FASTA.

El script calcula estadisticas por secuencia, composicion de residuos/bases,
resumen global y graficas sencillas. No requiere Biopython.
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from typing import Iterable, List, Tuple

import matplotlib.pyplot as plt
import pandas as pd


DNA_ALPHABET = set("ACGTUN")
PROTEIN_ALPHABET = set("ACDEFGHIKLMNPQRSTVWYBXZJUO")

# Masas moleculares promedio de aminoacidos libres menos H2O por enlace peptidico
# Se usa solo como estimacion rapida para una actividad introductoria.
AA_MASS = {
    "A": 89.09,
    "R": 174.20,
    "N": 132.12,
    "D": 133.10,
    "C": 121.15,
    "E": 147.13,
    "Q": 146.15,
    "G": 75.07,
    "H": 155.16,
    "I": 131.17,
    "L": 131.17,
    "K": 146.19,
    "M": 149.21,
    "F": 165.19,
    "P": 115.13,
    "S": 105.09,
    "T": 119.12,
    "W": 204.23,
    "Y": 181.19,
    "V": 117.15,
}

KYTE_DOOLITTLE = {
    "A": 1.8,
    "R": -4.5,
    "N": -3.5,
    "D": -3.5,
    "C": 2.5,
    "Q": -3.5,
    "E": -3.5,
    "G": -0.4,
    "H": -3.2,
    "I": 4.5,
    "L": 3.8,
    "K": -3.9,
    "M": 1.9,
    "F": 2.8,
    "P": -1.6,
    "S": -0.8,
    "T": -0.7,
    "W": -0.9,
    "Y": -1.3,
    "V": 4.2,
}


def read_fasta(path: Path) -> List[Tuple[str, str]]:
    records: List[Tuple[str, str]] = []
    header = None
    seq_chunks: List[str] = []

    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header is not None:
                    records.append((header, "".join(seq_chunks).upper()))
                header = line[1:]
                seq_chunks = []
            else:
                seq_chunks.append(line)

    if header is not None:
        records.append((header, "".join(seq_chunks).upper()))

    if not records:
        raise ValueError(f"No se encontraron secuencias FASTA en: {path}")
    return records


def sequence_type_default(seq: str) -> str:
    letters = set(seq.upper())
    if letters <= DNA_ALPHABET:
        return "nucleotide"
    return "protein"


def molecular_weight_protein(seq: str) -> float:
    aa = [res for res in seq if res in AA_MASS]
    if not aa:
        return float("nan")
    # Peso aproximado: suma de residuos libres - agua por cada enlace peptidico.
    return sum(AA_MASS[x] for x in aa) - 18.015 * max(len(aa) - 1, 0)


def gravy(seq: str) -> float:
    values = [KYTE_DOOLITTLE[x] for x in seq if x in KYTE_DOOLITTLE]
    if not values:
        return float("nan")
    return sum(values) / len(values)


def gc_percent(seq: str) -> float:
    valid = [x for x in seq if x in {"A", "C", "G", "T", "U", "N"}]
    if not valid:
        return float("nan")
    gc = sum(1 for x in valid if x in {"G", "C"})
    return 100.0 * gc / len(valid)


def n_percent(seq: str) -> float:
    valid = [x for x in seq if x in {"A", "C", "G", "T", "U", "N"}]
    if not valid:
        return float("nan")
    n_count = sum(1 for x in valid if x == "N")
    return 100.0 * n_count / len(valid)


def make_stats(records: List[Tuple[str, str]], seq_type: str) -> pd.DataFrame:
    rows = []
    for i, (header, seq) in enumerate(records, start=1):
        row = {
            "record_id": i,
            "header": header,
            "length": len(seq),
        }
        if seq_type == "protein":
            row["estimated_molecular_weight_Da"] = molecular_weight_protein(seq)
            row["estimated_molecular_weight_kDa"] = row["estimated_molecular_weight_Da"] / 1000
            row["gravy_kyte_doolittle"] = gravy(seq)
        else:
            row["gc_percent"] = gc_percent(seq)
            row["n_percent"] = n_percent(seq)
        rows.append(row)
    return pd.DataFrame(rows)


def make_composition(records: List[Tuple[str, str]], seq_type: str) -> pd.DataFrame:
    joined = "".join(seq for _, seq in records)
    alphabet = sorted(PROTEIN_ALPHABET if seq_type == "protein" else DNA_ALPHABET)
    counts = Counter(joined)
    total_known = sum(counts[x] for x in alphabet)
    rows = []
    for symbol in alphabet:
        count = counts[symbol]
        pct = 100.0 * count / total_known if total_known else 0.0
        rows.append({"symbol": symbol, "count": count, "percent": pct})
    extra = sorted(set(joined) - set(alphabet))
    for symbol in extra:
        count = counts[symbol]
        pct = 100.0 * count / len(joined) if joined else 0.0
        rows.append({"symbol": symbol, "count": count, "percent": pct})
    return pd.DataFrame(rows)


def save_summary(stats: pd.DataFrame, composition: pd.DataFrame, out_path: Path, seq_type: str) -> None:
    lines = []
    lines.append("Resumen del analisis FASTA")
    lines.append("==========================")
    lines.append(f"Tipo de secuencia: {seq_type}")
    lines.append(f"Numero de registros: {len(stats)}")
    lines.append(f"Longitud total: {int(stats['length'].sum())}")
    lines.append(f"Longitud minima: {int(stats['length'].min())}")
    lines.append(f"Longitud maxima: {int(stats['length'].max())}")
    lines.append(f"Longitud media: {stats['length'].mean():.2f}")
    if seq_type == "protein":
        lines.append(f"Peso molecular estimado medio (kDa): {stats['estimated_molecular_weight_kDa'].mean():.2f}")
        lines.append(f"GRAVY medio: {stats['gravy_kyte_doolittle'].mean():.3f}")
    else:
        lines.append(f"GC medio (%): {stats['gc_percent'].mean():.2f}")
        lines.append(f"N medio (%): {stats['n_percent'].mean():.2f}")
    lines.append("")
    lines.append("Composicion principal:")
    top = composition.sort_values("count", ascending=False).head(10)
    for _, row in top.iterrows():
        lines.append(f"  {row['symbol']}: {int(row['count'])} ({row['percent']:.2f}%)")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def plot_lengths(stats: pd.DataFrame, out_path: Path, title: str) -> None:
    plt.figure(figsize=(7, 4.5))
    if len(stats) == 1:
        plt.bar([stats.loc[0, "record_id"]], [stats.loc[0, "length"]])
        plt.xlabel("Registro FASTA")
        plt.ylabel("Longitud")
    else:
        plt.hist(stats["length"], bins=min(20, max(5, len(stats))))
        plt.xlabel("Longitud")
        plt.ylabel("Frecuencia")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def plot_composition(composition: pd.DataFrame, out_path: Path, title: str) -> None:
    df = composition[composition["count"] > 0].copy()
    df = df.sort_values("count", ascending=False)
    plt.figure(figsize=(9, 4.8))
    plt.bar(df["symbol"], df["percent"])
    plt.xlabel("Residuo/base")
    plt.ylabel("Porcentaje")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analisis basico de FASTA y graficas sencillas.")
    parser.add_argument("--input", required=True, type=Path, help="Archivo FASTA de entrada")
    parser.add_argument("--seq-type", choices=["auto", "protein", "nucleotide"], default="auto")
    parser.add_argument("--prefix", required=True, help="Prefijo para los archivos de salida")
    parser.add_argument("--processed-dir", type=Path, default=Path("data/processed"))
    parser.add_argument("--results-dir", type=Path, default=Path("results"))
    parser.add_argument("--figures-dir", type=Path, default=Path("figures"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    records = read_fasta(args.input)
    seq_type = args.seq_type
    if seq_type == "auto":
        seq_type = sequence_type_default(records[0][1])

    args.processed_dir.mkdir(parents=True, exist_ok=True)
    args.results_dir.mkdir(parents=True, exist_ok=True)
    args.figures_dir.mkdir(parents=True, exist_ok=True)

    stats = make_stats(records, seq_type)
    composition = make_composition(records, seq_type)

    stats_path = args.processed_dir / f"{args.prefix}_sequence_stats.csv"
    comp_path = args.processed_dir / f"{args.prefix}_composition.csv"
    summary_path = args.results_dir / f"{args.prefix}_summary.txt"
    length_fig = args.figures_dir / f"{args.prefix}_lengths.png"
    comp_fig = args.figures_dir / f"{args.prefix}_composition.png"

    stats.to_csv(stats_path, index=False)
    composition.to_csv(comp_path, index=False)
    save_summary(stats, composition, summary_path, seq_type)
    plot_lengths(stats, length_fig, f"{args.prefix}: longitud de secuencia")
    plot_composition(composition, comp_fig, f"{args.prefix}: composicion")

    print("Analisis completado")
    print(f"  Estadisticas: {stats_path}")
    print(f"  Composicion:  {comp_path}")
    print(f"  Resumen:      {summary_path}")
    print(f"  Figura 1:     {length_fig}")
    print(f"  Figura 2:     {comp_fig}")


if __name__ == "__main__":
    main()
