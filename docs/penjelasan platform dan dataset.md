# Penjelasan Platform Triase Forensik Memori & Pembuatan 7 Dataset

> Dokumen penjelas untuk dosen penguji.
> Bagian A menjelaskan **cara kerja platform dari awal hingga akhir**.
> Bagian B menjelaskan **pembuatan 7 dataset pengujian**.
> Peneliti: Kevin Armando Siburian (2221101800) — Rekayasa Keamanan Siber, PSSN.

---

# BAGIAN A — CARA KERJA PLATFORM

## A.1 Platform Ini Sebenarnya Apa?

Platform ini adalah **alat triase forensik memori**. Kata kuncinya **"triase"** — sama seperti triase di IGD rumah sakit: tugasnya **memilah cepat** mana yang butuh perhatian ("SUSPICIOUS") dan mana yang aman ("CLEAN"), **bukan** mendiagnosis tuntas.

Masukannya adalah **file memory dump** — potret isi RAM komputer pada satu waktu (file `.raw`/`.dmp`, ukuran 5 GB di penelitian ini). Keluarannya adalah **daftar semua proses** yang berjalan saat dump diambil, masing-masing sudah diberi vonis **CLEAN atau SUSPICIOUS** beserta **alasannya**.

Prinsip desain terpenting: **binary classification** (hanya 2 keputusan, tanpa skor/level risiko) dan **sensitivitas diprioritaskan atas spesifisitas** — artinya alat lebih memilih "waspada berlebihan" (mungkin ada false positive) daripada "kecolongan" (false negative). **Satu indikator anomali cukup** untuk memberi vonis SUSPICIOUS.

## A.2 Fondasi Ilmiah

Platform tidak dibangun dari asumsi pribadi, melainkan dari:

1. **Metodologi SANS** — kerangka *"6-Step Investigative Methodology"* forensik memori (Identify Rogue Processes, Review Network Artifacts, Look for Code Injection, Analyze Process Objects). Empat aturan platform ini adalah implementasi langkah-langkah tersebut.
2. **Wawancara Kepala LFD BSSN** (Ardian Bagus Setyadi) — khususnya Q13, tentang indikator anomali yang paling sering muncul di kasus nyata. Ini yang menentukan **indikator mana** yang diprioritaskan.
3. **MITRE ATT&CK** — pemetaan tiap aturan ke teknik serangan standar dunia (T1036, T1059, T1071, T1055, T1574, T1003).

## A.3 Arsitektur: Tiga Modul + Perekat

Platform dipecah jadi modul-modul terpisah agar rapi dan mudah diuji. GUI dan logika inti **sepenuhnya terpisah** — kalau GUI diganti, logika deteksi tidak perlu diubah.

```
                    ┌─────────────────────────────┐
   File dump  ───►  │   main.py  (run_analysis)   │  ◄── "lem" / orkestrator
   (.raw/.dmp)      └──────────────┬──────────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          ▼                        ▼                         ▼
   ┌─────────────┐         ┌───────────────┐         ┌──────────────┐
   │ runner.py   │  ───►   │  analyzer.py  │  ───►   │ reporter.py  │
   │ jalankan 6  │  data   │ evaluasi 4    │ vonis   │ ekspor hasil │
   │ plugin Vol3 │ mentah  │ aturan (rules)│ per-PID │ ke Excel     │
   └─────────────┘         └───────────────┘         └──────────────┘
```

| Modul | Tanggung jawab |
|---|---|
| `core/runner.py` | Menjalankan 6 plugin Volatility3 pada dump, mengubah output JSON jadi data terstruktur |
| `core/analyzer.py` | **Otak platform** — mengevaluasi tiap proses lewat 4 aturan, memberi vonis |
| `core/reporter.py` | Menulis hasil ke file Excel (laporan) |
| `main.py` | Perekat: memanggil ketiga modul berurutan (fungsi `run_analysis`) |
| `gui/app.py` | Antarmuka grafis (Tkinter): pilih file, klik analisis, lihat hasil |

## A.4 Enam Plugin Volatility3 yang Digunakan

Platform tidak "membaca RAM" sendiri — ia berdiri di atas **Volatility3 2.28.1** (kerangka forensik memori standar industri). Volatility bertugas mengekstrak artefak; platform bertugas **menilai** artefak itu.

| # | Plugin | Artefak yang diambil | Dipakai aturan |
|---|---|---|---|
| 1 | `windows.pslist` | Daftar proses (nama, PID) | Rule 1 |
| 2 | `windows.pstree` | Pohon proses induk→anak + Path | Rule 1 |
| 3 | `windows.netscan` | Koneksi jaringan (state, alamat, port) | Rule 2 |
| 4 | `windows.malware.malfind` | Segmen memori mencurigakan (RWX) | Rule 3 |
| 5 | `windows.dlllist` | Daftar DLL yang dimuat tiap proses + Path | Rule 4a |
| 6 | `windows.handles` | Handle antarproses (termasuk ke LSASS) | Rule 4b |

## A.5 Alur Kerja End-to-End (langkah demi langkah)

**Langkah 0 — Input.** Pengguna memilih file dump lewat GUI (atau memberi path lewat CLI). GUI memanggil `main.run_analysis(dump_path)`.

**Langkah 1 — Ekstraksi (runner.py).** Keenam plugin dijalankan **berurutan** terhadap dump. Tiap plugin menghasilkan JSON yang diubah jadi list-of-dict. Karena dump 5 GB, tahap ini yang paling lama (beberapa menit). Ada dukungan **pembatalan** (cancel) di sela plugin bila pengguna menghentikan analisis.

**Langkah 2 — Persiapan data (analyzer.py → `build_lookup_tables`).** Semua **PID unik** dari keenam plugin dikumpulkan. Dibangun tabel pencarian cepat: PID → data pslist, PID → data pstree, PID → koneksi, PID → segmen malfind, PID → DLL, PID → handle, dan pemetaan **PID → nama proses induk** (dari pstree). `pstree` yang bersarang "diratakan" (flatten) secara rekursif lebih dulu.

**Langkah 3 — Evaluasi (inti).** Untuk **setiap PID**, platform menjalankan **4 aturan** (lihat A.6). Tiap aturan mengembalikan `(menyala?, [alasan])`. Vonis:

```
SUSPICIOUS  jika  Rule1 ATAU Rule2 ATAU Rule3 ATAU Rule4 menyala
CLEAN       jika  tidak ada satu pun menyala
```

Semua alasan dari aturan yang menyala digabung ke daftar `Reasons`.

**Langkah 4 — Laporan (reporter.py).** Hasil ditulis ke Excel (lihat A.7).

**Langkah 5 — Tampilan.** GUI menampilkan tabel proses (baris SUSPICIOUS berwarna), statistik ringkas, dan panel detail berisi alasan + rekomendasi investigasi saat sebuah baris dipilih.

## A.6 Empat Aturan Deteksi (jantung platform)

Semua aturan bersandar pada **daftar acuan (baseline/whitelist)** proses & path Windows yang sah, bersumber dari SANS dan dokumentasi Microsoft. Filosofinya: *"kenali yang normal, tandai yang menyimpang."*

### Rule 1 — Identify Rogue Processes
Mendeteksi proses yang **menyamar** sebagai proses sistem. Tiga sub-pemeriksaan:
- **(a) Typosquatting** — nama proses dibandingkan dengan daftar proses Windows sah memakai **Levenshtein edit distance**. Jika jaraknya ≤ 2 (mis. `svch0st.exe` vs `svchost.exe`, jarak = 1) → mencurigakan. Nama yang **persis** ada di whitelist dilewati lebih dulu (agar tidak salah tuduh).
- **(b) Path mencurigakan** — proses berjalan dari lokasi tak wajar (`\Temp\`, `\Users\Public\`, `\Downloads\`, `\AppData\`, dll). Path yang diawali direktori sah (`C:\Windows\System32\`, `C:\Program Files\`, ...) dilewati.
- **(c) Relasi induk-anak menyimpang** — mis. `svchost.exe` yang induknya **bukan** `services.exe`, atau aplikasi dokumen (`soffice.bin`, `winword.exe`) yang **melahirkan shell** (`powershell.exe`, `cmd.exe`). Ini menangkap serangan makro. *(Catatan metodologis: sub-pemeriksaan ini semula dikira "Rule 4"; setelah verifikasi ke poster resmi SANS, `pstree` terbukti masuk kategori "Identify Rogue Processes", jadi dipindah ke Rule 1.)*

### Rule 2 — Review Network Artifacts
Menandai proses yang **tidak wajar berjaringan** (tidak ada di `LEGIT_NETWORK_PROCESSES` seperti browser, svchost, dll) tetapi punya koneksi **ESTABLISHED ke alamat eksternal**. Ini menangkap **komunikasi C2 (Command & Control)** malware.

### Rule 3 — Look for Evidence of Code Injection
Menandai proses yang punya segmen memori **`PAGE_EXECUTE_READWRITE` + PrivateMemory** (lewat `malfind`) — tanda klasik **kode disuntikkan** ke memori proses. Proses yang **sah** memakai RWX (Defender, browser dengan JIT, LibreOffice) ada di `LEGIT_RWX_PROCESSES` dan dikecualikan.

### Rule 4 — Analyze Process Objects
Dua sub-pemeriksaan:
- **(a) DLL dari path anomali** — via `dlllist`: proses memuat DLL dari lokasi tak wajar (mis. `evil.dll` dari `C:\Users\Public\`). Menangkap **DLL hijacking/side-loading**.
- **(b) Akses mencurigakan ke LSASS** — via `handles`: proses (di luar `LEGIT_LSASS_ACCESSORS`) memegang handle ke `lsass.exe` yang mengandung bit **`PROCESS_VM_READ` (0x0010)**. Menangkap **credential dumping** (mis. Mimikatz). *(Catatan: pemakaian bit VM_READ adalah elaborasi teknis peneliti berbasis MITRE T1003.001, bukan dari transkrip wawancara.)*

### Peran Whitelist (esensial)
Tanpa whitelist, banyak proses sah akan salah tuduh (mis. Defender memakai RWX; System memegang handle LSASS). Whitelist inilah yang menekan false positive — dan Dataset 7 membuktikan perannya nyata: dari 14 handle sah ke LSASS, hanya Mimikatz yang lolos sebagai SUSPICIOUS.

## A.7 Laporan yang Dihasilkan

Tiap sesi analisis menghasilkan **2 file Excel** (`reporter.py`), dinamai `[dump]_[timestamp]_...`:

**1. `results.xlsx` (5 sheet):**
- Sheet 1–4: output mentah `pslist`, `pstree`, `netscan`, `malfind` (bukti mentah).
- Sheet 5 **Klasifikasi** (inti): kolom `PID · Name · Path · Status · Rule1_Rogue · Rule2_Network · Rule3_Injection · Rule4_ProcObj · Reasons`. Baris diwarnai sesuai status.

**2. `summary.xlsx` (1 baris statistik sesi):**
`Dump · Timestamp · Total_PID · Suspicious · Clean · Rule1_Hits · Rule2_Hits · Rule3_Hits · Rule4_Hits`.

> Catatan desain: kolom Score/Risk dan level High/Medium/Low **dihapus** (arahan Pak Rahmat, 3 Juni 2026) agar konsisten dengan model **biner murni**.

---

# BAGIAN B — PEMBUATAN 7 DATASET PENGUJIAN

## B.1 Kenapa Perlu 7 Dataset?

Alat deteksi harus **dibuktikan**, bukan sekadar diklaim. Karena itu dibuat 7 skenario memory dump:
- **1 dataset bersih** → membuktikan alat tidak asal menuduh (uji false positive).
- **6 dataset terinfeksi** → tiap dataset menargetkan **satu aturan/sub-aturan**, agar terbukti tiap aturan **berdiri sendiri**.

Ini disebut **pengujian per-aturan terisolasi**. Dengan memisahkan serangan, saya bisa membuktikan: *"Ancaman ini lolos Rule 1, 2, 3 — tertangkap HANYA oleh Rule 4."* Itulah bukti **nilai deteksi mandiri** tiap aturan.

## B.2 Tiga Prinsip Penjaga Validitas

**(a) Landasan dua lapis.** Tiap skenario berpijak pada wawancara BSSN (Q13) **dan** MITRE ATT&CK + prevalensi global (Picus Red Report 2026). Bukan karangan.

**(b) Serangan nyata (anti *circular reasoning*).** Jika saya menanam sendiri "tanda mencurigakan" lalu alat mendeteksinya, itu penalaran melingkar. Maka serangan dijalankan dengan **tool sungguhan** (Meterpreter, Mimikatz, Sliver, rundll32) — indikator muncul **organik** sebagai akibat alami teknik, bukan ditempelkan.

**(c) Ground truth diketahui lebih dulu.** Sebelum alat dijalankan, proses/PID jahat sudah dicatat dan dikonfirmasi dari sisi penyerang (reverse shell, `tasklist`, `netstat`). Ada "kunci jawaban" untuk mengecek benar/salah vonis.

## B.3 Lingkungan Laboratorium (sama untuk semua dataset)

| Komponen | Detail |
|---|---|
| Korban (victim) | Windows 10 Pro 22H2 (Build 19045.2965), IP `192.168.70.130` |
| Penyerang (attacker) | Kali Linux, IP `192.168.70.131` |
| Jaringan | VMware **host-only, TANPA internet** — terisolasi total |
| Akuisisi memori | **DumpIt** (Administrator) → file `.raw` 5 GB |
| Kebersihan | Restore snapshot bersih **sebelum tiap skenario** |

Isolasi tanpa internet penting: menghilangkan koneksi telemetri sah yang bisa mengacaukan Rule 2 (pelajaran dari Dataset 1).

## B.4 Tujuh Dataset, Satu per Satu

| # | Dataset | Aturan | Teknik / Tool | MITRE | PID jahat | Hasil |
|---|---|---|---|---|---|---|
| 1 | `clean_baseline` | — (uji FP) | Aktivitas kantor normal | — | *(tidak ada)* | 1 FP jujur |
| 2 | `infected_r1a_masquerade` | **R1a** | Meterpreter dinamai `svch0st.exe` | T1036.005 | 4988 | ✅ |
| 3 | `infected_r1b_parentchild` | **R1b** | LibreOffice makro → PowerShell | T1059.001 | 9140→10120 | ✅ |
| 4 | `infected_r2_network` | **R2** | C2 **Sliver** (`AtlasAgent.exe`) | T1071.001 | 8732 | ✅ |
| 5 | `infected_r3_injection` | **R3** | Meterpreter migrate ke `notepad.exe` | T1055.001 | 3404 | ✅ |
| 6 | `infected_r4a_dll` | **R4a** | `rundll32` muat `evil.dll` | T1574 | 8392 | ✅ |
| 7 | `infected_r4b_lsass` | **R4b** | **Mimikatz** dump kredensial | T1003.001 | 8 | ✅ |

### Dataset 1 — `clean_baseline` (sistem bersih)
Pemakaian kantor normal (browser, Word/Excel, VS Code, aplikasi portabel), **tanpa serangan**. Hasil: dari **179 proses, 178 bersih, 1 ditandai** — `PaintStudio.Vi` (Paint 3D) yang membuka koneksi ke server Microsoft/Azure (telemetri **sah**). Ini **false positive jujur** yang **sengaja tidak disembunyikan**, sesuai filosofi *"lebih baik waspada daripada kecolongan"*. Justru memperkuat kredibilitas: hasil nyata, bukan dipoles.

### Dataset 2 — `infected_r1a_masquerade` (nama proses palsu)
Payload Meterpreter dinamai **`svch0st.exe`** (huruf "o" → angka "0"). Terdeteksi lewat **kemiripan nama (typosquatting)** + lokasi tak wajar. Contoh `svch0st.exe` bahkan **disebut eksplisit** narasumber BSSN di Q13.

### Dataset 3 — `infected_r1b_parentchild` (rantai induk-anak janggal)
Meniru dokumen ber-makro. Karena victim tak punya MS Office, dipakai **LibreOffice** yang makronya memanggil PowerShell. Kejanggalan: `soffice.bin` **tidak wajar** melahirkan `powershell.exe`. Alat menangkap **relasi induk→anak abnormal** ini. PowerShell-nya ikut memicu R2 & R3 (koneksi + shellcode) — dicatat sebagai **temuan sekunder organik**, bukti indikator muncul alami.

### Dataset 4 — `infected_r2_network` (koneksi C2)
Sengaja pakai **Sliver** (C2 profesional, bahasa Go), **bukan** Meterpreter — karena Sliver **tidak meninggalkan jejak RWX**, sehingga Rule 3 tidak ikut menyala. Implant disamarkan tiga lapis (nama benign, path sah, diluncurkan lewat Explorer) agar R1/R4 diam. Hasil: ancaman C2 nyata yang **lolos R1/R3/R4 — tertangkap HANYA oleh R2**. Bukti murni nilai Rule 2.

### Dataset 5 — `infected_r3_injection` (suntik kode ke proses sah)
Kebalikan Dataset 4. Kode Meterpreter **disuntik ke `notepad.exe`** lewat `migrate`, meninggalkan segmen **RWX** yang ditangkap `malfind`. Koneksi C2 "ditidurkan" (`sleep`) agar R2 diam. Hasil: proses sah yang tampak normal terbongkar **hanya lewat artefak injeksi di memori** — bukti murni Rule 3.

### Dataset 6 — `infected_r4a_dll` (DLL dari lokasi mencurigakan)
`evil.dll` ditaruh di `C:\Users\Public\` lalu dimuat **`rundll32.exe`** (program Windows asli). Memisahkan **pemuat** (rundll32, sah) dari **DLL** (path aneh) membuat **hanya DLL** yang mencurigakan → Rule 4a teruji sendirian.

> **Catatan kejujuran:** capture pertama sempat menghasilkan **false positive** — jendela PowerShell unduhan menyisakan segmen RWX benign sehingga Rule 3 menyala keliru. Capture diulang setelah PowerShell ditutup. Didokumentasikan untuk **Bab Keterbatasan** (Rule 3 memang sensitif terhadap PowerShell sah).

### Dataset 7 — `infected_r4b_lsass` (pencurian kredensial)
**Mimikatz** menjalankan `sekurlsa::logonpasswords`, membuka **handle ke `lsass.exe`** dengan izin baca memori (`PROCESS_VM_READ`). Mimikatz dipilih (bukan procdump) karena **menahan handle terbuka** di prompt interaktif → terjamin tertangkap DumpIt. Hasil: `mimikatz.exe` (PID 8) tertangkap Rule 4b, bukti bit `0x1010 & 0x0010 ≠ 0` terverifikasi manual. **14 handle sah** lain (System, csrss, lsass-self) **ditekan whitelist** → nol false positive. Membuktikan whitelist esensial pada data nyata.

## B.5 Antisipasi Pertanyaan Penguji

**T: "Bagaimana saya tahu alat Anda tidak dibuat khusus untuk lulus dataset ini?"**
J: Serangan pakai tool nyata; indikator muncul organik, bukan ditanam. Aturan ditulis independen dari dataset, berbasis SANS & MITRE.

**T: "Kenapa toolnya beda-beda (Sliver, Meterpreter, Mimikatz)?"**
J: Demi **isolasi aturan**. Tiap tool dipilih karena karakteristik forensiknya cocok menguji satu aturan tanpa mengotori aturan lain (Sliver zero-RWX untuk R2 murni; Meterpreter selalu-RWX untuk R3 murni; dst).

**T: "Kenapa masih ada false positive?"**
J: Itu **konsekuensi desain yang diterima**, bukan cacat. Alat ini triase — memprioritaskan **jangan kecolongan** (sensitivitas). FP-nya sedikit, transparan, sudah dianalisis akar penyebabnya.

**T: "Apakah 6 sampel cukup?"**
J: Ini pengujian **terkontrol per-aturan** dengan ground truth pasti. Dilengkapi rencana dataset **malware nyata** (Kategori B, *ecological validity*) dan **Bab Keterbatasan** yang jujur mendokumentasikan teknik yang bisa mengelabui alat.

---

*Rekaman resmi & detail tiap dataset: `docs/dataset_design.md` dan `docs/progress_log.md`.*
