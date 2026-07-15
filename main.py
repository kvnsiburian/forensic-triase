"""
main.py
=======
Entry point Platform Triase Forensik Memori.

File ini adalah "lem" yang menghubungkan tiga modul inti:
  runner.py   → jalankan 4 plugin Volatility3
  analyzer.py → evaluasi heuristik, klasifikasi CLEAN/SUSPICIOUS
  reporter.py → export hasil ke berkas Excel (.xlsx) dan CSV (.csv)

GUI (gui/app.py) hanya memanggil fungsi run_analysis() dari sini.
Dengan desain ini, GUI dan logika analisis sepenuhnya terpisah —
jika suatu saat GUI diganti, logika inti tidak perlu diubah.

"""

import logging
import threading
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
    cancel_event: Optional[threading.Event] = None,
    use_parallel: bool = False,
    collect_timing: bool = False,
) -> dict:
    """
    Jalankan pipeline analisis lengkap terhadap satu memory dump.

    Parameter
    ---------
    dump_path : str
        Path lengkap ke file memory dump (.dmp / .raw / .vmem)

    output_dir : Path
        Folder tujuan export (default: DEFAULT_OUTPUT_DIR, yaitu /mnt/d/forensic_triase/output
        bila drive D: ada, jika tidak ke folder forensic_triase_output di home pengguna)

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
            "results_path"   : Path | None,  # path results.xlsx (Excel lengkap)
            "summary_path"   : Path | None,  # path summary.xlsx (Excel ringkasan)
            "klasifikasi_csv": Path | None,  # path klasifikasi.csv (tabel vonis)
            "timing"         : dict,         # {plugin: durasi_detik} bila collect_timing=True
            "stats": {
                "total"     : int,
                "suspicious": int,
                "clean"     : int,
            }
        }

    collect_timing : bool
        Bila True (mode CLI uji skala), jalur berurutan mengukur durasi tiap
        plugin dan mengisinya ke result["timing"]. Tidak mengubah hasil
        klasifikasi. Diabaikan pada mode paralel (use_parallel=True).
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
        "klasifikasi_csv": None,
        "timing":          {},
        "stats": {
            "total":      0,
            "suspicious": 0,
            "clean":      0,
        },
    }

    try:
        # ── Step 1: Jalankan 6 plugin Volatility3 ──────────────────────
        _notify("Memulai analisis...")
        _notify(f"File: {Path(dump_path).name}")

        runner = VolatilityRunner(dump_path=dump_path)

        from core.runner import PLUGINS

        reran_plugins = []
        timing_data = {}
        if use_parallel:
            _notify("Menjalankan 6 plugin secara paralel (multiprocessing)...")
            plugin_results, reran_plugins = runner.run_all_parallel(
                list(PLUGINS), progress=_notify, cancel_event=cancel_event
            )
            if cancel_event and cancel_event.is_set():
                logger.info("Analisis dibatalkan oleh pengguna.")
                return result
        else:
            plugin_results = {}
            for i, plugin in enumerate(PLUGINS, start=1):
                _notify(f"[{i}/{len(PLUGINS)}] Menjalankan {plugin}...")
                if collect_timing:
                    # Mode uji skala: ukur durasi tiap plugin (tak mengubah hasil)
                    plugin_results[plugin], durasi = runner.run_plugin_timed(plugin)
                    timing_data[plugin] = durasi
                    _notify(f"    durasi {plugin}: {durasi:.2f} detik")
                else:
                    plugin_results[plugin] = runner.run_plugin(plugin)
                if cancel_event and cancel_event.is_set():
                    logger.info("Analisis dibatalkan oleh pengguna.")
                    return result

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

        # ── Step 3: Export Excel + CSV ─────────────────────────────────
        _notify("Mengekspor hasil ke berkas Excel dan CSV...")
        dump_name = Path(dump_path).name
        exported  = export_all(classifications, plugin_results, dump_name, output_dir)

        _notify(f"Berkas Excel dan CSV tersimpan di: {output_dir}")

        # ── Susun hasil akhir ──────────────────────────────────────────
        result.update({
            "success":         True,
            "classifications": classifications,
            "plugin_results":  plugin_results,
            "reran_plugins":   reran_plugins,
            "results_path":    exported["results_path"],
            "summary_path":    exported["summary_path"],
            "klasifikasi_csv": exported["klasifikasi_csv"],
            "timing":          timing_data,
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
# Quick test : python3 main.py /mnt/d/dump.dmp
# Mode paralel: python3 main.py /mnt/d/dump.dmp --parallel
# Uji skala   : python3 main.py /mnt/d/dump.raw --timing
#   (mencatat durasi tiap plugin + total, menulis <dump>_timing.csv)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    import csv

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
        flags = sys.argv[2:]
        # Mode paralel opsional: tambahkan --parallel setelah path dump
        use_parallel = "--parallel" in flags
        # Uji skala: --timing catat durasi tiap plugin (hanya jalur berurutan)
        collect_timing = "--timing" in flags
        if collect_timing and use_parallel:
            # Timing per-plugin hanya bermakna di jalur berurutan
            print("  [!] --timing diabaikan karena --parallel aktif "
                  "(durasi per-plugin hanya diukur pada mode berurutan).")
            collect_timing = False

        print("\n" + "=" * 60)
        print("  CLI MODE -- main.py")
        print(f"  Mode plugin: {'PARALEL (multiprocessing)' if use_parallel else 'BERURUTAN'}")
        if collect_timing:
            print("  Timing     : AKTIF (durasi per-plugin dicatat)")
        print("=" * 60)

        def on_progress(msg: str):
            print(f"  >> {msg}")

        result = run_analysis(
            dump,
            progress_callback=on_progress,
            use_parallel=use_parallel,
            collect_timing=collect_timing,
        )

        print("\n--- HASIL AKHIR ---")
        if result["success"]:
            stats = result["stats"]
            print(f"Status     : BERHASIL")
            print(f"Total PID  : {stats['total']}")
            print(f"SUSPICIOUS : {stats['suspicious']}")
            print(f"CLEAN      : {stats['clean']}")
            print(f"results.xlsx   : {result['results_path']}")
            print(f"klasifikasi.csv: {result['klasifikasi_csv']}")
            print(f"summary.xlsx   : {result['summary_path']}")

            # ── Tabel durasi (mode uji skala) ──────────────────────────
            timing = result.get("timing") or {}
            if timing:
                total_durasi = sum(timing.values())
                print("\n--- DURASI PER-PLUGIN (uji skala) ---")
                print(f"{'Plugin':<28} {'Durasi (detik)':>14}")
                print("-" * 43)
                for plugin, durasi in timing.items():
                    print(f"{plugin:<28} {durasi:>14.2f}")
                print("-" * 43)
                print(f"{'TOTAL':<28} {total_durasi:>14.2f}")

                # Tulis CSV kecil di folder yang sama dgn dump, untuk disalin ke tabel skripsi
                timing_csv = Path(dump).with_name(Path(dump).stem + "_timing.csv")
                try:
                    with open(timing_csv, "w", newline="", encoding="utf-8") as f:
                        w = csv.writer(f)
                        w.writerow(["plugin", "durasi_detik"])
                        for plugin, durasi in timing.items():
                            w.writerow([plugin, f"{durasi:.2f}"])
                        w.writerow(["TOTAL", f"{total_durasi:.2f}"])
                    print(f"\nTabel durasi disimpan: {timing_csv}")
                except OSError as e:
                    print(f"\n[!] Gagal menulis {timing_csv}: {e}")
        else:
            print(f"Status : GAGAL")
            print(f"Error  : {result['error']}")