# Revisi III.3 DESAIN PENELITIAN — Cari/Ganti siap-pakai

Status: draf per 14 Juli 2026. Basis tracing: III.3 milik Kevin (docx terbaru) vs
III.3 dua senior DRM (Fransiska Artia \& Yasmin), plus telaah Gambar 3.1 \& 3.2.

Aturan main: SEMUA perubahan lewat Cari/Ganti yang Kevin terapkan sendiri di Word.
Claude tidak menyentuh .docx maupun gambar. No em dash. Italic ditandai *asterisk*
(saat di Word, blok kata itu lalu Ctrl+I). Penomoran/format = urusan Kevin.

Ringkas temuan tracing:

* Kerangka III.3 Kevin PALING lengkap dari ketiganya (satu-satunya yang punya
paragraf penjelas Gambar 3.1; Descriptive Study II jauh lebih kaya). Arah revisi
BUKAN rombak besar, tapi poles bertarget.
* 1 ketidakcocokan gambar vs teks (SANS di kotak Quick Plan Gambar 3.1) -> diselaraskan
lewat teks (keputusan Kevin: "Selaraskan teks ke gambar").
* Beberapa rapian diksi \& pengayaan tipis di titik lemah.

Catatan yang HANYA dilaporkan (tidak diubah, karena format/gambar = urusan Kevin):

* Gaya penanda tahap Prototyping (Communication, Quick Plan, dst.) sekarang heading
polos; Fransiska \& Yasmin pakai a/b/c/d/e. Kevin memilih biarkan (format).
* "Modeling Quick Design" (par 739) idealnya "Modeling and Quick Design" biar sama
dengan roda Gambar 3.2 \& Fransiska. Ini format heading -> Kevin putuskan sendiri.

===============================================================================

## GANTI 1 — DIBATALKAN (14 Jul): diselesaikan lewat GAMBAR, bukan teks

===============================================================================

Keputusan Kevin 14 Jul: kotak di Gambar 3.1 diubah dari
"Perencanaan cepat (SANS Memory Forensics Methodology)" menjadi
"Perencanaan cepat" saja (buang tempelan SANS). Ini lebih benar secara metodologi
karena SANS Memory Forensics Methodology adalah acuan tahap DETEKSI anomali
(muncul di Modeling par 742 dan Modul Pemeriksaan par 765), BUKAN isi Quick Plan.

KONSEKUENSI: par 737 Quick Plan TIDAK diubah. Tidak ada Cari/Ganti untuk poin ini.
Pekerjaan ada di gambar (urusan Kevin), bukan teks.

\---

===============================================================================

## GANTI 2 — Paragraf pembuka DRM: kaitkan alasan pemilihan ke celah manual

===============================================================================

MASALAH: par 719 kuat menjelaskan APA itu DRM dan kenapa cocok untuk artefak, tapi
belum menautkan pemilihan DRM ke persoalan nyata (analisis manual yang jadi latar
belakang). Fransiska mengaitkan DRM ke fokus penelitiannya secara eksplisit; punyamu
bisa dibuat sekuat itu dengan satu tautan ke kondisi lokus.

CARI (kalimat di par 719, persis):
Hal ini sesuai dengan fokus penelitian ini, yaitu merancang dan membangun platform triase forensik memori berbasis Volatility3 yang dibutuhkan oleh Tim Laboratorium Forensik Digital.

GANTI:
Hal ini sesuai dengan fokus penelitian ini, yaitu merancang dan membangun platform triase forensik memori berbasis Volatility3 yang dibutuhkan oleh Tim Laboratorium Forensik Digital. Kerangka yang berangkat dari klarifikasi masalah menuju solusi ini selaras dengan konteks penelitian, karena persoalan yang diangkat bermula dari kendala analisis memori yang selama ini dikerjakan secara manual, sehingga arah solusinya perlu ditetapkan secara bertahap dan empiris.

STATUS: SUDAH DITERAPKAN & verified 14 Jul (mtime 15:26). Kevin memangkas ujungnya
jadi "secara bertahap" (tanpa "dan empiris") -> lebih ringkas, disetujui.

===============================================================================
## GANTI 2b — Manusiakan kalimat alasan pemilihan DRM (par 719, kalimat [40])
===============================================================================

MASALAH: kalimat "DRM dipilih karena kemampuannya menyediakan kerangka kerja yang
terstruktur dan empiris untuk mengembangkan solusi berbasis desain secara
sistematis..." menumpuk kata sifat abstrak (terstruktur, empiris, sistematis)
sehingga terasa kaku/robotik. Versi A dipilih: alasan praktis di depan, istilah
metodologis menyusul. Sitasi [40] tetap di ujung.

CARI (kalimat par 719, persis):
DRM dipilih karena kemampuannya menyediakan kerangka kerja yang terstruktur dan empiris untuk mengembangkan solusi berbasis desain secara sistematis, dimulai dari klarifikasi masalah hingga evaluasi solusi dalam konteks dunia nyata [40].

GANTI:
DRM dipilih karena metode ini menuntun penelitian langkah demi langkah, mulai dari memperjelas masalah sampai menguji solusinya langsung pada kondisi nyata di lapangan. Alurnya yang tertata dan berdasar pada bukti membuat pengembangan solusi rancang bangun dapat dilakukan secara teratur [40].

===============================================================================
## GANTI 2c — Manusiakan kalimat "Metode DRM merupakan metodologi..." (par 719)
===============================================================================

MASALAH: "Metode DRM merupakan metodologi yang dirancang untuk..." berputar
(metode = metodologi), dan "menghasilkan ... sebagai luaran utama" terasa
administratif. Versi B dipilih: lebih tegas & padat, platform diletakkan tegas.

CARI (kalimat par 719, persis):
Metode DRM merupakan metodologi yang dirancang untuk penelitian berorientasi perancangan dan pembangunan artefak teknis, sehingga sesuai dengan tujuan penelitian ini yang menghasilkan platform triase forensik memori sebagai luaran utama.

GANTI:
Metode ini dirancang untuk penelitian yang berujung pada pembangunan artefak teknis, sehingga sejalan dengan penelitian ini yang menghasilkan platform triase forensik memori sebagai luaran utamanya.

===============================================================================
## GANTI 8 — III.3.2 Descriptive Study I: buang pengulangan "analisis" & jargon (par 728)
===============================================================================

MASALAH: dalam 1 paragraf, bentukan "analisis" muncul 5 kali (terasa berputar),
dan "memposisikan kontribusi penelitian ini secara akademis" terasa jargon.
Versi B dipilih: mengalir tanpa penanda pertama/kedua (konsisten gaya III.3 lain),
pengulangan & jargon dibereskan. Kalimat penutup "Keluaran tahap ini..." TIDAK
diubah (sudah kuat via GANTI 3), jadi CARI hanya 3 kalimat pertama.

CARI (3 kalimat pertama par 728, persis):
Pada tahap Descriptive Study I, dilakukan analisis terhadap penelitian-penelitian terdahulu yang berkaitan dengan pembangunan platform forensik memori berbasis Volatility3 serta otomatisasi analisis memory dump. Analisis ini bertujuan untuk mengidentifikasi celah penelitian yang belum terjawab dan memposisikan kontribusi penelitian ini secara akademis. Selain itu, dilakukan analisis terhadap kondisi operasional Tim Laboratorium Forensik Digital saat ini, khususnya terhadap kendala yang dihadapi dalam proses analisis memori secara manual menggunakan command line interface.

GANTI:
Pada tahap Descriptive Study I, penelitian terdahulu yang berkaitan dengan pembangunan platform forensik memori berbasis Volatility3 dan otomatisasi analisis memory dump ditelaah untuk menemukan celah yang belum terjawab sekaligus menempatkan kontribusi penelitian ini di antara karya yang sudah ada. Selain itu, kondisi operasional Tim Laboratorium Forensik Digital saat ini ditinjau, khususnya kendala yang dihadapi saat analisis memori masih dikerjakan secara manual melalui command line interface.

\---

===============================================================================

## GANTI 3 — Descriptive Study I: pertegas keluaran tahap (biar tak menggantung)

===============================================================================

MASALAH: par 728 sudah baik, tapi kalimat penutupnya ("Hasil dari tahap ini menjadi
dasar perancangan solusi pada tahap berikutnya...") agak umum. Senior (Fransiska)
menutup tiap tahap dengan menyebut keluaran konkret yang mengalir ke tahap
berikutnya. Kita pertegas keluaran Descriptive Study I supaya rantai antar tahap
DRM terasa mengalir.

CARI (kalimat penutup par 728, persis):
Hasil dari tahap ini menjadi dasar perancangan solusi pada tahap berikutnya, dengan memastikan bahwa platform yang dibangun benar-benar menjawab kebutuhan nyata di lapangan.

GANTI:
Keluaran tahap ini berupa gambaran celah penelitian dan potret kondisi operasional saat ini, yang menjadi dasar perancangan solusi pada tahap Prescriptive Study agar platform yang dibangun benar-benar menjawab kebutuhan nyata di lapangan.

\---

===============================================================================

## GANTI 4 — Prescriptive Study: sinkronkan istilah "engine" -> konsisten

===============================================================================

MASALAH: sepanjang III.3 kamu memakai istilah "engine analisis". Ini istilah asing
yang muncul berulang (par 725, 737, 760). Untuk laporan yang terbaca natural dan
konsisten dengan gaya Indonesia, satu istilah baku lebih rapi. TAPI ini opsional:
kalau kamu memang mau pertahankan "engine" (istilah teknis yang lazim di forensik),
LEWATI ganti ini. Aku sertakan sebagai pilihan, bukan keharusan.

(OPSIONAL — terapkan hanya bila kamu setuju menyeragamkan)
CARI: sebagai engine analisis utama
GANTI: sebagai mesin analisis utama

Catatan: "engine" pada "engine ekstraksi artefak memori" (par 760) boleh dibiarkan
kalau kamu anggap itu istilah teknis. Konsistensi penuh = ganti semua "engine"
jadi "mesin"; tapi keputusan ada padamu. Kalau ragu, LEWATI ganti 4 seluruhnya.

\---

===============================================================================

## GANTI 5 — Communication: pertegas hasil jadi kebutuhan fungsional/non-fungsional

===============================================================================

MASALAH: par 735 (Communication) sudah menyebut hasil diturunkan jadi kebutuhan
fungsional dan non-fungsional, tapi kalimat penutupnya ("Hasil perumusan kebutuhan
pada tahap ini menjadi dasar bagi penyusunan perencanaan pada tahap berikutnya")
mengulang pola "jadi dasar tahap berikutnya" yang sama persis dengan beberapa tahap
lain. Kita variasikan sedikit agar tidak terasa mengulang, sekaligus menegaskan
keluaran konkretnya (dokumen kebutuhan/SRS).

CARI (kalimat penutup par 735, persis):
Hasil perumusan kebutuhan pada tahap ini menjadi dasar bagi penyusunan perencanaan pada tahap berikutnya.

GANTI:
Rumusan kebutuhan fungsional dan non-fungsional yang dihasilkan pada tahap ini menjadi acuan yang mengikat bagi perencanaan pembangunan platform pada tahap Quick Plan.

\---

===============================================================================

## GANTI 6 — Gambar 3.1: paragraf penjelas, samakan urutan dengan swimlane gambar

===============================================================================

MASALAH: par 722 menjelaskan alur DRM dengan sangat baik. Tapi diagram Gambar 3.1-mu
menampilkan empat swimlane berurut (Research Clarification, Descriptive Study I,
Prescriptive Study, Descriptive Study II) DAN di swimlane Prescriptive Study
kotaknya adalah 5 tahap Prototyping. Paragraf penjelas belum menyebut bahwa 5 tahap
Prototyping itulah isi swimlane Prescriptive Study di gambar. Menambah satu kalimat
penutup membuat pembaca bisa memetakan teks ke gambar secara langsung.

CARI (kalimat penutup par 722, persis):
Penelitian dimulai dari tahap Research Clarification untuk menetapkan rumusan masalah dan kebutuhan platform, dilanjutkan dengan Descriptive Study I untuk menganalisis kondisi operasional saat ini, kemudian Prescriptive Study untuk merancang dan membangun platform menggunakan model Prototyping, dan diakhiri dengan Descriptive Study II untuk mengevaluasi platform melalui serangkaian pengujian.

GANTI:
Penelitian dimulai dari tahap Research Clarification untuk menetapkan rumusan masalah dan kebutuhan platform, dilanjutkan dengan Descriptive Study I untuk menganalisis kondisi operasional saat ini, kemudian Prescriptive Study untuk merancang dan membangun platform menggunakan model Prototyping, dan diakhiri dengan Descriptive Study II untuk mengevaluasi platform melalui serangkaian pengujian. Sebagaimana tampak pada Gambar 3.1, kelima tahap pada model Prototyping berada di dalam kotak Prescriptive Study, sedangkan rangkaian pengujian pada Descriptive Study II mencakup uji fungsional, uji non-fungsional, dan User Acceptance Test.

\---

===============================================================================

## RINGKASAN URUTAN PENERAPAN

===============================================================================

DIBATALKAN:

* GANTI 1  -> diselesaikan lewat GAMBAR (kotak "Perencanaan cepat" saja),
par 737 TIDAK diubah.

Wajib (memperkuat alur):

1. GANTI 2  (pembuka DRM + tautan manual) -> par 719
2. GANTI 6  (penjelas Gambar 3.1)         -> par 722

Disarankan (mengalirkan rantai antar tahap):
3. GANTI 3  (keluaran Descriptive Study I) -> par 728
4. GANTI 5  (keluaran Communication)       -> par 735

Opsional (konsistensi istilah, boleh dilewati):
5. GANTI 4  (engine -> mesin)

Setelah kamu terapkan, kabari "sudah". Aku verifikasi ke disk (mtime berubah +
needle lama hilang + needle baru muncul) sebelum tandai selesai.

