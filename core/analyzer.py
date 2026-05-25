"""
analyzer.py
===========
Modul evaluasi heuristik untuk Platform Triase Forensik Memori.

Modul ini menerima hasil mentah dari runner.py (4 plugin Volatility3)
dan mengevaluasi setiap PID unik melalui 4 pemeriksaan indikator anomali
sesuai SANS Memory Forensics Methodology (proposal BAB III).

Alur kerja:
  1. Kumpulkan semua PID unik dari semua plugin
  2. Bangun lookup table: PID -> data proses dari setiap plugin
  3. Evaluasi setiap PID melalui 4 heuristic rules
  4. Klasifikasikan: SUSPICIOUS (>= 1 rule terpenuhi) atau CLEAN

Klasifikasi bersifat binary (proposal BAB III):
  - Sensitivitas diprioritaskan atas spesifisitas
  - Satu indikator cukup untuk flag SUSPICIOUS
  - Tidak ada "medium" atau "low" — hanya CLEAN / SUSPICIOUS

4 Heuristic Rules (sesuai field names aktual dari Volatility3 2.28.1):
  Rule 1: Identify Rogue Processes
    Source  : windows.pslist + windows.pstree
    Fields  : ImageFileName, Path
    Logic   : typosquatting nama proses sistem ATAU path eksekusi mencurigakan

  Rule 2: Review Network Artifacts
    Source  : windows.netscan
    Fields  : Owner, PID, State, ForeignAddr, ForeignPort
    Logic   : proses non-network punya koneksi ESTABLISHED outbound

  Rule 3: Look for Evidence of Code Injection
    Source  : windows.malware.malfind
    Fields  : Protection, PrivateMemory
    Logic   : PAGE_EXECUTE_READWRITE + PrivateMemory = 1

  Rule 4: Analyze Process Objects
    Source  : windows.pstree (flattened)
    Fields  : ImageFileName, PPID -> lookup ke ImageFileName parent
    Logic   : parent-child menyimpang dari baseline Windows

Author  : Kevin Armando Siburian (2221101800)
Program : Rekayasa Keamanan Siber - PSSN
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Baseline Windows — Rule 1: Typosquatting Detection
# ---------------------------------------------------------------------------

# Proses sistem Windows yang sah — digunakan sebagai referensi
# Sumber: SANS DFIR Cheat Sheet, Microsoft Documentation
LEGIT_WINDOWS_PROCESSES = {
    "system", "registry", "smss.exe", "csrss.exe", "wininit.exe",
    "services.exe", "lsass.exe", "svchost.exe", "winlogon.exe",
    "explorer.exe", "taskhostw.exe", "sihost.exe", "fontdrvhost.exe",
    "dwm.exe", "spoolsv.exe", "msdtc.exe", "wlanext.exe",
    "conhost.exe", "dllhost.exe", "lsaiso.exe", "runtimebroker.exe",
    "searchindexer.exe", "wmiprvse.exe", "wmiapsrv.exe",
    "searchprotocolhost.exe", "searchfilterhost.exe",
    "msmpeng.exe", "nissrv.exe", "securityhealthservice.exe",
    "sihclient.exe", "msiexec.exe", "wuauclt.exe",
    "audiodg.exe", "dashost.exe", "ctfmon.exe",
    "applicationframehost.exe", "shellexperiencehost.exe",
    "startmenuexperiencehost.exe", "textinputhost.exe", "fontdrvhost.ex", "nissrv.exe", "mpdefendercoreser",
}

# Path eksekusi yang mencurigakan (proses sistem tidak seharusnya di sini)
SUSPICIOUS_PATH_KEYWORDS = [
    "\\temp\\",
    "\\tmp\\",
    "\\appdata\\local\\temp\\",
    "\\appdata\\roaming\\",
    "\\users\\public\\",
    "\\downloads\\",
    "\\recycle",
    "\\programdata\\",
    "\\desktop\\",
]

# Proses yang secara legitimate menggunakan PAGE_EXECUTE_READWRITE ; mantap
# Karena teknik JIT compilation, scan engine, atau runtime optimization
# Sumber: Microsoft documentation + SANS FOR508 baseline
LEGIT_RWX_PROCESSES = {
    "msmpeng.exe",          # Windows Defender — JIT scan engine
    "nissrv.exe",           # Windows Defender NIS
    "mpdefendercoreser",    # Windows Defender Core (truncated 14 char)
    "onedrive.exe",         # OneDrive sync engine
    "smartscreen.exe",
    "smartscreen.ex",       # truncated 14 char
    "chrome.exe",           # V8 JIT
    "firefox.exe",          # SpiderMonkey JIT
    "msedge.exe",           # V8 JIT
    "node.exe",             # V8 JIT
    "searchapp.exe",    # Windows Search
    "searchapp.ex",     # truncated 14 char
    "phoneexperienc",   # Phone Experience Host (truncated 14 char)
}

# Path yang NORMAL untuk proses sistem Windows
LEGIT_PATH_PREFIXES = [
    "c:\\windows\\system32\\",
    "c:\\windows\\syswow64\\",
    "c:\\windows\\",
    "c:\\program files\\",
    "c:\\program files (x86)\\",
    "c:\\programdata\\microsoft\\windows defender\\",  # Windows Defender legitimate path

]


# ---------------------------------------------------------------------------
# Baseline Windows — Rule 2: Network Artifacts
# ---------------------------------------------------------------------------

# Proses yang WAJAR memiliki koneksi jaringan outbound
# Proses di luar daftar ini yang punya koneksi outbound → SUSPICIOUS
LEGIT_NETWORK_PROCESSES = {
    "svchost.exe", "lsass.exe", "services.exe",
    "explorer.exe", "chrome.exe", "firefox.exe", "msedge.exe",
    "iexplore.exe", "opera.exe", "brave.exe",
    "onedrive.exe", "dropbox.exe", "googledrivefs.exe",
    "teams.exe", "slack.exe", "zoom.exe", "discord.exe",
    "skype.exe", "outlook.exe", "thunderbird.exe",
    "wuauclt.exe", "msiexec.exe", "winlogon.exe",
    "spoolsv.exe", "searchindexer.exe", "wmiprvse.exe",
    "msmpeng.exe", "nissrv.exe", "securityhealthservice.exe",
    "dashost.exe", "runtimebroker.exe",
    # Proses khusus Windows Update
    "wuapihost.exe", "usoclient.exe", "musnotification.exe",
    # System-level
    "system",
    "smartscreen.exe",    # Windows SmartScreen — cek reputasi file ke Microsoft
    "searchapp.exe",      # Windows Search — koneksi ke Bing
    "searchui.exe",       # Versi lama SearchApp
    "onedrive.exe",       # Sudah ada, tapi pastikan ada
    "msmpeng.exe",        # Windows Defender — sudah ada
    "nissrv.exe",         # Windows Defender NIS
    "mpdefendercoreser",  # Windows Defender Core (truncated)
    # Tambahkan di LEGIT_NETWORK_PROCESSES:
    "smartscreen.ex",       # truncated dari smartscreen.exe (15 -> 14 char)
    "searchapp.exe",        # sudah ada, pastikan ada
    # Tambahkan di LEGIT_NETWORK_PROCESSES:
    "onedrive.sync.",       # OneDrive SyncEngine (truncated 14 char)
    "backgroundtask",       # backgroundTaskHost.exe (truncated 14 char)
    "m365copilot.ex",       # Microsoft 365 Copilot (truncated 14 char)
    "m365copilot.exe",      # full name
    "backgroundtaskh",      # variant truncated
    "msedgewebview2",   # Microsoft Edge WebView2
}


# ---------------------------------------------------------------------------
# Baseline Windows — Rule 4: Parent-Child Relationship
# ---------------------------------------------------------------------------

# Format: {nama_child: set of ALLOWED parent names}
# Jika parent child tidak ada dalam set -> SUSPICIOUS
# Sumber: SANS FOR508, Microsoft Process Security documentation
NORMAL_PARENT_CHILD = {
    # smss.exe seharusnya child dari System
    "smss.exe": {"system"},

    # csrss.exe seharusnya child dari smss.exe
    "csrss.exe": {"smss.exe"},

    # wininit.exe child dari smss.exe
    "wininit.exe": {"smss.exe"},

    # winlogon.exe child dari smss.exe
    "winlogon.exe": {"smss.exe"},

    # services.exe child dari wininit.exe
    "services.exe": {"wininit.exe"},

    # lsass.exe child dari wininit.exe
    "lsass.exe": {"wininit.exe"},

    # svchost.exe HARUS child dari services.exe
    "svchost.exe": {"services.exe"},

    # explorer.exe child dari userinit.exe atau winlogon.exe
    "explorer.exe": {"userinit.exe", "winlogon.exe"},

    # taskhost, taskhostw child dari services.exe
    "taskhostw.exe": {"services.exe", "svchost.exe"},

    # RuntimeBroker child dari svchost.exe
    "runtimebroker.exe": {"svchost.exe"},

    # spoolsv child dari services.exe
    "spoolsv.exe": {"services.exe"},

    # searchindexer child dari services.exe
    "searchindexer.exe": {"services.exe"},

    # conhost biasanya child dari berbagai proses (lebih fleksibel)
    # tidak dimasukkan karena terlalu umum

    # cmd.exe dan powershell.exe yang TIDAK wajar jika parent adalah Office/PDF
    # → ditangani di SUSPICIOUS_CHILD_SPAWNERS di bawah
}

# Proses yang TIDAK seharusnya spawn shell atau interpreter
# Jika proses ini punya child cmd.exe/powershell.exe/wscript.exe → SUSPICIOUS
SUSPICIOUS_CHILD_SPAWNERS = {
    "winword.exe", "excel.exe", "powerpnt.exe",  # Microsoft Office
    "acrord32.exe", "acrobat.exe",                # Adobe
    "outlook.exe",
    "iexplore.exe", "chrome.exe", "firefox.exe", "msedge.exe",
    "notepad.exe",
}

SHELL_PROCESSES = {
    "cmd.exe", "powershell.exe", "powershell_ise.exe",
    "wscript.exe", "cscript.exe", "mshta.exe",
    "wmic.exe", "regsvr32.exe", "rundll32.exe",
    "certutil.exe", "bitsadmin.exe",
}


# ---------------------------------------------------------------------------
# Helper: Flatten pstree (recursive)
# ---------------------------------------------------------------------------

def flatten_pstree(pstree_records: list) -> list:
    """
    Flatten struktur pstree yang nested menjadi list of dict datar.

    pstree menggunakan __children untuk menyimpan child processes.
    Fungsi ini mengekstrak semua node dari tree secara rekursif.

    Parameter
    ---------
    pstree_records : list
        Output mentah dari windows.pstree (bisa nested)

    Return
    ------
    list[dict]
        Semua proses dalam struktur flat, setiap dict berisi field
        yang sama dengan record pstree (termasuk PID, PPID, ImageFileName, Path)
    """
    flat = []
    for record in pstree_records:
        # Buat salinan tanpa __children untuk record ini
        node = {k: v for k, v in record.items() if k != "__children"}
        flat.append(node)
        # Rekursif untuk children
        children = record.get("__children", [])
        if children and isinstance(children, list):
            flat.extend(flatten_pstree(children))
    return flat


# ---------------------------------------------------------------------------
# Helper: Build lookup tables dari hasil plugin
# ---------------------------------------------------------------------------

def build_lookup_tables(plugin_results: dict) -> dict:
    """
    Bangun lookup tables dari hasil 4 plugin untuk mempercepat evaluasi.

    Return dict berisi:
        all_pids         : set semua PID unik dari semua plugin
        pslist_by_pid    : dict PID -> record pslist
        pstree_flat      : list semua record pstree (sudah di-flatten)
        pstree_by_pid    : dict PID -> record pstree (untuk akses Path)
        pid_to_parent_name: dict PID -> nama ImageFileName parent-nya
        netscan_by_pid   : dict PID -> list record netscan
        malfind_by_pid   : dict PID -> list record malfind
    """
    pslist  = plugin_results.get("windows.pslist") or []
    pstree  = plugin_results.get("windows.pstree") or []
    netscan = plugin_results.get("windows.netscan") or []
    malfind = plugin_results.get("windows.malware.malfind") or []

    # Flatten pstree
    pstree_flat = flatten_pstree(pstree)

    # Build pslist lookup
    pslist_by_pid = {}
    for rec in pslist:
        pid = rec.get("PID")
        if pid is not None:
            pslist_by_pid[pid] = rec

    # Build pstree lookup (by PID, setelah flatten)
    pstree_by_pid = {}
    for rec in pstree_flat:
        pid = rec.get("PID")
        if pid is not None:
            pstree_by_pid[pid] = rec

    # Build parent name lookup: PID -> nama ImageFileName parent
    pid_to_parent_name = {}
    for rec in pstree_flat:
        pid  = rec.get("PID")
        ppid = rec.get("PPID")
        if pid is None or ppid is None:
            continue
        parent_rec = pstree_by_pid.get(ppid) or pslist_by_pid.get(ppid)
        if parent_rec:
            parent_name = str(parent_rec.get("ImageFileName", "")).lower()
            pid_to_parent_name[pid] = parent_name

    # Build netscan lookup: PID -> list of records
    netscan_by_pid = {}
    for rec in netscan:
        pid = rec.get("PID")
        if pid is not None:
            netscan_by_pid.setdefault(pid, []).append(rec)

    # Build malfind lookup: PID -> list of records
    malfind_by_pid = {}
    for rec in malfind:
        pid = rec.get("PID")
        if pid is not None:
            malfind_by_pid.setdefault(pid, []).append(rec)

    # Kumpulkan semua PID unik dari semua plugin
    all_pids = (
        set(pslist_by_pid.keys())
        | set(pstree_by_pid.keys())
        | set(netscan_by_pid.keys())
        | set(malfind_by_pid.keys())
    )

    logger.info(f"Total PID unik ditemukan: {len(all_pids)}")

    return {
        "all_pids":           all_pids,
        "pslist_by_pid":      pslist_by_pid,
        "pstree_flat":        pstree_flat,
        "pstree_by_pid":      pstree_by_pid,
        "pid_to_parent_name": pid_to_parent_name,
        "netscan_by_pid":     netscan_by_pid,
        "malfind_by_pid":     malfind_by_pid,
    }


# ---------------------------------------------------------------------------
# Rule 1: Identify Rogue Processes
# ---------------------------------------------------------------------------

def _edit_distance(s1: str, s2: str) -> int:
    """Hitung Levenshtein distance antara dua string."""
    m, n = len(s1), len(s2)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, n + 1):
            temp = dp[j]
            if s1[i - 1] == s2[j - 1]:
                dp[j] = prev
            else:
                dp[j] = 1 + min(prev, dp[j], dp[j - 1])
            prev = temp
    return dp[n]

def check_rogue_process(
    proc_name: str,
    proc_path: Optional[str],
) -> tuple[bool, list[str]]:
    reasons = []
    name_lower = proc_name.lower()

    # (a) Typosquatting check
    # PENTING: Cek apakah nama PERSIS ada di whitelist SEBELUM loop.
    # Tanpa ini, proses legit bisa kena flag karena mirip dengan proses
    # legit lain di set (contoh: lsass.exe vs lsaiso.exe, edit distance=2).
    if name_lower not in LEGIT_WINDOWS_PROCESSES:
        for legit in LEGIT_WINDOWS_PROCESSES:
            dist = _edit_distance(name_lower, legit)
            if dist <= 2 and len(name_lower) >= 4:
                reasons.append(
                    f"[Rule1] Typosquatting: '{proc_name}' mirip '{legit}' "
                    f"(edit distance={dist})"
                )
                break

    # (b) Suspicious path check
    # Cek path HANYA jika path bukan None dan bukan path legitimate yang dikenal
    if proc_path and proc_path not in (None, "None", ""):
        path_lower = proc_path.lower()

        # Jika path dimulai dengan prefix legitimate, skip cek suspicious keyword
        is_legit_path = any(
            path_lower.startswith(prefix) for prefix in LEGIT_PATH_PREFIXES
        )

        if not is_legit_path:
            for keyword in SUSPICIOUS_PATH_KEYWORDS:
                if keyword in path_lower:
                    reasons.append(
                        f"[Rule1] Path mencurigakan: '{proc_path}' "
                        f"mengandung '{keyword}'"
                    )
                    break

    return (len(reasons) > 0, reasons)


# ---------------------------------------------------------------------------
# Rule 2: Review Network Artifacts
# ---------------------------------------------------------------------------

def check_network_artifacts(
    proc_name: str,
    netscan_records: list,
) -> tuple[bool, list[str]]:
    """
    Rule 2: Review Network Artifacts.

    Proses yang tidak seharusnya punya koneksi jaringan (tidak ada dalam
    LEGIT_NETWORK_PROCESSES) tetapi memiliki koneksi ESTABLISHED ke
    alamat eksternal (ForeignAddr != 0.0.0.0 dan != ::) → SUSPICIOUS.

    Return
    ------
    (is_suspicious: bool, reasons: list[str])
    """
    reasons = []
    name_lower = proc_name.lower()

    # Proses legitimate tidak perlu diperiksa lebih lanjut
    if name_lower in LEGIT_NETWORK_PROCESSES:
        return (False, [])

    for rec in netscan_records:
        state       = str(rec.get("State", "")).upper()
        foreign     = str(rec.get("ForeignAddr", ""))
        foreign_port= str(rec.get("ForeignPort", ""))
        proto       = str(rec.get("Proto", ""))

        is_established = state == "ESTABLISHED"
        is_external    = foreign not in ("0.0.0.0", "::", "*", "")

        if is_established and is_external:
            reasons.append(
                f"[Rule2] Koneksi outbound abnormal: '{proc_name}' "
                f"-> {foreign}:{foreign_port} ({proto}, {state})"
            )

    return (len(reasons) > 0, reasons)


# ---------------------------------------------------------------------------
# Rule 3: Look for Evidence of Code Injection
# ---------------------------------------------------------------------------

def check_code_injection(
    proc_name: str,
    malfind_records: list,
) -> tuple[bool, list[str]]:
    """
    Rule 3: Look for Evidence of Code Injection.

    Indikator: segmen memori dengan Protection PAGE_EXECUTE_READWRITE
    DAN PrivateMemory = 1 (True).

    Pengecualian: proses dalam LEGIT_RWX_PROCESSES menggunakan teknik
    ini secara legitimate (JIT compilation, scan engine, dll).
    """
    reasons = []
    name_lower = proc_name.lower()

    # Skip proses yang secara legitimate pakai RWX
    if name_lower in LEGIT_RWX_PROCESSES:
        return (False, [])

    for rec in malfind_records:
        protection     = str(rec.get("Protection", ""))
        private_memory = rec.get("PrivateMemory")

        is_rwx     = "PAGE_EXECUTE_READWRITE" in protection
        is_private = private_memory in (1, "1", True, "True")

        if is_rwx and is_private:
            start = rec.get("Start VPN", "?")
            reasons.append(
                f"[Rule3] Code injection: '{proc_name}' "
                f"punya segmen PAGE_EXECUTE_READWRITE + PrivateMemory "
                f"di alamat {start}"
            )

    return (len(reasons) > 0, reasons)


# ---------------------------------------------------------------------------
# Rule 4: Analyze Process Objects
# ---------------------------------------------------------------------------

def check_process_objects(
    proc_name: str,
    pid: int,
    pid_to_parent_name: dict,
    pstree_by_pid: dict,
) -> tuple[bool, list[str]]:
    """
    Rule 4: Analyze Process Objects.

    Dua kondisi yang diperiksa:
    a. Proses memiliki parent yang tidak sesuai baseline NORMAL_PARENT_CHILD.
    b. Proses dalam SUSPICIOUS_CHILD_SPAWNERS meng-spawn shell/interpreter.

    Return
    ------
    (is_suspicious: bool, reasons: list[str])
    """
    reasons = []
    name_lower = proc_name.lower()

    # Ambil nama parent proses ini
    parent_name = pid_to_parent_name.get(pid)

    # (a) Cek apakah parent sesuai baseline
    if name_lower in NORMAL_PARENT_CHILD:
        allowed_parents = NORMAL_PARENT_CHILD[name_lower]
        if parent_name and parent_name not in allowed_parents:
            reasons.append(
                f"[Rule4] Parent abnormal: '{proc_name}' (PID={pid}) "
                f"dijalankan oleh '{parent_name}', "
                f"seharusnya oleh {allowed_parents}"
            )

    # (b) Cek apakah proses Office/browser meng-spawn shell
    if name_lower in SUSPICIOUS_CHILD_SPAWNERS:
        # Cari semua proses yang PPID-nya adalah PID ini
        for child_pid, child_rec in pstree_by_pid.items():
            if child_rec.get("PPID") == pid:
                child_name = str(child_rec.get("ImageFileName", "")).lower()
                if child_name in SHELL_PROCESSES:
                    reasons.append(
                        f"[Rule4] Spawn mencurigakan: '{proc_name}' (PID={pid}) "
                        f"-> '{child_rec.get('ImageFileName')}' (PID={child_pid})"
                    )

    return (len(reasons) > 0, reasons)


# ---------------------------------------------------------------------------
# Classifier utama
# ---------------------------------------------------------------------------

def classify_all(plugin_results: dict) -> list[dict]:
    """
    Klasifikasikan semua PID dari hasil 4 plugin Volatility3.

    Parameter
    ---------
    plugin_results : dict
        Output dari VolatilityRunner.run_all()

    Return
    ------
    list[dict]
        Setiap dict berisi hasil evaluasi satu PID:
        {
            "PID"        : int,
            "Name"       : str,
            "Path"       : str | None,
            "Status"     : "SUSPICIOUS" | "CLEAN",
            "Reasons"    : list[str],  # kosong jika CLEAN
            "Rule1_hit"  : bool,
            "Rule2_hit"  : bool,
            "Rule3_hit"  : bool,
            "Rule4_hit"  : bool,
        }
    """
    logger.info("Memulai klasifikasi semua PID...")

    tables = build_lookup_tables(plugin_results)

    all_pids          = tables["all_pids"]
    pslist_by_pid     = tables["pslist_by_pid"]
    pstree_by_pid     = tables["pstree_by_pid"]
    pid_to_parent     = tables["pid_to_parent_name"]
    netscan_by_pid    = tables["netscan_by_pid"]
    malfind_by_pid    = tables["malfind_by_pid"]

    results = []
    suspicious_count = 0

    for pid in sorted(all_pids):
        # Ambil nama proses — prioritas pslist, fallback pstree, fallback malfind
        pslist_rec  = pslist_by_pid.get(pid, {})
        pstree_rec  = pstree_by_pid.get(pid, {})
        malfind_recs = malfind_by_pid.get(pid, [])

        proc_name = (
            pslist_rec.get("ImageFileName")
            or pstree_rec.get("ImageFileName")
            or (malfind_recs[0].get("Process") if malfind_recs else None)
            or "Unknown"
        )
        proc_name = str(proc_name)

        # Ambil path dari pstree (pslist tidak punya field Path)
        proc_path = pstree_rec.get("Path")
        if proc_path in (None, "None"):
            proc_path = None

        # --- Evaluasi 4 Rules ---
        r1_hit, r1_reasons = check_rogue_process(proc_name, proc_path)
        r2_hit, r2_reasons = check_network_artifacts(
            proc_name, netscan_by_pid.get(pid, [])
        )
        r3_hit, r3_reasons = check_code_injection(
            proc_name, malfind_by_pid.get(pid, [])
        )
        r4_hit, r4_reasons = check_process_objects(
            proc_name, pid, pid_to_parent, pstree_by_pid
        )

        all_reasons = r1_reasons + r2_reasons + r3_reasons + r4_reasons
        is_suspicious = r1_hit or r2_hit or r3_hit or r4_hit

        status = "SUSPICIOUS" if is_suspicious else "CLEAN"
        if is_suspicious:
            suspicious_count += 1
            logger.warning(
                f"[SUSPICIOUS] PID={pid} ({proc_name}) | "
                f"Rules hit: "
                f"R1={'Y' if r1_hit else 'N'} "
                f"R2={'Y' if r2_hit else 'N'} "
                f"R3={'Y' if r3_hit else 'N'} "
                f"R4={'Y' if r4_hit else 'N'}"
            )

        results.append({
            "PID":       pid,
            "Name":      proc_name,
            "Path":      proc_path,
            "Status":    status,
            "Reasons":   all_reasons,
            "Rule1_hit": r1_hit,
            "Rule2_hit": r2_hit,
            "Rule3_hit": r3_hit,
            "Rule4_hit": r4_hit,
        })

    logger.info(
        f"Klasifikasi selesai: {len(results)} PID total | "
        f"{suspicious_count} SUSPICIOUS | "
        f"{len(results) - suspicious_count} CLEAN"
    )

    return results


# ---------------------------------------------------------------------------
# Quick test: python3 core/analyzer.py /mnt/d/dump.dmp
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    import json
    import subprocess
    from pathlib import Path

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
    print("  QUICK TEST -- Analyzer")
    print("=" * 60)

    # Jalankan plugin langsung dari sini untuk test standalone
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
            plugin_results[plugin] = [
                dict(zip(cols, row)) for row in data["rows"]
            ]
        else:
            plugin_results[plugin] = None

    # Klasifikasi
    classifications = classify_all(plugin_results)

    # Tampilkan semua SUSPICIOUS
    suspicious = [r for r in classifications if r["Status"] == "SUSPICIOUS"]
    clean      = [r for r in classifications if r["Status"] == "CLEAN"]

    print(f"\n{'='*60}")
    print(f"TOTAL : {len(classifications)} PID")
    print(f"CLEAN : {len(clean)}")
    print(f"SUSPICIOUS: {len(suspicious)}")
    print(f"{'='*60}")

    if suspicious:
        print("\n--- SUSPICIOUS PROCESSES ---")
        for rec in suspicious:
            print(f"\n  PID={rec['PID']} | {rec['Name']}")
            print(f"  Path: {rec['Path']}")
            print(f"  Rules: R1={rec['Rule1_hit']} R2={rec['Rule2_hit']} "
                  f"R3={rec['Rule3_hit']} R4={rec['Rule4_hit']}")
            for reason in rec["Reasons"]:
                print(f"    -> {reason}")