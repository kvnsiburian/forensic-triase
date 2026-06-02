"""
main.py
=======
Entry point Platform Triase Forensik Memori.

File ini adalah "lem" yang menghubungkan tiga modul inti:
  runner.py   → jalankan 4 plugin Volatility3
  analyzer.py → evaluasi heuristik, klasifikasi CLEAN/SUSPICIOUS
  reporter.py → export hasil ke CSV

GUI (gui/app.py) hanya memanggil fungsi run_analysis() dari sini.
Dengan desain ini, GUI dan logika analisis sepenuhnya terpisah —
jika suatu saat GUI diganti, logika inti tidak perlu diubah.

Author  : Kevin Armando Siburian (2221101800)
Program : Rekayasa Keamanan Siber - PSSN
"""

import logging
from pathlib import Path
from typing import Optional, Callable

from core.runner   import VolatilityRunner
from core.analyzer import classify_all
from core.reporter import export_all, DEFAULT_OUTPUT_DIR

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Fungsi utama — dipanggil oleh GUI
# ---------------------------------------------------------------------------

def run_analysis(
    dump_path: str,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    progress_callback: Optional[Callable[[str], None]] = None,
) -> dict:
    """
    Jalankan pipeline analisis lengkap terhadap satu memory dump.

    Parameter
    ---------
    dump_path : str
        Path lengkap ke file memory dump (.dmp / .raw / .vmem)

    output_dir : Path
        Folder tujuan export CSV (default: /mnt/d/forensic_triase/output)

    progress_callback : callable, optional
        Fungsi yang dipanggil setiap ada update status.
        GUI menggunakan ini untuk update label progress.
        Signature: callback(pesan: str) -> None

    Return
    ------
    dict
        {
            "success"        : bool,
            "error"          : str | None,
            "classifications": list[dict],   # output classify_all()
            "results_path"   : Path | None,  # path results.csv
            "summary_path"   : Path | None,  # path summary.csv
            "stats": {
                "total"     : int,
                "suspicious": int,
                "clean"     : int,
            }
        }
    """
    def _notify(msg: str) -> None:
        logger.info(msg)
        if progress_callback:
            progress_callback(msg)

    # Struktur return default
    result = {
        "success":         False,
        "error":           None,
        "classifications": [],
        "results_path":    None,
        "summary_path":    None,
        "stats": {
            "total":      0,
            "suspicious": 0,
            "clean":      0,
        },
    }

    try:
        # ── Step 1: Jalankan 4 plugin Volatility3 ──────────────────────
        _notify("Memulai analisis...")
        _notify(f"File: {Path(dump_path).name}")

        runner = VolatilityRunner(dump_path=dump_path)

        plugins = [
            "windows.pslist",
            "windows.pstree",
            "windows.netscan",
            "windows.malware.malfind",
        ]

        plugin_results = {}
        for i, plugin in enumerate(plugins, start=1):
            _notify(f"[{i}/4] Menjalankan {plugin}...")
            plugin_results[plugin] = runner.run_plugin(plugin)

        # Cek apakah semua plugin berhasil
        failed = [p for p, data in plugin_results.items() if data is None]
        if failed:
            # Plugin gagal tidak fatal — analyzer akan handle data None
            _notify(f"Peringatan: {len(failed)} plugin gagal: {failed}")

        # ── Step 2: Klasifikasi semua PID ──────────────────────────────
        _notify("Menganalisis proses...")
        classifications = classify_all(plugin_results)

        # Hitung statistik
        total      = len(classifications)
        suspicious = sum(1 for r in classifications if r["Status"] == "SUSPICIOUS")
        clean      = total - suspicious

        _notify(f"Selesai: {total} PID | {suspicious} SUSPICIOUS | {clean} CLEAN")

        # ── Step 3: Export CSV ─────────────────────────────────────────
        _notify("Mengekspor hasil ke CSV...")
        dump_name = Path(dump_path).name
        exported  = export_all(classifications, dump_name, output_dir)

        _notify(f"CSV tersimpan di: {output_dir}")

        # ── Susun hasil akhir ──────────────────────────────────────────
        result.update({
            "success":         True,
            "classifications": classifications,
            "results_path":    exported["results_path"],
            "summary_path":    exported["summary_path"],
            "stats": {
                "total":      total,
                "suspicious": suspicious,
                "clean":      clean,
            },
        })

    except FileNotFoundError as e:
        msg = str(e)
        logger.error(f"File tidak ditemukan: {msg}")
        result["error"] = msg

    except Exception as e:
        msg = f"Kesalahan tidak terduga: {e}"
        logger.exception(msg)
        result["error"] = msg

    return result


# ---------------------------------------------------------------------------
# Quick test: python3 main.py /mnt/d/dump.dmp
# ---------------------------------------------------------------------------
# Di bagian __main__ main.py, ganti seluruh blok if __name__ == "__main__":
if __name__ == "__main__":
    import sys

    # Jika dipanggil tanpa argumen → launch GUI
    if len(sys.argv) == 1:
        from gui.app import launch
        launch()
    else:
        # Jika ada argumen → mode CLI (untuk testing)
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)-7s | %(message)s",
            datefmt="%H:%M:%S",
        )
        dump = sys.argv[1]
        print("\n" + "=" * 60)
        print("  CLI MODE -- main.py")
        print("=" * 60)

        def on_progress(msg: str):
            print(f"  >> {msg}")

        result = run_analysis(dump, progress_callback=on_progress)

        print("\n--- HASIL AKHIR ---")
        if result["success"]:
            stats = result["stats"]
            print(f"Status     : BERHASIL")
            print(f"Total PID  : {stats['total']}")
            print(f"SUSPICIOUS : {stats['suspicious']}")
            print(f"CLEAN      : {stats['clean']}")
            print(f"results.csv: {result['results_path']}")
            print(f"summary.csv: {result['summary_path']}")
        else:
            print(f"Status : GAGAL")
            print(f"Error  : {result['error']}")