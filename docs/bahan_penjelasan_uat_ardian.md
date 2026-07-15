# Bahan Penjelasan Platform untuk Pak Ardian (Sebelum Pengisian UAT)

Konteks: dibawakan langsung ke Pak Ardian (Kepala Lab Forensik Digital BSSN) pada
pelaksanaan UAT, 14 Juli 2026 di Sawangan. Ini naskah penjelasan lisan, bukan
dokumen resmi. Alurnya: jelaskan platform dari awal sampai akhir, tunjukkan
datasetnya, tunjukkan hasil validasinya, baru serahkan lembar UAT untuk dinilai.

Nada: praktisi lapangan, bukan sidang. Pimpin dengan apa yang dideteksi dalam
istilah nyata, kaitkan ke pengalaman LFD sendiri (Q13 wawancara 13 April 2025),
tutup dengan ajakan mengisi UAT. Posisikan platform sebagai alat bantu triase
awal, analis tetap memegang keputusan akhir. Jangan memimpin dengan istilah MITRE.

Cara pakai: baca poin-poin di tiap bagian, sampaikan dengan bahasamu sendiri.
Bagian yang ditandai [DEMO] adalah tempat kamu memperlihatkan platform berjalan.
Bagian [KAITKAN KE BUTIR] menunjukkan butir UAT mana yang sedang kamu "buktikan"
lewat penjelasan itu, supaya saat Pak Ardian mengisi, setiap butir sudah pernah
beliau lihat sendiri.

---

## 0. Pembuka singkat (30 detik)

- Terima kasih atas kesediaan Bapak, terutama karena rancangan enam aturan deteksi
  di platform ini berangkat langsung dari hasil wawancara dengan Bapak pada April
  2025, khususnya jawaban Bapak tentang enam indikator anomali yang paling sering
  Tim LFD temui di lapangan.
- Hari ini saya ingin menunjukkan platform yang sudah jadi, dari awal sampai akhir,
  lalu memperlihatkan bahwa aturannya benar bekerja pada data uji. Setelah itu saya
  mohon kesediaan Bapak menilai lewat lembar penerimaan pengguna yang sudah saya
  siapkan.

---

## 1. Masalah yang ingin dibantu (latar belakang)

Sampaikan dalam bahasa lapangan, singkat:

- Analisis memori itu penting karena banyak jejak serangan hanya ada di RAM, tidak
  menyentuh disk. Contohnya serangan tanpa berkas (*fileless*), kode yang disuntik
  ke proses sah, atau kredensial yang dicuri dari memori.
- Masalahnya, membaca memori secara manual dengan Volatility3 di baris perintah itu
  makan waktu dan menuntut ketelitian tinggi. Analis harus menjalankan banyak plugin
  satu per satu, lalu membaca keluaran mentah yang panjang, lalu menyimpulkan sendiri
  mana proses yang mencurigakan.
- Untuk kasus yang banyak, tahap paling awal (memilah mana yang perlu diperiksa lebih
  dulu) inilah yang paling menyita waktu. Di sinilah triase dibutuhkan.
- Platform ini dibuat untuk membantu tahap paling awal itu. Bukan menggantikan analis,
  tetapi menyaring lebih dulu supaya perhatian analis langsung tertuju ke proses yang
  paling mencurigakan.

> Posisi kunci yang harus jelas sejak awal: **ini alat bantu triase awal, keputusan
> akhir tetap di tangan analis.** Ini juga jawaban kalau muncul keraguan soal cakupan
> atau kelengkapan: platform tidak diklaim mendeteksi segalanya secara mandiri.

---

## 2. Apa sebenarnya platform ini (dan apa peran Volatility3)

Ini penting supaya tidak disalahpahami sebagai "sekadar tampilan untuk Volatility3":

- Volatility3 di sini berperan sebagai **mesin pembaca memori**. Dia yang membuka
  memory dump dan mengeluarkan data mentah, misalnya daftar proses, koneksi jaringan,
  dan DLL yang dimuat.
- Platform inilah yang **mengolah data mentah itu menjadi kesimpulan**. Platform
  menjalankan enam plugin Volatility3 secara otomatis dalam satu proses, lalu menilai
  hasilnya dengan aturan yang saya bangun sendiri, lalu menandai tiap proses sebagai
  *clean* atau *suspicious*, lalu menyusun laporannya.
- Jadi kalimat singkatnya: **Volatility3 bahannya, platform inilah yang mengolahnya
  menjadi kesimpulan.**
- Platform dibangun dengan Python, tampilannya memakai Tkinter, dan dijalankan di
  Linux (Kali di atas WSL2). Yang dianalisis adalah memory dump Windows.

[KAITKAN KE BUTIR] Ini menyiapkan pemahaman untuk Butir 1 (tanpa perlu menghafal
perintah Volatility3) dan Butir 13 (mengurangi ketergantungan membaca keluaran
mentah Volatility3 secara manual).

---

## 3. Cara kerja platform dari awal sampai akhir (alur satu analisis)

Ini bagian inti. Jelaskan sambil memperlihatkan platform berjalan.

**Langkah 1 — Muat memory dump.** [DEMO]
- Analis membuka platform, memilih berkas memory dump lewat antarmuka, tanpa mengetik
  perintah apa pun.
- [KAITKAN KE BUTIR] Butir 2 (pemuatan dump dan memulai analisis mudah lewat antarmuka).

**Langkah 2 — Jalankan enam plugin Volatility3 secara otomatis.** [DEMO]
- Sekali tekan, platform menjalankan enam plugin sekaligus. Ini yang di analisis manual
  harus dijalankan satu per satu.
- Selama proses berjalan, platform menampilkan tahap mana yang sedang dikerjakan,
  jadi analis tahu progresnya.
- [KAITKAN KE BUTIR] Butir 3 (informasi tahap yang sedang berjalan ditampilkan jelas)
  dan Butir 6 (eksekusi otomatis enam plugin menyederhanakan pekerjaan).

Enam plugin itu dipetakan ke empat langkah metode SANS Memory Forensics:
- Mencari proses menyamar (*rogue process*): pslist dan pstree.
- Memeriksa artefak jaringan: netscan.
- Mencari jejak injeksi kode: malfind.
- Menganalisis objek proses: dlllist dan handles.

**Langkah 3 — Nilai tiap proses dengan aturan, lalu klasifikasikan.**
- Dari data mentah tadi, platform menilai tiap proses dengan enam aturan (dijelaskan
  di Bagian 4).
- Hasilnya klasifikasi **biner**: *clean* atau *suspicious*. Tidak ada skor angka atau
  tingkat risiko. Prinsipnya, **satu indikator anomali saja sudah cukup untuk menandai
  proses sebagai suspicious.**
- Alasan memilih pendekatan ini: pada tahap triase, kami sengaja mengutamakan
  kepekaan. Lebih baik menandai sesuatu untuk diperiksa daripada melewatkannya.
  Konsekuensinya, sesekali bisa ada penandaan yang ternyata wajar, dan itu memang
  sudah kami perhitungkan (nanti saya tunjukkan satu contohnya yang jujur saya
  sampaikan di data uji).
- [KAITKAN KE BUTIR] Butir 8 (klasifikasi clean/suspicious memfokuskan pemeriksaan).

**Langkah 4 — Tampilkan Panel Detail Indikator dan rekomendasi investigasi.** [DEMO]
- Untuk proses yang ditandai suspicious, platform menampilkan panel yang menjelaskan
  indikator mana yang terpicu dan alasannya, disertai rekomendasi langkah investigasi
  lanjutan.
- Jadi analis tidak hanya diberi tahu "ini mencurigakan", tetapi juga "kenapa" dan
  "sebaiknya diperiksa dengan cara apa".
- [KAITKAN KE BUTIR] Butir 4 (Panel Detail dan rekomendasi mudah dibaca) dan Butir 9
  (rekomendasi membantu menentukan langkah lanjutan).

**Langkah 5 — Ekspor hasil ke CSV dan Excel.** [DEMO]
- Sekali tekan Export, platform menghasilkan dua bentuk keluaran: berkas CSV dan
  berkas Excel.
- Berkas Excel-nya berisi tujuh sheet dalam satu berkas: enam sheet keluaran mentah
  tiap plugin, ditambah satu sheet Klasifikasi yang merangkum vonis platform per
  proses. Gunanya, analis bisa memeriksa ulang kesimpulan platform terhadap data
  mentahnya tanpa harus menjalankan ulang Volatility3.
- Berkas CSV disediakan untuk pengolahan data lebih lanjut.
- [KAITKAN KE BUTIR] Butir 10 (ekspor CSV dan Excel berguna untuk dokumentasi dan
  pelaporan).

> Catatan kalau Pak Ardian menyinggung format PDF: platform sengaja berhenti di data
> terstruktur (CSV dan Excel). Laporan resmi PDF memakai template internal LFD, dan
> itu ranah analis, bukan yang direplikasi platform. Platform menyiapkan datanya,
> analis yang menuangkan ke laporan resmi.

---

## 4. Enam aturan deteksi (jelaskan dalam istilah lapangan, kaitkan ke Q13)

Ini bagian yang paling menyentuh audiens LFD, karena keenam aturan ini berasal
langsung dari enam indikator yang Bapak sebut di wawancara. Sampaikan pola:
"Bapak menyebut X, aturan ini menangkap X."

Empat kelompok SANS, enam aturan:

**Kelompok 1 — Proses menyamar (Rogue Process).**
- R1a: proses yang namanya sengaja mirip proses sistem tapi berjalan dari lokasi yang
  tidak wajar. Contoh persis yang Bapak sebut: `svch0st.exe` (bukan `svchost.exe`)
  yang berjalan dari folder publik.
- R1b: proses induk dan anak yang tidak wajar. Contohnya aplikasi Office atau dokumen
  yang tiba-tiba meluncurkan cmd atau PowerShell. Ini indikator makro berbahaya.

**Kelompok 2 — Artefak jaringan (Network Artifacts).**
- R2: proses yang seharusnya tidak berkomunikasi keluar, tapi punya koneksi aktif ke
  alamat IP publik atau port yang tidak wajar. Ini menangkap kanal kendali jarak jauh
  (C2).

**Kelompok 3 — Injeksi kode (Code Injection).**
- R3: jejak kode yang disuntikkan ke proses sah, terlihat dari area memori yang bisa
  ditulis sekaligus dieksekusi. Ini pola khas injeksi.

**Kelompok 4 — Objek proses (Process Objects).**
- R4a: DLL yang dimuat dari lokasi yang mencurigakan, meski proses pemuatnya sendiri
  sah.
- R4b: akses ke `lsass.exe` yang mengarah ke pencurian kredensial, misalnya pola yang
  ditinggalkan Mimikatz. Platform membedakan akses yang wajar dari yang mencurigakan.

> Poin yang perlu disampaikan dengan percaya diri: **keenam aturan ini bukan saya
> karang dari statistik global.** Keenamnya persis mengikuti enam indikator yang
> Bapak sebut sebagai yang paling sering ditemui Tim LFD. Jadi platform ini memang
> dirancang untuk kebutuhan operasional LFD, bukan sekadar mengejar tren malware
> dunia.

- [KAITKAN KE BUTIR] Butir 7 (cakupan deteksi relevan dengan kebutuhan analisis
  memori) dan Butir 11 (keluaran relevan dengan kebutuhan triase awal di Tim LFD).

---

## 5. Dari mana datanya (dataset uji)

Jelaskan supaya jelas bahwa pengujian tidak mengarang:

- Karena Bapak sendiri menyampaikan di wawancara bahwa data kasus asli LFD tidak bisa
  dibagikan dan menyarankan saya membuat dataset uji yang sesuai skenario platform,
  saya membangun tujuh memory dump sendiri di laboratorium terkontrol.
- Lingkungannya: korban Windows 10, penyerang Kali Linux, jaringan terisolasi tanpa
  internet. Serangannya memakai alat serangan nyata, bukan simulasi manual.
- Tujuh dataset itu:
  - Satu **baseline bersih**: workstation normal yang realistis (ada Edge, Office, VS
    Code, aplikasi portable dari Downloads). Ini kebenaran dasar untuk yang bersih.
  - Enam **terinfeksi**, masing-masing dirancang untuk memicu satu aturan saja, supaya
    bisa dibuktikan tiap aturan benar-benar bekerja sendiri-sendiri:
    - R1a: payload meterpreter disamarkan jadi `svch0st.exe` dari folder publik.
    - R1b: makro LibreOffice yang meluncurkan PowerShell langsung.
    - R2: implan C2 Sliver. Sengaja dipilih Sliver karena tidak meninggalkan jejak
      memori yang bisa dieksekusi, jadi membuktikan R2 menangkap kanal C2 yang aturan
      lain justru lewatkan.
    - R3: DLL reflektif meterpreter disuntik ke `notepad.exe`.
    - R4a: DLL disisipkan lewat `rundll32.exe` dari folder publik.
    - R4b: Mimikatz mengakses `lsass.exe` untuk mencuri kredensial.
- Alasan tiap dataset mengisolasi satu aturan: supaya kalau aturan itu menyala, kita
  yakin penyebabnya memang skenario yang ditanam, bukan kebetulan.

---

## 6. Hasil pengujian (bukti aturannya bekerja)

Sampaikan angkanya dengan tenang, termasuk yang satu penandaan wajar, karena kejujuran
justru memperkuat:

- Total ada 1127 proses yang dianalisis di tujuh dataset.
- Ketujuh ancaman yang ditanam **semuanya tertangkap** (tidak ada yang lolos). Dalam
  istilah metrik: Recall 100 persen, tidak ada yang terlewat (*false negative* nol).
- Ada **satu** penandaan pada dataset bersih yang sebenarnya wajar, yaitu proses Paint
  3D yang punya koneksi ke IP telemetri Microsoft yang belum masuk daftar proses
  jaringan yang diizinkan.
  - Ini saya sampaikan apa adanya, tidak saya sembunyikan. Ini justru konsekuensi
    yang sudah diperhitungkan dari pilihan mengutamakan kepekaan tadi. Lebih baik satu
    penandaan wajar untuk diperiksa daripada melewatkan ancaman.
- Kesimpulan pengujian: tiap aturan terbukti menyala hanya pada skenario yang
  seharusnya, dan tidak ada ancaman yang lolos.

> Kalau Pak Ardian bertanya "kenapa tidak diuji dengan malware asli?": jawab bahwa
> validasi dengan sampel malware asli memang direncanakan sebagai pengembangan
> lanjutan untuk memperkuat validitas ekologis, tetapi untuk membuktikan tiap aturan
> bekerja, dataset terkontrol dengan kebenaran dasar yang pasti justru lebih tepat.

---

## 7. Ringkas ulang sebelum menyerahkan lembar UAT

Rangkum dalam tiga kalimat:

1. Platform ini menjalankan enam plugin Volatility3 otomatis, menilai tiap proses
   dengan enam aturan yang berasal dari pengalaman Tim LFD sendiri, lalu menandainya
   clean atau suspicious dengan penjelasan dan rekomendasi.
2. Hasilnya bisa diperiksa ulang dan diekspor ke CSV dan Excel.
3. Posisinya alat bantu triase awal, keputusan akhir tetap di tangan analis.

Lalu serahkan lembar UAT:

- "Lembar ini berisi 15 pernyataan dalam tiga aspek: kemudahan penggunaan, kegunaan
  fitur, dan relevansi terhadap kebutuhan operasional Tim LFD. Mohon Bapak mengisi
  Ya atau Tidak berdasarkan kondisi sebenarnya."
- Tiga aspek itu persis yang sudah kita jalani di penjelasan tadi, jadi setiap
  pernyataan sudah Bapak lihat sendiri buktinya.

---

## Peta penjelasan ke 15 butir UAT (untuk memastikan tidak ada yang terlewat)

Sebelum menyerahkan lembar, pastikan tiap butir sudah "terbukti" di penjelasanmu:

| Aspek | Butir | Sudah dibuktikan di bagian |
|-------|-------|----------------------------|
| A. Kemudahan | 1 antarmuka tanpa hafal perintah | Bagian 2, 3 Langkah 1 |
| A | 2 muat dump dan mulai analisis mudah | Bagian 3 Langkah 1 [DEMO] |
| A | 3 tahap berjalan ditampilkan jelas | Bagian 3 Langkah 2 [DEMO] |
| A | 4 Panel Detail dan rekomendasi mudah dibaca | Bagian 3 Langkah 4 [DEMO] |
| A | 5 keseluruhan mudah dioperasikan | seluruh demo Bagian 3 |
| B. Fitur | 6 eksekusi otomatis 6 plugin | Bagian 3 Langkah 2 |
| B | 7 cakupan deteksi relevan | Bagian 4 |
| B | 8 klasifikasi clean/suspicious memfokuskan | Bagian 3 Langkah 3 |
| B | 9 rekomendasi bantu langkah lanjutan | Bagian 3 Langkah 4 |
| B | 10 ekspor CSV dan Excel bermanfaat | Bagian 3 Langkah 5 [DEMO] |
| C. Relevansi LFD | 11 keluaran relevan triase awal LFD | Bagian 4, 6 |
| C | 12 offline sesuai lingkungan terisolasi | sebut saat demo (jalan tanpa internet) |
| C | 13 kurangi ketergantungan baca Vol3 manual | Bagian 2, 3 Langkah 3 dan 5 |
| C | 14 permudah alur triase dibanding manual | Bagian 1, 3 keseluruhan |
| C | 15 layak sebagai alat bantu triase awal LFD | rangkuman Bagian 7 |

Catatan: Butir 12 (offline) mudah lupa dibuktikan. Selipkan satu kalimat saat demo,
misalnya "seluruh proses ini berjalan tanpa koneksi internet, sesuai lingkungan
forensik yang terisolasi."
