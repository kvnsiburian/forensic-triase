# Catatan Diskusi Revisi — Masukan Analis LFD (Abang) → Rencana Bimbingan Pak Rahmat

> **Dokumen hidup.** Diperbarui terus seiring diskusi Kevin ↔ Claude.
> Tujuan akhir: menyiapkan bahan bimbingan Pak Rahmat (rencana besok, setelah 9 Juli 2026)
> dan memastikan revisi selesai sebelum **batas pengumpulan dokumen: 15 Juli 2026**.

Terakhir diperbarui: 9 Juli 2026.

---

## 0. Konteks & batasan waktu (paling menentukan)

- **Hari ini: 9 Juli 2026. Kumpul dokumen: 15 Juli 2026 → sisa ± 6 hari.**
- Prinsip pengambilan keputusan: **lindungi timeline.** Apa pun yang mengguncang desain
  final (6 plugin / 6 aturan / 4 kelompok SANS / 7 dataset) atau menuntut **validasi ulang**
  adalah **berisiko** dan default-nya **ditolak untuk siklus ini** → jadikan Saran BAB VI.
- Framing efisiensi TA (dikonfirmasi Kevin): **"efisiensi waktu analis / alur kerja"**,
  BUKAN kecepatan mesin. Kata **"mempercepat" sudah dihapus** dari laporan.
  → Konsekuensi: **tidak menambah pengujian kecepatan mesin** (lihat §2).

---

## 1. Ringkasan 11 poin masukan Abang (analis LFD)

**Pengujian kecepatan:**
1. Tujuan = efisiensi → uji **waktu analisis**, bukan hanya akurasi.
2. Buat **3 dataset beda ukuran** (perbesar RAM saat dump), pakai **timer** → **tabel waktu**.
3. **malfind lambat**; makin besar RAM makin lama → harus "diakali".

**Saran fitur:**
4. Tambah **CUDA (GPU) + multiprocessing**; trade-off = portabilitas (Ubuntu / non-GPU) →
   solusi: **opsi di GUI** (checklist CUDA/biasa, dropdown jumlah core).
5. **Dump bersih harus tetap ekspor Excel** (dugaan Abang: output hanya untuk suspicious).
6. Output masih ke **/mnt/d** — bisakah langsung ke **disk lokal D:/C:**?

**Dataset & sidang:**
7. Kendala membuat dataset RAM → masukkan ke **batasan masalah** + **narasi kredibilitas
   dataset** + **konfirmasi ke Pak Rahmat** agar bisa dibela ke penguji.

**Dari transkrip (wawasan terdalam):**
8. Kasus nyata LFD: sering hanya dapat IP/koneksi C2 (jika masih running) atau file scan
   menemukan encryptor ransomware yang **sudah tidak ada** → malfind/pslist/pstree **sering
   tidak menghasilkan apa-apa** di kasus nyata.
9. 6 plugin cukup? **Tergantung tujuan:** target "masih berjalan" → cukup; target "pernah
   dijalankan (past execution)" → kurang, perlu plugin tambahan (**shimcache**, file scan, registry).
10. Shimcache deteksi **berdasarkan nama** → butuh **wordlist nama file malicious**.
11. Sumber wordlist: **MITRE** (data JSON APT→malware; Abang akan kirim nama reponya),
    ekstrak nama malware, grep `.exe`.

---

## 2. Triase keputusan atas masukan Abang (di bawah tenggat 6 hari)

| Masukan | Keputusan | Alasan |
|---|---|---|
| Uji kecepatan (3 dataset ukuran, timer) | **JANGAN sekarang → Saran** | Bertabrakan dengan framing "waktu analis"; menghidupkan lagi klaim "mempercepat" yang sudah dihapus; malfind jadi liabilitas; butuh dataset+bab baru dalam 6 hari |
| CUDA + multiprocessing + dropdown core | **Saran (future work)** | Perubahan kode besar, risiko portabilitas; CUDA untuk vol3 diragukan manfaatnya |
| Shimcache + wordlist MITRE (past execution) | **Saran (unggulan)** | Plugin+logika+dataset+validasi ulang = mustahil aman dalam 6 hari; emas sebagai Saran |
| Dump bersih tetap ekspor Excel | **TIDAK PERLU** (bukan bug) | Sudah terbukti dari kode (lihat §4) |
| Output ke D:/C: lokal | **Sudah teratasi** (tombol Export = folder picker) | Hanya path *default* auto-export yang hardcoded; tidak wajib diubah untuk demo |
| Batasan masalah + narasi kredibilitas dataset | **WAJIB tulis** | Harus ada; di sinilah wawasan Abang jadi emas (lihat §5) |

**Inti:** dari seluruh masukan, **tidak ada** yang wajib masuk kode sekarang. Yang wajib =
**dokumentasi** (batasan masalah + Saran) + jalur kritis (UAT + penulisan bab).

---

## 3. Dua wawasan strategis

**W1 — Dua makna "efisien".** Abang menafsirkan efisien = kecepatan mesin. TA Kevin =
efisiensi **alur kerja/waktu analis** (sudah dibuktikan lewat **UAT**, bukan stopwatch).
Menambah tabel waktu mesin justru memancing pertanyaan penguji "lebih cepat dari apa?".

**W2 — Ini soal SCOPE, bukan kurang plugin.** 6 plugin membaca **keadaan live/aktif**.
Menegaskan lingkup ini secara jujur (batasan masalah + Saran) **mengubah "kelemahan" jadi
bukti paham realita operasional** — justru mengesankan penguji.

---

## 4. Hasil verifikasi kode (9 Juli)

**(a) Dump bersih TETAP mengekspor Excel — bukan bug.**
- `main.py:129` **selalu** memanggil `export_all(...)` tiap analisis selesai, tanpa syarat suspicious.
- Tombol Export (`gui/app.py:780`) aktif berdasarkan *analisis sudah jalan*, bukan jumlah suspicious.
- Dump bersih → tetap dapat `results.xlsx` (7 sheet, semua PID CLEAN) + `summary.xlsx` (Suspicious=0).
- Sumber kesalahpahaman Abang: dump bersih tak punya baris oranye/merah → *terlihat* kosong,
  padahal file Excel tetap ditulis. **Tidak ada yang diperbaiki.**

**(b) Hasil sama di laptop lain — YA (deterministik).**
- Volatility3 membaca berkas dump tetap (bukan keadaan host) + analyzer.py logika deterministik
  → TP=7, FP=1, dst. **identik** di laptop mana pun.
- Syarat sama: (1) versi Volatility3 v2.28.1, (2) tabel simbol (ISF) tersedia, (3) kode/whitelist sama.
- Yang BEDA antar-laptop: **durasi** (hardware) & **lokasi simpan** (`/mnt/d` hanya ada bila WSL+drive D:).
- Tombol Export sudah pakai folder picker (`gui/app.py:691`) → penyimpanan ke C:/D: **sudah teratasi**.
- Determinisme ini **memperkuat validitas** hasil validasi TA.

---

## 5. Bahan batasan masalah + Saran (draf, siap dipoles)

**Batasan masalah — Lapisan 1 (sifat dasar bukti):**
> Analisis forensik memori bekerja pada snapshot RAM pada satu titik waktu. Proses yang telah
> terminasi dan strukturnya telah direklamasi sistem sebelum akuisisi berada di luar jangkauan
> semua alat berbasis daftar proses aktif — keterbatasan inheren bukti, bukan platform semata.

**Batasan masalah — Lapisan 2 (ruang lingkup):**
> Platform difokuskan pada triase proses yang aktif/hadir dalam daftar proses aktif saat
> akuisisi. Pemulihan proses terminasi/tersembunyi via pool scanning (mis. `windows.psscan`)
> serta analisis artefak riwayat eksekusi (mis. shimcache) tidak termasuk ruang lingkup.

**Saran BAB VI:**
> Menambahkan `windows.psscan` untuk memulihkan proses terminasi/tersembunyi, serta analisis
> artefak riwayat eksekusi (shimcache/amcache), agar platform menjangkau proses yang tidak lagi
> aktif namun pernah dijalankan. (Sejalan masukan analis LFD: past-execution.)

**Cara menjawab penguji (fakta akurat):** pslist/pstree hanya daftar proses **aktif**; proses
terminasi dipulihkan lewat **pool scanning** (`windows.psscan`) — itu di luar cakupan.
JANGAN klaim pslist menangkap semua proses (keliru & mudah dipatahkan).

**Tiga lapisan "proses yang pernah ada":**
1. Masih aktif → pslist/pstree ✅ (platform saat ini)
2. Baru mati, struktur masih di RAM → `psscan` (pool scan) — belum ada
3. Sudah hilang dari RAM, tapi ada jejak → shimcache/amcache (registry) — belum ada (maksud Abang)

---

## 6. Diskusi lingkungan (portabilitas)

- Demo sidang: **di laptop WSL Kevin sendiri** → `/mnt/d` = drive D: Windows → **aman, tak perlu diubah**.
- Laptop lain: hasil deteksi tetap sama (deterministik, §4b); yang rapuh hanya **path default**
  auto-export bila laptop tanpa drive D:. Perbaikan opsional (aman, jika sempat): ganti path
  default ke lokasi yang selalu ada. **Bukan keharusan sidang.**

---

## 7. Jalur kritis 6 hari (JANGAN tergeser oleh masukan fitur)

1. **Jalankan UAT 7 responden** (blocker BAB V.3 & BAB VI) — pakai `docs/uat_kuesioner_platform.md`.
2. Tulis **V.3 (hasil UAT)** + **BAB VI (Kesimpulan & Saran)** + kalimat UAT di 2 abstrak.
3. Tulis **batasan masalah + narasi kredibilitas dataset** (§5).
4. **2 screenshot GUI** tertunda (R1b soffice.bin, R4b mimikatz).

---

## 8. Untuk bimbingan Pak Rahmat (bawa sebagai OPSI, bukan keputusan)

- Sampaikan masukan Abang; usulkan **memuliakannya sebagai batasan masalah + Saran**, bukan fitur baru.
- **Siapkan diri:** Pak Rahmat kemungkinan **tidak ingin** menambah scope 6 hari sebelum kumpul
  (beliau yang membekukan desain & mengarahkan framing "waktu analis"). Datang dengan pertanyaan,
  bukan asumsi "pasti setuju".
- (Catatan bimbingan lengkap disusun **setelah** diskusi Kevin↔Claude selesai — sesuai permintaan Kevin.)

---

## 9. Item terbuka / menunggu

- [ ] Poin diskusi lanjutan Kevin (akan ditambah di bawah seiring diskusi).
- [ ] Nama repo/JSON MITRE dari Abang (untuk referensi Saran wordlist).
- [ ] Keputusan final Pak Rahmat atas scope (setelah bimbingan).
- [ ] Isi angka UAT ke Kesimpulan c (setelah UAT 7 responden jalan).
- [ ] Tambah pembatasan masalah I.3 poin (e): live-state vs past-execution (§5).

**>> TARGET BERIKUTNYA (ingatkan Kevin setelah tugas modifikasi fitur selesai):**
- [ ] **Kerangka V.3 (UAT)** supaya begitu UAT jalan tinggal isi angka.
- [ ] **Paragraf pembatasan masalah I.3 (e)** soal live-state (tulis dengan aturan gaya baru: tanpa em dash, bahasa mudah).

---

## 10. Draf BAB VI (disepakati 9 Juli — prosa gaya Fransiska)

**Keputusan format:** paragraf mengalir (BUKAN butir a/b/c). Kesimpulan = 3 paragraf
memetakan rumusan masalah a/b/c (validasi dilipat ke paragraf b). Saran = prosa, 5 arah (a–e).
**Angka terverifikasi via regression_test.py (9 Juli):** 1.127 proses, TP=7, FP=1, FN=0,
TN=1.119 → Recall 100%, Accuracy 99,91%, FPR 0,09%, Precision 87,5%.
⚠️ JANGAN tiru framing "lebih cepat" Fransiska (kecepatan mesin) — kita klaim efisiensi alur kerja.

### VI.1 KESIMPULAN
- **Par.1 (RM-a):** platform berhasil dibangun; otomatisasi alur utuh (load dump → 6 plugin →
  6 aturan/4 kelompok SANS → klasifikasi clean/suspicious + rekomendasi → ekspor Excel);
  8 kebutuhan fungsional (F01–F08) terpenuhi & lolos pengujian fungsional.
- **Par.2 (RM-b + validasi):** SANS Memory Forensics dipetakan ke 4 kelompok indikator →
  6 aturan (R1a–R4b) di analyzer.py; terbukti efektif: Recall 100%, Accuracy 99,91%, FPR 0,09%
  atas 1.127 proses / 7 skenario; Recall sempurna + hanya 1 FP (prioritas minim ancaman terlewat).
- **Par.3 (RM-c) — PLACEHOLDER UAT:** penerimaan pengguna via UAT 7 responden Tim LFD BSSN →
  penerimaan **[X]%** → kategori **[Diterima]** (Tabel 3.1). *(isi setelah UAT jalan)*

### VI.2 SARAN (prosa, 5 arah)
a. `windows.psscan` (pool scanning) + artefak riwayat eksekusi (shimcache/amcache) → jangkau
   proses tidak-aktif-tapi-pernah-jalan. *(inti Abang: past-execution)*
b. Perkaya deteksi dengan wordlist nama malware dari threat intel terbuka (MITRE ATT&CK). *(Abang)*
c. Dukungan dump besar (versi AMAN, mengganti multiprocessing): (1) pengguna bisa memilih
   plugin yang dijalankan untuk pemeriksaan cepat; (2) batas waktu tiap plugin menyesuaikan
   ukuran dump. Alasan buang multiprocessing: risiko output tidak lengkap karena rebutan RAM
   (paling parah justru di dump besar), dan regression tidak menjalankan runner sehingga tak
   bisa memverifikasinya. Kedua ide baru tidak mengubah hasil deteksi dataset 2 GB.
d. Deteksi fileless malware (menyambung pembatasan I.3.d).
e. Portabilitas lintas OS / pemaketan di luar WSL (Windows asli / Linux lain).

> Teks prosa lengkap siap-tempel ada di jawaban Claude (sesi 9 Juli), dengan italic ditandai.
> **Versi final:** sudah direvisi tanpa em dash, kalimat pendek & mudah (aturan gaya baru Kevin:
> NO em dash, bahasa mudah, hindari istilah aneh agar terlihat diketik sendiri).
> Status: menunggu konfirmasi akhir Kevin.

---

## 11. Fitur Multiprocessing (DIIMPLEMENTASIKAN 9 Juli, membalik keputusan §10c)

**Perubahan keputusan:** Kevin memutuskan multiprocessing **tetap dibuat** sebagai fitur
opsional (bukan hanya Saran). Argumennya: dibuat centang, default mati, jadi risikonya
opt-in dan tidak memaksa. Desain final: **satu kotak centang "Gunakan multiprocessing"**,
default mati, tanpa dropdown. Kalau nyala, keenam plugin jalan paralel; kalau ada plugin
gagal, ada **notifikasi + jalankan-ulang otomatis** (pilihan nomor 2 Kevin) agar output tetap lengkap.

**Kode yang diubah (semua terverifikasi, jalur berurutan TIDAK disentuh):**
- `core/runner.py`: method baru `run_all_parallel()` (ThreadPoolExecutor, worker auto = min(6, cpu), pengaman re-run plugin gagal (None), hasil kosong [] tidak diulang).
- `main.py`: param `use_parallel` (default False) + cabang paralel; bawa `reran_plugins` ke hasil.
- `gui/app.py`: kotak centang di baris sendiri (default mati), salurkan `use_parallel`, notifikasi bila ada plugin diulang, nonaktif saat berjalan. Perbaikan tampilan: border sorot & garis putih progress bar dihilangkan.

**Hasil uji manual (bukti output aman, karena regression TIDAK menguji runner):**
- `clean_baseline`: berurutan 574 dtk (9,6 mnt) vs paralel 212 dtk (3,5 mnt) = **2,71x**.
  Output **SAMA PERSIS** (6 plugin + klasifikasi identik), 0 plugin gagal, 0 re-run.
- `infected_r3_injection`: sedang diuji (memastikan deteksi malfind selamat saat paralel).

⚠️ Angka percepatan (2,71x) **JANGAN masuk klaim laporan** (kita klaim efisiensi alur kerja,
bukan kecepatan mesin). Fitur ini murni untuk pemakaian nyata, opsional.
Catatan: §10c (Saran) mungkin perlu disesuaikan karena mp kini diimplementasikan, bukan future work.
