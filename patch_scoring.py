"""
patch_scoring.py
================
Patch script: menambahkan scoring model ke Platform Triase Forensik Memori.

Perubahan:
  1. analyzer.py  — tambah RULE_WEIGHTS, compute_risk(), field Score + Risk
  2. app.py       — tambah kolom Score/Risk, warna per risk level
  3. reporter.py  — tambah kolom Score, Risk, dan risk counts di CSV

Cara pakai (di WSL):
  cd ~/forensic_triase/platform
  python3 /tmp/patch_scoring.py

Backup otomatis dibuat: *.py.bak
"""

from pathlib import Path
import shutil

BASE = Path.home() / "forensic_triase/platform"

# ---------------------------------------------------------------------------
# Patch 1: analyzer.py
# ---------------------------------------------------------------------------

ANALYZER = BASE / "core/analyzer.py"

SCORING_CODE = '''
# ---------------------------------------------------------------------------
# Scoring Model — Risk Level Classification
# ---------------------------------------------------------------------------
# Bobot tiap rule berdasarkan tingkat keparahan indikator:
#   Rule 1 & 3 = bobot 3 (indikator kuat: typosquatting, RWX injection)
#   Rule 2 & 4 = bobot 2 (indikator sedang: network anomali, parent-child)
#
# Skor maksimum = 10 (semua rule terpenuhi)
# Threshold:
#   0        → CLEAN
#   1–2      → LOW
#   3–5      → MEDIUM
#   6–10     → HIGH

RULE_WEIGHTS = {
    "rule1": 3,  # Identify Rogue Processes
    "rule2": 2,  # Review Network Artifacts
    "rule3": 3,  # Look for Evidence of Code Injection
    "rule4": 2,  # Analyze Process Objects
}

RISK_THRESHOLDS = [
    (6, "HIGH"),
    (3, "MEDIUM"),
    (1, "LOW"),
    (0, "CLEAN"),
]


def compute_risk(r1: bool, r2: bool, r3: bool, r4: bool) -> "tuple[int, str]":
    """
    Hitung skor risiko berdasarkan rule yang terpenuhi.

    Return
    ------
    (score: int, risk_level: str)
        score      : akumulasi bobot rule yang terpenuhi (0–10)
        risk_level : "CLEAN" | "LOW" | "MEDIUM" | "HIGH"
    """
    score = (
        (RULE_WEIGHTS["rule1"] if r1 else 0) +
        (RULE_WEIGHTS["rule2"] if r2 else 0) +
        (RULE_WEIGHTS["rule3"] if r3 else 0) +
        (RULE_WEIGHTS["rule4"] if r4 else 0)
    )
    for threshold, level in RISK_THRESHOLDS:
        if score >= threshold:
            return score, level
    return 0, "CLEAN"

'''

# Patch 1a: sisipkan SCORING_CODE setelah baris "from typing import Optional"
OLD_IMPORT = "from typing import Optional\n\nlogger = logging.getLogger(__name__)"
NEW_IMPORT = "from typing import Optional\n" + SCORING_CODE + "\nlogger = logging.getLogger(__name__)"

# Patch 1b: tambah Score dan Risk di results.append()
OLD_APPEND = '''        results.append({
            "PID":       pid,
            "Name":      proc_name,
            "Path":      proc_path,
            "Status":    status,
            "Reasons":   all_reasons,
            "Rule1_hit": r1_hit,
            "Rule2_hit": r2_hit,
            "Rule3_hit": r3_hit,
            "Rule4_hit": r4_hit,
        })'''

NEW_APPEND = '''        score, risk = compute_risk(r1_hit, r2_hit, r3_hit, r4_hit)

        results.append({
            "PID":       pid,
            "Name":      proc_name,
            "Path":      proc_path,
            "Status":    status,
            "Score":     score,
            "Risk":      risk,
            "Reasons":   all_reasons,
            "Rule1_hit": r1_hit,
            "Rule2_hit": r2_hit,
            "Rule3_hit": r3_hit,
            "Rule4_hit": r4_hit,
        })'''

# Patch 1c: tambah Score/Risk di log WARNING
OLD_LOG = '''            logger.warning(
                f"[SUSPICIOUS] PID={pid} ({proc_name}) | "
                f"Rules hit: "
                f"R1={'Y' if r1_hit else 'N'} "
                f"R2={'Y' if r2_hit else 'N'} "
                f"R3={'Y' if r3_hit else 'N'} "
                f"R4={'Y' if r4_hit else 'N'}"
            )'''

NEW_LOG = '''            logger.warning(
                f"[{risk}] PID={pid} ({proc_name}) | "
                f"Score={score} | "
                f"R1={'Y' if r1_hit else 'N'} "
                f"R2={'Y' if r2_hit else 'N'} "
                f"R3={'Y' if r3_hit else 'N'} "
                f"R4={'Y' if r4_hit else 'N'}"
            )'''

# ---------------------------------------------------------------------------
# Patch 2: app.py
# ---------------------------------------------------------------------------

APP = BASE / "gui/app.py"

# Patch 2a: tambah warna risk level setelah COLOR_GREEN
OLD_COLORS = '''COLOR_RED        = "#ef4444"   # teks SUSPICIOUS
COLOR_GREEN      = "#22c55e"   # teks CLEAN
COLOR_BORDER     = "#3f3f5f"   # border panel'''

NEW_COLORS = '''COLOR_RED        = "#ef4444"   # teks HIGH
COLOR_ORANGE     = "#f97316"   # teks MEDIUM
COLOR_YELLOW     = "#eab308"   # teks LOW
COLOR_GREEN      = "#22c55e"   # teks CLEAN
COLOR_BORDER     = "#3f3f5f"   # border panel

# Background baris per risk level
COLOR_BG_HIGH    = "#3b1a1a"
COLOR_BG_MEDIUM  = "#2e1a0a"
COLOR_BG_LOW     = "#2a2a0a"
COLOR_BG_CLEAN   = "#1a2e1a"'''

# Patch 2b: tambah kolom Score dan Risk ke Treeview
OLD_COLUMNS = '        columns = ("PID", "Name", "Path", "Status", "R1", "R2", "R3", "R4")'
NEW_COLUMNS = '        columns = ("PID", "Name", "Path", "Status", "Score", "Risk", "R1", "R2", "R3", "R4")'

# Patch 2c: tambah konfigurasi kolom Score dan Risk
OLD_COL_CONFIG = '''        col_config = {
            "PID":    (60,  "center"),
            "Name":   (160, "w"),
            "Path":   (340, "w"),
            "Status": (100, "center"),
            "R1":     (40,  "center"),
            "R2":     (40,  "center"),
            "R3":     (40,  "center"),
            "R4":     (40,  "center"),
        }'''

NEW_COL_CONFIG = '''        col_config = {
            "PID":    (60,  "center"),
            "Name":   (160, "w"),
            "Path":   (280, "w"),
            "Status": (90,  "center"),
            "Score":  (55,  "center"),
            "Risk":   (80,  "center"),
            "R1":     (36,  "center"),
            "R2":     (36,  "center"),
            "R3":     (36,  "center"),
            "R4":     (36,  "center"),
        }'''

# Patch 2d: tambah header kolom Score dan Risk
OLD_COL_HEADERS = '''        col_headers = {
            "PID":    "PID",
            "Name":   "Nama Proses",
            "Path":   "Path Eksekusi",
            "Status": "Status",
            "R1":     "R1",
            "R2":     "R2",
            "R3":     "R3",
            "R4":     "R4",
        }'''

NEW_COL_HEADERS = '''        col_headers = {
            "PID":    "PID",
            "Name":   "Nama Proses",
            "Path":   "Path Eksekusi",
            "Status": "Status",
            "Score":  "Skor",
            "Risk":   "Risiko",
            "R1":     "R1",
            "R2":     "R2",
            "R3":     "R3",
            "R4":     "R4",
        }'''

# Patch 2e: ganti tag warna dari binary ke risk-based
OLD_TAGS = '''        # Tag warna per status
        self._tree.tag_configure(
            "suspicious",
            background=COLOR_SUSPICIOUS,
            foreground=COLOR_RED,
        )
        self._tree.tag_configure(
            "clean",
            background=COLOR_CLEAN,
            foreground=COLOR_GREEN,
        )'''

NEW_TAGS = '''        # Tag warna per risk level
        self._tree.tag_configure(
            "high",
            background=COLOR_BG_HIGH,
            foreground=COLOR_RED,
        )
        self._tree.tag_configure(
            "medium",
            background=COLOR_BG_MEDIUM,
            foreground=COLOR_ORANGE,
        )
        self._tree.tag_configure(
            "low",
            background=COLOR_BG_LOW,
            foreground=COLOR_YELLOW,
        )
        self._tree.tag_configure(
            "clean",
            background=COLOR_BG_CLEAN,
            foreground=COLOR_GREEN,
        )'''

# Patch 2f: update _populate_table — gunakan Risk untuk tag dan tampilan
OLD_POPULATE = '''        for rec in sorted_data:
            tag    = "suspicious" if rec["Status"] == "SUSPICIOUS" else "clean"
            r1     = "✓" if rec["Rule1_hit"] else "·"
            r2     = "✓" if rec["Rule2_hit"] else "·"
            r3     = "✓" if rec["Rule3_hit"] else "·"
            r4     = "✓" if rec["Rule4_hit"] else "·"
            path   = rec["Path"] or "—"
            status = rec["Status"]

            self._tree.insert(
                "", "end",
                values=(rec["PID"], rec["Name"], path, status, r1, r2, r3, r4),
                tags=(tag,),
            )'''

NEW_POPULATE = '''        for rec in sorted_data:
            risk   = rec.get("Risk", "CLEAN")
            tag    = risk.lower()  # "high" / "medium" / "low" / "clean"
            r1     = "✓" if rec["Rule1_hit"] else "·"
            r2     = "✓" if rec["Rule2_hit"] else "·"
            r3     = "✓" if rec["Rule3_hit"] else "·"
            r4     = "✓" if rec["Rule4_hit"] else "·"
            path   = rec["Path"] or "—"
            score  = rec.get("Score", 0)
            status = rec["Status"]

            self._tree.insert(
                "", "end",
                values=(rec["PID"], rec["Name"], path, status, score, risk,
                        r1, r2, r3, r4),
                tags=(tag,),
            )'''

# Patch 2g: update sorted_data — urutkan berdasarkan Score (desc)
OLD_SORT = '''        sorted_data = sorted(
            classifications,
            key=lambda r: (0 if r["Status"] == "SUSPICIOUS" else 1, r["PID"]),
        )'''

NEW_SORT = '''        sorted_data = sorted(
            classifications,
            key=lambda r: (-r.get("Score", 0), r["PID"]),
        )'''

# ---------------------------------------------------------------------------
# Patch 3: reporter.py
# ---------------------------------------------------------------------------

REPORTER = BASE / "core/reporter.py"

# Patch 3a: tambah Score dan Risk ke fieldnames results.csv
OLD_FIELDNAMES = '''    fieldnames = [
        "PID",
        "Name",
        "Path",
        "Status",
        "Rule1_Rogue",
        "Rule2_Network",
        "Rule3_Injection",
        "Rule4_ProcObj",
        "Reasons",
    ]'''

NEW_FIELDNAMES = '''    fieldnames = [
        "PID",
        "Name",
        "Path",
        "Status",
        "Score",
        "Risk",
        "Rule1_Rogue",
        "Rule2_Network",
        "Rule3_Injection",
        "Rule4_ProcObj",
        "Reasons",
    ]'''

# Patch 3b: tambah Score dan Risk ke writer.writerow di export_results
OLD_WRITEROW = '''            writer.writerow({
                "PID":             rec["PID"],
                "Name":            rec["Name"],
                "Path":            rec["Path"] or "",
                "Status":          rec["Status"],
                "Rule1_Rogue":     rec["Rule1_hit"],
                "Rule2_Network":   rec["Rule2_hit"],
                "Rule3_Injection": rec["Rule3_hit"],
                "Rule4_ProcObj":   rec["Rule4_hit"],
                "Reasons":         reasons_str,
            })'''

NEW_WRITEROW = '''            writer.writerow({
                "PID":             rec["PID"],
                "Name":            rec["Name"],
                "Path":            rec["Path"] or "",
                "Status":          rec["Status"],
                "Score":           rec.get("Score", 0),
                "Risk":            rec.get("Risk", "CLEAN"),
                "Rule1_Rogue":     rec["Rule1_hit"],
                "Rule2_Network":   rec["Rule2_hit"],
                "Rule3_Injection": rec["Rule3_hit"],
                "Rule4_ProcObj":   rec["Rule4_hit"],
                "Reasons":         reasons_str,
            })'''

# Patch 3c: tambah High/Medium/Low counts ke fieldnames summary.csv
OLD_SUMMARY_FIELDS = '''    fieldnames = [
        "Dump",
        "Timestamp",
        "Total_PID",
        "Suspicious",
        "Clean",
        "Rule1_Hits",
        "Rule2_Hits",
        "Rule3_Hits",
        "Rule4_Hits",
    ]'''

NEW_SUMMARY_FIELDS = '''    fieldnames = [
        "Dump",
        "Timestamp",
        "Total_PID",
        "Suspicious",
        "High",
        "Medium",
        "Low",
        "Clean",
        "Rule1_Hits",
        "Rule2_Hits",
        "Rule3_Hits",
        "Rule4_Hits",
    ]'''

# Patch 3d: tambah kalkulasi dan row untuk High/Medium/Low
OLD_SUMMARY_ROW = '''    total      = len(classifications)
    suspicious = sum(1 for r in classifications if r["Status"] == "SUSPICIOUS")
    clean      = total - suspicious

    rule1_hits = sum(1 for r in classifications if r["Rule1_hit"])
    rule2_hits = sum(1 for r in classifications if r["Rule2_hit"])
    rule3_hits = sum(1 for r in classifications if r["Rule3_hit"])
    rule4_hits = sum(1 for r in classifications if r["Rule4_hit"])

    fieldnames = ['''

NEW_SUMMARY_ROW = '''    total      = len(classifications)
    suspicious = sum(1 for r in classifications if r["Status"] == "SUSPICIOUS")
    clean      = total - suspicious
    high       = sum(1 for r in classifications if r.get("Risk") == "HIGH")
    medium     = sum(1 for r in classifications if r.get("Risk") == "MEDIUM")
    low        = sum(1 for r in classifications if r.get("Risk") == "LOW")

    rule1_hits = sum(1 for r in classifications if r["Rule1_hit"])
    rule2_hits = sum(1 for r in classifications if r["Rule2_hit"])
    rule3_hits = sum(1 for r in classifications if r["Rule3_hit"])
    rule4_hits = sum(1 for r in classifications if r["Rule4_hit"])

    fieldnames = ['''

# Patch 3e: tambah High/Medium/Low ke writer.writerow summary
OLD_SUMMARY_WRITEROW = '''        writer.writerow({
            "Dump":       dump_name,
            "Timestamp":  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Total_PID":  total,
            "Suspicious": suspicious,
            "Clean":      clean,
            "Rule1_Hits": rule1_hits,
            "Rule2_Hits": rule2_hits,
            "Rule3_Hits": rule3_hits,
            "Rule4_Hits": rule4_hits,
        })'''

NEW_SUMMARY_WRITEROW = '''        writer.writerow({
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
        })'''


# ---------------------------------------------------------------------------
# Fungsi helper patch
# ---------------------------------------------------------------------------

def patch_file(path: Path, replacements: list[tuple[str, str]], label: str):
    """Apply list of (old, new) replacements ke file."""
    shutil.copy(path, str(path) + ".bak")
    content = path.read_text(encoding="utf-8")
    
    for i, (old, new) in enumerate(replacements, 1):
        if old not in content:
            print(f"  [!] Patch {i} GAGAL — string tidak ditemukan di {label}")
            print(f"      Cek apakah file sudah dimodifikasi sebelumnya.")
            continue
        content = content.replace(old, new, 1)
        print(f"  [✓] Patch {i} berhasil")
    
    path.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# Jalankan semua patch
# ---------------------------------------------------------------------------

print("\n" + "=" * 60)
print("  PATCH: Scoring Model — Platform Triase Forensik Memori")
print("=" * 60)

print("\n[1/3] Patching analyzer.py...")
patch_file(ANALYZER, [
    (OLD_IMPORT,   NEW_IMPORT),
    (OLD_APPEND,   NEW_APPEND),
    (OLD_LOG,      NEW_LOG),
], "analyzer.py")

print("\n[2/3] Patching app.py...")
patch_file(APP, [
    (OLD_COLORS,       NEW_COLORS),
    (OLD_COLUMNS,      NEW_COLUMNS),
    (OLD_COL_CONFIG,   NEW_COL_CONFIG),
    (OLD_COL_HEADERS,  NEW_COL_HEADERS),
    (OLD_TAGS,         NEW_TAGS),
    (OLD_SORT,         NEW_SORT),
    (OLD_POPULATE,     NEW_POPULATE),
], "app.py")

print("\n[3/3] Patching reporter.py...")
patch_file(REPORTER, [
    (OLD_FIELDNAMES,      NEW_FIELDNAMES),
    (OLD_WRITEROW,        NEW_WRITEROW),
    (OLD_SUMMARY_ROW,     NEW_SUMMARY_ROW),
    (OLD_SUMMARY_FIELDS,  NEW_SUMMARY_FIELDS),
    (OLD_SUMMARY_WRITEROW, NEW_SUMMARY_WRITEROW),
], "reporter.py")

print("\n" + "=" * 60)
print("  SELESAI. Backup disimpan sebagai *.py.bak")
print("  Jalankan test:")
print("  python3 ~/forensic_triase/platform/main.py /mnt/d/forensic_triase/dataset/infected_rogue.raw")
print("=" * 60 + "\n")