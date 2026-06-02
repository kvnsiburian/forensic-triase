"""
patch_b4_rekomendasi.py
=======================
Patch B4: Tambahkan rekomendasi investigasi di detail panel GUI.

Ketika baris SUSPICIOUS dipilih, panel detail menampilkan:
  1. Alasan deteksi (sudah ada)
  2. Rekomendasi langkah investigasi selanjutnya (baru)

Rekomendasi berdasarkan rule yang terpenuhi:
  Rule 1 → verifikasi hash dan path eksekusi
  Rule 2 → investigasi koneksi jaringan dan reputasi IP
  Rule 3 → dump dan analisis region memori mencurigakan
  Rule 4 → verifikasi rantai proses dan command line

Cara pakai:
  python3 ~/forensic_triase/platform/patch_b4_rekomendasi.py
"""

from pathlib import Path
import shutil

APP = Path.home() / "forensic_triase/platform/gui/app.py"

# ---------------------------------------------------------------------------
# Patch 1: Tambahkan konstanta REKOMENDASI setelah konstanta FONT
# ---------------------------------------------------------------------------

OLD_FONT = '''FONT_TITLE   = ("Segoe UI", 16, "bold")
FONT_HEADER  = ("Segoe UI", 11, "bold")
FONT_NORMAL  = ("Segoe UI", 10)
FONT_SMALL   = ("Segoe UI", 9)
FONT_MONO    = ("Consolas", 9)'''

NEW_FONT = '''FONT_TITLE   = ("Segoe UI", 16, "bold")
FONT_HEADER  = ("Segoe UI", 11, "bold")
FONT_NORMAL  = ("Segoe UI", 10)
FONT_SMALL   = ("Segoe UI", 9)
FONT_MONO    = ("Consolas", 9)

# Rekomendasi investigasi per rule
REKOMENDASI = {
    "Rule1": (
        "📋 Rule 1 — Identify Rogue Processes\\n"
        "   → Verifikasi hash file executable menggunakan tools seperti Get-FileHash (PowerShell)\\n"
        "   → Bandingkan nama proses dengan daftar proses sistem Windows yang legitimate\\n"
        "   → Periksa apakah path eksekusi wajar untuk proses tersebut\\n"
        "   → Lanjutkan dengan: windows.dlllist untuk melihat DLL yang dimuat proses ini"
    ),
    "Rule2": (
        "🌐 Rule 2 — Review Network Artifacts\\n"
        "   → Telusuri reputasi IP tujuan menggunakan threat intelligence (VirusTotal, AbuseIPDB)\\n"
        "   → Periksa port yang digunakan — apakah wajar untuk proses ini?\\n"
        "   → Lanjutkan dengan: windows.netstat untuk koneksi aktif yang lebih detail\\n"
        "   → Cek apakah ada proses lain yang berkomunikasi ke IP yang sama"
    ),
    "Rule3": (
        "💉 Rule 3 — Evidence of Code Injection\\n"
        "   → Dump region memori mencurigakan untuk analisis lebih lanjut\\n"
        "   → Gunakan: windows.memmap untuk memetakan region memori proses\\n"
        "   → Analisis hexdump dan disassembly di region PAGE_EXECUTE_READWRITE\\n"
        "   → Periksa apakah ada proses lain yang juga menunjukkan pola serupa"
    ),
    "Rule4": (
        "🔗 Rule 4 — Analyze Process Objects\\n"
        "   → Verifikasi rantai proses lengkap menggunakan windows.pstree\\n"
        "   → Periksa command line argument proses dengan windows.cmdline\\n"
        "   → Bandingkan dengan baseline parent-child Windows yang normal\\n"
        "   → Investigasi proses parent — apakah parent juga mencurigakan?"
    ),
}'''

# ---------------------------------------------------------------------------
# Patch 2: Update _on_row_select untuk tampilkan rekomendasi
# ---------------------------------------------------------------------------

OLD_ROW_SELECT = '''    def _on_row_select(self, event):
        """Tampilkan detail Reasons ketika baris dipilih."""
        selected = self._tree.selection()
        if not selected:
            return

        item    = self._tree.item(selected[0])
        pid_str = item["values"][0]

        # Cari record yang sesuai
        rec = next(
            (r for r in self._classifications if str(r["PID"]) == str(pid_str)),
            None,
        )
        if not rec:
            return

        reasons = rec.get("Reasons", [])
        if reasons:
            detail = "\\n".join(reasons)
        else:
            detail = f"✓ PID {pid_str} ({rec['Name']}) — tidak ada indikator anomali ditemukan."

        self._detail_text.configure(state="normal")
        self._detail_text.delete("1.0", "end")
        self._detail_text.insert("1.0", detail)
        self._detail_text.configure(state="disabled")'''

NEW_ROW_SELECT = '''    def _on_row_select(self, event):
        """Tampilkan detail Reasons dan rekomendasi investigasi ketika baris dipilih."""
        selected = self._tree.selection()
        if not selected:
            return

        item    = self._tree.item(selected[0])
        pid_str = item["values"][0]

        # Cari record yang sesuai
        rec = next(
            (r for r in self._classifications if str(r["PID"]) == str(pid_str)),
            None,
        )
        if not rec:
            return

        reasons = rec.get("Reasons", [])

        if reasons:
            # Bagian 1: Alasan deteksi
            detail = "─── INDIKATOR ANOMALI ───────────────────────────────────\\n"
            detail += "\\n".join(reasons)

            # Bagian 2: Rekomendasi investigasi
            detail += "\\n\\n─── REKOMENDASI INVESTIGASI ─────────────────────────────"
            if rec.get("Rule1_hit"):
                detail += "\\n\\n" + REKOMENDASI["Rule1"]
            if rec.get("Rule2_hit"):
                detail += "\\n\\n" + REKOMENDASI["Rule2"]
            if rec.get("Rule3_hit"):
                detail += "\\n\\n" + REKOMENDASI["Rule3"]
            if rec.get("Rule4_hit"):
                detail += "\\n\\n" + REKOMENDASI["Rule4"]
        else:
            detail = f"✓ PID {pid_str} ({rec['Name']}) — tidak ada indikator anomali ditemukan."

        self._detail_text.configure(state="normal")
        self._detail_text.delete("1.0", "end")
        self._detail_text.insert("1.0", detail)
        self._detail_text.configure(state="disabled")'''

# ---------------------------------------------------------------------------
# Patch 3: Perbesar panel detail dari height=4 ke height=10
# ---------------------------------------------------------------------------

OLD_DETAIL = '''        self._detail_text = scrolledtext.ScrolledText(
            frame,
            height=4,
            font=FONT_MONO,
            bg="#0f0f1a", fg=COLOR_TEXT,
            relief="flat",
            state="disabled",
            wrap="word",
        )'''

NEW_DETAIL = '''        self._detail_text = scrolledtext.ScrolledText(
            frame,
            height=10,
            font=FONT_MONO,
            bg="#0f0f1a", fg=COLOR_TEXT,
            relief="flat",
            state="disabled",
            wrap="word",
        )'''

# ---------------------------------------------------------------------------
# Jalankan patch
# ---------------------------------------------------------------------------

def patch_file(path, replacements, label):
    shutil.copy(path, str(path) + ".bak_b4")
    content = path.read_text(encoding="utf-8")
    for i, (old, new) in enumerate(replacements, 1):
        if old not in content:
            print(f"  [!] Patch {i} GAGAL — string tidak ditemukan di {label}")
            continue
        content = content.replace(old, new, 1)
        print(f"  [✓] Patch {i} berhasil")
    path.write_text(content, encoding="utf-8")


print("\n" + "=" * 60)
print("  PATCH B4: Rekomendasi Investigasi")
print("=" * 60)

print("\n[1/1] Patching app.py...")
patch_file(APP, [
    (OLD_FONT,        NEW_FONT),
    (OLD_ROW_SELECT,  NEW_ROW_SELECT),
    (OLD_DETAIL,      NEW_DETAIL),
], "app.py")

print("\n" + "=" * 60)
print("  SELESAI.")
print("  Test GUI:")
print("  python3 ~/forensic_triase/platform/gui/app.py")
print("=" * 60 + "\n")