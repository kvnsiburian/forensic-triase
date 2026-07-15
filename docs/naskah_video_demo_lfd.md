# Naskah Rekaman Video Demo Platform untuk Analis LFD

Konteks: Kevin tidak bisa mempresentasikan langsung, jadi platform dijelaskan lewat
rekaman video (berbagi layar + suara, tanpa menampilkan wajah). Video ini dikirim ke
analis LFD supaya mereka paham platform dari awal sampai akhir. Lembar UAT dikirim
terpisah, jadi video ini fokus pada penjelasan platform, dataset, dan hasil.

Mode demo: campuran. Bagian awal dijalankan live (muat dump sampai analisis mulai
berjalan), lalu bagian tunggu dipotong atau dipercepat, lanjut ke hasil yang sudah
jadi supaya video tetap ringkas.

Cara pakai naskah ini:
- [LAYAR] = apa yang harus terlihat di layar saat itu.
- [UCAPKAN] = garis besar yang kamu katakan. Jangan dibaca kaku, sampaikan dengan
  bahasamu sendiri seperti sedang menjelaskan ke rekan kerja.
- [POTONG] = titik untuk berhenti merekam atau mempercepat rekaman saat penyuntingan.
- Perkiraan total durasi: 8 sampai 12 menit. Cukup untuk dipahami tanpa bertele-tele.

Sebelum mulai, siapkan dulu:
- Satu memory dump yang siap dimuat untuk demo live (pakai yang paling kecil biar
  tidak lama, misalnya dataset 5 GB).
- Satu hasil analisis yang SUDAH JADI dan sudah kamu buka, siap ditunjukkan (tabel
  proses, Panel Detail, dan file Excel hasil ekspor). Sebaiknya pakai salah satu
  dataset terinfeksi supaya ada baris suspicious yang bisa dijelaskan.
- Tutup aplikasi lain, rapikan desktop, perbesar jendela platform.
- Coba rekam 20 detik dulu untuk memastikan suara mikrofon jelas dan layar terekam.
- Bicara pelan dan jelas. Diam sebentar di antara segmen memudahkan penyuntingan.

===============================================================================

## Segmen 0 — Pembuka (sekitar 30 sampai 45 detik)

[LAYAR] Jendela platform sudah terbuka di kondisi awal (belum ada dump dimuat).

[UCAPKAN]
- Perkenalkan diri singkat: nama, dan bahwa ini rekaman untuk menjelaskan platform
  triase forensik memori yang kamu bangun untuk tugas akhir.
- Sampaikan bahwa karena tidak bisa presentasi langsung, penjelasan ini dibuat dalam
  bentuk video, supaya analis LFD bisa melihat sendiri cara kerja platform dari awal
  sampai akhir.
- Sebutkan bahwa rancangan enam aturan deteksi di platform ini berangkat langsung dari
  hasil wawancara dengan Tim LFD pada April 2025, khususnya enam indikator anomali yang
  paling sering ditemui di lapangan. Jadi ini memang dirancang untuk kebutuhan LFD.

===============================================================================

## Segmen 1 — Masalah yang ingin dibantu (sekitar 1 menit)

[LAYAR] Boleh tetap di jendela platform, atau tampilkan satu slide sederhana kalau
kamu punya. Tidak wajib pindah layar.

[UCAPKAN]
- Analisis memori penting karena banyak jejak serangan hanya ada di RAM, tidak
  menyentuh disk. Contohnya serangan tanpa berkas (fileless), kode yang disuntikkan ke
  proses sah, atau kredensial yang dicuri dari memori.
- Masalahnya, membaca memori secara manual dengan Volatility3 di baris perintah makan
  waktu dan menuntut ketelitian tinggi. Analis harus menjalankan banyak plugin satu per
  satu, membaca keluaran mentah yang panjang, lalu menyimpulkan sendiri mana proses
  yang mencurigakan.
- Tahap paling awal, yaitu memilah mana yang perlu diperiksa lebih dulu, itulah yang
  paling menyita waktu. Di sinilah triase dibutuhkan.
- Posisi kunci yang harus jelas: ini alat bantu triase awal. Platform menyaring lebih
  dulu supaya perhatian analis langsung tertuju ke proses paling mencurigakan.
  Keputusan akhir tetap di tangan analis. Platform tidak diklaim mendeteksi segalanya
  sendiri.

===============================================================================

## Segmen 2 — Apa sebenarnya platform ini (sekitar 1 menit)

[LAYAR] Jendela platform.

[UCAPKAN]
- Perjelas peran Volatility3: di sini Volatility3 berperan sebagai mesin pembaca
  memori. Dia yang membuka memory dump dan mengeluarkan data mentah, misalnya daftar
  proses, koneksi jaringan, dan DLL yang dimuat.
- Platform inilah yang mengolah data mentah itu menjadi kesimpulan. Platform
  menjalankan enam plugin Volatility3 secara otomatis dalam satu proses, menilai
  hasilnya dengan aturan yang dibangun sendiri, menandai tiap proses clean atau
  suspicious, lalu menyusun laporannya.
- Kalimat singkatnya: Volatility3 bahannya, platform inilah yang mengolahnya menjadi
  kesimpulan. Jadi ini bukan sekadar tampilan untuk Volatility3.
- Sebutkan teknisnya singkat: dibangun dengan Python, tampilannya Tkinter, dijalankan
  di Linux, dan yang dianalisis adalah memory dump Windows.

===============================================================================

## Segmen 3 — Demo alur analisis (bagian inti, sekitar 3 sampai 4 menit)

Ini bagian paling penting. Di sinilah mode campuran dipakai.

### 3a. Muat memory dump (LIVE)

[LAYAR] Tunjukkan kamu menekan tombol untuk memilih berkas, lalu memilih file dump
lewat antarmuka.

[UCAPKAN]
- Jelaskan bahwa analis cukup membuka platform dan memilih berkas memory dump lewat
  antarmuka, tanpa mengetik perintah apa pun.
- Selipkan satu kalimat penting: seluruh proses ini berjalan tanpa koneksi internet,
  sesuai lingkungan forensik yang terisolasi.

### 3b. Jalankan analisis (LIVE sampai proses mulai berjalan)

[LAYAR] Tekan tombol analisis. Tunjukkan platform mulai berjalan dan menampilkan tahap
mana yang sedang dikerjakan.

[UCAPKAN]
- Jelaskan bahwa sekali tekan, platform menjalankan enam plugin Volatility3 sekaligus.
  Ini yang di analisis manual harus dijalankan satu per satu.
- Tunjukkan bahwa selama proses berjalan, platform menampilkan tahap yang sedang
  dikerjakan, jadi analis tahu progresnya.
- Sebutkan enam plugin dipetakan ke empat langkah metode SANS Memory Forensics:
  mencari proses menyamar (pslist dan pstree), memeriksa artefak jaringan (netscan),
  mencari jejak injeksi kode (malfind), dan menganalisis objek proses (dlllist dan
  handles).

[POTONG] Di sini analisis akan berjalan beberapa menit karena dump besar. Berhenti
merekam atau, saat menyunting, percepat bagian tunggu ini. Sampaikan lewat suara:
"analisis berjalan beberapa menit, saya percepat bagian ini." Lalu lanjut ke hasil
yang sudah jadi.

### 3c. Hasil analisis dan klasifikasi (pakai hasil yang SUDAH JADI)

[LAYAR] Buka atau tampilkan hasil analisis yang sudah jadi: tabel semua proses dengan
baris suspicious berwarna, dan statistik ringkas.

[UCAPKAN]
- Jelaskan bahwa dari data mentah tadi, platform menilai tiap proses dengan enam aturan
  dan memberi klasifikasi biner: clean atau suspicious. Tidak ada skor angka atau
  tingkat risiko.
- Prinsipnya: satu indikator anomali saja sudah cukup untuk menandai proses sebagai
  suspicious.
- Alasan pendekatan ini: pada tahap triase, kepekaan sengaja diutamakan. Lebih baik
  menandai sesuatu untuk diperiksa daripada melewatkannya. Konsekuensinya sesekali bisa
  ada penandaan yang ternyata wajar, dan itu sudah diperhitungkan.

### 3d. Panel Detail Indikator dan rekomendasi (pakai hasil yang SUDAH JADI)

[LAYAR] Klik salah satu baris yang suspicious. Tunjukkan Panel Detail yang menjelaskan
indikator apa yang terpicu, alasannya, dan rekomendasi investigasi lanjutan.

[UCAPKAN]
- Jelaskan bahwa untuk proses yang ditandai suspicious, platform menampilkan panel yang
  menjelaskan indikator mana yang terpicu dan alasannya, disertai rekomendasi langkah
  investigasi lanjutan.
- Tekankan: analis tidak hanya diberi tahu bahwa sesuatu mencurigakan, tapi juga kenapa,
  dan sebaiknya diperiksa dengan cara apa.

### 3e. Ekspor hasil (pakai hasil yang SUDAH JADI)

[LAYAR] Tunjukkan tombol Export, lalu buka file hasilnya. Buka file Excel, tunjukkan
tab atau sheet-nya: enam sheet keluaran mentah tiap plugin ditambah satu sheet
Klasifikasi. Buka juga file CSV sebentar.

[UCAPKAN]
- Jelaskan bahwa sekali tekan Export, platform menghasilkan dua bentuk keluaran: berkas
  CSV dan berkas Excel.
- Excel-nya berisi tujuh sheet dalam satu berkas: enam sheet keluaran mentah tiap
  plugin, ditambah satu sheet Klasifikasi yang merangkum vonis platform per proses.
  Gunanya, analis bisa memeriksa ulang kesimpulan platform terhadap data mentahnya
  tanpa harus menjalankan ulang Volatility3.
- CSV disediakan untuk pengolahan data lebih lanjut.
- Kalau relevan, sebutkan singkat soal PDF: platform sengaja berhenti di data
  terstruktur. Laporan resmi PDF memakai template internal LFD dan itu ranah analis,
  bukan yang direplikasi platform. Platform menyiapkan datanya, analis yang menuangkan
  ke laporan resmi.

===============================================================================

## Segmen 4 — Enam aturan deteksi (sekitar 2 menit)

[LAYAR] Boleh tetap di Panel Detail atau sheet Klasifikasi supaya aturan yang kamu
sebut ada wujudnya di layar. Bisa juga slide daftar aturan kalau kamu punya.

[UCAPKAN]
Sampaikan pola: indikator ini disebut Tim LFD di wawancara, aturan ini menangkapnya.
Empat kelompok SANS, enam aturan:

- Kelompok 1, proses menyamar:
  - R1a: proses yang namanya sengaja mirip proses sistem tapi berjalan dari lokasi tak
    wajar. Contoh persis yang disebut Tim LFD: svch0st.exe (bukan svchost.exe) yang
    berjalan dari folder publik.
  - R1b: proses induk dan anak yang tidak wajar. Misalnya aplikasi Office atau dokumen
    yang tiba-tiba meluncurkan cmd atau PowerShell. Ini indikator makro berbahaya.
- Kelompok 2, artefak jaringan:
  - R2: proses yang seharusnya tidak berkomunikasi keluar tapi punya koneksi aktif ke
    IP publik atau port tak wajar. Ini menangkap kanal kendali jarak jauh (C2).
- Kelompok 3, injeksi kode:
  - R3: jejak kode yang disuntikkan ke proses sah, terlihat dari area memori yang bisa
    ditulis sekaligus dieksekusi. Ini pola khas injeksi.
- Kelompok 4, objek proses:
  - R4a: DLL yang dimuat dari lokasi mencurigakan, meski proses pemuatnya sendiri sah.
  - R4b: akses ke lsass.exe yang mengarah ke pencurian kredensial, misalnya pola yang
    ditinggalkan Mimikatz. Platform membedakan akses yang wajar dari yang mencurigakan.

- Tutup segmen ini dengan percaya diri: keenam aturan ini bukan dikarang dari statistik
  global. Keenamnya mengikuti enam indikator yang disebut Tim LFD sebagai yang paling
  sering ditemui. Jadi platform ini memang dirancang untuk kebutuhan operasional LFD.

===============================================================================

## Segmen 5 — Dari mana datanya (dataset uji, sekitar 1,5 menit)

[LAYAR] Slide atau tabel dataset kalau ada. Kalau tidak, cukup suara sambil menampilkan
sheet Klasifikasi atau folder dataset.

[UCAPKAN]
- Karena Tim LFD menyampaikan bahwa data kasus asli tidak bisa dibagikan dan menyarankan
  membuat dataset uji sesuai skenario platform, dibangun tujuh memory dump sendiri di
  laboratorium terkontrol.
- Lingkungannya: korban Windows 10, penyerang Kali Linux, jaringan terisolasi tanpa
  internet. Serangannya memakai alat serangan nyata, bukan simulasi manual.
- Tujuh dataset: satu baseline bersih (workstation normal yang realistis, sebagai
  kebenaran dasar untuk yang bersih), dan enam terinfeksi, masing-masing dirancang untuk
  memicu satu aturan saja:
  - R1a: payload meterpreter disamarkan jadi svch0st.exe dari folder publik.
  - R1b: makro LibreOffice yang meluncurkan PowerShell langsung.
  - R2: implan C2 Sliver, dipilih karena tidak meninggalkan jejak memori yang bisa
    dieksekusi, jadi membuktikan R2 menangkap kanal C2 yang aturan lain justru lewatkan.
  - R3: DLL reflektif meterpreter disuntik ke notepad.exe.
  - R4a: DLL disisipkan lewat rundll32.exe dari folder publik.
  - R4b: Mimikatz mengakses lsass.exe untuk mencuri kredensial.
- Alasan tiap dataset mengisolasi satu aturan: supaya kalau aturan itu menyala, kita
  yakin penyebabnya memang skenario yang ditanam, bukan kebetulan.

===============================================================================

## Segmen 6 — Hasil pengujian (sekitar 1 menit)

[LAYAR] Slide atau tabel hasil kalau ada. Kalau tidak, cukup suara.

[UCAPKAN]
- Sebutkan angkanya dengan tenang: total ada 1127 proses yang dianalisis di tujuh
  dataset.
- Ketujuh ancaman yang ditanam semuanya tertangkap, tidak ada yang lolos. Dalam istilah
  metrik: recall 100 persen, tidak ada yang terlewat.
- Ada satu penandaan pada dataset bersih yang sebenarnya wajar, yaitu proses Paint 3D
  yang punya koneksi ke IP telemetri Microsoft yang belum masuk daftar proses jaringan
  yang diizinkan.
- Sampaikan apa adanya, jangan disembunyikan. Ini justru konsekuensi yang sudah
  diperhitungkan dari pilihan mengutamakan kepekaan. Lebih baik satu penandaan wajar
  untuk diperiksa daripada melewatkan ancaman.
- Kesimpulan pengujian: tiap aturan terbukti menyala hanya pada skenario yang
  seharusnya, dan tidak ada ancaman yang lolos.

===============================================================================

## Segmen 7 — Penutup (sekitar 30 sampai 45 detik)

[LAYAR] Kembali ke jendela platform, atau tampilan hasil.

[UCAPKAN]
Rangkum dalam tiga kalimat:
1. Platform ini menjalankan enam plugin Volatility3 otomatis, menilai tiap proses
   dengan enam aturan yang berasal dari pengalaman Tim LFD sendiri, lalu menandainya
   clean atau suspicious dengan penjelasan dan rekomendasi.
2. Hasilnya bisa diperiksa ulang dan diekspor ke CSV dan Excel.
3. Posisinya alat bantu triase awal, keputusan akhir tetap di tangan analis.

Lalu tutup:
- Ucapkan terima kasih atas waktu analis LFD sudah menonton.
- Arahkan ke langkah berikutnya: sampaikan bahwa lembar penilaian (UAT) dikirim
  terpisah, dan mohon kesediaan mengisinya berdasarkan apa yang sudah ditunjukkan di
  video ini.
- Sampaikan kalau ada yang ingin ditanyakan, kamu siap dihubungi.

===============================================================================

## Checklist sebelum mengirim video

- Suara jelas dari awal sampai akhir, tidak ada bagian yang terlalu pelan.
- Tidak ada informasi sensitif yang tidak sengaja terlihat di layar (path pribadi,
  jendela lain, notifikasi).
- Bagian tunggu analisis sudah dipotong atau dipercepat, video tidak ada jeda diam yang
  panjang.
- Baris suspicious dan Panel Detail benar-benar terlihat jelas saat dijelaskan.
- Sebutan "tanpa internet" muncul minimal sekali (Segmen 3a).
- Durasi akhir wajar, sekitar 8 sampai 12 menit.
- Sudah disebutkan bahwa lembar UAT menyusul terpisah.
