"""
patch_summary_xlsx.py
=====================
Patch: Ubah export summary dari .csv menjadi .xlsx

Cara pakai:
  python3 ~/forensic_triase/platform/patch_summary_xlsx.py
"""

from pathlib import Path
import shutil

REPORTER = Path.home() / "forensic_triase/platform/core/reporter.py"

OLD_SUMMARY = '''def export_summary(
    classifications: list,
    dump_name: str,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> Path:
    _prepare_output_dir(output_dir)
    output_path = _make_filename(dump_name, "summary", output_dir, ext="csv")

    total      = len(classifications)
    suspicious = sum(1 for r in classifications if r["Status"] == "SUSPICIOUS")
    clean      = total - suspicious
    high       = sum(1 for r in classifications if r.get("Risk") == "HIGH")
    medium     = sum(1 for r in classifications if r.get("Risk") == "MEDIUM")
    low        = sum(1 for r in classifications if r.get("Risk") == "LOW")
    rule1_hits = sum(1 for r in classifications if r["Rule1_hit"])
    rule2_hits = sum(1 for r in classifications if r["Rule2_hit"])
    rule3_hits = sum(1 for r in classifications if r["Rule3_hit"])
    rule4_hits = sum(1 for r in classifications if r["Rule4_hit"])

    fieldnames = [
        "Dump", "Timestamp", "Total_PID", "Suspicious",
        "High", "Medium", "Low", "Clean",
        "Rule1_Hits", "Rule2_Hits", "Rule3_Hits", "Rule4_Hits",
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({
            "Dump":       dump_name,
            "Timestamp":  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Total_PID":  total,
            "Suspicious": suspicious,
            "High":       high,
            "Medium":     medium,
            "Low":        low,
            "Clean":      clean,
            "Rule1_Hits": rule1_hits,
            "Rule2_Hits": rule2_hits,
            "Rule3_Hits": rule3_hits,
            "Rule4_Hits": rule4_hits,
        })

    logger.info(f"summary.csv ditulis: {output_path.name}")
    return output_path'''

NEW_SUMMARY = '''def export_summary(
    classifications: list,
    dump_name: str,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> Path:
    _prepare_output_dir(output_dir)
    output_path = _make_filename(dump_name, "summary", output_dir, ext="xlsx")

    total      = len(classifications)
    suspicious = sum(1 for r in classifications if r["Status"] == "SUSPICIOUS")
    clean      = total - suspicious
    high       = sum(1 for r in classifications if r.get("Risk") == "HIGH")
    medium     = sum(1 for r in classifications if r.get("Risk") == "MEDIUM")
    low        = sum(1 for r in classifications if r.get("Risk") == "LOW")
    rule1_hits = sum(1 for r in classifications if r["Rule1_hit"])
    rule2_hits = sum(1 for r in classifications if r["Rule2_hit"])
    rule3_hits = sum(1 for r in classifications if r["Rule3_hit"])
    rule4_hits = sum(1 for r in classifications if r["Rule4_hit"])

    headers = [
        "Dump", "Timestamp", "Total_PID", "Suspicious",
        "High", "Medium", "Low", "Clean",
        "Rule1_Hits", "Rule2_Hits", "Rule3_Hits", "Rule4_Hits",
    ]
    values = [
        dump_name,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total, suspicious, high, medium, low, clean,
        rule1_hits, rule2_hits, rule3_hits, rule4_hits,
    ]

    wb = Workbook()
    ws = wb.active
    ws.title = "Summary"
    ws.append(headers)
    _style_header(ws)
    ws.append(values)
    _auto_width(ws)
    wb.save(output_path)

    logger.info(f"summary.xlsx ditulis: {output_path.name}")
    return output_path'''

print("\\n" + "=" * 60)
print("  PATCH: Summary CSV → XLSX")
print("=" * 60)

shutil.copy(REPORTER, str(REPORTER) + ".bak_summary")
content = REPORTER.read_text(encoding="utf-8")

if OLD_SUMMARY not in content:
    print("  [!] GAGAL — string tidak ditemukan.")
else:
    content = content.replace(OLD_SUMMARY, NEW_SUMMARY, 1)
    REPORTER.write_text(content, encoding="utf-8")
    print("  [✓] Patch berhasil")

print("\\n  Test:")
print("  python3 ~/forensic_triase/platform/main.py /mnt/d/forensic_triase/dataset/infected_rogue.raw")
print("=" * 60 + "\\n")