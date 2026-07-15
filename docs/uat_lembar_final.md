# LEMBAR USER ACCEPTANCE TEST (UAT) — Platform Triase Forensik Memori Berbasis Volatility3

Status: DRAF FINAL siap tempel ke Word (per 13 Juli 2026).
Basis format: Lembar UAT TA Stefanus Santori Zen (ForenSeeker) — struktur diikuti
(judul, pengantar, data responden, tabel Ya/Tidak, penutup tanda tangan), isi
disesuaikan penuh ke konteks Platform Triase Forensik Memori.
Skala: Guttman (Ya = 1, Tidak = 0). Ambang penerimaan: Tabel 3.1 (>= 60% = Diterima).
Persentase Penerimaan = (total jawaban "Ya") / (jumlah responden x jumlah pernyataan) x 100%.
Jumlah butir: 15 (3 aspek). Rencana responden: 7 orang (diusahakan memuat personel Tim LFD BSSN).

Catatan penyesuaian ke konteks TA (dibanding template Stefanus):
- Butir "instalasi" dan "Bot Telegram" milik Stefanus DIBUANG (tidak relevan; platform
  Kevin bukan berbasis instalasi kompleks / tanpa Bot Telegram).
- Butir generik "produktivitas/efektivitas" diganti butir yang menempel ke fitur nyata
  platform: eksekusi otomatis 6 plugin, klasifikasi clean/suspicious, Panel Detail
  Indikator, rekomendasi investigasi, ekspor CSV dan Excel, kemampuan offline.
- Aspek C mengikat langsung ke kebutuhan operasional Tim LFD (audiens sebenarnya).

===============================================================================
BAGIAN YANG DITEMPEL KE WORD MULAI DARI SINI
(Kop halaman: POLITEKNIK SIBER DAN SANDI NEGARA, samakan dengan template lampiran)
===============================================================================

# USER ACCEPTANCE TEST

Pengujian ini dilakukan guna memperoleh data tingkat penerimaan pengguna terhadap Platform Triase Forensik Memori Berbasis Volatility3 yang telah dibangun, baik dari sisi kesesuaian operasional maupun pengalaman pengguna. Diharapkan untuk mengisi kuesioner ini berdasarkan kondisi sebenarnya dengan cara memilih salah satu jawaban, yaitu "Ya" atau "Tidak", dengan memberikan tanda checklist (✓) pada jawaban yang dipilih.

Atas waktu dan kesediaan Anda untuk mengisi kuesioner ini, saya ucapkan terima kasih.

## DATA RESPONDEN

Nama:

Jabatan:

Instansi:

Sertifikasi Keahlian:

Hari/Tanggal:

Tempat:

Waktu:

---

### Aspek A — Kemudahan Penggunaan

| No | Pernyataan | Ya | Tidak |
|----|------------|:--:|:-----:|
| 1 | Antarmuka platform mudah dipahami sehingga analisis dapat dilakukan tanpa perlu menghafal perintah Volatility3 di baris perintah | | |
| 2 | Pemuatan memory dump dan proses memulai analisis mudah dilakukan melalui antarmuka | | |
| 3 | Informasi tahap analisis yang sedang berjalan ditampilkan dengan jelas selama proses berlangsung | | |
| 4 | Panel Detail Indikator beserta rekomendasi investigasi mudah dibaca dan dipahami | | |
| 5 | Secara keseluruhan, platform mudah dioperasikan | | |

### Aspek B — Kegunaan Fitur

| No | Pernyataan | Ya | Tidak |
|----|------------|:--:|:-----:|
| 6 | Eksekusi otomatis keenam plugin Volatility3 dalam satu proses membantu menyederhanakan pekerjaan analisis | | |
| 7 | Cakupan deteksi indikator anomali (rogue process, artefak jaringan, injeksi kode, dan objek proses) sudah relevan dengan kebutuhan analisis memori | | |
| 8 | Klasifikasi clean/suspicious membantu memfokuskan pemeriksaan pada proses yang paling memerlukan investigasi | | |
| 9 | Rekomendasi investigasi pada setiap indikator membantu menentukan langkah pemeriksaan lanjutan | | |
| 10 | Fitur ekspor hasil triase ke berkas CSV dan Excel bermanfaat untuk keperluan dokumentasi dan pelaporan | | |

### Aspek C — Relevansi terhadap Kebutuhan Operasional Tim LFD

| No | Pernyataan | Ya | Tidak |
|----|------------|:--:|:-----:|
| 11 | Keluaran platform relevan dengan kebutuhan triase awal pada analisis memori di Tim LFD | | |
| 12 | Kemampuan platform beroperasi secara offline sesuai dengan lingkungan kerja forensik yang terisolasi | | |
| 13 | Platform membantu mengurangi ketergantungan pada penafsiran keluaran mentah Volatility3 secara manual | | |
| 14 | Platform membantu mempermudah alur kerja triase awal dibandingkan analisis manual melalui baris perintah | | |
| 15 | Secara keseluruhan, platform layak digunakan sebagai alat bantu triase awal dalam pekerjaan Tim LFD | | |

---

Bogor, ................. 2026

Responden,




( ................................. )

===============================================================================
BAGIAN YANG DITEMPEL KE WORD SELESAI DI SINI
===============================================================================


## Lampiran pendukung (diisi SETELAH pelaksanaan UAT — untuk rekap Bab V)

### Rekap Responden

| Kode | Nama | Jabatan | Instansi | Sertifikasi |
|------|------|---------|----------|-------------|
| R-1 | | | | |
| R-2 | | | | |
| R-3 | | | | |
| R-4 | | | | |
| R-5 | | | | |
| R-6 | | | | |
| R-7 | | | | |

### Rekap Jawaban

| Kode | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | P10 | P11 | P12 | P13 | P14 | P15 | Ya |
|------|----|----|----|----|----|----|----|----|----|-----|-----|-----|-----|-----|-----|----|
| R-1 | | | | | | | | | | | | | | | | |
| R-2 | | | | | | | | | | | | | | | | |
| R-3 | | | | | | | | | | | | | | | | |
| R-4 | | | | | | | | | | | | | | | | |
| R-5 | | | | | | | | | | | | | | | | |
| R-6 | | | | | | | | | | | | | | | | |
| R-7 | | | | | | | | | | | | | | | | |
| Total | | | | | | | | | | | | | | | | |

Perhitungan:
- Total "Ya" = ..... dari (7 x 15 = 105)
- Persentase Penerimaan = (Total "Ya" / 105) x 100% = ..... %
- Kategori (Tabel 3.1) = ..... (>= 60% = Diterima)

Persentase per aspek (opsional, memperkuat pembahasan):
- Aspek A (P1-P5) = (Ya A) / (7 x 5) x 100% = ..... %
- Aspek B (P6-P10) = (Ya B) / (7 x 5) x 100% = ..... %
- Aspek C (P11-P15) = (Ya C) / (7 x 5) x 100% = ..... %

### Saran Responden

| Kode | Saran |
|------|-------|
| R-1 | |
| R-2 | |
| ... | |

Saran menjadi bahan langsung untuk subbab Saran di BAB VI.
