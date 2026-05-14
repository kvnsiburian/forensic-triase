"""
reporter.py
===========
Modul ekspor hasil triase ke format CSV.

Modul ini menerima output dari analyzer.classify_all() dan menulis
dua file CSV ke folder output:

  1. [nama_dump]_[timestamp]_results.csv
     Satu baris per PID — berisi semua field klasifikasi.
     Ini yang digunakan untuk Performance Testing di BAB V.

  2. [nama_dump]_[timestamp]_summary.csv
     Satu baris per sesi analisis — berisi statistik ringkasan.
     Total PID, jumlah SUSPICIOUS, CLEAN, dan hit count per Rule.

Format CSV dipilih karena:
  - Mudah dibuka di Excel/LibreOffice untuk verifikasi manual
  - Kompatibel dengan tools analisis lain (pandas, dll)
  - Sesuai keputusan teknis final (proposal BAB III, PDF ditunda)

Kolom results.csv:
  PID, Name, Path, Status,
  Rule1_Rogue, Rule2_Network, Rule3_Injection, Rule4_ProcObj,
  Reasons

Kolom summary.csv:
  Dump, Timestamp, Total_PID, Suspicious, Clean,
  Rule1_Hits, Rule2_Hits, Rule3_Hits, Rule4_Hits

Author  : Kevin Armando Siburian (2221101800)
Program : Rekayasa Keamanan Siber - PSSN
"""

import csv
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# Folder output default — sesuai struktur project (proposal BAB III)
DEFAULT_OUTPUT_DIR = Path("/mnt/d/forensic_triase/output")


# ---------------------------------------------------------------------------
# Helper: siapkan folder output
# ---------------------------------------------------------------------------

def _prepare_output_dir(output_dir: Path) -> None:
    """Buat folder output jika belum ada."""
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Output folder: {output_dir}")


# ---------------------------------------------------------------------------
# Helper: buat nama file dengan timestamp
# ---------------------------------------------------------------------------

def _make_filename(dump_name: str, suffix: str, output_dir: Path) -> Path:
    """
    Buat nama file output dengan format:
    [nama_dump]_[YYYYMMDD_HHMMSS]_[suffix].csv

    Contoh: dump_20241019_145836_results.csv
    """
    stem = Path(dump_name).stem          # hilangkan ekstensi, ambil nama saja
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{stem}_{timestamp}_{suffix}.csv"
    return output_dir / filename


# ---------------------------------------------------------------------------
# Export results.csv — satu baris per PID
# ---------------------------------------------------------------------------

def export_results(
    classifications: list,
    dump_name: str,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> Path:
    """
    Tulis hasil klasifikasi semua PID ke CSV.

    Parameter
    ---------
    classifications : list[dict]
        Output dari analyzer.classify_all()
    dump_name : str
        Nama file memory dump (untuk penamaan file output)
    output_dir : Path
        Folder tujuan output

    Return
    ------
    Path
        Path lengkap file CSV yang ditulis
    """
    _prepare_output_dir(output_dir)
    output_path = _make_filename(dump_name, "results", output_dir)

    fieldnames = [
        "PID",
        "Name",
        "Path",
        "Status",
        "Rule1_Rogue",
        "Rule2_Network",
        "Rule3_Injection",
        "Rule4_ProcObj",
        "Reasons",
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for rec in classifications:
            # Gabungkan semua reasons menjadi satu string, pisah dengan " | "
            reasons_str = " | ".join(rec.get("Reasons", []))

            writer.writerow({
                "PID":             rec["PID"],
                "Name":            rec["Name"],
                "Path":            rec["Path"] or "",
                "Status":          rec["Status"],
                "Rule1_Rogue":     rec["Rule1_hit"],
                "Rule2_Network":   rec["Rule2_hit"],
                "Rule3_Injection": rec["Rule3_hit"],
                "Rule4_ProcObj":   rec["Rule4_hit"],
                "Reasons":         reasons_str,
            })

    suspicious_count = sum(1 for r in classifications if r["Status"] == "SUSPICIOUS")
    logger.info(
        f"results.csv ditulis: {output_path.name} "
        f"({len(classifications)} baris, {suspicious_count} SUSPICIOUS)"
    )
    return output_path


# ---------------------------------------------------------------------------
# Export summary.csv — satu baris per sesi analisis
# ---------------------------------------------------------------------------

def export_summary(
    classifications: list,
    dump_name: str,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> Path:
    """
    Tulis ringkasan statistik sesi analisis ke CSV.

    File ini digunakan untuk tabel Performance Testing di BAB V:
    menghitung TP, TN, FP, FN membutuhkan data per-sesi yang ringkas.

    Return
    ------
    Path
        Path lengkap file CSV yang ditulis
    """
    _prepare_output_dir(output_dir)
    output_path = _make_filename(dump_name, "summary", output_dir)

    total      = len(classifications)
    suspicious = sum(1 for r in classifications if r["Status"] == "SUSPICIOUS")
    clean      = total - suspicious

    rule1_hits = sum(1 for r in classifications if r["Rule1_hit"])
    rule2_hits = sum(1 for r in classifications if r["Rule2_hit"])
    rule3_hits = sum(1 for r in classifications if r["Rule3_hit"])
    rule4_hits = sum(1 for r in classifications if r["Rule4_hit"])

    fieldnames = [
        "Dump",
        "Timestamp",
        "Total_PID",
        "Suspicious",
        "Clean",
        "Rule1_Hits",
        "Rule2_Hits",
        "Rule3_Hits",
        "Rule4_Hits",
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({
            "Dump":       dump_name,
            "Timestamp":  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Total_PID":  total,
            "Suspicious": suspicious,
            "Clean":      clean,
            "Rule1_Hits": rule1_hits,
            "Rule2_Hits": rule2_hits,
            "Rule3_Hits": rule3_hits,
            "Rule4_Hits": rule4_hits,
        })

    logger.info(f"summary.csv ditulis: {output_path.name}")
    return output_path


# ---------------------------------------------------------------------------
# Fungsi utama — panggil keduanya sekaligus
# ---------------------------------------------------------------------------

def export_all(
    classifications: list,
    dump_name: str,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> dict:
    """
    Export results.csv dan summary.csv sekaligus.

    Return
    ------
    dict
        {
            "results_path": Path,
            "summary_path": Path,
        }
    """
    results_path = export_results(classifications, dump_name, output_dir)
    summary_path = export_summary(classifications, dump_name, output_dir)
    return {
        "results_path": results_path,
        "summary_path": summary_path,
    }


# ---------------------------------------------------------------------------
# Quick test: python3 core/reporter.py /mnt/d/dump.dmp
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    import json
    import subprocess
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))

    from core.analyzer import classify_all

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%H:%M:%S",
    )

    dump = sys.argv[1] if len(sys.argv) > 1 else "/mnt/d/dump.dmp"
    vol  = str(Path.home() / ".local/bin/vol")

    PLUGINS = [
        "windows.pslist",
        "windows.pstree",
        "windows.netscan",
        "windows.malware.malfind",
    ]

    print("\n" + "=" * 60)
    print("  QUICK TEST -- Reporter")
    print("=" * 60)

    # Jalankan plugin
    plugin_results = {}
    for plugin in PLUGINS:
        print(f"Menjalankan {plugin}...")
        r = subprocess.run(
            [vol, "-f", dump, "--renderer", "json", plugin],
            capture_output=True, text=True, timeout=300
        )
        data = json.loads(r.stdout)
        if isinstance(data, list):
            plugin_results[plugin] = data
        elif isinstance(data, dict) and "rows" in data:
            cols = data["columns"]
            plugin_results[plugin] = [dict(zip(cols, row)) for row in data["rows"]]
        else:
            plugin_results[plugin] = None

    # Klasifikasi
    classifications = classify_all(plugin_results)

    # Export
    dump_name = Path(dump).name
    output = export_all(classifications, dump_name)

    print(f"\nOutput:")
    print(f"  results → {output['results_path']}")
    print(f"  summary → {output['summary_path']}")

    # Preview 3 baris pertama results.csv
    print(f"\nPreview results.csv (3 baris pertama):")
    with open(output["results_path"], encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i > 3:
                break
            print(f"  {line.rstrip()}")