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
| 3 | `infected_r1b_parentchild.raw` | R1b | T1059.001 | #6 | #2 (T1059) |
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

**Rule primer:** R1b (parent-child abnormal). **MITRE:** T1059.001 — PowerShell.
**Q13 poin 6** (aplikasi dokumen meluncurkan cmd/PowerShell).

**Skenario (aktual):** dokumen/aplikasi kantor ber-makro men-spawn shell.
Karena victim tak punya MS Office, dipakai **LibreOffice** (`soffice.bin` ∈
`SUSPICIOUS_CHILD_SPAWNERS`). Makro LibreOffice Basic memanggil COM automation:
`CreateObject("WScript.Shell").Run("powershell -nop -ep bypass -File C:\Users\Public\p.ps1", 1, False)`.
Rantai proses aktual: **`soffice.bin → powershell.exe`** (langsung).

**Catatan teknis (kenapa WScript.Shell, bukan `Shell()`):** `Shell()` LibreOffice
bisa meluncurkan proses tanpa argumen (notepad OK) & lewat `cmd /c` (OK), tapi
**gagal meluncurkan `powershell.exe` langsung dengan argumen** — dibuktikan lewat
tes terkontrol (dengan `p.ps1` sudah di disk, tetap tak ada proses/koneksi).
`CreateObject("WScript.Shell")` di-load in-process ke `soffice.bin`, jadi `.Run`
memanggil `CreateProcess` dari dalam soffice → `powershell.exe` jadi **anak
langsung soffice.bin** (T1059.001 murni, tanpa perantara). Metode `cmd /c`
sebelumnya juga valid (rantai `soffice.bin → cmd.exe → powershell.exe`,
terdeteksi R1b via `soffice.bin → cmd.exe`) tapi versi langsung dipilih sebagai
final karena cocok desain awal.

**Payload:** `p.ps1` = **plain PowerShell TCP reverse shell** ke Kali
`192.168.70.131:4444` (BUKAN meterpreter — `psh-reflection` gagal connect;
reverse shell murni lebih andal & menjaga `powershell.exe` tetap hidup di loop).
Sinyal sukses = koneksi masuk di listener nc, BUKAN GET (p.ps1 lokal di disk).
Indikator R2/R3 muncul organik dari payload nyata (anti-circular-reasoning).

**Environment aktual:** victim 192.168.70.130 (Win10 22H2 19045.2965), Kali
192.168.70.131. Capture 2 Juli 2026 via DumpIt selagi C2 aktif. Dump 5 GB.

**Ground Truth (dikonfirmasi via reverse shell, `Get-CimInstance Win32_Process`):**
- `soffice.bin` **PID 9140** (PPID 11232) — spawner
- `powershell.exe` **PID 10120** (PPID 9140) — anak LANGSUNG soffice.bin, pemegang C2
- (proses PowerShell manual liar PID 4740 di-`Stop-Process` sebelum dump → dataset bersih)

**Hasil aktual analyzer (2 Juli 2026):**
- Plugin: pslist 168, pstree 8, netscan 107, malfind 245, dlllist 8353, handles 65137 — semua sukses.
- Total **169 PID | CLEAN 167 | SUSPICIOUS 2** | FP 0.
- **PID 9140 `soffice.bin` — R1=True (PRIMER):**
  `[Rule1] Spawn mencurigakan: 'soffice.bin' (PID=9140) -> 'powershell.exe' (PID=10120)`
- **PID 10120 `powershell.exe` — R2=True, R3=True (sekunder organik):**
  `[Rule2]` C2 ke `192.168.70.131:4444` (TCPv4, ESTABLISHED) +
  `[Rule3]` RWX (PAGE_EXECUTE_READWRITE) + PrivateMemory (5 segmen, .NET/shellcode).

**Verifikasi:**
- ✅ Target primer R1b tercapai: `soffice.bin` PID 9140 flag Rule1 dengan reason
  "Spawn mencurigakan", PID + anak LANGSUNG (powershell.exe 10120) cocok persis ground truth.
- ✅ Zero FP di 167 proses lain; hanya 2 SUSPICIOUS, keduanya bagian rantai yang
  ditanam → tidak ada proses liar sisa troubleshooting.
- ✅ Deteksi berlapis (R2/R3 pada powershell 10120) muncul organik dari reverse
  shell nyata, bukan ditanam.

**Lokasi dump:** `D:\forensic_triase\dataset_update\infected_r1b_parentchild.raw`
(versi langsung; versi cmd lama di-backup `infected_r1b_parentchild_cmd.raw` bila disimpan).

---

## 7. Dataset 4 — `infected_r2_network.raw`  [FINAL]

**Rule primer:** R2 (network). **MITRE:** T1071.001 — Application Layer Protocol.
**Q13 poin 4** (outbound ke host lain, port tak umum). **Prevalensi:** Picus Red
Report 2026 — T1071 #5 global.

**Skenario (aktual):** implant **C2 framework Sliver** (Bishop Fox) — BUKAN
meterpreter — dipilih justru karena implant Go native **tidak meninggalkan
segmen RWX**, sehingga R2 dapat diuji **terisolasi murni** (R3 tidak ikut
menyala). Implant mTLS di-generate di Kali, dijalankan di victim dengan tiga
lapis penyamaran agar HANYA R2 yang relevan:
- **Nama benign** `AtlasAgent.exe` (jauh dari nama proses sistem → R1a diam).
- **Path sah** `C:\Program Files\AtlasSync\` (→ R1-path & R4a diam; modul EXE
  utama tak kena keyword path — pelajaran dari temuan Dataset 2).
- **Diluncurkan via double-click Explorer** → parent `explorer.exe` (→ R1b
  parent-child diam).
Tanpa post-exploitation apa pun (tidak `shell`/`execute`/`migrate`) supaya tak
memunculkan RWX / proses anak yang merusak isolasi.

**Kenapa Sliver, bukan meterpreter:** meterpreter (reflective DLL) selalu
meninggalkan RWX+PrivateMemory → R3 ikut menyala (terbukti Dataset 2 & 3).
Implant Go Sliver memuat kode dari section `.text` image (RX, bukan RWX) → R3
tidak menyala. Ini memungkinkan pembuktian **nilai deteksi mandiri R2**: ancaman
C2 nyata kelas profesional yang LOLOS R1/R3/R4, tertangkap HANYA oleh R2.

**Environment aktual:** victim 192.168.70.130 (Win10 22H2 19045.2965), Kali
192.168.70.131, **host-only tanpa internet** (kritis: menghilangkan koneksi
telemetri sah yang bisa memicu R2-FP seperti `PaintStudio.Vi` di Dataset 1 — di
sini koneksi ESTABLISHED eksternal satu-satunya dijamin C2). VMnet host-only
tanpa DHCP → IP di-set statis (`.131` via nmcli di Kali, `.130` via netsh di
victim). Listener mTLS `:8443`. Capture 3 Juli 2026 via DumpIt selagi C2 aktif.
Dump 5 GB.

**Ground Truth (dikonfirmasi via `netstat -ano` + `tasklist` saat capture):**
- `AtlasAgent.exe` **PID 8732** (PPID 6052 = `explorer.exe`) — implant C2
- C2: `192.168.70.130:61575 → 192.168.70.131:8443` (TCPv4, ESTABLISHED)
- Path: `C:\Program Files\AtlasSync\AtlasAgent.exe`

**Hasil aktual analyzer (3 Juli 2026):**
- Plugin: pslist 154, pstree 7, netscan 114, malfind 7, dlllist 7247, handles 54765 — semua sukses.
- Total **154 PID | CLEAN 153 | SUSPICIOUS 1** | FP 0.
- **PID 8732 `AtlasAgent.exe` — R2=True (PRIMER), R1=R3=R4=False:**
  `[Rule2] Koneksi outbound abnormal: 'AtlasAgent.exe' -> 192.168.70.131:8443 (TCPv4, ESTABLISHED)`

**Verifikasi (isolasi R2 tercapai — tanpa fallback):**
- ✅ Target primer R2 tercapai; PID 8732 + ForeignAddr:Port cocok persis ground truth.
- ✅ **R1=R3=R4=False** → membuktikan R2 menangkap ancaman yang rule lain lewatkan
  (nilai deteksi mandiri). Gate R3 lolos: `AtlasAgent.exe` tak muncul di malfind
  sama sekali (Sliver Go implant zero RWX) — bukan sekadar tersupresi whitelist.
- ✅ malfind mengembalikan 7 record namun semuanya proses whitelist (`MsMpEng.exe`
  ×6 Defender, `smartscreen.ex` ×1) ∈ `LEGIT_RWX_PROCESSES` → R3 tersupresi benar.
- ✅ Zero FP di 153 proses lain (host-only → tanpa telemetri internet).

**Lokasi dump:** `D:\forensic_triase\dataset_update\infected_r2_network.raw`.
Hasil analyzer + JSON plugin: `results/r2_network/`.

---

## 8. Dataset 5 — `infected_r3_injection.raw`  [FINAL]

**Rule primer:** R3 (code injection). **MITRE:** T1055.001 — Process Injection:
DLL / Reflective DLL Injection. **Q13 poin 2** (proses legit disusupi kode asing).
**Prevalensi:** Picus Red Report 2026 — T1055 #1 global.

**Skenario (aktual):** kode **meterpreter reflective DLL** disuntik ke proses
**sah** `notepad.exe` lewat teknik `migrate`, meninggalkan segmen
`PAGE_EXECUTE_READWRITE` + `PrivateMemory=1` yang tertangkap `malfind`. Ini
KEBALIKAN Dataset 4: di sini artefak RWX-nya yang justru diuji. Tiga lapis agar
HANYA R3 yang relevan (isolasi R3 murni):
- **Proses target sah** `notepad.exe` — nama asli, path asli
  `C:\Windows\System32\notepad.exe`, dibuka manual via Explorer (parent
  `explorer.exe`) → R1a/R1-path/R1b diam. `notepad.exe` TIDAK ada di
  `LEGIT_RWX_PROCESSES` → R3 tetap menyala.
- **Koneksi C2 disenyapkan** sebelum capture via meterpreter `sleep 300` (socket
  ditutup, kode tetap resident) → netscan tak punya ESTABLISHED ke Kali → R2 diam.
- **Stager dibersihkan** — proses payload `AtlasHelper.exe` mati otomatis saat
  `migrate` → tak ada proses tambahan ber-path `\Temp\` yang memicu R1/R4.

**Kenapa meterpreter (kebalikan Dataset 4):** reflective DLL meterpreter SELALU
meninggalkan RWX+PrivateMemory — justru inilah artefak target uji R3. Dataset 4
(Sliver, zero RWX) membuktikan "C2 tanpa injeksi"; Dataset 5 membuktikan
pelengkapnya: "injeksi tanpa C2 aktif", tertangkap HANYA oleh R3.

**Environment aktual:** victim 192.168.70.130 (Win10 22H2 19045.2965), Kali
192.168.70.131, host-only tanpa internet, IP statis (nmcli/netsh). Defender
Real-time protection OFF (meterpreter mentah kena signature → `certutil` gagal
"Access is denied" saat Defender ON; sah sebagai prasyarat lab, setara MITRE
T1562.001 Impair Defenses; MsMpEng.exe tetap berjalan). Handler `multi/handler`
reverse_tcp `:4444`. Capture 5 Juli 2026 via DumpIt dalam jendela `sleep` (tanpa
ESTABLISHED). Dump 5 GB.

**Ground Truth (dikonfirmasi via meterpreter):**
- `notepad.exe` **PID 3404** (PPID 4944 = `explorer.exe`) — proses sah tersuntik
- 2 segmen RWX sisa reflective loader @ `0x22319910000` & `0x22319950000`
- Stager `AtlasHelper.exe` PID 8712 sudah mati saat `migrate` (tanpa noise)

**Hasil aktual analyzer (5 Juli 2026):**
- Plugin: pslist 147, pstree 5, netscan 53, malfind 20, dlllist 7473, handles 52206 — semua sukses.
- Total **147 PID | CLEAN 146 | SUSPICIOUS 1** | FP 0.
- **PID 3404 `notepad.exe` — R3=True (PRIMER), R1=R2=R4=False:**
  `[Rule3] Code injection: 'notepad.exe' punya segmen PAGE_EXECUTE_READWRITE + PrivateMemory di alamat 0x22319910000` (+ `0x22319950000`)

**Verifikasi (isolasi R3 tercapai):**
- ✅ Target primer R3 tercapai; PID 3404 + 2 segmen RWX cocok ground truth.
- ✅ **R1=R2=R4=False** → membuktikan R3 menangkap ancaman yang rule lain lewatkan
  (nilai deteksi mandiri): proses sah tanpa C2 aktif hanya terbongkar lewat
  artefak memori injeksinya.
- ✅ malfind mengembalikan 20 record, hanya 2 (notepad) yang diflag; 18 sisanya
  proses whitelist (`MsMpEng.exe` ×15 Defender, `SearchApp.exe` ×2,
  `smartscreen.ex` ×1) ∈ `LEGIT_RWX_PROCESSES` → R3 tersupresi benar, 0 FP.
- ✅ Defender Real-time OFF tak mematikan proses `MsMpEng.exe` → latar RWX
  realistis tetap ada (setara Dataset 4).

**Lokasi dump:** `D:\forensic_triase\dataset_update\infected_r3_injection.raw`.
Hasil analyzer + JSON plugin: `results/r3_injection/`.

---

## 9. Dataset 6 — `infected_r4a_dll.raw`  [FINAL]

**Rule primer:** R4a (DLL path). **MITRE:** T1574.001/002 — DLL Search-Order
Hijacking / Side-Loading (mekanisme muat via T1218.011 — rundll32, LOLBin).
**Q13 poin 3** (DLL dimuat dari path tidak wajar / library injection).
**Prevalensi:** Picus Red Report 2026 — T1574 Hijack Execution Flow, high-impact.

**Skenario (aktual):** sebuah **DLL benign** (`evil.dll`) ditanam di direktori
user-writable `C:\Users\Public\` lalu dimuat oleh **`rundll32.exe`** — binary
Windows asli bertanda-tangan dari `C:\Windows\System32`. Artefak forensiknya:
`windows.dlllist` untuk PID `rundll32` memuat modul `evil.dll` ber-`Path`
`C:\Users\Public\evil.dll` (mengandung keyword `\users\public\`) → R4a menyala.
Isolasi R4a murni dicapai dengan memisahkan **loader** dari **DLL**:
- **Loader = LOLBin sah** `rundll32.exe` jalan dari path sah `C:\Windows\System32\`
  → R1-path & R1-typosquat diam; induk `cmd.exe` (bukan `SUSPICIOUS_CHILD_SPAWNER`)
  → R1-parent diam. Memenuhi catatan desain (progress_log): R4a WAJIB diuji lewat
  **DLL sideload terpisah**, BUKAN EXE utama (yang akan memicu R1-path + R4a redundan).
- **DLL benign** (hanya `MessageBox`, tanpa shellcode/RWX/jaringan/akses LSASS) →
  R2/R3/R4b semua diam. Karena benign, **Defender boleh tetap ON** (beda dari
  Dataset 4 & 5) — teknik ini justru lebih senyap.

**Kenapa rundll32 (bukan side-loading klasik):** side-loading klasik menaruh EXE
sah + DLL jahat di folder writable yang sama → EXE-nya sendiri ber-path
mencurigakan → R1-path ikut menyala (redundan). Memakai `rundll32` sebagai loader
dari System32 membuat HANYA modul DLL yang ber-path mencurigakan → R4a teruji
independen. Artefak memori (modul termuat dari direktori writable) identik dengan
DLL side-loaded nyata.

**Environment aktual:** victim 192.168.70.130 (Win10 22H2 19045.2965), Kali
192.168.70.131, host-only tanpa internet, IP statis. **Defender Real-time
protection ON** (DLL benign, tak kena signature). `evil.dll` di-cross-compile di
Kali (`x86_64-w64-mingw32-gcc -shared`, 64-bit) lalu diunduh ke
`C:\Users\Public\`; dimuat via `rundll32.exe C:\Users\Public\evil.dll,Run`
(MessageBox menahan proses resident selama DumpIt). Capture 6 Juli 2026. Dump 5 GB.

**Ground Truth (dikonfirmasi via `tasklist`/`wmic`):**
- Proses pemuat: **`rundll32.exe` PID 8392** (PPID 1820 = `cmd.exe`) — LOLBin sah
- Modul jahat: `evil.dll` @ `C:\Users\Public\evil.dll`
- Tanpa C2, tanpa RWX pada rundll32, tanpa handle LSASS

**Hasil aktual analyzer (6 Juli 2026):**
- Plugin: pslist 159, pstree 11, netscan 96, malfind 17, dlllist 8629, handles 61105 — semua sukses.
- Total **160 PID | CLEAN 159 | SUSPICIOUS 1** | FP 0.
- **PID 8392 `rundll32.exe` — R4a=True (PRIMER), R1=R2=R3=False:**
  `[Rule4] DLL path mencurigakan: 'rundll32.exe' memuat 'evil.dll' dari 'C:\Users\Public\evil.dll' (mengandung '\users\public\')`

**Verifikasi (isolasi R4a tercapai):**
- ✅ Target primer R4a tercapai; PID 8392 + modul `evil.dll` cocok ground truth.
- ✅ **R1=R2=R3=False** → membuktikan R4a menangkap ancaman yang rule lain
  lewatkan: DLL dari path writable pada proses sistem sah hanya terbongkar lewat
  enumerasi modul (`dlllist`), bukan anomali proses/jaringan/injeksi.
- ✅ malfind 17 record SEMUA proses whitelist (`MsMpEng.exe` ×14, `SearchApp.exe`
  ×2, `smartscreen.ex` ×1 ∈ `LEGIT_RWX_PROCESSES`) → R3 tak menyala, 0 FP.

**Catatan spesifisitas (temuan capture pertama):** capture awal meninggalkan
jendela **PowerShell unduhan** (PID 9496, `Invoke-WebRequest`) tetap terbuka; CLR
.NET JIT/AMSI PowerShell membuat segmen RWX benign → **R3 false positive**.
`powershell.exe` sengaja TIDAK di-`LEGIT_RWX_PROCESSES` (target injeksi favorit
malware). Capture diulang setelah menutup PowerShell → FP hilang, isolasi murni.
Temuan ini relevan untuk Bab Keterbatasan/Spesifisitas (Rule 3 sensitif → potensi
FP pada PowerShell sah).

**Lokasi dump:** `D:\forensic_triase\dataset_update\infected_r4a_dll.raw`.
Hasil analyzer + JSON plugin: `results/r4a_dll/`.

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
