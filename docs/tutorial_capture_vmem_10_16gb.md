# Tutorial Capture RAM via .vmem (suspend VM) — 10 & 16 GB

> Pengganti metode DumpIt untuk uji skala, setelah DumpIt terbukti GAGAL pada
> dump besar (12 & 20 GB rusak, 10 Juli). Metode ini mengambil RAM dari VM yang
> di-PAUSE, jadi snapshot memori KONSISTEN sempurna (OS tak sedang mengubah RAM
> saat direkam). Jauh lebih cepat: tak perlu DumpIt menulis belasan GB.
>
> Target uji skala (revisi 10 Juli): **5 / 10 / 16 GB**. Titik 5 GB tetap pakai
> dump DumpIt lama (`infected_r3_injection.raw`, sudah terukur). Yang di-capture
> via .vmem: **10 GB & 16 GB**.
>
> Kapasitas host terverifikasi: RAM fisik 31,7 GB -> VM 16 GB menyisakan ~15,7
> GB untuk host = aman. Disk D: sisa 165 GB = lega. Saat jalankan VM 16 GB,
> tutup aplikasi berat host (mis. `wsl --shutdown` bila tak sedang analisis).

---

## Kenapa .vmem, bukan DumpIt (untuk catatan metodologi)

DumpIt = live acquisition: baca RAM sambil OS jalan. Untuk dump besar,
penulisan belasan GB butuh lama -> OS keburu mengubah/memetakan ulang halaman
memori -> tabel halaman (DTB) yang direkam di awal tak cocok dengan isi RAM yang
direkam belakangan -> Volatility3 tersesat saat translasi alamat.

**Bukti kegagalan 12 GB (10 Juli):** dump berisi data (83 proses via psscan,
186/400 blok padat) TAPI ~47% halaman notepad hilang -> pslist putus di 24
proses, malfind 0 segmen, R3 tak menyala. Akar: inkonsistensi live-capture,
bukan file kosong.

`.vmem` = seluruh RAM VM pada SATU titik beku (VM di-suspend/snapshot). Tak ada
perubahan saat direkam -> DTB dan isi RAM konsisten -> Volatility3 membaca
bersih. Volatility3 mendukung format ini secara native (dibaca sama seperti
.raw).

**Keterbatasan yang WAJIB ditulis jujur di skripsi:**
> Titik 5 GB memakai akuisisi DumpIt (live, di dalam guest), sedangkan titik 8
> dan 12 GB memakai berkas .vmem (RAM VM yang di-suspend). Perbedaan metode ini
> diperlukan karena DumpIt tidak sanggup menghasilkan dump besar yang konsisten.
> Kedua metode menghasilkan flat memory image yang dibaca Volatility3 dengan
> cara setara, sehingga durasi analisis tetap sebanding.

---

## Lokasi file (sudah dikonfirmasi bisa diakses dari WSL)

Folder VM victim: `/mnt/d/VMWare/Windows 10 - Forensic/`
File .vmem muncul di sini saat VM di-suspend atau di-snapshot-with-memory.
Ukuran .vmem = RAM VM saat itu (contoh: RAM 8 GB -> .vmem ~8 GiB).

**Tidak perlu menyalin .vmem ke `dataset_update/`** — Volatility3 bisa baca
langsung dari folder VM. (Boleh disalin kalau mau arsip, tapi opsional.)

---

## Parameter r3 injection (TETAP SAMA seperti Dataset 5 / DumpIt)

Yang berubah HANYA cara akuisisi (suspend, bukan DumpIt) dan RAM VM. Reproduksi
injeksi tetap identik:
- Payload meterpreter reflective DLL -> migrate ke `notepad.exe` (dibuka via
  Explorer, parent explorer.exe).
- `sleep 300` untuk menutup socket C2 (R2 diam).
- Defender Real-time OFF. Host-only, IP statis .130/.131.

---

## Prosedur per ukuran (ulangi: 10 GB, lalu 16 GB)

### A. Siapkan VM
- [ ] **A1.** Restore snapshot `clean-base-attack-hostonly`.
- [ ] **A2.** Shutdown VM penuh. Set RAM ke target: **10240 MB (10 GB)** /
      **16384 MB (16 GB)**.
- [ ] **A3.** Nyalakan VM. Cek `ipconfig` = 192.168.70.130. Ping Kali .131.
- [ ] **A4.** Konfirmasi Defender Real-time OFF.

### B. Reproduksi injeksi r3 (SAMA seperti tutorial DumpIt)
- [ ] **B1.** Kali: payload `msfvenom ... -o /tmp/AtlasHelper.exe`, `chmod 644`,
      `python3 -m http.server 8000`, handler `multi/handler` (LHOST .131 :4444).
- [ ] **B2.** Victim: buka notepad via Explorer. Catat PID (`tasklist | findstr
      notepad`).
- [ ] **B3.** Victim: `certutil` unduh AtlasHelper.exe -> jalankan -> sesi
      meterpreter terbuka.
- [ ] **B4.** Kali meterpreter: `sessions -i 1` -> `migrate <PID notepad>` ->
      `getpid` konfirmasi -> **`Migration completed successfully`**.
- [ ] **B5.** Kali: `sleep 300` (socket C2 tertutup).

### C. AKUISISI via suspend (INI YANG BEDA — pengganti DumpIt)
- [ ] **C1.** Catat ground truth DULU (sebelum suspend): di victim `tasklist |
      findstr notepad` -> catat PID notepad + PPID explorer.exe.
- [ ] **C2.** Di VMware, SELAGI injeksi resident (dalam jendela sleep):
      **VM > Power > Suspend** (atau tombol Suspend / Ctrl+Alt tergantung versi).
      VMware akan menulis file `.vmem` di folder VM. Tunggu suspend selesai
      (VM jadi status Suspended).
- [ ] **C3.** File `.vmem` sekarang ada di
      `/mnt/d/VMWare/Windows 10 - Forensic/Windows 10 - Forensic.vmem`
      (saat suspend, biasanya nama tanpa akhiran Snapshot). Ukuran ~8/12 GiB.

> **Alternatif snapshot (kalau mau simpan state):** VM > Snapshot > Take
> Snapshot, PASTIKAN opsi "Snapshot the virtual machine's memory" tercentang.
> Ini menghasilkan `...-SnapshotN.vmem`. Suspend lebih simpel untuk uji ini.

### D. Verifikasi & beri nama
- [ ] **D1.** Dari WSL, cek dump SEHAT (langkah kritis — pengganti verifikasi
      lab):
      ```
      vol -f "/mnt/d/VMWare/Windows 10 - Forensic/Windows 10 - Forensic.vmem" windows.pslist 2>/dev/null | tail -n +2 | wc -l
      ```
      Harus **>= 120 proses** (bukan 24 seperti dump DumpIt rusak).
- [ ] **D2.** Cek notepad ada:
      ```
      vol -f ".../Windows 10 - Forensic.vmem" windows.pslist 2>/dev/null | grep -i notepad
      ```
      PID harus cocok ground truth C1.
- [ ] **D3.** Salin + beri nama jelas (opsional tapi disarankan, biar tak
      tertimpa saat resume VM):
      ```
      cp "/mnt/d/VMWare/Windows 10 - Forensic/Windows 10 - Forensic.vmem" \
         /mnt/d/forensic_triase/dataset_update/infected_r3_injection_10gb.vmem
      ```
      (ganti `_10gb` / `_16gb` sesuai ukuran)

> ⚠️ **PENTING:** kalau kamu **resume** VM lalu suspend lagi, file `.vmem` akan
> DITIMPA. Maka SALIN dulu (D3) sebelum resume, atau langsung ukur timing (TAHAP
> E) sebelum menyentuh VM lagi.

### E. Jalankan timing (mode berurutan)
- [ ] **E1.**
      ```
      cd /home/kevin/forensic_triase/platform
      python3 main.py /mnt/d/forensic_triase/dataset_update/infected_r3_injection_10gb.vmem --timing
      ```
- [ ] **E2.** Cek deteksi: **notepad -> SUSPICIOUS, R3=Y** (TP). Ambil TOTAL +
      malfind dari terminal + `<dump>_timing.csv`.

---

## Titik data (target revisi 5 / 10 / 16 GB)

| Titik | Ukuran | Metode | Status |
|---|---|---|---|
| 1 | 5 GB | DumpIt (`infected_r3_injection.raw`) | ✅ TOTAL 328,57 / malfind 134,47 |
| 2 | 10 GB | .vmem suspend | ⏳ capture |
| 3 | 16 GB | .vmem suspend | ⏳ capture |

---

## Kenapa ini menyelesaikan masalah 10 Juli

- Tak ada live-capture lama -> tak ada inkonsistensi DTB vs isi RAM.
- Suspend = beku sesaat -> semua halaman konsisten -> pslist/malfind/handles
  jalan penuh -> R3 menyala (TP).
- Gratis waktu: suspend jauh lebih cepat dari DumpIt menulis belasan GB.
- File langsung terbaca dari folder VM (sudah dikonfirmasi akses WSL).
