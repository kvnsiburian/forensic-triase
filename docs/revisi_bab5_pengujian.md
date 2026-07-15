# Revisi Bab V PENGUJIAN + Data Uji Stabilitas (dokumen kerja)

===============================================================================
## DRAF NARASI V.2.2 (siap tempel ke Word) — tulis SESUDAH Tabel 5.3, SEBELUM UAT
===============================================================================

Cara pakai: sisipkan sebagai subbab baru di akhir V.2 PENGUJIAN NON-FUNGSIONAL,
tepat sebelum heading "User Acceptance Test (UAT)". Kalau subbab akurasi
(confusion matrix) mau diberi nomor V.2.1, silakan; yang di bawah ini V.2.2.
Nomor tabel: stabilitas = Tabel 5.4. Nomor gambar chart: Kevin sesuaikan
(mis. Gambar 5.x). Gaya: tanpa em dash. Italic istilah asing pakai *asterisk*.

--- HEADING ---
Stabilitas dan Kompatibilitas Ukuran Memory Dump

--- PARAGRAF 1 (pengantar, sambung ke NF03 Bab IV) ---
Selain akurasi deteksi, pengujian non-fungsional juga menilai kestabilan platform
saat memproses *memory dump* dengan ukuran yang bervariasi, sebagaimana kebutuhan
non-fungsional NF03 yang telah diuraikan pada subbab IV.4.2. Pengujian pada tahap
konstruksi menggunakan tujuh sampel berukuran sama, yaitu 5 GB, sehingga pada
tahap ini pengujian diperluas ke tiga ukuran dump yang berbeda untuk memastikan
platform tetap sanggup memproses berkas yang lebih besar dengan hasil yang
konsisten. Pengujian menggunakan tiga *memory dump* dengan skenario serangan yang
identik, yaitu injeksi kode pada proses notepad.exe (Rule 3), namun dengan alokasi
memori mesin virtual yang berbeda, yaitu 5 GB, 10 GB, dan 16 GB. Ketiga ukuran
tersebut dipilih dengan mempertimbangkan kapasitas memori host sehingga proses
analisis tetap berjalan tanpa kehabisan memori. Setiap dump dijalankan sebanyak
lima kali secara berturut-turut, sehingga diperoleh 15 kali proses analisis, untuk
menilai apakah platform memberikan hasil yang stabil pada setiap pengulangan.

--- PARAGRAF 2 (pengantar Tabel 5.4) ---
Durasi total setiap proses analisis dicatat melalui pengukur waktu internal
platform. Hasil pencatatan durasi untuk seluruh 15 proses analisis disajikan pada
Tabel 5.4, beserta durasi rata-rata dan selisih durasi tertinggi dengan terendah
untuk masing-masing ukuran dump.

--- TABEL 5.4 (buat di Word; angka detik, koma sbg desimal) ---
Judul: Tabel 5.4 Durasi Analisis pada Pengujian Stabilitas Ukuran Dump

| Ukuran Dump | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Rata-rata | Selisih |
|-------------|-------|-------|-------|-------|-------|-----------|---------|
| 5 GB        | 120,45 | 124,23 | 136,64 | 133,75 | 129,82 | 128,98 | 16,19 |
| 10 GB       | 121,74 | 114,50 | 120,94 | 113,88 | 113,84 | 116,98 | 7,90  |
| 16 GB       | 124,73 | 120,05 | 120,05 | 118,75 | 118,30 | 120,38 | 6,43  |
(satuan seluruh angka: detik)

--- PARAGRAF 3 (bukti 1 & 3: selesai semua + durasi konsisten) ---
Berdasarkan Tabel 5.4, seluruh 15 proses analisis berhasil diselesaikan tanpa
kegagalan maupun penghentian di tengah proses pada ketiga ukuran dump. Durasi
setiap proses analisis pada masing-masing ukuran juga berkerumun pada rentang yang
sempit, dengan selisih antara durasi tertinggi dan terendah hanya berkisar 6 sampai
16 detik dari durasi rata-rata sekitar 117 sampai 129 detik. Rentang durasi yang
sempit ini menunjukkan bahwa waktu pemrosesan platform relatif stabil dan tidak
berfluktuasi tajam antar pengulangan pada ukuran dump yang sama. Perlu dicatat bahwa
angka durasi pada pengujian ini diperoleh dengan mode pemrosesan paralel yang
merupakan mode standar platform, sehingga tidak dapat langsung diperbandingkan
dengan durasi pemrosesan berurutan, dan durasi tersebut ditampilkan untuk menilai
kestabilan waktu antar pengulangan, bukan untuk mengukur kecepatan.

--- PARAGRAF 4 (bukti 2, inti: deteksi konsisten & deterministik) ---
Selain durasi, aspek yang lebih penting untuk kestabilan sebuah alat forensik adalah
konsistensi hasil deteksi. Pada seluruh 15 proses analisis, platform secara konsisten
menandai proses notepad.exe sebagai suspicious melalui Rule 3 sebagai target injeksi
kode pada setiap pengulangan, tanpa satu pun yang terlewat. Lebih dari itu, hasil
klasifikasi pada setiap ukuran dump bersifat identik di seluruh lima pengulangannya,
yakni jumlah dan identitas proses yang ditandai suspicious selalu sama persis pada
setiap kali analisis. Hal ini menunjukkan bahwa platform bersifat deterministik, yaitu
memberikan keluaran yang sama untuk masukan yang sama, yang merupakan sifat penting
bagi alat forensik agar hasilnya dapat diandalkan dan diulang.

--- PARAGRAF 5 (catatan FP jujur, ringkas, jadikan keterbatasan) ---
Pada pengujian ini terdapat satu catatan pada dump berukuran 10 GB, di mana selain
notepad.exe, dua proses sistem yang sah yaitu csrss.exe dan winlogon.exe turut
ditandai suspicious oleh Rule 1. Penandaan ini muncul karena proses induk kedua
proses tersebut, yaitu smss.exe, telah berakhir segera setelah menjalankan tugasnya
sehingga nomor prosesnya digunakan kembali oleh proses lain saat *memory dump* diambil,
yang menyebabkan platform membaca relasi induk-anak yang tampak menyimpang. Kemunculan
ini bersifat konsisten pada seluruh lima pengulangan dump 10 GB, dan tidak muncul pada
dump 5 GB maupun 16 GB, sehingga menegaskan bahwa hal tersebut merupakan artefak dari
kondisi pengambilan citra memori dan bukan kesalahan logika deteksi maupun akibat
perbedaan ukuran dump. Keterbatasan pada pendekatan relasi induk-anak yang bertumpu
pada penomoran proses ini dibahas lebih lanjut sebagai bahan pengembangan pada BAB VI.

--- PARAGRAF 6 (penutup V.2.2) ---
Secara keseluruhan, hasil pada Tabel 5.4 menunjukkan bahwa platform mampu memproses
*memory dump* pada ketiga ukuran yang diuji secara stabil, dengan durasi pemrosesan
yang konsisten antar pengulangan dan hasil deteksi target yang identik pada setiap
proses analisis. Dengan demikian, kebutuhan non-fungsional NF03 mengenai kompatibilitas
terhadap berbagai ukuran memory dump terpenuhi.

===============================================================================
## Bagian 1 — Cari/Ganti Tabel 5.1 (SUDAH SELESAI & terverifikasi 14 Jul)

## Bagian 1 — Cari/Ganti Tabel 5.1 (SUDAH SELESAI & terverifikasi 14 Jul)

V.1 PENGUJIAN FUNGSIONAL final. Judul tabel "Hasil Pengujian Black Box",
F01-F08 ringkas & akurat terhadap kode, F01 Expected sudah dikembalikan
(tidak lagi identik dengan Skenario). Detail Cari/Ganti tidak diulang di sini.

===============================================================================

## Bagian 2 — DATA UJI STABILITAS V.2 (NF03), mode MULTIPROCESSING

Konsep (analis LFD + keputusan Kevin 14 Jul):
- 3 ukuran dump uji skala (5 / 10 / 16 GB), skenario r3 injection identik.
- Tiap ukuran dijalankan 5x lewat GUI = 15 run total.
- Mode: **multiprocessing / paralel (centang ON)** di SEMUA run. Kevin pilih ini
  14 Jul (mode nyata analis sehari-hari). WAJIB konsisten ON agar sebanding.
- Menjawab NF03 (Tabel 4.3 Bab IV): kompatibilitas terhadap berbagai ukuran
  memory dump. Kesimpulan = STABILITAS/KONSISTENSI antar-run, BUKAN kecepatan.
- Data diisi dari screenshot GUI yang dikirim Kevin (bukan skrip otomatis).

Ground truth benar tiap run (patokan "lulus"):
- 5 GB  : Total PID 147, notepad.exe PID 3404 R3=Y, 1 suspicious, 146 clean.
- 10 GB : notepad.exe PID 6236 R3=Y (target). Total PID 138.
- 16 GB : notepad.exe PID 7704 R3=Y (target). (isi saat run masuk)

KEPUTUSAN FOKUS UJI (Kevin, 14 Jul): uji stabilitas fokus pada KONSISTENSI
DETEKSI TARGET r3 (notepad R3=Y) tiap run, BUKAN jumlah total suspicious dan
BUKAN zero-FP. Yang dinilai: apakah platform menemukan target yang sama secara
konsisten di 15 run. FP proses sistem disebut singkat sebagai catatan.

TEMUAN TEKNIS (penyebab FP di 10 GB, untuk bahan lisan bila ditanya):
Dump 10 GB memunculkan 3 suspicious: notepad (R3, BENAR/target) + csrss.exe
PID 536 (R1) + winlogon.exe PID 628 (R1). Kedua proses sistem itu FALSE
POSITIVE. Alasan persis dari klasifikasi:
  "[Rule1] Parent abnormal: 'csrss.exe' (PID=536) dijalankan oleh 'dllhost.exe',
   seharusnya oleh {'smss.exe'}"
  "[Rule1] Parent abnormal: 'winlogon.exe' (PID=628) dijalankan oleh 'dllhost.exe',
   seharusnya oleh {'smss.exe'}"
Penyebab: smss.exe (induk sah csrss/winlogon) mati segera setelah membuat anak;
PID bekasnya DIDAUR ULANG Windows, di dump 10 GB kebetulan dipakai dllhost.exe.
Saat platform menelusuri induk, yang terbaca penghuni baru PID (dllhost), bukan
smss asli -> R1 parent-abnormal menyala. Ini ARTEFAK CAPTURE (PID reuse), BUKAN
malware dan BUKAN cacat logika. 5 GB tak kena karena PID induk belum terdaur
ulang saat capture (soal timing, bukan ukuran). Cocok jadi contoh keterbatasan
heuristik relasi induk-anak + bahan Saran (pakai PPID+waktu-buat, bukan PID saja).

### Tabel 5.4 (calon) — Durasi total per run (detik), mode paralel

| Ukuran | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 |
|--------|-------|-------|-------|-------|-------|
| 5 GB   | 120,45 | 124,23 | 136,64 | 133,75 | 129,82 |
| 10 GB  | 121,74 | 114,50 | 120,94 | 113,88 | 113,84 |
| 16 GB  | 124,73 | 120,05 | 120,05 | 118,75 | 118,30 |

### Log rinci (durasi + hasil deteksi tiap run)

| Ukuran | Run | Waktu (tampilan GUI) | Detik | Total PID | Suspicious | Clean | Deteksi benar? |
|--------|-----|----------------------|-------|-----------|------------|-------|----------------|
| 5 GB   | 1   | 2m 00.45s            | 120,45| 147       | 1          | 146   | YA (notepad R3) |
| 5 GB   | 2   | 2m 04.23s            | 124,23| 147       | 1          | 146   | YA (notepad R3) |
| 5 GB   | 3   | 2m 16.64s            | 136,64| 147       | 1          | 146   | YA (notepad R3) |
| 5 GB   | 4   | 2m 13.75s            | 133,75| 147       | 1          | 146   | YA (notepad R3) |
| 5 GB   | 5   | 2m 09.82s            | 129,82| 147       | 1          | 146   | YA (notepad R3) |

Ringkasan 5 GB (5 run): rata-rata 128,98 dtk | min 120,45 | maks 136,64 |
selisih 16,19 dtk | deteksi 5/5 identik (147 PID, 1 suspicious notepad R3).

| 10 GB  | 1   | 2m 01.74s            | 121,74| 138       | 3 (target notepad R3=Y + 2 FP sistem*) | 135 | YA (notepad R3) |
| 10 GB  | 2   | 1m 54.50s            | 114,50| 138       | 3 (IDENTIK run1: csrss+winlogon+notepad) | 135 | YA (notepad R3) |
| 10 GB  | 3   | 2m 00.94s            | 120,94| 138       | 3 (IDENTIK: csrss+winlogon+notepad)      | 135 | YA (notepad R3) |
| 10 GB  | 4   | 1m 53.88s            | 113,88| 138       | 3 (IDENTIK: csrss+winlogon+notepad)      | 135 | YA (notepad R3) |
| 10 GB  | 5   | 1m 53.84s            | 113,84| 138       | 3 (IDENTIK: csrss+winlogon+notepad)      | 135 | YA (notepad R3) |
* 2 FP = csrss.exe(536) & winlogon.exe(628) R1, artefak PID reuse. Target r3 TERDETEKSI.
  10 GB: 5/5 run IDENTIK (proses & rule sama) -> platform DETERMINISTIK (poin stabilitas).

Ringkasan 10 GB (5 run): rata-rata 116,98 dtk | min 113,84 | maks 121,74 |
selisih 7,90 dtk | deteksi 5/5 identik (138 PID, 3 suspicious: notepad R3 target
+ csrss/winlogon FP artefak). Target r3 TERDETEKSI konsisten 5/5.

| 16 GB  | 1   | 2m 04.73s            | 124,73| 146       | 1 (HANYA notepad R3 target, BERSIH)      | 145 | YA (notepad R3) |
| 16 GB  | 2   | 2m 00.05s            | 120,05| 146       | 1 (IDENTIK: notepad R3, csrss/winlogon CLEAN) | 145 | YA (notepad R3) |
| 16 GB  | 3   | 2m 00.05s            | 120,05| 146       | 1 (IDENTIK: notepad R3, csrss/winlogon CLEAN) | 145 | YA (notepad R3) |
| 16 GB  | 4   | 1m 58.75s            | 118,75| 146       | 1 (IDENTIK: notepad R3, csrss/winlogon CLEAN) | 145 | YA (notepad R3) |
| 16 GB  | 5   | 1m 58.30s            | 118,30| 146       | 1 (IDENTIK: notepad R3, csrss/winlogon CLEAN) | 145 | YA (notepad R3) |

=== RINGKASAN LENGKAP 15 RUN (SELESAI 14 Jul) ===
| Ukuran | Rata-rata (dtk) | Min | Maks | Selisih | Stdev | Deteksi target r3 |
|--------|-----------------|-----|------|---------|-------|-------------------|
| 5 GB   | 128,98 | 120,45 | 136,64 | 16,19 | 5,96 | 5/5 YA (notepad R3) |
| 10 GB  | 116,98 | 113,84 | 121,74 | 7,90  | 3,58 | 5/5 YA (notepad R3) |
| 16 GB  | 120,38 | 118,30 | 124,73 | 6,43  | 2,29 | 5/5 YA (notepad R3) |

KESIMPULAN STABILITAS (3 bukti):
1. 15/15 run SELESAI tanpa gagal (tak ada crash/plugin error).
2. Deteksi target r3 (notepad R3=Y) KONSISTEN 15/15 run. Tiap ukuran hasilnya
   IDENTIK antar-run (jumlah & proses suspicious sama persis tiap run) ->
   platform DETERMINISTIK.
3. Durasi antar-run berkerumun rapat (stdev 2,29-5,96 dtk; selisih maks-min
   6-16 dtk dari total ~117-129 dtk) -> konsisten.
Catatan FP: hanya 10 GB memunculkan 2 FP sistem (csrss/winlogon, artefak PID
reuse), KONSISTEN di 5/5 run 10 GB. 5 & 16 GB bersih. Bukan pola ikut ukuran.
Framing: deteksi target STABIL; FP sistem = keterbatasan heuristik induk-anak
(bahan Saran), bukan gagal stabilitas.
** 16 GB BERSIH: csrss(456,556)/winlogon(648) semua CLEAN. Membuktikan FP 10 GB
   = artefak ACAK per-capture (PID reuse), BUKAN pola ikut ukuran. Dump lebih
   besar (16GB) justru tak kena. Memperkuat argumen "artefak capture bukan cacat".

Catatan konversi waktu: "2m 00.45s" = 2*60 + 0,45 = 120,45 detik.

### Yang dipantau untuk kesimpulan stabilitas (diisi setelah 15 run lengkap)
1. Berapa run selesai tanpa gagal (target 15/15).
2. Apakah hasil deteksi IDENTIK tiap run (jumlah suspicious & PID notepad sama).
3. Konsistensi durasi antar-run (selisih kecil per ukuran).
