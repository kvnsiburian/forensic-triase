# Rancangan Pengujian Dataset — Platform Triase Forensik Memori

> Dokumen kerja **test-design** (bukan narasi skripsi). Menjadi rujukan saat
> eksekusi pembuatan dataset di VM. Narasi TA ditulis terpisah oleh peneliti.
>
> Status: Dataset 1 FINAL. Dataset 2–7 kerangka (skenario disepakati, prosedur
> detail difinalkan per dataset sebelum eksekusi).

---

## 1. Prinsip Umum

1. **Grounding dua lapis** untuk setiap dataset:
   - *Primer (operasional):* wawancara Kepala LFD BSSN, Q13 — 6 indikator anomali
     tersering di kasus nyata. (Form Wawancara, 13 April 2025, Ardian Bagus Setyadi.)
   - *Sekunder (literatur):* MITRE ATT&CK + prevalensi global (Picus Red Report
     2026 / Red Canary) untuk indikator yang juga tinggi secara global.
2. **Filosofi triase** (analyzer.py): binary CLEAN/SUSPICIOUS, *sensitivitas
   diprioritaskan atas spesifisitas*, satu indikator cukup untuk flag. FP
   dipandang konsekuensi desain yang diterima, bukan cacat.
3. **Real tooling → indikator organik.** Serangan dieksekusi dengan tool nyata
   (Metasploit, Mimikatz, ProcDump) agar indikator muncul sebagai konsekuensi
   alami teknik — mematahkan tuduhan *circular reasoning* penguji.
4. **Lingkungan terisolasi** (Q10): VM host-only, tanpa internet. Kali (attacker)
   ↔ Windows 10 (victim).
5. **Ground truth eksplisit.** Untuk tiap dataset diketahui PID/proses mana yang
   jahat dan mengapa, SEBELUM analyzer dijalankan.
6. **Multi-rule firing diterima.** Payload nyata sering memicu >1 rule (mis.
   meterpreter → R1+R2+R3). Untuk dataset per-rule, dicatat **rule primer** yang
   ditargetkan; rule sekunder yang ikut menyala dicatat sebagai temuan wajar.
7. **Akuisisi konsisten:** DumpIt (Administrator) untuk semua dataset. Restore
   snapshot bersih sebelum tiap skenario (reproducibility).

### ⚠️ Catatan konstanta bersama
`SUSPICIOUS_PATH_KEYWORDS` dan `LEGIT_PATH_PREFIXES` dipakai bersama oleh Rule 1
dan Rule 4a. Mengubahnya memengaruhi kedua rule DAN membatalkan baseline regresi
lama (845 PID, TP=10, FP=1, FN=0, TN=834). Jangan ubah tanpa data — tangani
setelah temuan empiris dari clean_baseline.

---

## 2. Ringkasan 7 Dataset

| # | Dataset | Rule primer | MITRE | Q13 | Prevalensi global |
|---|---|---|---|---|---|
| 1 | `clean_baseline.raw` | — | — | — | Baseline berisik (level Sedang) |
| 2 | `infected_r1a_masquerade.raw` | R1a | T1036.005 | #1 | Top 6 (T1036) |
| 3 | `infected_r1b_parentchild.raw` | R1b | T1059.003 + .001 | #6 | #2 (T1059) |
| 4 | `infected_r2_network.raw` | R2 | T1071.001 | #4 | #5 (T1071) |
| 5 | `infected_r3_injection.raw` | R3 | T1055.001 | #2 | #1 (T1055) |
| 6 | `infected_r4a_dll.raw` | R4a | T1574.001/002 | #3 | high-impact (Q13) |
| 7 | `infected_r4b_lsass.raw` | R4b | T1003.001 | #5 | high-impact (Q13) |

Kategori B (ecological validity): `infected_realmalware.raw` — sampel nyata.
Kategori C (dokumen): Bab Keterbatasan / evasion.

---

## 3. Environment Bersama

- VM: Windows 10, catat build persis (mis. 22H2 19045.xxxx).
- Attacker: Kali Linux, jaringan host-only ke VM Windows.
- Restore snapshot bersih sebelum tiap dataset.
- Akuisisi: DumpIt (Administrator) → `<nama_dataset>.raw`.
- Catat per dataset: build OS, waktu capture, daftar proses/aktivitas (lampiran
  ground truth), IP Kali & port listener bila relevan.

Template tiap dataset: **Environment → Prosedur → MITRE → Q13 → Ground Truth →
Expected Output → Verifikasi.**

---

## 4. Dataset 1 — `clean_baseline.raw`  [FINAL]

**Tujuan:** baseline sistem bersih (ground-truth negatif) + uji false-positive
Rule 1 & Rule 4a pada workstation realistis. Level kebisingan: **Sedang**.

**Prosedur (level Sedang):**

| Aplikasi | Cara jalankan | Peran |
|---|---|---|
| Edge/Chrome | 3–4 tab wajar | realisme + whitelist |
| Word/Excel | buka 1 dokumen | realisme, probe R1c |
| VS Code (`Code.exe`) | buka 1 folder | **probe R3** (RWX non-whitelist) |
| App portable (PuTTY/7-Zip portable) | jalankan dari `C:\Users\<user>\Downloads\` | **probe R1b + R4a** |
| Python | interpreter, JANGAN panggil shell | kontrol R1c (CLEAN) |
| PDF reader, Explorer, Notepad | aktivitas latar | realisme |
| Defender, Search, OneDrive | default OS | CLEAN (whitelisted) |

Tidak termasuk Slack/Discord/Spotify (itu level Tinggi).

Langkah: restore snapshot → boot → tunggu CPU idle <10% → buka semua app →
diamkan 2–3 menit → DumpIt → `clean_baseline.raw` → catat lampiran.

**MITRE / Q13:** N/A (baseline).

**Ground Truth:** semua proses CLEAN. Target SUSPICIOUS = 0.

**Expected Output:** SUSPICIOUS = 0 idealnya. Jika 1–2 proses ⚠️ ter-flag →
FP nyata, dianalisis akar penyebab, difram­ing sebagai konsekuensi
sensitivitas > spesifisitas (Q9). JANGAN dibuang.

**Verifikasi (3 titik kritis):**
1. `Code.exe` ter-flag R3? → kandidat FP / masuk `LEGIT_RWX_PROCESSES`.
2. App portable ter-flag R4a via `\downloads\`? → konfirmasi isu keyword.
3. `windows.dlllist` mengeluarkan kolom `Path`? → verifikasi `TODO VERIFIKASI`.

**Lampiran ground truth (aktual):**
- Build OS: Windows 10 Pro 22H2 (OS Build 19045.2965)
- Waktu capture: _(diisi saat DumpIt)_
- App berjalan: _(diisi: Edge, Word/Excel, VS Code, <portable>, Python, ...)_

**Hasil aktual analyzer (1 Juli 2026):**
- Plugin: pslist 179, pstree 12 (root), netscan 154, malfind 14, dlllist 8657, handles 74336 — semua sukses.
- Total 179 PID | CLEAN 178 | **SUSPICIOUS 1** | Specificity 178/179 = 99,4%.
- **1 FP:** `PaintStudio.Vi` (Paint 3D, PID 12152) → Rule2, koneksi `192.168.70.130:51252 → 48.209.133.15:443` (IP Microsoft/Azure, telemetri sah). Akar: tidak ada di `LEGIT_NETWORK_PROCESSES`. Keputusan: dibiarkan & didokumentasikan (sensitivitas>spesifisitas).
- Rule3 tersupresi benar: 14 malfind semuanya `MsMpEng.exe` (Defender) ∈ `LEGIT_RWX_PROCESSES` → 0 FP.
- Rule4b benar: 14 handle ke lsass semuanya dipegang `System` (PID 4) ∈ `LEGIT_LSASS_ACCESSORS` → 0 flag.
- **TODO VERIFIKASI RESOLVED:** field terkonfirmasi — dlllist(`Path`,`Name`,`Process`); handles(`Type`,`Name`=`"lsass.exe Pid N"`,`GrantedAccess`=int desimal).

---

## 5. Dataset 2 — `infected_r1a_masquerade.raw`  [KERANGKA]

**Rule primer:** R1a (typosquatting + path). **MITRE:** T1036.005 —
Masquerading: Match Legitimate Name or Location. **Q13 poin 1** (LFD menyebut
contoh eksplisit `svch0st.exe`, proses jalan dari Temp/AppData).

**Skenario:** payload meterpreter (`msfvenom -p windows/x64/meterpreter/
reverse_tcp`) dinamai `svch0st.exe`, dijalankan dari `C:\Users\Public\`.
Memicu R1a (edit distance 1 dari `svchost.exe`) + path (`\users\public\`).
Kemungkinan ikut memicu R2 (C2) & R3 (shellcode) — dicatat sebagai sekunder.

**Ground Truth:** `svch0st.exe` = SUSPICIOUS (primer R1a). Sisanya CLEAN.

**Verifikasi:** Rule1_hit=True dengan reason typosquatting + path.

_(Prosedur detail + expected output difinalkan sebelum eksekusi.)_

---

## 6. Dataset 3 — `infected_r1b_parentchild.raw`  [FINAL]

**Rule primer:** R1b (parent-child abnormal). **MITRE:** T1059.003 (Windows
Command Shell, relasi yang terdeteksi) + T1059.001 (PowerShell, cucu di rantai).
**Q13 poin 6** (aplikasi dokumen meluncurkan cmd/PowerShell).

**Skenario (aktual):** dokumen/aplikasi kantor ber-makro men-spawn shell.
Karena victim tak punya MS Office, dipakai **LibreOffice** (`soffice.bin` ∈
`SUSPICIOUS_CHILD_SPAWNERS`). Makro LibreOffice Basic memanggil:
`Shell("...\cmd.exe", 1, "/c powershell -nop -ep bypass -File C:\Users\Public\p.ps1", False)`.
Rantai proses aktual: **`soffice.bin → cmd.exe → powershell.exe`**.

**Catatan teknis (kenapa ada cmd.exe di tengah):** `Shell()` LibreOffice bisa
meluncurkan proses (notepad OK) tapi oper argumen ke `powershell.exe` langsung
tidak reliabel; lewat `cmd /c` argumen lolos bersih. Relasi yang **terdeteksi
Rule 1b** = `soffice.bin → cmd.exe` (cmd.exe ∈ `SHELL_PROCESSES`) → T1059.003;
`powershell.exe` adalah cucu (T1059.001). Dua interpreter hadir — justru lebih
realistis (macro sering pakai perantara cmd/wscript).

**Payload:** `p.ps1` = **plain PowerShell TCP reverse shell** ke Kali
`192.168.70.131:4444` (BUKAN meterpreter — `psh-reflection` gagal connect;
reverse shell murni lebih andal & menjaga `powershell.exe` tetap hidup di loop).
Indikator R2/R3 muncul organik dari payload nyata (anti-circular-reasoning).

**Environment aktual:** victim 192.168.70.130 (Win10 22H2 19045.2965), Kali
192.168.70.131. Capture 2 Juli 2026 via DumpIt selagi C2 aktif. Dump 5 GB.

**Ground Truth (dikonfirmasi via reverse shell, `Get-CimInstance Win32_Process`):**
- `soffice.bin` **PID 9140** (PPID 11232) — spawner
- `cmd.exe` **PID 11200** (PPID 9140) — anak soffice.bin, target deteksi R1b
- `powershell.exe` **PID 7456** (PPID 11200) — pemegang C2 reverse shell
- (proses PowerShell manual liar PID 2556 ditutup sebelum dump → dataset bersih)

**Hasil aktual analyzer (2 Juli 2026):**
- Plugin: pslist 170, pstree 7, netscan 111, malfind 237, dlllist 8724, handles 60896 — semua sukses.
- Total **170 PID | CLEAN 168 | SUSPICIOUS 2** | FP 0.
- **PID 9140 `soffice.bin` — R1=True (PRIMER):**
  `[Rule1] Spawn mencurigakan: 'soffice.bin' (PID=9140) -> 'cmd.exe' (PID=11200)`
- **PID 7456 `powershell.exe` — R2=True, R3=True (sekunder organik):**
  `[Rule2]` C2 ke `192.168.70.131:4444` (TCPv4, ESTABLISHED) +
  `[Rule3]` RWX (PAGE_EXECUTE_READWRITE) + PrivateMemory (5 segmen, .NET/shellcode).

**Verifikasi:**
- ✅ Target primer R1b tercapai: `soffice.bin` PID 9140 flag Rule1 dengan reason
  "Spawn mencurigakan", PID + anak (cmd.exe 11200) cocok persis ground truth.
- ✅ Zero FP di 168 proses lain; hanya 2 SUSPICIOUS, keduanya bagian rantai yang
  ditanam → tidak ada proses liar sisa troubleshooting.
- ✅ Deteksi berlapis (R2/R3 pada powershell 7456) muncul organik dari reverse
  shell nyata, bukan ditanam.

---

## 7. Dataset 4 — `infected_r2_network.raw`  [KERANGKA]

**Rule primer:** R2 (network). **MITRE:** T1071.001 — Application Layer Protocol.
**Q13 poin 4** (outbound ke IP publik, port tak umum).

**Skenario:** proses non-whitelist dengan koneksi ESTABLISHED outbound ke
listener Kali. Nama proses TIDAK boleh menyerupai proses di
`LEGIT_NETWORK_PROCESSES`. Perhatikan netscan butuh `ForeignAddr` eksternal
(bukan 0.0.0.0) & State ESTABLISHED saat capture.

**Ground Truth:** proses C2 = SUSPICIOUS (primer R2). Sisanya CLEAN.

**Verifikasi:** Rule2_hit=True; catat ForeignAddr:Port.

_(Difinalkan sebelum eksekusi. Perlu koneksi aktif saat DumpIt — timing.)_

---

## 8. Dataset 5 — `infected_r3_injection.raw`  [KERANGKA]

**Rule primer:** R3 (code injection). **MITRE:** T1055.001 — DLL / reflective
injection. **Q13 poin 2** (proses legit disusupi kode).

**Skenario:** injeksi meterpreter ke proses legit (mis. `migrate` ke
`notepad.exe`), meninggalkan segmen `PAGE_EXECUTE_READWRITE` + `PrivateMemory=1`
yang terdeteksi `malfind`. Proses target TIDAK boleh ada di `LEGIT_RWX_PROCESSES`.

**Ground Truth:** proses yang disuntik = SUSPICIOUS (primer R3). Sisanya CLEAN.

**Verifikasi:** Rule3_hit=True; catat alamat segmen RWX.

_(Difinalkan sebelum eksekusi.)_

---

## 9. Dataset 6 — `infected_r4a_dll.raw`  [KERANGKA]

**Rule primer:** R4a (DLL path). **MITRE:** T1574.001/002 — DLL Search-Order
Hijacking / Side-Loading. **Q13 poin 3** (DLL dari path mencurigakan).

**Skenario:** DLL berbahaya/proof ditempatkan di path mencurigakan (mis.
`C:\Users\Public\` atau `\Temp\`) lalu dimuat oleh sebuah proses (mis. via
side-loading atau `rundll32`). Harus muncul entri `windows.dlllist` dengan
`Path` di direktori ber-keyword.

**Ground Truth:** proses pemuat = SUSPICIOUS (primer R4a). Sisanya CLEAN.

**Verifikasi:** Rule4_hit=True dengan reason "DLL path mencurigakan".
Lingkup: hanya anomali path (lihat Batasan Masalah §12).

_(Difinalkan sebelum eksekusi.)_

---

## 10. Dataset 7 — `infected_r4b_lsass.raw`  [KERANGKA]

**Rule primer:** R4b (akses LSASS). **MITRE:** T1003.001 — OS Credential
Dumping: LSASS Memory. **Q13 poin 5** (dump LSASS, Mimikatz dsb).

**Skenario:** `procdump.exe -ma lsass.exe` (atau `comsvcs.dll MiniDump` /
Mimikatz). Proses dumper memegang handle ke `lsass.exe` dengan bit
`PROCESS_VM_READ` (0x0010). **Timing kritis:** akuisisi memori dilakukan
SELAGI handle masih aktif (sebelum dumper exit).

**Ground Truth:** `procdump.exe` (atau dumper) = SUSPICIOUS (primer R4b).
Sisanya CLEAN.

**Verifikasi (rangkap):**
- Rule4_hit=True dengan reason "Akses mencurigakan ke LSASS".
- **Sekaligus verifikasi `TODO VERIFIKASI`:** cocokkan kolom `Type`, `Name`
  (format `lsass.exe Pid <PID>`), `GrantedAccess` (integer desimal) pada output
  `windows.handles` Volatility3 2.28.1 nyata. Jika cocok → hapus TODO di kode.

_(Difinalkan sebelum eksekusi.)_

---

## 11. Kategori B — `infected_realmalware.raw`  [KERANGKA]

Ecological validity. Detonasi sampel nyata (MalwareBazaar / theZoo) di VM
terisolasi. **Wajib known-condition** (Q15): ground truth tetap dikuasai —
identifikasi sampel, hash, dan perilaku terdokumentasi sebelum klaim.
_(Sumber & sampel dipilih kemudian.)_

---

## 12. Kategori C — Batasan Masalah & Keterbatasan

**Batasan Masalah (BAB I) — Rule 4 (final):**

> Pemeriksaan Analyze Process Objects (Rule 4) dibatasi pada dua indikator sesuai
> hasil wawancara penetapan konteks dengan Tim LFD BSSN (Q13 poin 3 dan poin 5):
> (a) DLL yang dimuat dari anomali lokasi/path, dan (b) akses antarproses ke
> `lsass.exe` yang mengandung bit `PROCESS_VM_READ`. Deteksi bersifat berbasis
> artefak yang tersedia di memori pada saat akuisisi, dan berbasis daftar acuan
> (baseline) nama proses dan path yang bersumber dari SANS serta MITRE ATT&CK.
> Teknik yang tidak meninggalkan jejak path anomali maupun handle aktif
> ber-`PROCESS_VM_READ` — termasuk pemuatan DLL dari path sah dan penyamaran
> sebagai proses pengakses sah — berada di luar lingkup penelitian, konsisten
> dengan sifat platform sebagai alat triase yang memprioritaskan efisiensi (Q9)
> atas kelengkapan deteksi.

**Keterbatasan Penelitian (BAB V) — kandidat evasion untuk didokumentasikan:**
- Rule 4a: DLL hijacking dari path legitimate (tak terdeteksi anomali path).
- Rule 4b: credential dumping tanpa handle VM_READ aktif (handle duplication,
  direct syscall); penyamaran sebagai pengakses sah (baseline berbasis nama).
- Umum: sifat volatile memori (Q6) — artefak bisa tak lengkap saat akuisisi.

---

## 13. Metrik & Pelaporan

- *Confusion matrix* per dataset & agregat: TP, FP, FN, TN.
- FP nyata WAJIB dilaporkan + dianalisis akar penyebab; difram­ing sebagai
  konsekuensi sensitivitas > spesifisitas (bukan minta maaf).
- Baseline lama sbg pembanding regresi: 845 PID, TP=10, FP=1, FN=0, TN=834
  (akan berubah setelah rebuild; angka baru menggantikan setelah semua dataset
  selesai & regresi ulang dijalankan).
