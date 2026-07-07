#!/usr/bin/env python3
"""
run_dataset.py — driver analisis satu dataset untuk pengujian platform.

Menjalankan 6 plugin Volatility3 (tanpa timeout artifisial), menyimpan JSON
mentah tiap plugin, lalu mengklasifikasikan dengan core.analyzer.classify_all.

Pemakaian:
    python3 run_dataset.py <path_dump> <out_dir> [label]
"""
import sys, json, subprocess, time
from pathlib import Path

VOL = str(Path.home() / ".local" / "bin" / "vol")
PLUGINS = [
    "windows.pslist", "windows.pstree", "windows.netscan",
    "windows.malware.malfind", "windows.dlllist", "windows.handles",
]

def main():
    dump = sys.argv[1]
    outdir = Path(sys.argv[2]); outdir.mkdir(parents=True, exist_ok=True)
    label = sys.argv[3] if len(sys.argv) > 3 else Path(dump).stem

    print(f"=== DRIVER: {label} ===", flush=True)
    print(f"dump  : {dump}", flush=True)
    print(f"outdir: {outdir}", flush=True)

    plugin_results = {}
    for i, p in enumerate(PLUGINS, 1):
        t0 = time.time()
        print(f"[{i}/6] {p} ...", flush=True)
        r = subprocess.run([VOL, "-f", dump, "--renderer", "json", p],
                           capture_output=True, text=True)
        dt = time.time() - t0
        if r.returncode != 0:
            print(f"    FAIL rc={r.returncode} ({dt:.0f}s): {r.stderr[-400:]}", flush=True)
            plugin_results[p] = None
            (outdir / f"{label}.{p}.error.txt").write_text(r.stderr[-4000:])
            continue
        try:
            data = json.loads(r.stdout) if r.stdout.strip() else []
        except json.JSONDecodeError as e:
            print(f"    JSON parse error ({dt:.0f}s): {e}", flush=True)
            plugin_results[p] = None
            continue
        if isinstance(data, dict) and "columns" in data and "rows" in data:
            recs = [dict(zip(data["columns"], row)) for row in data["rows"]]
        elif isinstance(data, list):
            recs = data
        else:
            recs = []
        plugin_results[p] = recs
        (outdir / f"{label}.{p}.json").write_text(json.dumps(recs))
        print(f"    OK {len(recs)} records in {dt:.0f}s", flush=True)

    # Klasifikasi
    sys.path.insert(0, str(Path.home() / "forensic_triase" / "platform"))
    from core.analyzer import classify_all
    results = classify_all(plugin_results)
    susp = [r for r in results if r["Status"] == "SUSPICIOUS"]
    clean = [r for r in results if r["Status"] == "CLEAN"]

    print(f"\n=== TOTAL {len(results)} | CLEAN {len(clean)} | SUSPICIOUS {len(susp)} ===", flush=True)
    for r in susp:
        print(f"PID={r['PID']} {r['Name']} | R1={r['Rule1_hit']} R2={r['Rule2_hit']} "
              f"R3={r['Rule3_hit']} R4={r['Rule4_hit']}", flush=True)
        for reason in r["Reasons"]:
            print(f"   -> {reason}", flush=True)

    (outdir / f"{label}.classification.json").write_text(
        json.dumps(results, indent=2, default=str))
    print(f"\nsaved: {label}.classification.json", flush=True)
    print("=== DONE ===", flush=True)

if __name__ == "__main__":
    main()
