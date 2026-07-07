"""
regression_test.py
==================
Skrip regresi Platform Triase Forensik Memori.

Membaca hasil klasifikasi yang SUDAH TERSIMPAN di folder results/
(*.classification.json) -- TIDAK menjalankan ulang dump/plugin
Volatility3 -- lalu membandingkan Status SUSPICIOUS/CLEAN per PID
dengan ground truth lab. Menghasilkan confusion matrix (TP/FP/FN/TN)
per dataset, plus metrik agregat Sensitivity (Recall), Specificity,
dan Precision.

Ground truth (dari dokumentasi lab):
  clean_baseline            -> tidak ada PID jahat (semua proses clean)
  infected_r1a_masquerade   -> PID 4988 (svch0st.exe)
  infected_r1b_parentchild  -> PID 9140 (soffice.bin), PID 10120 (powershell.exe)
  infected_r2_network       -> PID 8732 (AtlasAgent.exe)
  infected_r3_injection     -> PID 3404 (notepad.exe)
  infected_r4a_dll          -> PID 8392 (rundll32.exe)
  infected_r4b_lsass        -> PID 8 (mimikatz.exe)

Catatan: PID 12152 (PaintStudio.Vi) di clean_baseline adalah FP yang
disengaja tidak di-whitelist -- tetap dihitung sebagai FP dalam
confusion matrix, bukan diabaikan.

Jalankan: python3 regression_test.py
Output  : regression_results.log (di folder yang sama)
"""

import json
import logging
from pathlib import Path

BASE_DIR    = Path(__file__).parent
RESULTS_DIR = BASE_DIR / "results"
LOG_FILE    = BASE_DIR / "regression_results.log"

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S",
)

# ---------------------------------------------------------------------------
# Registry dataset: (label, path file classification.json, {PID jahat})
# ---------------------------------------------------------------------------
# infected_r1b_parentchild dibaca dari folder "r1b_direct", bukan "r1b":
# "r1b" adalah percobaan awal (soffice.bin -> cmd.exe -> powershell.exe,
# PID powershell 7456) yang digantikan oleh metode WScript.Shell langsung
# (soffice.bin -> powershell.exe, PID 10120) sesuai hasil FINAL di
# docs/progress_log.md Dataset 3. "r1b_direct" cocok persis dengan
# ground truth (PID 9140 & 10120) sementara "r1b" tidak.

DATASETS = [
    ("clean_baseline",
     RESULTS_DIR / "clean_baseline" / "clean_baseline.classification.json",
     set()),
    ("infected_r1a_masquerade",
     RESULTS_DIR / "infected_r1a_masquerade" / "infected_r1a_masquerade.classification.json",
     {4988}),
    ("infected_r1b_parentchild",
     RESULTS_DIR / "r1b_direct" / "infected_r1b_parentchild.classification.json",
     {9140, 10120}),
    ("infected_r2_network",
     RESULTS_DIR / "r2_network" / "infected_r2_network.classification.json",
     {8732}),
    ("infected_r3_injection",
     RESULTS_DIR / "r3_injection" / "infected_r3_injection.classification.json",
     {3404}),
    ("infected_r4a_dll",
     RESULTS_DIR / "r4a_dll" / "infected_r4a_dll.classification.json",
     {8392}),
    ("infected_r4b_lsass",
     RESULTS_DIR / "r4b_lsass" / "infected_r4b_lsass.classification.json",
     {8}),
]


def log(msg: str):
    print(msg, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")


# ---------------------------------------------------------------------------
# Evaluasi satu dataset terhadap ground truth
# ---------------------------------------------------------------------------

def evaluate_dataset(label: str, path: Path, malicious_pids: set) -> dict:
    log(f"\n{'='*70}")
    log(f"DATASET : {label}")
    log(f"FILE    : {path.relative_to(BASE_DIR)}")
    log(f"{'='*70}")

    if not path.exists():
        log(f"[ERROR] File tidak ditemukan: {path}")
        return None

    with open(path, encoding="utf-8") as f:
        records = json.load(f)

    seen_pids = set()
    tp = fp = fn = tn = 0
    tp_list, fp_list, fn_list = [], [], []

    for rec in records:
        pid = rec["PID"]
        seen_pids.add(pid)
        predicted = rec["Status"] == "SUSPICIOUS"
        actual    = pid in malicious_pids

        if predicted and actual:
            tp += 1
            tp_list.append(rec)
        elif predicted and not actual:
            fp += 1
            fp_list.append(rec)
        elif not predicted and actual:
            fn += 1
            fn_list.append(rec)
        else:
            tn += 1

    # PID jahat di ground truth yang tidak muncul sama sekali di data plugin
    # (mis. proses sudah exit sebelum dump) -> tetap dihitung FN.
    missing = malicious_pids - seen_pids
    for pid in missing:
        fn += 1
        log(f"  [WARNING] PID {pid} (ground truth) tidak ditemukan di data -- dihitung FN")

    total = len(records)

    log(f"  Total PID          : {total}")
    log(f"  Ground truth jahat : {sorted(malicious_pids) if malicious_pids else '(tidak ada)'}")
    log(f"  TP={tp}  FP={fp}  FN={fn}  TN={tn}")

    if tp_list:
        log("  --- True Positive (terdeteksi & memang jahat) ---")
        for rec in tp_list:
            log(f"    PID={rec['PID']:<6} {rec['Name']}")

    if fp_list:
        log("  --- False Positive (terdeteksi tapi seharusnya clean) ---")
        for rec in fp_list:
            log(f"    PID={rec['PID']:<6} {rec['Name']:<20} Reasons={rec['Reasons']}")

    if fn_list:
        log("  --- False Negative (jahat tapi lolos, tidak terdeteksi) ---")
        for rec in fn_list:
            log(f"    PID={rec['PID']:<6} {rec['Name']}")

    return {"label": label, "total": total, "tp": tp, "fp": fp, "fn": fn, "tn": tn}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if LOG_FILE.exists():
        LOG_FILE.unlink()

    log("REGRESI PLATFORM TRIASE FORENSIK MEMORI (baca hasil tersimpan di results/)")
    log(f"Log     : {LOG_FILE}")
    log(f"Datasets: {len(DATASETS)}")

    all_results = []
    for label, path, gt in DATASETS:
        result = evaluate_dataset(label, path, gt)
        if result:
            all_results.append(result)

    # -----------------------------------------------------------------------
    # Confusion matrix per dataset + agregat
    # -----------------------------------------------------------------------
    log(f"\n{'='*70}")
    log("CONFUSION MATRIX PER DATASET")
    log(f"{'='*70}")
    log(f"  {'Dataset':<26} {'Total':>6} {'TP':>4} {'FP':>4} {'FN':>4} {'TN':>4}")
    log("  " + "-" * 58)
    for r in all_results:
        log(f"  {r['label']:<26} {r['total']:>6} {r['tp']:>4} {r['fp']:>4} {r['fn']:>4} {r['tn']:>4}")

    grand_total = sum(r["total"] for r in all_results)
    grand_tp    = sum(r["tp"]    for r in all_results)
    grand_fp    = sum(r["fp"]    for r in all_results)
    grand_fn    = sum(r["fn"]    for r in all_results)
    grand_tn    = sum(r["tn"]    for r in all_results)

    log("  " + "-" * 58)
    log(f"  {'TOTAL':<26} {grand_total:>6} {grand_tp:>4} {grand_fp:>4} {grand_fn:>4} {grand_tn:>4}")

    # -----------------------------------------------------------------------
    # Metrik agregat
    # -----------------------------------------------------------------------
    sensitivity = grand_tp / (grand_tp + grand_fn) if (grand_tp + grand_fn) else float("nan")
    specificity = grand_tn / (grand_tn + grand_fp) if (grand_tn + grand_fp) else float("nan")
    precision   = grand_tp / (grand_tp + grand_fp) if (grand_tp + grand_fp) else float("nan")

    log(f"\n{'='*70}")
    log("METRIK AGREGAT")
    log(f"{'='*70}")
    log(f"  Sensitivity (Recall) : {sensitivity:.4f}   ({grand_tp}/{grand_tp + grand_fn})")
    log(f"  Specificity          : {specificity:.4f}   ({grand_tn}/{grand_tn + grand_fp})")
    log(f"  Precision            : {precision:.4f}   ({grand_tp}/{grand_tp + grand_fp})")

    log(f"\nSelesai.")
