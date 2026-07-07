"""
runner.py
=========
Modul eksekusi plugin Volatility3 untuk Platform Triase Forensik Memori.

Tanggung jawab modul ini:
  - Memvalidasi keberadaan vol binary dan file memory dump
  - Menjalankan 6 plugin Volatility3 secara sekuensial
  - Mem-parsing output JSON dari setiap plugin menjadi list of dict
  - Mengembalikan hasil mentah ke analyzer.py untuk evaluasi heuristik

Plugin yang dieksekusi (struktur final pasca revisi, 6 plugin / 4 kategori SANS):
  1. windows.pslist           → Identify Rogue Processes (daftar proses, typosquatting/path)
  2. windows.pstree           → Identify Rogue Processes (anomali induk-anak)
  3. windows.netscan          → Review Network Artifacts
  4. windows.malware.malfind  → Look for Evidence of Code Injection
  5. windows.dlllist          → Analyze Process Objects (DLL dari path mencurigakan)
  6. windows.handles          → Analyze Process Objects (akses mencurigakan ke LSASS)

Catatan revisi:
  - pstree sebelumnya keliru dikategorikan sebagai "Analyze Process Objects".
    Berdasarkan verifikasi ke poster resmi SANS Memory Forensics Cheat Sheet
    (edisi Volatility3), pstree termasuk kategori "Identify Rogue Processes".
    dlllist dan handles adalah anggota asli kategori "Analyze Process Objects".
  - windows.dlllist dan windows.handles ditambahkan atas persetujuan Pak Rahmat
    (WhatsApp, 30 Juni 2026), berdasar Q13 poin 3 dan poin 5 transkrip wawancara.

Catatan teknis:
  - Menggunakan --renderer json agar output terstruktur dan mudah di-parse
  - Volatility3 menulis log ke stderr, output data ke stdout -> aman di-split
  - Timeout default 300 detik per plugin (memory dump ~2GB butuh waktu)
  - Platform Linux only sesuai pembatasan masalah (proposal BAB I)

Author  : Kevin Armando Siburian (2221101800)
Program : Rekayasa Keamanan Siber - PSSN
"""

import subprocess
import json
import logging
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Konfigurasi
# ---------------------------------------------------------------------------

# Path default vol binary di Kali Linux WSL2 (hasil pip install volatility3)
DEFAULT_VOL_PATH = Path.home() / ".local" / "bin" / "vol"

# 6 plugin yang digunakan -- urutan ini juga urutan eksekusi
PLUGINS = [
    "windows.pslist",           # daftar proses aktif
    "windows.pstree",           # hierarki parent-child proses
    "windows.netscan",          # koneksi jaringan aktif
    "windows.malware.malfind",  # segmen memori PAGE_EXECUTE_READWRITE
    "windows.dlllist",          # DLL yang dimuat tiap proses
    "windows.handles",          # handle antarproses (termasuk akses ke LSASS)
]

# Timeout per plugin dalam detik
PLUGIN_TIMEOUT = 300

# ---------------------------------------------------------------------------
# Setup logging
# ---------------------------------------------------------------------------
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Kelas utama
# ---------------------------------------------------------------------------

class VolatilityRunner:
    """
    Wrapper eksekusi Volatility3 untuk 6 plugin triase.

    Contoh penggunaan:
        runner = VolatilityRunner("/mnt/d/forensic_triase/dataset/dump.dmp")
        results = runner.run_all()
        # results["windows.pslist"] -> list of dict, atau None jika gagal
    """

    def __init__(
        self,
        dump_path: str,
        vol_path: str = str(DEFAULT_VOL_PATH),
    ):
        self.dump_path = Path(dump_path)
        self.vol_path = Path(vol_path)

    # ------------------------------------------------------------------
    # Validasi awal
    # ------------------------------------------------------------------

    def validate(self) -> None:
        """
        Periksa apakah vol binary dan file dump ada sebelum eksekusi.
        Raise FileNotFoundError jika salah satu tidak ditemukan.
        """
        if not self.vol_path.exists():
            raise FileNotFoundError(
                f"Volatility3 binary tidak ditemukan di: {self.vol_path}\n"
                f"Pastikan volatility3 sudah diinstall: pip install volatility3"
            )
        if not self.dump_path.exists():
            raise FileNotFoundError(
                f"Memory dump tidak ditemukan: {self.dump_path}"
            )
        logger.info(f"Validasi OK -- dump: {self.dump_path} | vol: {self.vol_path}")

    # ------------------------------------------------------------------
    # Eksekusi satu plugin
    # ------------------------------------------------------------------

    def run_plugin(self, plugin: str) -> Optional[list]:
        """
        Jalankan satu plugin Volatility3 dan kembalikan hasilnya sebagai
        list of dict. Kembalikan None jika plugin gagal atau timeout.

        Parameter
        ---------
        plugin : str
            Nama plugin Volatility3, contoh "windows.pslist"

        Return
        ------
        list[dict] | None
            Setiap dict mewakili satu baris output plugin.
            Key = nama kolom (string), Value = nilai baris.

            Contoh satu record windows.pslist:
            {
                "PID": 1234,
                "PPID": 5678,
                "ImageFileName": "svchost.exe",
                ...
            }
        """
        cmd = [
            str(self.vol_path),
            "-f", str(self.dump_path),
            "--renderer", "json",   # output JSON terstruktur ke stdout
            plugin,
        ]
        logger.info(f"[{plugin}] Memulai eksekusi...")
        logger.debug(f"Perintah: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=PLUGIN_TIMEOUT,
            )

            # Volatility3 kadang menulis warning non-fatal ke stderr
            if result.stderr:
                for line in result.stderr.splitlines():
                    if line.strip():
                        logger.debug(f"[{plugin}] stderr: {line}")

            if result.returncode != 0:
                logger.error(
                    f"[{plugin}] Eksekusi gagal (returncode={result.returncode}). "
                    f"Pesan: {result.stderr[:300]}"
                )
                return None

            return self._parse_json_output(plugin, result.stdout)

        except subprocess.TimeoutExpired:
            logger.error(
                f"[{plugin}] Timeout setelah {PLUGIN_TIMEOUT} detik. "
                f"Memory dump mungkin terlalu besar atau corrupt."
            )
            return None

        except Exception as e:
            logger.exception(f"[{plugin}] Kesalahan tidak terduga: {e}")
            return None

    # ------------------------------------------------------------------
    # Parse output JSON dari Volatility3
    # ------------------------------------------------------------------

    def _parse_json_output(self, plugin: str, raw_stdout: str) -> Optional[list]:
        """
        Parse stdout JSON dari Volatility3 menjadi list of dict.

        Volatility3 --renderer json menghasilkan format:
            {"columns": ["PID", "PPID", ...], "rows": [[4, 0, ...], ...]}

        Setiap row dikonversi menjadi dict menggunakan columns sebagai key.
        """
        if not raw_stdout.strip():
            logger.warning(f"[{plugin}] Output kosong. Tidak ada data ditemukan.")
            return []

        try:
            data = json.loads(raw_stdout)
        except json.JSONDecodeError as e:
            logger.error(
                f"[{plugin}] Gagal parse JSON: {e}\n"
                f"Output awal (100 char): {raw_stdout[:100]!r}"
            )
            return None

        # Format Volatility3: dict dengan key "columns" dan "rows"
        if isinstance(data, dict) and "columns" in data and "rows" in data:
            columns = data["columns"]
            rows = data["rows"]
            records = [dict(zip(columns, row)) for row in rows]
            logger.info(f"[{plugin}] Berhasil parse {len(records)} record.")
            return records

        # Fallback: jika output sudah berupa list of dict langsung
        if isinstance(data, list):
            logger.info(f"[{plugin}] Berhasil parse {len(data)} record (format list).")
            return data

        logger.error(
            f"[{plugin}] Format JSON tidak dikenali. "
            f"Keys: {list(data.keys()) if isinstance(data, dict) else type(data)}"
        )
        return None

    # ------------------------------------------------------------------
    # Jalankan semua 6 plugin
    # ------------------------------------------------------------------

    def run_all(self) -> dict:
        """
        Jalankan keenam plugin secara sekuensial terhadap memory dump.

        Return
        ------
        dict
            Key   = nama plugin (str)
            Value = list of dict (hasil plugin), atau None jika plugin gagal

        Contoh:
            {
                "windows.pslist": [ {...}, {...}, ... ],
                "windows.pstree": [ {...}, ... ],
                "windows.netscan": [ {...}, ... ],
                "windows.malware.malfind": [ {...}, ... ] atau None,
                "windows.dlllist": [ {...}, ... ],
                "windows.handles": [ {...}, ... ]
            }
        """
        self.validate()

        logger.info("=" * 60)
        logger.info(f"Memulai analisis: {self.dump_path.name}")
        logger.info(f"Total plugin: {len(PLUGINS)}")
        logger.info("=" * 60)

        results = {}

        for i, plugin in enumerate(PLUGINS, start=1):
            logger.info(f"[{i}/{len(PLUGINS)}] {plugin}")
            results[plugin] = self.run_plugin(plugin)

        # Ringkasan hasil
        logger.info("=" * 60)
        logger.info("Ringkasan eksekusi plugin:")
        for plugin, data in results.items():
            if data is None:
                status = "GAGAL"
            elif len(data) == 0:
                status = "OK (0 record)"
            else:
                status = f"OK ({len(data)} record)"
            logger.info(f"  {plugin:<35} -> {status}")
        logger.info("=" * 60)

        return results

    # ------------------------------------------------------------------
    # Info summary (berguna untuk GUI)
    # ------------------------------------------------------------------

    def get_summary(self, results: dict) -> dict:
        """
        Buat ringkasan hasil run_all() untuk ditampilkan di GUI.

        Return dict berisi:
            dump_name    : nama file memory dump
            plugin_count : jumlah plugin yang dieksekusi
            record_counts: dict plugin -> jumlah record (-1 jika gagal)
            has_error    : True jika ada minimal satu plugin yang gagal
        """
        record_counts = {}
        has_error = False

        for plugin, data in results.items():
            if data is None:
                record_counts[plugin] = -1
                has_error = True
            else:
                record_counts[plugin] = len(data)

        return {
            "dump_name": self.dump_path.name,
            "plugin_count": len(PLUGINS),
            "record_counts": record_counts,
            "has_error": has_error,
        }


# ---------------------------------------------------------------------------
# Quick test -- jalankan langsung untuk verifikasi koneksi Volatility3
# python3 runner.py [path/ke/dump.dmp]
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%H:%M:%S",
    )

    DUMP_DEV = "/mnt/d/dump.dmp"

    print("\n" + "=" * 60)
    print("  QUICK TEST -- VolatilityRunner")
    print("=" * 60)

    dump = sys.argv[1] if len(sys.argv) > 1 else DUMP_DEV
    if dump == DUMP_DEV:
        print(f"Tidak ada argumen. Menggunakan dump default: {dump}")

    try:
        runner = VolatilityRunner(dump_path=dump)
        results = runner.run_all()
        summary = runner.get_summary(results)

        print("\n--- SUMMARY ---")
        print(f"Dump     : {summary['dump_name']}")
        print(f"Plugins  : {summary['plugin_count']}")
        print(f"Has Error: {summary['has_error']}")
        for plugin, count in summary["record_counts"].items():
            label = f"{count} record" if count >= 0 else "GAGAL"
            print(f"  {plugin:<35} -> {label}")

        # Sanity check: tampilkan 2 record pertama dari pslist
        pslist = results.get("windows.pslist")
        if pslist:
            print("\n--- Contoh 2 record windows.pslist ---")
            for rec in pslist[:2]:
                print(f"  PID={rec.get('PID')} | "
                      f"PPID={rec.get('PPID')} | "
                      f"Name={rec.get('ImageFileName')}")

    except FileNotFoundError as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)