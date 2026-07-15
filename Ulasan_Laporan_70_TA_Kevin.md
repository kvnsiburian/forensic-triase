# Ulasan Kritis Laporan 70% Tugas Akhir

**Judul dokumen:** Rancang Bangun Platform Triase Forensik Memori Berbasis Volatility3
**Penulis:** Kevin Armando Siburian (2221101800)
**Dokumen yang ditelaah:** `Kevin Armando\\\_Laporan 70 TA\\\_RKS\\\_mulai revisi sendiri.pdf` (92 halaman PDF, isi sampai halaman cetak 77)
**Tanggal ulasan:** 8 Juli 2026

> \\\*\\\*Batas kewenangan ulasan ini.\\\*\\\* Ulasan ini adalah telaah editorial dan substantif independen, bukan sumber koreksi resmi. Sumber koreksi yang sah tetap hanya catatan perbaikan penguji bertanda tangan, rekomendasi pembimbing, dan transkrip wawancara. Temuan yang beririsan dengan rekomendasi pembimbing saya tandai eksplisit. Setiap temuan saya tambatkan ke halaman cetak dokumen; mana yang fakta tertulis dan mana interpretasi saya dipisahkan.

\---

## Ringkasan Eksekutif

Dokumen ini secara keseluruhan sudah berada di atas rata-rata laporan 70%: argumentasi pengujian jujur secara metodologis, narasi teknis BAB IV rinci dan dapat ditelusuri, dan alur latar belakang sudah mengikuti kerangka yang direkomendasikan pembimbing. Namun dokumen saat ini **terjebak di antara dua generasi desain**: desain lama (5 sampel, 4 aturan, plugin 4) dan desain final (7 dataset, 6 aturan dalam 4 kelompok, 6 plugin). Akibatnya muncul kontradiksi internal yang tersebar di hampir semua bab, dan ini adalah risiko terbesar dokumen bila dibaca penguji sebagai satu kesatuan.

Tiga temuan paling material:

1. **Abstrak melaporkan angka yang tidak ada di badan dokumen.** Abstrak (hal. vi) menyebut 1.127 proses, tujuh skenario, sensitivitas 100%, spesifisitas 99,91%. BAB V.2 (hal. 59–60) justru berisi Tabel 5.2/5.3 dengan tujuh baris dataset baru yang **sel-selnya kosong**, sementara narasinya masih memuat angka generasi lama (845 proses, 10 TP, akurasi 99,88%, FP = MicrosoftEdgeUpdate.exe). Tiga versi hasil yang saling bertentangan dalam satu dokumen.
2. **Enam sitasi kosong `\\\[]`** pada subbab II.1.5 (hal. 9–10) dan **tiga referensi yatim** (\[8], \[9], \[15]) yang tidak pernah dipanggil di teks — termasuk \[9] yang justru adalah ISO/IEC 27042.
3. **Inkonsistensi 4-vs-6** (jumlah plugin, aturan, sampel) di sekurangnya 15 titik lintas BAB II–V, dirinci di bagian Kejelasan.

Sebagian besar hal di atas konsisten dengan status revisi yang memang belum selesai (penulisan ulang BAB IV–V menunggu dataset 3–7). Ulasan ini memetakan semuanya agar tidak ada yang lolos saat revisi menuju 100%.

\---

## 1\. Teknik Penulisan

### 1.1 Nada akademik

**Fakta tertulis.** Nada umumnya sudah formal, pasif, dan naratif. Namun terdapat selipan register informal/calque Inggris:

|Lokasi|Temuan|Saran|
|-|-|-|
|hal. 9|"proses yang *ter-flag*"|"proses yang tertandai"|
|hal. 42|"keliru diflag"|"keliru ditandai"|
|hal. 46–47 (3×)|"meng-*spawn*"|"memunculkan/meluncurkan proses"|
|hal. 44–45|"indikator dengan *intent* jahat"|"indikasi niat jahat"|
|hal. 6|"menundukkan seluruh bukti digital pada pemeriksaan penuh" (calque dari *subjecting*)|"memeriksa seluruh bukti secara penuh" — frasa ini terulang di hal. 53|

### 1.2 Konsistensi istilah (fakta tertulis, hasil pemeriksaan terprogram)

* **"klasifikasi binary" (4×) vs "klasifikasi biner" (5×)** — pilih satu; "biner" lebih tepat untuk prosa Indonesia.
* **"orkestrator" (hal. 38) vs "orchestrator" (hal. 39)** dalam dua halaman berurutan.
* **"kuisioner" (hal. 29, BAB III) vs "kuesioner" (hal. 62, BAB V)** — bentuk baku KBBI: *kuesioner*.
* **"pengembangan/dikembangkan/mengembangkan" muncul ±45 kali vs "pembangunan" ±21 kali.** Konvensi penulisan Anda sendiri menetapkan istilah *pembangunan* untuk platform ini. Pemakaian "pengembangan" yang merujuk platform sendiri (mis. hal. 17–18, 19, 24–27, 51) perlu disapu; yang merujuk penelitian orang lain di II.2 boleh tetap.

### 1.3 Struktur dokumen

* **DAFTAR ISI (hal. x–xi) tidak memuat I.5 Sistematika Penulisan dan tidak memuat BAB VI**, padahal I.5 ada di teks (hal. 4) dan Sistematika menjanjikan enam bab. BAB VI memang belum ditulis — ini wajar untuk 70%, tetapi daftar isi tetap harus jujur terhadap rencana final.
* **Penomoran romawi ganda:** LEMBAR JUDUL dan LEMBAR PERNYATAAN ORISINALITAS sama-sama tertulis halaman "II" di daftar isi.
* **Penamaan BAB VI:** Sistematika (hal. 4) menyebut "BAB VI PENUTUP", sedangkan acuan struktur (skripsi Fransiska) menggunakan "BAB VI KESIMPULAN DAN SARAN". Selaraskan dengan acuan.
* **Pengantar BAB III (hal. 19) menjanjikan "jadwal penelitian"** ("objek, jenis, desain, serta jadwal penelitian"), tetapi subbab jadwal tidak ada (III hanya berisi III.1–III.3). Hapus frasa itu atau tambahkan subbabnya.
* **Caption tabel berulang kata:** "Tabel 4.1 **Tabel** Software Requirement Specification…", "Tabel 4.2 **Tabel** Kebutuhan Fungsional", "Tabel 4.3 **Tabel** Kebutuhan Non-fungsional" (hal. 32–34). Kata "Tabel" kedua dihapus. Posisi caption sudah benar di atas tabel.

### 1.4 Kepatuhan standar sitasi (IEEE)

**Fakta tertulis, material:**

* **Enam sitasi kosong `\\\[]`** di II.1.5 Triase Forensik Memori (hal. 9–10) pada enam kalimat berbeda. Seluruh klaim definisi triase saat ini tidak bersumber.
* **Referensi yatim:** \[8] (El Hafidy dkk.), \[9] (ISO/IEC 27042:2015), dan \[15] (Stoykova dkk.) tidak ditemukan pemanggilannya di badan teks. Konsekuensinya: entri \[9] pun tidak lengkap — nomor standar "ISO/IEC 27042:2015" tidak tertulis di entri (hal. 64). Jika keputusan final menjadikan ISO 27042 landasan implisit di badan teks, standar ini justru harus dipanggil setidaknya sekali (kandidat alami: kalimat *repeatability* di III.3.2 hal. 23); jika tidak, entri harus dibuang. Referensi yang tidak pernah dikutip lazim dipermasalahkan penguji.
* **Sitasi salah tambat:** klaim hasil wawancara Kepala LFD di Latar Belakang (hal. 1) diberi sitasi **\[10]** (Nyholm dkk., *The Evolution of Volatile Memory Forensics*). Temuan wawancara tidak boleh ditambatkan ke pustaka pihak ketiga; rujuk Lampiran 1 (transkrip) dan biarkan \[10] hanya menyokong klaim literaturnya.
* **Kandidat salah nomor:** klaim "otomatisasi dapat mengurangi beban kerja dan konsumsi waktu" di hal. 53 dikutip \[13], padahal klaim identik di hal. 1–2 dikutip \[11] (Michelet dkk., tentang otomatisasi). \[13] adalah studi perbandingan *tools*. Mohon verifikasi silang.
* **Entri rusak/tidak lengkap** (hal. 64–67): \[1] nama lembaga terduplikasi di dalam judul; \[2] tanpa nama jurnal/volume; \[20] prosiding ditulis seperti buku beratribut penulis "Asaf. Varol"; \[22] "A. FFaizal" (dobel F); \[25] judul tercampur teks sampul jurnal ("…INFORMASI ARTIKEL ABSTRAK"); \[26] judul dwibahasa terduplikasi tanpa jurnal; \[29] NIST SP 800-86 tanpa tahun/penerbit; \[34] "Svetlana. Ostrovskaya and Oleg. Skulkin" plus spasi sebelum titik; \[37] tanpa penerbit; \[45] buku Pressman \& Maxim ditulis sebagai artikel tanpa edisi/penerbit; \[46], \[47] tanpa nama jurnal/venue.
* **Nama penulis tidak konsisten:** Tabel 2.1 (hal. 16) menulis "Santori et al. (2025)" untuk ForenSeeker, sedangkan entri \[17] menulis "S. S. Zen" sebagai penulis pertama. Bila nama keluarga penulis adalah Zen, tabel seharusnya "Zen et al."
* **Interpretasi saya:** \[39] (blog vendor Belkasoft) dipakai menyokong klaim "diakui sebagai teknik standar" (hal. 13). Sumber vendor lemah untuk klaim normatif akademik; cari padanan di literatur peer-reviewed atau turunkan kekuatan klaimnya.

### 1.5 Konvensi internal penulisan Anda

* **Nama fungsi internal Python muncul di narasi** (hal. 38): `run\\\_analysis()`, `classify\\\_all`, `export\\\_all()` pada penjelasan Gambar 4.3. Konvensi Anda: cukup modul tingkat pengguna (app.py, main.py, runner.py, analyzer.py, reporter.py). Tulis ulang interaksi dalam bahasa perilaku ("app.py mendelegasikan eksekusi analisis kepada main.py"), tanpa nama fungsi.
* **Penulisan miring *clean*/<i>suspicious</i>** sudah konsisten di hampir semua tempat (terverifikasi terprogram: 29 + 62 kemunculan miring). **Pengecualian tidak miring terdeteksi pada halaman PDF 43 dan 48** — berdasarkan pemetaan saya itu adalah hal. cetak 28 (paragraf definisi TP/TN/FP/FN di III.3.4.b) dan hal. cetak 33 (baris F07 Tabel 4.2). Mohon cek manual kedua titik itu; deteksi font otomatis bisa meleset.
* **Em dash:** tidak ditemukan di prosa (satu-satunya kemunculan ada di judul resmi ISO pada daftar pustaka — itu sah).

\---

## 2\. Typo \& Mekanik

|#|Lokasi|Fakta tertulis|Koreksi|
|-|-|-|-|
|1|hal. vi (Abstrak)|Kalimat terakhir diakhiri "…Tim LFD BSSN.."|Satu titik|
|2|hal. vi|Placeholder kosong: " + halaman + lampiran (2026)"|Isi, mis. "xiii + 76 halaman + 2 lampiran (2026)" — versi Inggris (hal. vii) sudah terisi, versi Indonesia belum|
|3|hal. vi|"Kata kunci : Forensik Memori (1), Triase (2), open-source (3), Otomatisasi (4)…"|Kapitalisasi tidak seragam (open-source huruf kecil sendiri); spasi sebelum titik dua|
|4|hal. viii (Kata Pengantar)|Baris berisi tanda titik tunggal yatim di bawah judul|Hapus|
|5|hal. xii (Daftar Gambar)|"Gambar 4.6 Eksekusi Otomatis **Empat** Plugin Volatility3" padahal caption aslinya di hal. 41 sudah "**Enam** Plugin"|Perbarui bidang daftar gambar (update field TOC)|
|6|hal. 5|"dimana" (II.1.1)|"di mana" — di tempat lain sudah benar (13×)|
|7|hal. 28|"Dataset pengujian terdiri dari **7 (lima)** sampel"|Angka dan huruf bertabrakan; final seharusnya "7 (tujuh)" dan seluruh paragraf disesuaikan (lihat §3.1)|
|8|hal. 29–30|"kuisioner" (3×, termasuk penyebut Persamaan 3.1 "Jawaban Kuisioner")|"kuesioner"; penyebut formula juga ambigu — sebaiknya "jumlah seluruh pernyataan kuesioner" agar konsisten dengan penjelasan di hal. 62|
|9|hal. 30 (Tabel 3.1)|Desimal titik: "79.99%", "59.99%", "39.99%", "19.99%"|Desimal koma sesuai PUEBI: "79,99%" dst.|
|10|hal. 41|Format pesan status "\[i/4] Menjalankan…"|Sisa era 4 plugin; harus "\[i/6]" (dan pastikan sesuai perilaku kode aktual)|
|11|hal. 65|\[22] "A. FFaizal"|"A. Faizal" (verifikasi ke sumber asli)|
|12|hal. 19|"mengukur tingkat penerimaan pengguna User Acceptance Test (UAT)"|Kata hilang: "…pengguna **melalui** User Acceptance Test (UAT)"|
|13|hal. 53|"di mana dari seluruh proses yang ditemukan pada sebuah memory dump **maka** platform…"|Konstruksi "yang… maka" tidak gramatikal; hapus "maka"|
|14|hal. 18|"…Tim LFD BSSN sebagai **platform pengguna utama** yang akan dikembangkan"|Urutan kata terbalik: "sebagai **pengguna utama platform** yang akan dibangun"|

\---

## 3\. Kejelasan (Clarity)

### 3.1 Inkonsistensi 4-vs-6: pemetaan lengkap

Ini masalah kejelasan paling serius. Pembaca tidak dapat memastikan berapa plugin, berapa aturan, dan berapa sampel yang sebenarnya dipakai. **Fakta tertulis, titik demi titik:**

|Lokasi|Tertulis|Seharusnya (desain final)|
|-|-|-|
|hal. 12–13 (II.1.8.a \& d)|Rogue Processes hanya 2 mekanisme (tanpa induk-anak); Process Objects = relasi induk-anak|II.1.8 masih struktur lama — bertentangan langsung dengan II.1.6 (hal. 10) yang sudah benar (Rogue = 3 mekanisme; Process Objects = DLL + LSASS)|
|hal. 26 (III.3.3.d)|"mengeksekusi **enam** plugin… yaitu" lalu hanya menyebut **empat** (pslist, pstree, netscan, malfind)|Tambahkan dlllist dan handles|
|hal. 26–27 (III.3.3.d)|"empat pemeriksaan", Process Objects = induk-anak|Struktur enam aturan dalam empat kelompok; Process Objects = DLL + LSASS|
|hal. 28 (III.3.4.b)|"7 (lima) sampel… **Kelima** sampel… **empat** memory dump terinfeksi… **empat** indikator"|7 sampel = 1 *baseline* + 6 terinfeksi, masing-masing menargetkan satu dari enam aturan|
|hal. 32 (Tabel 4.1 baris 2)|Deskripsi "Eksekusi otomatis **empat** plugin" vs Solusi "menjalankan **6** plugin" pada baris yang sama|"enam plugin" di kedua kolom (gaya angka konsisten: huruf)|
|hal. 32|Narasi "beserta **skala prioritas** dan solusi teknis"|Kolom prioritas sudah dihapus permanen dari Tabel 4.1 (keputusan desain berdasar ketiadaan data peringkat di transkrip) — narasi belum menyusul|
|hal. 38|"dievaluasi… melalui **keenam** heuristic rule" (Gambar 4.3) vs "analyzer.py yang mengimplementasikan **keempat** heuristic rule" (Gambar 4.4) — di halaman yang sama|Konsisten: enam aturan dalam empat kelompok tampilan (R1–R4) — jelaskan sekali, pakai konsisten|
|hal. 39|"kedelapan kebutuhan fungsional yang dirumuskan pada **Tabel 4.1**, yaitu F01 hingga F08"|F01–F08 ada di **Tabel 4.2**|
|hal. 41–47 (IV.4.1 item 3–6)|"aturan pertama/kedua/ketiga/keempat **dari empat heuristik**"; F03 tanpa induk-anak; F06 = induk-anak|Seluruh subbab implementasi masih struktur lama; harus ditulis ulang mengikuti F01–F08 final (R1a/R1b, R2, R3, R4a/R4b) — saya pahami penulisan ulang ini memang menunggu dataset 3–7 selesai|
|hal. 50 \& 58 (F08)|Berkas *results* "lima sheet" (4 plugin + Klasifikasi)|Dengan enam plugin: tujuh *sheet* — sesuaikan dengan perilaku reporter.py aktual|
|hal. 52 (NF03)|"**kelima** memory dump… masing-masing berukuran 5 GB"|Tujuh dataset; verifikasi ukuran aktual|
|hal. 56–57 (Tabel 5.1, F02)|"keenam plugin (windows.pslist, windows.pstree, windows.netscan, windows.malware.malfind)" — enam tapi daftar empat|Lengkapi daftar|
|hal. 59 (penutup V.1)|"eksekusi otomatis **keempat** plugin… deteksi **keempat** indikator"|keenam plugin; enam aturan|
|hal. 59 (V.2)|"menggunakan **lima** sampel… satu baseline dan **empat** terinfeksi" — di halaman yang sama dengan Tabel 5.2 yang berisi **tujuh** baris dataset baru|Tujuh|
|hal. 60–62|Narasi angka lama: 165 TN clean\_baseline; 845 proses; 10 TP; akurasi 99,88%; FP = MicrosoftEdgeUpdate.exe pada infected\_injection.raw; "13 pemicuan"; "tujuh pemicuan R3" — sementara **Tabel 5.2 dan 5.3 kosong**|Isi tabel dan tulis ulang seluruh narasi dari hasil regresi final pada kode terkini; angka lama tidak boleh tersisa|

**Interpretasi saya:** sebelum menulis ulang, tetapkan satu kalimat kanonik dan pakai di semua bab, misalnya: "Platform mengimplementasikan enam aturan deteksi yang terorganisasi dalam empat kelompok indikator SANS dan ditopang oleh enam plugin Volatility3." Kalimat semacam ini menghilangkan ambiguitas 4-vs-6 sekali untuk seluruh dokumen.

### 3.2 Abstrak Indonesia vs Abstract Inggris tidak sinkron (hal. vi–vii)

**Fakta tertulis.** Abstract Inggris: (a) menyebut eksplisit "in accordance with the international standard **ISO/IEC 27042**" — bertentangan dengan keputusan final (ISO tidak disebut eksplisit; landasan implisit di badan teks) dan dengan abstrak Indonesia yang sudah bersih dari ISO; (b) menyebut "**four** main anomaly indicators" vs "enam aturan deteksi heuristik" di versi Indonesia; (c) validasi hanya "functional testing", tanpa pengujian performa dan UAT yang disebut versi Indonesia; (d) tidak memuat angka hasil, sementara versi Indonesia memuat. Abstract Inggris tampak belum diregenerasi dari abstrak Indonesia terbaru. Terjemahkan ulang setelah abstrak Indonesia final.

### 3.3 Angka hasil di abstrak mendahului badan dokumen

**Fakta tertulis.** Abstrak (hal. vi) menyebut 1.127 proses dan spesifisitas 99,91%, tetapi tidak ada satu pun tempat di BAB V yang memuat angka itu (Tabel 5.2/5.3 kosong; narasi memuat 845/99,88%). Juga abstrak memakai metrik "spesifisitas", sedangkan III.3.4.b mendefinisikan metrik resmi sebagai Recall, Accuracy, dan FPR — spesifisitas tidak pernah didefinisikan di metodologi. Selaraskan: baik tambahkan definisi spesifisitas di III.3.4.b, atau laporkan FPR di abstrak.

### 3.4 Rumusan masalah dikutip menyimpang

**Fakta tertulis.** Hal. 53 mengklaim menjawab "rumusan masalah pertama, yaitu bagaimana platform dapat **mempercepat alur kerja analisis bukti digital**…", padahal RM (a) di hal. 3 berbunyi "…**mengotomatisasi deteksi indikator anomali pada proses sesuai kebutuhan Tim LFD**". Parafrase ini menggeser klaim dari otomatisasi ke percepatan — dan percepatan kuantitatif justru dinyatakan di luar lingkup dua paragraf kemudian. Kutip RM apa adanya.

### 3.5 Tujuan (c) tidak memakai kata kerja terukur

**Fakta tertulis + tambatan rekomendasi pembimbing.** I.4.1 (c): "**Mengetahui** tingkat penerimaan pengguna akhir…". Rekomendasi pembimbing eksplisit meminta kata kerja operasional yang dapat diukur, dan formulasi final yang pernah disepakati adalah "**mengukur** penerimaan Tim LFD melalui UAT". Ganti "Mengetahui" → "Mengukur".

### 3.6 Ambang keberhasilan tanpa dasar

**Fakta tertulis.** Target Recall ≥ 80%, Accuracy ≥ 80%, FPR ≤ 15% (hal. 28–29) tidak diberi rujukan atau justifikasi. **Interpretasi saya:** penguji hampir pasti menanyakan asal angka ini. Tiga jalur perbaikan yang jujur: tambatkan ke penelitian terkait yang memakai ambang serupa (jika memang ada — jangan dipaksakan), atau nyatakan eksplisit sebagai target rekayasa yang ditetapkan peneliti dengan argumen konteks triase (toleransi FN sangat rendah, toleransi FP moderat), atau tambatkan ke kebutuhan pengguna bila transkrip wawancara mendukung. Jangan biarkan tanpa keterangan.

\---

## 4\. Koherensi Antarparagraf

### 4.1 Redundansi di Latar Belakang (hal. 2) — beririsan dengan catatan pembimbing "hapus redundansi"

**Fakta tertulis.** Dua pasang duplikasi berdekatan: (a) kalimat "belum tersedia platform triase memori berbasis open-source yang secara spesifik mengotomatisasi deteksi indikator heuristik dalam satu alur kerja terpadu dan dapat beroperasi secara offline" diikuti dua kalimat kemudian oleh "belum ada yang secara spesifik mengintegrasikan deteksi indikator anomali heuristik dalam satu alur kerja triase otomatis yang dapat beroperasi secara offline…" — substansi identik; (b) "penelitian ini mengusulkan rancang bangun Platform Triase Forensik Memori Berbasis Volatility3" muncul dua kali dalam dua paragraf berurutan (hal. 2 bawah dan hal. 2–3). Padatkan menjadi satu pernyataan celah dan satu pernyataan usulan.

### 4.2 Ketegangan *fileless* antara motivasi dan batasan

**Fakta tertulis.** I.1 dan II.1.3 memotivasi urgensi forensik memori dengan *fileless malware* ("bukti kejahatan siber modern seringkali hanya dapat ditemukan di dalam RAM"), tetapi Batasan I.3 (d) menyatakan "Platform tidak mendeteksi teknik fileless malware", sementara R3 (malfind) justru mendeteksi injeksi kode — yang dalam banyak taksonomi termasuk teknik *fileless*. **Interpretasi saya:** batasan ini benar maksudnya tetapi salah rumusannya, dan dalam bentuk sekarang membuka celah pertanyaan penguji ("katanya tidak mendeteksi fileless, tapi malfind mendeteksi injeksi kode?"). Rumuskan ulang batasannya secara presisi, misalnya: platform tidak diklaim mampu mendeteksi seluruh spektrum teknik *fileless* maupun teknik evasif yang memanipulasi proteksi halaman pasca-alokasi; deteksi dibatasi pada indikator yang terjangkau enam aturan heuristik.

### 4.3 Alur Live/Dead Forensics (hal. 6)

**Fakta tertulis.** Paragraf pertama menutup dengan "pendekatan Live Forensics menjadi semakin esensial", lalu paragraf berikutnya membuka "penelitian ini berada dalam lingkup Dead Forensics". Kalimat jembatan sebenarnya ada ("karena objek yang dianalisis adalah memory dump yang telah diakuisisi"), tetapi urutan penyajian membuat pembaca menabrak kontradiksi dulu sebelum mendapat resolusi. **Interpretasi saya:** balik strukturnya — posisikan penelitian dulu (analisis *post-mortem* terhadap *dump* hasil akuisisi *live*), baru uraikan dua pendekatan sebagai konteks.

### 4.4 Logika urgensi triase (hal. 9)

**Fakta tertulis.** "…keputusan tentang proses mana yang perlu diselidiki lebih lanjut harus dapat dibuat dalam waktu singkat **sebelum kesempatan akuisisi terlewat**." Keputusan triase pada penelitian ini terjadi *setelah* akuisisi (objeknya *dump*), sehingga penalaran urgensinya salah tambat: urgensi akuisisi (volatilitas) dicampur dengan urgensi analisis (kecepatan respons insiden). Pisahkan kedua urgensi tersebut.

### 4.5 Transisi II.2 → II.3: celah tidak disintesiskan — beririsan dengan rekomendasi pembimbing

**Fakta tertulis.** Setelah Tabel 2.1 (hal. 15–16), teks langsung melompat ke Kerangka Konseptual tanpa paragraf sintesis. Rekomendasi pembimbing eksplisit meminta *summary statement* yang menegaskan celah ("apa yang sudah ada, apa yang belum, supaya terlihat novelty"). Lihat §5 untuk usulan isinya.

### 4.6 Penamaan pengujian tidak konsisten lintas bab — beririsan dengan rekomendasi pembimbing

**Fakta tertulis.** III.3.4 menamai tiga pengujian "Pengujian Fungsional / Pengujian Non-Fungsional / **Beta Testing**" (hal. 27–29), sedangkan BAB V memakai "**Alpha Testing** / Performance Testing / Beta Testing" (hal. 55–62), dan IV.4/IV.5 ikut menyebut "beta testing" (hal. 53–54). Rekomendasi pembimbing: hilangkan istilah alpha/beta. Konsekuensinya bukan sekadar ganti judul subbab — semua rujukan silang ikut berubah, dan sumber sitasi \[46] (yang khusus tentang alpha/beta testing) perlu ditinjau ulang relevansinya, termasuk Tabel 3.1 yang kategorinya diambil dari \[46].

### 4.7 Mixed-method perlu dipertegas — beririsan dengan rekomendasi pembimbing ("perlu diperjelas")

**Fakta tertulis.** III.2 memetakan kualitatif = wawancara + uji fungsional; kuantitatif = UAT + uji non-fungsional. **Interpretasi saya:** memasukkan uji fungsional *black box* (hasil biner PASS/FAIL) ke ranah kualitatif dapat dipertanyakan, dan UAT skala Guttman yang dihitung persentase memang kuantitatif tetapi datanya opini. Satu kalimat justifikasi per pemetaan (apa datanya, mengapa tergolong kualitatif/kuantitatif) akan menutup celah ini.

\---

## 5\. Kesenjangan Penelitian \& Kebaruan

### 5.1 Yang sudah baik (fakta tertulis)

Celah dirumuskan cukup spesifik di I.1: *open-source*, otomatisasi deteksi heuristik (bukan sekadar GUI), satu alur kerja terpadu, beroperasi *offline*, konteks operasional pemerintah. Positioning kontribusi juga jujur: III.3.4.b dan V.2 secara eksplisit membatasi klaim ("validasi fungsional pada skenario terkontrol, bukan tolok ukur generalisasi terhadap malware dunia nyata") — ini kekuatan metodologis yang jarang ada di laporan setingkat ini dan sebaiknya dipertahankan kata-katanya.

### 5.2 Kelemahan material

1. **Basis perbandingan tipis dan tidak dioperasionalkan.** Tabel 2.1 hanya memuat tiga penelitian (Fernando \& Rupasinghe 2022; Shakhsheer dkk. 2023; Zen dkk. 2025), dan kolom "Keterkaitan" mendeskripsikan kesamaan, bukan ketidakhadiran fitur yang menjadi celah. **Interpretasi saya:** tanpa mengubah format tabel warisan, tambahkan paragraf sintesis pasca-tabel yang memetakan secara eksplisit: Fernando \& Rupasinghe menyederhanakan CLI menjadi GUI tetapi deteksi tetap manual oleh analis; Shakhsheer dkk. mengotomatisasi analisis berbasis perbandingan dua *snapshot* (prasyarat *baseline* yang tidak selalu tersedia dalam respons insiden); ForenSeeker mengotomatisasi pemeriksaan multi-jenis bukti tetapi bukan triase memori dengan aturan deteksi anomali per proses. Baru tutup dengan pernyataan celah. Pastikan setiap karakterisasi di atas Anda verifikasi ulang terhadap papernya sebelum ditulis — jangan ambil dari ulasan ini tanpa cek.
2. **Klaim ketiadaan terlalu mutlak.** "Belum tersedia platform…" dan "belum ada yang…" (hal. 2) adalah klaim absen yang tidak mungkin dibuktikan. Lunakkan menjadi "sepanjang penelusuran literatur yang dilakukan penulis, belum ditemukan…". Murah diubah, mahal jika ditembak penguji.
3. **Diferensiasi terhadap ForenSeeker perlu satu kalimat tegas.** ForenSeeker \[17] satu lokus (BSSN) dan salah satu penulisnya adalah penguji II Anda. **Interpretasi saya:** pertanyaan "apa bedanya dengan ForenSeeker?" hampir pasti muncul di sidang 100%. Jawaban yang kuat sudah tersirat (kedalaman domain memori + deteksi anomali per proses + rekomendasi investigasi, vs platform pemeriksaan multi-bukti) — tuliskan eksplisit di paragraf sintesis II.2.
4. **Kebaruan bersifat integratif-kontekstual, bukan algoritmik — akui itu.** Enam aturan heuristik Anda diturunkan dari metodologi SANS dan literatur yang ada, bukan teknik deteksi baru. Dokumen pada umumnya sudah memposisikan ini dengan benar (operasionalisasi metodologi ke dalam platform tervalidasi di lokus nyata). Hindari kalimat apa pun yang bisa terbaca sebagai klaim kebaruan algoritme deteksi.

\---

## 6\. Prioritas Perbaikan

**P1 — Blokir kelulusan konsistensi (kerjakan sebelum bagian lain):**

1. Selesaikan dataset dan regresi final, lalu isi Tabel 5.2/5.3 dan tulis ulang seluruh narasi V.2 dari angka kode terkini; hapus semua angka generasi lama (hal. 59–62).
2. Sapu inkonsistensi 4-vs-6 memakai daftar di §3.1 sebagai *checklist* (15 titik).
3. Perbaiki enam sitasi kosong `\\\[]` di II.1.5 dan tiga referensi yatim \[8]\[9]\[15]; putuskan nasib \[9] (panggil atau buang).
4. Sinkronkan II.1.8 dengan II.1.6 (struktur aturan final).
5. Regenerasi Abstract Inggris dari abstrak Indonesia final; hapus penyebutan ISO/IEC 27042 di dalamnya; isi placeholder halaman abstrak Indonesia.
6. Tulis BAB VI Kesimpulan dan Saran (keterbatasan platform menyatu di VI.2) dan perbarui Daftar Isi.

**P2 — Substansi yang akan ditanyakan penguji:**
7. Justifikasi ambang 80/80/15 (§3.6).
8. Paragraf sintesis celah pasca-Tabel 2.1 + pelunakan klaim absen + diferensiasi ForenSeeker (§5).
9. Rumusan ulang batasan *fileless* (§4.2); kutip RM apa adanya di hal. 53 (§3.4); "Mengetahui" → "Mengukur" (§3.5).
10. Eliminasi istilah alpha/beta testing lintas III–V beserta tinjauan ulang \[46] (§4.6); perjelas pemetaan mixed-method (§4.7).
11. Perbaiki salah tambat sitasi wawancara \[10] dan verifikasi \[11] vs \[13] (§1.4).

**P3 — Mekanik (sapu terakhir sebelum cetak):**
12. Seluruh butir tabel §2; register informal §1.1; konsistensi biner/kuesioner/orkestrator/pembangunan §1.2; caption "Tabel Tabel" §1.3; perbaikan entri Daftar Pustaka §1.4; dua titik non-miring *clean*/*suspicious* §1.5.

\---

## 7\. Catatan Penutup

Kerangka dokumen ini sehat: metodologi DRM-Prototyping dijalankan runtut, keterlacakan kebutuhan (wawancara → SRS → F01–F08 → pengujian) terjaga, dan kejujuran epistemik bagian pengujian adalah nilai jual di hadapan penguji. Hampir semua masalah material bermuara pada satu hal yang sama — dokumen belum selesai bermigrasi ke desain final — dan itu sudah Anda ketahui serta rencanakan. Nilai tambah ulasan ini adalah peta lengkapnya, supaya ketika migrasi dilakukan tidak ada titik lama yang tertinggal dan saling bertentangan di hadapan penguji sidang 100%.

Hal yang belum dapat saya verifikasi dari berkas ini: isi visual seluruh gambar (hasil ekstraksi teks tidak memuat citra — khususnya apakah Gambar 4.5–4.14 masih menampilkan antarmuka era 4 aturan), kesesuaian Tabel 4.6 dengan dokumentasi umpan balik aslinya, dan ketepatan pemetaan halaman PDF→cetak untuk temuan italic (§1.5). Ketiganya perlu pemeriksaan manual.

