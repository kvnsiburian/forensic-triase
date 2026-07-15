# Konsep FINAL — Uji Skala Dump + Perbandingan Platform vs Manual

> Draf untuk direview Kevin. Menyatukan dua hal:
>  (A) uji skala: durasi analisis platform pada 3 ukuran dump (5/12/20 GB);
>  (B) perbandingan: waktu platform vs waktu kerja manual analis, di 3 ukuran.
> Menjawab masukan Abang (uji waktu analisis, malfind melambat di RAM besar).
> Aturan gaya: tanpa em dash, bahasa mudah.

---

## 0. Keputusan yang sudah dikunci

- Host 32 GB (terverifikasi). D: sisa 215 GB (cukup).
- 3 ukuran RAM: **5 / 12 / 20 GB**. Titik 5 GB pakai ulang
  `infected_r3_injection.raw` (sudah ada). Cuma 2 capture baru (12, 20 GB).
- Skenario 3 titik SAMA: **r3 injection** (meterpreter reflective DLL ->
  notepad.exe). Isolasi variabel: hanya ukuran yang berubah.
- Analis manual = **Kevin sendiri** (estimasi peneliti, disebut jujur di
  keterbatasan).
- Batas "waktu manual" = **sampai kesimpulan clean/suspicious** (termasuk baca
  output + cocokkan acuan + tulis simpulan). BUKAN cuma 6 perintah selesai.
- Perbandingan platform-vs-manual diukur di **ketiga ukuran** (5/12/20).

---

## 1. Dua pertanyaan penelitian yang dijawab

**A. Kesanggupan skala + karakterisasi durasi (untuk Abang):**
> Platform sanggup memproses dump s/d 20 GB? Bagaimana durasi berubah seiring
> ukuran? (khususnya malfind)

**B. Nilai otomasi platform (menjawab "cepat dari apa"):**
> Berapa waktu kerja analis yang dipangkas platform dibanding melakukan
> analisis yang sama secara manual, sampai memperoleh kesimpulan?

Klaim yang BOLEH ditarik:
- "Platform sanggup s/d 20 GB; durasi total naik seiring ukuran; malfind
  penyumbang terbesar." (A)
- "Platform memangkas waktu KERJA ANALIS dibanding cara manual; selisihnya
  melebar seiring ukuran dump." (B)

Klaim yang DILARANG:
- "Mesin platform lebih cepat dari Volatility3." (SALAH: mesinnya sama.)
- Menyeret angka multiprocessing 2,71x ke klaim laporan.

---

## 2. Konsep kunci: pisahkan waktu MESIN vs waktu MANUSIA

Setiap analisis punya 2 komponen:

**Bagian 1 - Waktu mesin (Volatility3 berjalan).**
SAMA di manual & platform. Vol3 memindai dump butuh waktu X, entah dipanggil
tangan atau platform. Ini BUKAN keunggulan platform. Diakui jujur sama.

**Bagian 2 - Waktu manusia (analisis + interpretasi).**
Di sinilah platform menang. Manual mengharuskan analis:
baca pslist/pstree/netscan/malfind/dlllist/handles (dlllist ribuan baris,
handles puluhan ribu baris) -> cocokkan dgn acuan -> simpulkan proses mana
mencurigakan -> susun tabel. Platform mengerjakan Bagian 2 otomatis ~nol.

Makin besar dump -> Bagian 2 (baca manual) makin lama -> keunggulan platform
makin besar. Inilah yang menyambungkan uji skala (A) dengan perbandingan (B):
gap platform-vs-manual DIHARAPKAN melebar dari 5 GB ke 20 GB.

---

## 3. Desain eksperimen

**Variabel bebas:** ukuran dump (5/12/20 GB). **Yang dikunci:** skenario
(r3 injection identik), build OS, kode/analyzer (dibekukan), laptop pengukur,
mode BERURUTAN (bukan paralel, biar angka bersih).

| Titik | RAM | Sumber dump | Isi |
|---|---|---|---|
| 1 | 5 GB | `infected_r3_injection.raw` (ADA) | r3 injection |
| 2 | 12 GB | capture baru `_12gb.raw` | r3 injection (sama) |
| 3 | 20 GB | capture baru `_20gb.raw` | r3 injection (sama) |

Kenapa r3: sekalian buktikan deteksi R3 tetap TP di 5/12/20 (aturan tak jebol
saat dump besar). Kenapa 3 bukan 18: durasi ditentukan ukuran, bukan jenis
ancaman; 18 dump = mengukur variabel sama berulang + mencampur dua variabel.

---

## 4. Cara mengukur (per dump, 3 ukuran)

### 4a. Waktu PLATFORM
Stopwatch dari klik "Mulai Analisis" (atau start CLI) sampai vonis
clean/suspicious + Excel keluar. Sudah mencakup vol3 + analisis + export.
Idealnya diambil dari timer internal (lihat §5), bukan stopwatch tangan.

### 4b. Waktu MANUAL (Kevin sendiri)
Stopwatch dari mulai mengetik perintah vol3 pertama SAMPAI selesai menuliskan
kesimpulan "PID X suspicious karena Y". WAJIB:
- Benar-benar menjalankan 6 plugin vol3 satu per satu (BERURUTAN).
- Benar-benar MEMBACA output dan menyisir mencari indikator (jangan menyontek
  hasil platform - itu membuat angka palsu & merobohkan seluruh perbandingan).
- Cocokkan dgn acuan (cheat sheet SANS/daftar proses sah) selayaknya analis.
- Tulis kesimpulan per proses.

### 4c. Catatan bias (WAJIB masuk keterbatasan)
Kevin sudah tahu ground truth (menanam malware sendiri) -> saat manual akan
tak sadar terlalu cepat (loncat ke notepad.exe terinjeksi tanpa menyisir semua).
Ini MENGUNTUNGKAN sisi manual (manual terlihat lebih cepat dari nyata). Maka
kalau platform TETAP menang, klaim makin kuat. Framing:
> "Waktu manual kemungkinan lebih singkat dari kondisi nyata karena peneliti
> sudah mengetahui ground truth; artinya keunggulan platform di dunia nyata
> kemungkinan lebih besar lagi."

---

## 5. Yang perlu ditambahkan ke KODE (kecil, aman)

CLI belum mencatat durasi. Rencana (tidak menyentuh logika deteksi):
1. `core/runner.py` jalur BERURUTAN: `time.perf_counter()` sebelum/sesudah tiap
   plugin -> `{plugin: durasi_detik}`.
2. `main.py` mode CLI: cetak tabel durasi per-plugin + total, tulis ke
   `<dump>_timing.csv`.
3. Tidak menyentuh GUI, jalur paralel, analyzer.
4. **WAJIB** jalankan `regression_test.py` sesudahnya: TP=7/FP=1/FN=0 tak boleh
   berubah (timer tak boleh menyentuh hasil).

Ini memberi durasi PER-PLUGIN (penting: Abang menyoroti malfind). Timer platform
(§4a) juga bisa diambil dari total instrumentasi ini, lebih presisi dari
stopwatch tangan.

Untuk waktu manual (§4b): pakai stopwatch/HP, dicatat manual di tabel. Tidak ada
kode untuk ini (memang kerja manusia).

---

## 6. Prosedur lab (capture baru: 12 GB & 20 GB)

Per ukuran baru:
1. Restore snapshot bersih (Win10 22H2 19045.2965).
2. Matikan VM, set RAM VM ke target (12, lalu 20 GB).
3. Putus internet (host-only). Kali attacker host-only.
4. Reproduksi r3: msfvenom meterpreter reflective DLL -> migrate/inject ke
   `notepad.exe`. Pastikan injeksi terbentuk di memori (sesi meterpreter aktif).
5. Buka aktivitas latar yang mirip titik 5 GB.
6. Akuisisi DumpIt (Administrator) selagi injeksi aktif ->
   `infected_r3_injection_12gb.raw` / `_20gb.raw`.
7. Catat ground truth (`tasklist`): PID notepad.exe terinjeksi.
8. Salin ke `D:\forensic_triase\dataset_update\`. Buang snapshot terinfeksi.

---

## 7. Prosedur ukur (di laptop yang sama, kondisi seragam)

Untuk tiap dump (5, 12, 20 GB), berurutan:
- Jalankan **platform** (mode berurutan), catat durasi per-plugin + total (§5)
  dan waktu platform total (§4a).
- Jalankan **manual** (§4b), catat waktu manual total dengan stopwatch.

Kondisi seragam: laptop sama, tak ada beban berat lain, mode berurutan, ISF
simbol sudah ter-cache (pemanasan dulu biar unduh simbol tak mengotori titik
pertama). Idealnya ukur 2-3x, ambil median (kurangi noise). Realistis 5 hari:
minimal platform diukur rapi; manual boleh 1x (sebut sbg estimasi).

---

## 8. Bentuk tabel hasil

**Tabel A - Durasi platform per-plugin vs ukuran (detik):**

| Plugin | 5 GB | 12 GB | 20 GB |
|---|---|---|---|
| pslist | | | |
| pstree | | | |
| netscan | | | |
| malfind | | | |  <- disorot, diharapkan naik tertajam |
| dlllist | | | |
| handles | | | |
| **Total platform** | | | |

**Tabel B - Platform vs Manual (menit):**

| Ukuran | Waktu platform | Waktu manual (peneliti) | Selisih | Deteksi R3 |
|---|---|---|---|---|
| 5 GB | | | | TP |
| 12 GB | | | | TP |
| 20 GB | | | | TP |

Klaim dari Tabel B: selisih (waktu manual - platform) melebar seiring ukuran
-> nilai otomasi makin terasa pada dump besar. Deteksi R3 tetap TP di ketiganya
-> akurasi stabil terhadap ukuran.

---

## 9. Narasi laporan (arah)

- **Metodologi:** desain isolasi variabel (1 skenario, 3 ukuran, kenapa 3 bukan
  18). Definisi waktu platform vs manual. Sebut analis = peneliti + bias
  ground-truth (§4c) sebagai keterbatasan sejak awal.
- **Hasil:** Tabel A (durasi platform, malfind menonjol) + Tabel B (platform vs
  manual, gap melebar). Deteksi R3 stabil TP.
- **Pembahasan:** platform hemat waktu KERJA ANALIS (Bagian 2), bukan waktu
  mesin (Bagian 1, diakui sama). Makin besar dump makin terasa. Akui malfind
  melambat -> sambung ke Saran BAB VI (batas waktu per-plugin, pilih plugin).
- **Keterbatasan (WAJIB, biar tak diserang):** (1) analis = peneliti tunggal,
  tahu ground truth -> manual bias cepat; (2) manual sangat bergantung skill,
  satu angka tak wakili semua; (3) pengukuran terbatas (idealnya banyak
  orang/ulang). Justru pengakuan ini memperkuat kredibilitas.
- **DILARANG:** "mesin lebih cepat", "mempercepat", angka 2,71x.

---

## 10. Risiko & prioritas (jujur)

- **UAT tetap prioritas #1.** Ini kerja tambahan, bukan blocker lulus. Kalau
  bentrok waktu, UAT menang.
- **Manual di 20 GB melelahkan** (baca puluhan ribu baris sungguhan). Kalau tak
  sanggup, turunkan ke manual 5 & 12 saja (platform tetap 3 titik). Sudah
  disepakati coba ketiganya dulu.
- **Analisis 20 GB ~40+ menit** sekali jalan (malfind bisa lebih parah dari
  linear). Bisa dijalankan background.
- **Capture & reproduksi r3** harus benar (injeksi terbentuk saat capture).
  Ikuti prosedur r3 lama yang sudah terbukti.
- **Timer tak boleh ubah deteksi** -> regression_test.py wajib.

---

## 11. Keputusan tersisa dari Kevin

1. Setuju tambah instrumentasi timer per-plugin di CLI sekarang (bisa saya
   kerjakan tanpa menunggu lab)? Ini yang paling siap dikerjakan hari ini.
2. Penamaan `infected_r3_injection_12gb.raw` / `_20gb.raw` -> oke?
3. Slot lab kapan (setelah UAT)?
