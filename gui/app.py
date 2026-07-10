"""
app.py
======
Antarmuka GUI Platform Triase Forensik Memori berbasis Tkinter.

Layout:
  ┌─────────────────────────────────────────┐
  │  HEADER — judul platform                │
  ├─────────────────────────────────────────┤
  │  Panel File — pilih memory dump         │
  ├─────────────────────────────────────────┤
  │  Panel Statistik — Total/SUSPICIOUS/CLEAN│
  ├─────────────────────────────────────────┤
  │  Tabel Hasil — semua PID + status       │
  │  [resizable — bisa digeser]             │
  ├─────────────────────────────────────────┤
  │  Detail Indikator — resizable           │
  ├─────────────────────────────────────────┤
  │  Status Bar — progress analisis         │
  └─────────────────────────────────────────┘

Desain:
  - Analisis berjalan di thread terpisah supaya GUI tidak freeze
  - Baris SUSPICIOUS berwarna merah, CLEAN berwarna hijau
  - Klik baris untuk lihat detail Reasons di panel bawah
  - Tombol Export Hasil memanggil reporter (Excel + CSV) langsung dari GUI
  - Panel tabel dan detail bisa digeser proporsinya (PanedWindow)
  - Search bar untuk filter proses secara real-time

Author  : Kevin Armando Siburian (2221101800)
Program : Rekayasa Keamanan Siber - PSSN
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import logging
import re
import time
from pathlib import Path
import sys

# Pastikan root platform/ ada di path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import run_analysis
from core.reporter import DEFAULT_OUTPUT_DIR

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Konstanta tampilan
# ---------------------------------------------------------------------------

APP_TITLE   = "Platform Triase Forensik Memori"
APP_VERSION = ""
WIN_WIDTH   = 1100
WIN_HEIGHT  = 750
MIN_WIDTH   = 900
MIN_HEIGHT  = 600

# Warna
COLOR_BG         = "#0d1b2a"
COLOR_PANEL      = "#1b2c3e"
COLOR_ACCENT     = "#1565c0"
COLOR_ACCENT_HOV = "#0d47a1"
COLOR_SUSPICIOUS = "#3b1a1a"
COLOR_CLEAN      = "#1a2e1a"
COLOR_TEXT       = "#e2e8f0"
COLOR_SUBTEXT    = "#94a3b8"
COLOR_RED        = "#ef4444"
COLOR_ORANGE     = "#f97316"
COLOR_YELLOW     = "#eab308"
COLOR_GREEN      = "#22c55e"
COLOR_BORDER     = "#1e3a5f"

COLOR_BG_HIGH    = "#3b1a1a"
COLOR_BG_MEDIUM  = "#2e1a0a"
COLOR_BG_LOW     = "#2a2a0a"
COLOR_BG_CLEAN   = "#1a2e1a"

FONT_TITLE   = ("Segoe UI", 16, "bold")
FONT_HEADER  = ("Segoe UI", 11, "bold")
FONT_NORMAL  = ("Segoe UI", 10)
FONT_SMALL   = ("Segoe UI", 9)
FONT_MONO    = ("Consolas", 9)

REKOMENDASI = {
    "Rule1": (
        "Rule 1 -- Identify Rogue Processes\n"
        "   -> Verifikasi hash file executable (Get-FileHash / VirusTotal)\n"
        "   -> Bandingkan nama proses dengan whitelist proses sistem Windows\n"
        "   -> Periksa apakah path eksekusi wajar untuk proses tersebut\n"
        "   -> Lanjutkan dengan: windows.dlllist untuk melihat DLL yang dimuat"
    ),
    "Rule2": (
        "Rule 2 -- Review Network Artifacts\n"
        "   -> Telusuri reputasi IP tujuan (VirusTotal, AbuseIPDB)\n"
        "   -> Periksa apakah port yang digunakan wajar untuk proses ini\n"
        "   -> Lanjutkan dengan: windows.netstat untuk detail koneksi aktif\n"
        "   -> Cek proses lain yang berkomunikasi ke IP yang sama"
    ),
    "Rule3": (
        "Rule 3 -- Evidence of Code Injection\n"
        "   -> Dump region memori mencurigakan untuk analisis lebih lanjut\n"
        "   -> Gunakan: windows.memmap untuk memetakan region memori proses\n"
        "   -> Analisis hexdump di region PAGE_EXECUTE_READWRITE\n"
        "   -> Periksa proses lain yang menunjukkan pola serupa"
    ),
    "Rule4": (
        "Rule 4 -- Analyze Process Objects\n"
        "   -> Lihat kolom Reasons: nama dan path DLL mencurigakan atau handle ke LSASS\n"
        "   -> Jika DLL mencurigakan: hash file tersebut dan verifikasi di VirusTotal\n"
        "   -> Periksa apakah DLL bertanda tangan sah (Get-AuthenticodeSignature)\n"
        "   -> Baca output windows.dlllist di tab detail untuk melihat seluruh DLL yang dimuat proses ini\n"
        "   -> Jika ada akses ke LSASS: indikasi credential dumping (MITRE ATT&CK T1003.001)\n"
        "   -> Periksa apakah ProcDump / Mimikatz atau alat serupa sedang berjalan\n"
        "   -> Gunakan windows.handles untuk memeriksa semua handle antarproses secara lengkap"
    ),
}


# ---------------------------------------------------------------------------
# Kelas utama GUI
# ---------------------------------------------------------------------------

class ForensicTriaseApp(tk.Tk):
    """Window utama Platform Triase Forensik Memori."""

    def __init__(self):
        super().__init__()

        self.title(f"{APP_TITLE} {APP_VERSION}")
        self.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
        self.minsize(MIN_WIDTH, MIN_HEIGHT)
        self.configure(bg=COLOR_BG)

        # State
        self._dump_path        = tk.StringVar()
        self._status_text      = tk.StringVar(value="Siap. Pilih file memory dump untuk memulai.")
        self._total_var        = tk.StringVar(value="--")
        self._suspicious_var   = tk.StringVar(value="--")
        self._clean_var        = tk.StringVar(value="--")
        self._elapsed_var      = tk.StringVar(value="--")
        self._classifications  = []
        self._is_running       = False
        self._cancel_event     = threading.Event()
        self._search_var       = tk.StringVar()
        self._use_parallel_var = tk.BooleanVar(value=False)
        self._start_time       = None   # penanda waktu mulai analisis (time.monotonic)
        self._timer_job        = None   # id job self.after untuk timer live

        self._build_ui()
        self._apply_treeview_style()

        # Tangani penutupan jendela agar analisis yang sedang berjalan dihentikan
        # lebih dulu, tidak meninggalkan thread/subprocess Volatility menggantung.
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ------------------------------------------------------------------
    # Build UI
    # ------------------------------------------------------------------

    def _build_ui(self):
        """Bangun semua komponen UI."""
        self._build_statusbar()   # pack side=bottom dulu
        self._build_header()
        self._build_file_panel()
        self._build_stats_panel()
        self._build_table_detail_panel()  # PanedWindow — tabel + detail

    def _build_header(self):
        """Header — judul platform beserta subjudul singkat."""
        frame = tk.Frame(self, bg=COLOR_ACCENT, pady=10)
        frame.pack(fill="x")

        judul = tk.Frame(frame, bg=COLOR_ACCENT)
        judul.pack(side="left", padx=16)

        tk.Label(
            judul,
            text=f"{APP_TITLE}",
            font=FONT_TITLE,
            fg="white",
            bg=COLOR_ACCENT,
        ).pack(anchor="w")

        tk.Label(
            judul,
            text="Triase forensik memori berbasis Volatility 3",
            font=FONT_SMALL,
            fg="#bcd7f5",
            bg=COLOR_ACCENT,
        ).pack(anchor="w")

    def _build_file_panel(self):
        """Panel pemilihan file memory dump dan tombol analisis."""
        outer = tk.Frame(self, bg=COLOR_PANEL, pady=10, padx=16)
        outer.pack(fill="x", padx=12, pady=(10, 4))

        # Baris atas: label, entry, tombol-tombol
        controls = tk.Frame(outer, bg=COLOR_PANEL)
        controls.pack(fill="x")

        tk.Label(
            controls, text="Memory Dump:",
            font=FONT_HEADER, fg=COLOR_TEXT, bg=COLOR_PANEL,
        ).pack(side="left")

        self._entry_path = tk.Entry(
            controls,
            textvariable=self._dump_path,
            font=FONT_MONO,
            bg="#e2e6ec", fg="#1b2c3e",
            insertbackground="#1b2c3e",
            relief="flat", bd=0,
            highlightthickness=0,
            width=52,
        )
        self._entry_path.pack(side="left", padx=(8, 10), ipady=6)

        self._btn_browse = tk.Button(
            controls, text="Browse",
            font=FONT_NORMAL,
            bg=COLOR_BORDER, fg="white",
            activebackground="#555577", activeforeground="white",
            relief="flat", bd=0, highlightthickness=0,
            padx=14, pady=6,
            cursor="hand2",
            command=self._browse_file,
        )
        self._btn_browse.pack(side="left", padx=(0, 8))

        self._btn_analyze = tk.Button(
            controls, text="Mulai Analisis",
            font=FONT_NORMAL,
            bg=COLOR_ACCENT, fg="white",
            activebackground=COLOR_ACCENT_HOV,
            relief="flat", bd=0, highlightthickness=0,
            padx=14, pady=6,
            cursor="hand2",
            command=self._start_analysis,
        )
        self._btn_analyze.pack(side="left", padx=(0, 8))

        self._btn_cancel = tk.Button(
            controls, text="Batal",
            font=FONT_NORMAL,
            bg="#7f1d1d", fg="white",
            activebackground="#991b1b",
            disabledforeground="#8a9bb0",
            relief="flat", bd=0, highlightthickness=0,
            padx=14, pady=6,
            cursor="hand2",
            state="disabled",
            command=self._cancel_analysis,
        )
        self._btn_cancel.pack(side="left", padx=(0, 8))

        # Reset diletakkan di antara Batal dan Export Hasil, semua berdempet
        # rapat (side="left") agar tidak ada celah menganga di tengah baris.
        self._btn_reset = tk.Button(
            controls, text="Reset",
            font=FONT_NORMAL,
            bg=COLOR_BORDER, fg="white",
            activebackground=COLOR_ACCENT, activeforeground="white",
            disabledforeground="#8a9bb0",
            relief="flat", bd=0, highlightthickness=0,
            padx=14, pady=6,
            cursor="hand2",
            state="disabled",
            command=self._reset_all,
        )
        self._btn_reset.pack(side="left", padx=(0, 8))

        self._btn_export = tk.Button(
            controls, text="Export Hasil",
            font=FONT_NORMAL,
            bg="#166534", fg="white",
            activebackground="#14532d",
            disabledforeground="#8a9bb0",
            relief="flat", bd=0, highlightthickness=0,
            padx=14, pady=6,
            cursor="hand2",
            state="disabled",
            command=self._export_csv,
        )
        self._btn_export.pack(side="left")

        # Baris bawah: indikator kemajuan (teks + progress bar).
        # Keduanya hanya ditampilkan saat analisis berjalan, disembunyikan
        # saat idle supaya tidak ada "kotak" asing yang membingungkan.
        self._progress_frame = tk.Frame(outer, bg=COLOR_PANEL)

        self._progress_label_var = tk.StringVar(value="")
        self._progress_label = tk.Label(
            self._progress_frame,
            textvariable=self._progress_label_var,
            font=FONT_SMALL, fg=COLOR_SUBTEXT, bg=COLOR_PANEL,
            anchor="w",
        )
        self._progress_label.pack(fill="x", pady=(0, 3))

        self._progress = ttk.Progressbar(
            self._progress_frame,
            orient="horizontal",
            mode="determinate",
            maximum=100,
            style="Dark.Horizontal.TProgressbar",
        )
        self._progress.pack(fill="x")
        # Sengaja belum di-pack ke jendela: _progress_frame baru muncul saat
        # analisis mulai (lihat _show_progress) dan disembunyikan saat selesai.

    def _build_stats_panel(self):
        """Panel statistik — Total PID, SUSPICIOUS, CLEAN, WAKTU."""
        frame = tk.Frame(self, bg=COLOR_BG)
        frame.pack(fill="x", padx=12, pady=(4, 0))

        cards = tk.Frame(frame, bg=COLOR_BG)
        cards.pack(fill="x")

        # Kartu WAKTU dimulai netral (abu-abu) karena "--" berarti belum jalan;
        # warnanya baru dibiruan (COLOR_ACCENT) saat timer aktif, lihat _start_timer.
        stats = [
            ("Total PID",   self._total_var,      COLOR_TEXT),
            ("SUSPICIOUS",  self._suspicious_var,  COLOR_RED),
            ("CLEAN",       self._clean_var,        COLOR_GREEN),
            ("WAKTU",       self._elapsed_var,      COLOR_SUBTEXT),
        ]

        for i, (label, var, color) in enumerate(stats):
            # Kartu terakhir tanpa margin kanan agar tepinya lurus dengan
            # panel di atasnya (sama-sama padx=12 dari tepi jendela).
            right_pad = 0 if i == len(stats) - 1 else 8
            card = tk.Frame(cards, bg=COLOR_PANEL, padx=20, pady=8, relief="flat")
            card.pack(side="left", padx=(0, right_pad), fill="x", expand=True)

            tk.Label(
                card, text=label,
                font=FONT_SMALL, fg=COLOR_SUBTEXT, bg=COLOR_PANEL,
            ).pack()
            value_lbl = tk.Label(
                card, textvariable=var,
                font=("Segoe UI", 22, "bold"), fg=color, bg=COLOR_PANEL,
            )
            value_lbl.pack()
            if label == "WAKTU":
                self._elapsed_label = value_lbl

    def _build_table_detail_panel(self):
        """Panel tabel + detail yang bisa digeser proporsinya (PanedWindow)."""

        paned = tk.PanedWindow(
            self,
            orient="vertical",
            bg=COLOR_BG,
            sashwidth=6,
            sashrelief="flat",
            borderwidth=0,
            relief="flat",
        )
        paned.pack(fill="both", expand=True, padx=12, pady=(0, 0))

        # ── Frame atas: label + search + treeview ────────────────────
        top_frame = tk.Frame(paned, bg=COLOR_BG)

        # Label judul (beri jarak kecil dari kartu statistik di atasnya,
        # cukup untuk bernapas tapi tidak mepet)
        tk.Label(
            top_frame, text="Hasil Klasifikasi Proses",
            font=FONT_HEADER, fg=COLOR_TEXT, bg=COLOR_BG,
        ).pack(anchor="w", pady=(8, 3))

        # Search bar
        search_frame = tk.Frame(top_frame, bg=COLOR_BG)
        search_frame.pack(fill="x", pady=(0, 4))

        tk.Label(
            search_frame, text="Cari Proses:",
            font=FONT_SMALL, fg=COLOR_SUBTEXT, bg=COLOR_BG,
        ).pack(side="left", padx=(0, 6))

        # Opsi multiprocessing sejajar di sisi kanan baris pencarian.
        # Teks dibuat tebal & putih agar labelnya menonjol. selectcolor sengaja
        # TIDAK diubah jadi warna terang: nilai selain COLOR_BORDER membuat
        # kotak centang tak bisa diklik di lingkungan ini (sudah terbukti).
        self._chk_parallel = tk.Checkbutton(
            search_frame,
            text="Gunakan multiprocessing",
            variable=self._use_parallel_var,
            font=("Segoe UI", 10, "bold"),
            bg=COLOR_BG, fg="white",
            selectcolor=COLOR_BORDER,
            activebackground=COLOR_BG,
            activeforeground="white",
            relief="flat",
            bd=0,
            highlightthickness=0,
            cursor="hand2",
        )
        self._chk_parallel.pack(side="right")

        self._search_var.trace("w", self._on_search)

        self._search_entry = tk.Entry(
            search_frame,
            textvariable=self._search_var,
            font=FONT_MONO,
            bg="#e2e6ec", fg="#1b2c3e",
            insertbackground="#1b2c3e",
            relief="flat", bd=0,
            highlightthickness=0,
            width=30,
        )
        self._search_entry.pack(side="left", ipady=6)

        tk.Button(
            search_frame, text="X",
            font=FONT_SMALL,
            bg=COLOR_BORDER, fg=COLOR_TEXT,
            activebackground="#555577", activeforeground=COLOR_TEXT,
            relief="flat", bd=0,
            highlightthickness=0,
            padx=10,
            cursor="hand2",
            command=lambda: self._search_var.set(""),
        ).pack(side="left", padx=(4, 0), ipady=3)

        # Treeview + Scrollbar
        tree_frame = tk.Frame(top_frame, bg=COLOR_BG)
        tree_frame.pack(fill="both", expand=True)

        columns = ("PID", "Name", "Path", "Status", "Score", "Risk",
                   "R1", "R2", "R3", "R4")
        # Skor & Risiko di-hide dari display per arahan Pak Rahmat (3 Juni 2026):
        # klasifikasi binary murni, scoring tetap di-compute internal tapi tidak ditampilkan.
        displaycolumns = ("PID", "Name", "Path", "Status",
                          "R1", "R2", "R3", "R4")
        self._tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            displaycolumns=displaycolumns,
            show="headings",
            selectmode="browse",
        )

        col_config = {
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
        }
        col_headers = {
            "PID": "PID", "Name": "Nama Proses", "Path": "Path Eksekusi",
            "Status": "Status", "Score": "Skor", "Risk": "Risiko",
            "R1": "R1", "R2": "R2", "R3": "R3", "R4": "R4",
        }

        for col, (width, anchor) in col_config.items():
            self._tree.heading(col, text=col_headers[col])
            self._tree.column(
                col, width=width, anchor=anchor,
                stretch=(col == "Path"),
            )

        vsb = ttk.Scrollbar(tree_frame, orient="vertical",
                             command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        self._tree.bind("<<TreeviewSelect>>", self._on_row_select)

        paned.add(top_frame, minsize=200)

        # ── Frame bawah: detail indikator ────────────────────────────
        bottom_frame = tk.Frame(paned, bg=COLOR_BG)

        tk.Label(
            bottom_frame, text="Detail Indikator:",
            font=FONT_SMALL, fg=COLOR_SUBTEXT, bg=COLOR_BG,
        ).pack(anchor="w", pady=(4, 2))

        self._detail_text = scrolledtext.ScrolledText(
            bottom_frame,
            font=FONT_MONO,
            bg="#0f0f1a", fg=COLOR_TEXT,
            relief="flat",
            state="disabled",
            wrap="word",
        )
        self._detail_text.pack(fill="both", expand=True)

        # Tag warna untuk Detail Indikator
        self._detail_text.tag_configure("header",      foreground="#90caf9", font=("Consolas", 9, "bold"))
        self._detail_text.tag_configure("rule_line",   foreground="#f97316")
        self._detail_text.tag_configure("rekomendasi", foreground="#22c55e", font=("Consolas", 9, "bold"))
        self._detail_text.tag_configure("arrow_line",  foreground="#94a3b8")
        self._detail_text.tag_configure("placeholder", foreground=COLOR_SUBTEXT, font=("Consolas", 9, "italic"))

        # Tampilkan arahan awal supaya panel tidak kosong tanpa keterangan.
        self._show_detail_placeholder()

        paned.add(bottom_frame, minsize=100)

    def _show_detail_placeholder(self):
        """Isi panel Detail Indikator dengan teks arahan saat belum ada proses dipilih."""
        self._detail_text.configure(state="normal")
        self._detail_text.delete("1.0", "end")
        self._detail_text.insert(
            "end",
            "Pilih satu proses pada tabel di atas untuk melihat alasan klasifikasinya.",
            "placeholder",
        )
        self._detail_text.configure(state="disabled")

    def _build_statusbar(self):
        """Status bar di bagian bawah."""
        frame = tk.Frame(self, bg=COLOR_BORDER, pady=4)
        frame.pack(fill="x", side="bottom")

        tk.Label(
            frame,
            textvariable=self._status_text,
            font=FONT_SMALL,
            fg=COLOR_SUBTEXT,
            bg=COLOR_BORDER,
            anchor="w",
        ).pack(side="left", padx=12)

    def _apply_treeview_style(self):
        """Apply style gelap ke Treeview."""
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=COLOR_PANEL,
            foreground=COLOR_TEXT,
            fieldbackground=COLOR_PANEL,
            rowheight=24,
            font=FONT_SMALL,
        )
        style.configure(
            "Treeview.Heading",
            background=COLOR_BORDER,
            foreground=COLOR_TEXT,
            font=FONT_SMALL,
            relief="flat",
        )
        style.map(
            "Treeview",
            background=[("selected", COLOR_ACCENT)],
            foreground=[("selected", "white")],
        )

        self._tree.tag_configure("high",   background=COLOR_BG_HIGH,   foreground=COLOR_RED)
        self._tree.tag_configure("medium", background=COLOR_BG_MEDIUM, foreground=COLOR_ORANGE)
        self._tree.tag_configure("low",    background=COLOR_BG_LOW,    foreground=COLOR_YELLOW)
        self._tree.tag_configure("clean",  background=COLOR_BG_CLEAN,  foreground=COLOR_GREEN)
        # Tag binary baru per arahan Pak Rahmat (3 Juni 2026)
        self._tree.tag_configure("suspicious", background=COLOR_BG_MEDIUM, foreground=COLOR_ORANGE)

        style.configure(
            "Dark.Horizontal.TProgressbar",
            troughcolor="#132234",
            background=COLOR_ACCENT,
            thickness=8,
            borderwidth=0,
            bordercolor="#132234",
            lightcolor=COLOR_ACCENT,
            darkcolor=COLOR_ACCENT,
        )

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _browse_file(self):
        path = filedialog.askopenfilename(
            title="Pilih Memory Dump",
            filetypes=[
                ("Memory Dump", "*.dmp *.raw *.vmem *.mem"),
                ("Semua File", "*.*"),
            ],
            initialdir=str(Path("/mnt/d") if Path("/mnt/d").exists() else Path.home()),
        )
        if path:
            self._dump_path.set(path)
            self._set_status(f"File dipilih: {Path(path).name}")

    def _start_analysis(self):
        dump = self._dump_path.get().strip()

        if not dump:
            messagebox.showwarning(
                "File Belum Dipilih",
                "Pilih file memory dump terlebih dahulu.",
            )
            return

        if not Path(dump).exists():
            messagebox.showerror(
                "File Tidak Ditemukan",
                f"File tidak ditemukan:\n{dump}",
            )
            return

        if self._is_running:
            return

        self._cancel_event.clear()
        self._clear_table()
        self._reset_stats()
        self._search_var.set("")
        self._show_progress()
        self._set_buttons_running(True)
        self._set_status("Memulai analisis...")
        self._start_timer()

        thread = threading.Thread(
            target=self._run_analysis_thread,
            args=(dump,),
            daemon=True,
        )
        thread.start()

    def _run_analysis_thread(self, dump: str):
        try:
            result = run_analysis(
                dump_path=dump,
                progress_callback=self._on_progress,
                cancel_event=self._cancel_event,
                use_parallel=self._use_parallel_var.get(),
            )
            if not self._cancel_event.is_set():
                self.after(0, self._on_analysis_done, result)
        except Exception as e:
            if not self._cancel_event.is_set():
                self.after(0, self._on_analysis_error, str(e))

    def _on_progress(self, msg: str):
        if self._cancel_event.is_set():
            return
        self.after(0, self._set_status, msg)
        m = re.search(r'\[(\d+)/(\d+)\]', msg)
        if m:
            done, total = int(m.group(1)), int(m.group(2))
            self.after(0, self._set_progress, done, total)

    def _cancel_analysis(self):
        if not self._is_running:
            return
        self._cancel_event.set()
        self._clear_table()
        self._stop_timer()
        self._reset_stats()
        self._hide_progress()
        self._set_buttons_running(False)
        self._set_status("Analisis dibatalkan.")

    def _on_close(self):
        """Konfirmasi sebelum menutup jendela saat analisis masih berjalan.

        Bila pengguna tetap keluar, cancel_event di-set lebih dulu supaya
        thread analisis berhenti dan tidak ada subprocess Volatility yang
        menggantung setelah jendela ditutup.
        """
        if self._is_running:
            keluar = messagebox.askyesno(
                "Analisis sedang berjalan",
                "Analisis masih berlangsung.\n\n"
                "Jika keluar sekarang, proses analisis akan dihentikan dan "
                "hasilnya tidak tersimpan. Tetap keluar?",
            )
            if not keluar:
                return
            # Beri sinyal berhenti ke thread analisis sebelum jendela ditutup.
            self._cancel_event.set()
            if self._timer_job is not None:
                self.after_cancel(self._timer_job)
                self._timer_job = None
        self.destroy()

    def _on_analysis_done(self, result: dict):
        self._set_buttons_running(False)
        self._stop_timer()   # hentikan timer & kunci nilai akhir di kartu WAKTU
        self._hide_progress()

        if not result["success"]:
            messagebox.showerror("Analisis Gagal", result["error"])
            self._set_status(f"Gagal: {result['error']}")
            return

        self._classifications = result["classifications"]
        self._plugin_results  = result.get("plugin_results", {})
        stats = result["stats"]

        self._total_var.set(str(stats["total"]))
        self._suspicious_var.set(str(stats["suspicious"]))
        self._clean_var.set(str(stats["clean"]))

        self._populate_table(self._classifications)
        self._btn_export.configure(state="normal")
        self._btn_reset.configure(state="normal")
        self._hide_progress()

        self._set_status(
            "Analisis selesai. Hasil telah tersimpan dalam format Excel dan CSV."
        )

        reran = result.get("reran_plugins") or []
        if reran:
            messagebox.showinfo(
                "Multiprocessing",
                "Sebagian plugin sempat gagal saat mode paralel, lalu dijalankan "
                "ulang secara berurutan agar hasil tetap lengkap:\n\n  "
                + "\n  ".join(reran),
            )

    def _on_analysis_error(self, error: str):
        self._set_buttons_running(False)
        self._stop_timer()
        self._hide_progress()
        messagebox.showerror("Error", error)
        self._set_status(f"Error: {error}")

    def _on_row_select(self, event):
        selected = self._tree.selection()
        if not selected:
            return

        item    = self._tree.item(selected[0])
        pid_str = item["values"][0]

        rec = next(
            (r for r in self._classifications if str(r["PID"]) == str(pid_str)),
            None,
        )
        if not rec:
            return

        self._detail_text.configure(state="normal")
        self._detail_text.delete("1.0", "end")

        reasons = rec.get("Reasons", [])
        if reasons:
            # Header indikator anomali
            self._detail_text.insert("end", "--- INDIKATOR ANOMALI -------------------------------------------\n", "header")
            for reason in reasons:
                self._detail_text.insert("end", f"{reason}\n", "rule_line")

            self._detail_text.insert("end", "\n")

            # Ekstrak artefak spesifik dari reasons
            rule2_ips      = []
            rule4_children = []
            for reason in reasons:
                if "[Rule2]" in reason:
                    # Format: -> 192.168.1.1:4444 (TCP, ESTABLISHED)
                    m = re.search(r'-> (\d+\.\d+\.\d+\.\d+:\d+)', reason)
                    if m:
                        rule2_ips.append(m.group(1))
                if "[Rule4]" in reason:
                    # Format: -> 'cmd.exe' (PID=...)
                    m = re.search(r"-> '([^']+)' \(PID=", reason)
                    if m:
                        rule4_children.append(m.group(1))

            # Header rekomendasi
            self._detail_text.insert("end", "--- REKOMENDASI INVESTIGASI -------------------------------------\n", "header")

            rule_meta = [
                ("Rule1", rec.get("Rule1_hit"), 3),
                ("Rule2", rec.get("Rule2_hit"), 2),
                ("Rule3", rec.get("Rule3_hit"), 3),
                ("Rule4", rec.get("Rule4_hit"), 2),
            ]

            for key, flag, weight in rule_meta:
                if flag:
                    lines = REKOMENDASI[key].split("\n")
                    self._detail_text.insert("end", f"\n{lines[0]}\n", "rekomendasi")
                    for line in lines[1:]:
                        self._detail_text.insert("end", f"{line}\n", "arrow_line")
                        # Rule 2: sisipkan IP spesifik setelah baris VirusTotal generik
                        if key == "Rule2" and "Telusuri reputasi IP tujuan" in line:
                            for ip in rule2_ips:
                                self._detail_text.insert("end",
                                    f"   -> Telusuri reputasi {ip} di VirusTotal\n", "arrow_line")
                        # Rule 4: sisipkan nama child process setelah baris pstree
                        if key == "Rule4" and "windows.pstree" in line and rule4_children:
                            for child in rule4_children:
                                self._detail_text.insert("end",
                                    f"   -> Child process mencurigakan terdeteksi: {child}\n", "arrow_line")
        else:
            self._detail_text.insert(
                "end",
                f"  PID {pid_str} ({rec['Name']}) -- tidak ada indikator anomali ditemukan.",
                "rekomendasi",
            )

        self._detail_text.configure(state="disabled")

    def _on_search(self, *args):
        """Filter tabel secara real-time berdasarkan teks pencarian."""
        query = self._search_var.get().lower().strip()

        if not self._classifications:
            return

        if not query:
            self._populate_table(self._classifications)
            return

        filtered = [
            r for r in self._classifications
            if query in str(r["Name"]).lower()
            or query in str(r.get("Path") or "").lower()
            or query in str(r["Status"]).lower()
        ]
        self._populate_table(filtered)

    def _export_csv(self):
        if not self._classifications:
            return

        from core.reporter import export_all

        folder = filedialog.askdirectory(
            title="Pilih Folder Tujuan Export",
            initialdir=str(Path("/mnt/d") if Path("/mnt/d").exists() else Path.home()),
        )
        if not folder:
            return

        dump_name      = Path(self._dump_path.get()).name
        plugin_results = getattr(self, "_plugin_results", {})

        try:
            exported = export_all(
                self._classifications,
                plugin_results,
                dump_name,
                output_dir=Path(folder),
            )
        except PermissionError:
            # Penyebab paling umum: berkas hasil lama masih dibuka di Excel,
            # atau folder tujuan tidak dapat ditulisi.
            messagebox.showerror(
                "Export Gagal",
                "Tidak dapat menulis berkas hasil.\n\n"
                "Pastikan berkas hasil sebelumnya (results.xlsx / summary.xlsx) "
                "tidak sedang dibuka di Excel, lalu coba lagi.",
            )
            self._set_status("Export gagal: berkas hasil sedang dibuka atau folder tidak bisa ditulisi.")
            return
        except Exception as e:
            messagebox.showerror(
                "Export Gagal",
                f"Terjadi kesalahan saat menyimpan hasil:\n\n{e}",
            )
            self._set_status(f"Export gagal: {e}")
            return

        messagebox.showinfo(
            "Export Berhasil",
            f"Hasil disimpan dalam tiga berkas:\n\n"
            f"  {exported['results_path'].name}\n"
            f"  {exported['klasifikasi_csv'].name}\n"
            f"  {exported['summary_path'].name}\n\n"
            f"Lokasi: {folder}",
        )
        self._set_status(f"Export selesai (Excel + CSV): {folder}")

    # ------------------------------------------------------------------
    # Helper UI
    # ------------------------------------------------------------------

    def _populate_table(self, classifications: list):
        self._clear_table()

        # Sort: jumlah rule terpicu (desc), lalu PID (asc).
        # Penggunaan rule-count bukan score per arahan Pak Rahmat (3 Juni 2026).
        sorted_data = sorted(
            classifications,
            key=lambda r: (
                -sum([
                    bool(r.get("Rule1_hit")),
                    bool(r.get("Rule2_hit")),
                    bool(r.get("Rule3_hit")),
                    bool(r.get("Rule4_hit")),
                ]),
                r["PID"],
            ),
        )

        for rec in sorted_data:
            status = rec["Status"]
            # Tag binary: suspicious atau clean (tidak lagi pakai HIGH/MEDIUM/LOW)
            tag    = "suspicious" if status == "SUSPICIOUS" else "clean"
            r1     = "\u2714" if rec["Rule1_hit"] else "\u00b7"
            r2     = "\u2714" if rec["Rule2_hit"] else "\u00b7"
            r3     = "\u2714" if rec["Rule3_hit"] else "\u00b7"
            r4     = "\u2714" if rec["Rule4_hit"] else "\u00b7"
            path   = rec["Path"] or "--"
            # Score & Risk masih disertakan di values untuk menjaga struktur kolom,
            # tapi kolomnya di-hide via displaycolumns (tidak tampil ke user).
            score  = rec.get("Score", 0)
            risk   = rec.get("Risk", "CLEAN")

            self._tree.insert(
                "", "end",
                values=(rec["PID"], rec["Name"], path, status,
                        score, risk, r1, r2, r3, r4),
                tags=(tag,),
            )

    def _clear_table(self):
        for item in self._tree.get_children():
            self._tree.delete(item)

        # Kembalikan panel detail ke arahan awal, bukan kotak kosong.
        self._show_detail_placeholder()

    def _reset_stats(self):
        self._total_var.set("--")
        self._suspicious_var.set("--")
        self._clean_var.set("--")
        self._elapsed_var.set("--")
        # Kartu WAKTU kembali netral (abu-abu) saat belum ada analisis.
        if hasattr(self, "_elapsed_label"):
            self._elapsed_label.configure(fg=COLOR_SUBTEXT)

    def _reset_all(self):
        """Kembalikan platform ke kondisi seperti baru dibuka.

        Meminta konfirmasi Ya/Tidak lebih dulu. Bila Ya, seluruh hasil,
        pilihan file, statistik, dan tabel dibersihkan.
        """
        if self._is_running:
            return
        yakin = messagebox.askyesno(
            "Reset",
            "Apakah Anda yakin ingin mengatur ulang platform?\n\n"
            "Seluruh hasil analisis dan pilihan file saat ini akan dihapus, "
            "lalu platform kembali ke kondisi awal.",
        )
        if not yakin:
            return

        self._stop_timer()
        self._clear_table()
        self._reset_stats()
        self._classifications = []
        self._plugin_results = {}
        self._dump_path.set("")
        self._search_var.set("")
        self._use_parallel_var.set(False)
        self._hide_progress()
        self._btn_export.configure(state="disabled")
        self._btn_reset.configure(state="disabled")
        self._set_status("Siap. Pilih file memory dump untuk memulai.")

    # ------------------------------------------------------------------
    # Indikator kemajuan (progress bar + teks persentase)
    # ------------------------------------------------------------------

    def _show_progress(self):
        """Tampilkan indikator kemajuan di bawah baris tombol saat analisis mulai."""
        self._progress["value"] = 0
        self._progress_label_var.set("Memproses... 0%")
        if not self._progress_frame.winfo_ismapped():
            self._progress_frame.pack(fill="x", pady=(10, 0))

    def _hide_progress(self):
        """Sembunyikan indikator kemajuan saat idle/selesai supaya tidak membingungkan."""
        if self._progress_frame.winfo_ismapped():
            self._progress_frame.pack_forget()
        self._progress["value"] = 0
        self._progress_label_var.set("")

    def _set_progress(self, done: int, total: int):
        """Perbarui bar dan teks persentase, misal 'Memproses... 33%'.

        Rincian (i/n) dan nama plugin sudah tampil di status bar bawah, jadi
        di sini cukup persentasenya saja agar tidak berulang.
        """
        persen = round(done / total * 100) if total else 0
        self._progress["value"] = persen
        self._progress_label_var.set(f"Memproses... {persen}%")

    # ------------------------------------------------------------------
    # Timer waktu pengerjaan
    # ------------------------------------------------------------------

    @staticmethod
    def _format_duration(seconds: float) -> str:
        """Ubah detik menjadi format ringkas, misal 45s, 3m 12s, 1j 04m."""
        total = int(round(seconds))
        jam, sisa = divmod(total, 3600)
        menit, detik = divmod(sisa, 60)
        if jam:
            return f"{jam}j {menit:02d}m"
        if menit:
            return f"{menit}m {detik:02d}s"
        return f"{detik}s"

    def _start_timer(self):
        """Mulai menghitung waktu dan tampilkan detiknya secara live."""
        self._start_time = time.monotonic()
        self._elapsed_var.set("0s")
        # Angka waktu dibiruan agar menonjol selama/ sesudah analisis.
        if hasattr(self, "_elapsed_label"):
            self._elapsed_label.configure(fg=COLOR_ACCENT)
        self._tick_timer()

    def _tick_timer(self):
        """Perbarui tampilan waktu tiap detik selama analisis berjalan.

        Waktu hanya ditampilkan pada kartu WAKTU di panel statistik atas,
        tidak lagi disisipkan ke status bar bawah agar tidak menempel pada
        pesan progres plugin.
        """
        if self._start_time is None:
            return
        elapsed = time.monotonic() - self._start_time
        self._elapsed_var.set(self._format_duration(elapsed))
        self._timer_job = self.after(1000, self._tick_timer)

    def _stop_timer(self) -> str:
        """Hentikan timer, kunci nilai akhir di kartu, kembalikan teks durasi."""
        if self._timer_job is not None:
            self.after_cancel(self._timer_job)
            self._timer_job = None
        if self._start_time is None:
            return "--"
        elapsed = time.monotonic() - self._start_time
        teks = self._format_duration(elapsed)
        self._elapsed_var.set(teks)
        self._start_time = None
        return teks

    def _set_status(self, msg: str):
        self._status_text.set(msg)

    def _set_buttons_running(self, running: bool):
        self._is_running = running
        state_analyze = "disabled" if running else "normal"
        state_browse  = "disabled" if running else "normal"
        state_export  = "disabled" if running else (
            "normal" if self._classifications else "disabled"
        )
        state_reset   = "disabled" if running else (
            "normal" if self._classifications else "disabled"
        )
        self._btn_analyze.configure(state=state_analyze)
        self._btn_browse.configure(state=state_browse)
        self._btn_export.configure(state=state_export)
        self._btn_reset.configure(state=state_reset)
        self._btn_cancel.configure(state="normal" if running else "disabled")
        self._chk_parallel.configure(state="disabled" if running else "normal")

        if running:
            self._btn_analyze.configure(text="  Menganalisis...")
        else:
            self._btn_analyze.configure(text="  Mulai Analisis")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def launch():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%H:%M:%S",
    )
    app = ForensicTriaseApp()
    app.mainloop()


if __name__ == "__main__":
    launch()