# Instrumen User Acceptance Test (UAT) — Platform Triase Forensik Memori

Status: DRAF instrumen (UAT belum dijalankan per 8 Juli 2026).
Basis format: LAMPIRAN 5 TA Stefanus Santori Zen (ForenSeeker) — kerangka diadopsi,
isi diadaptasi ke platform triase memori (tanpa Bot Telegram / eksaminasi multi-bukti).
Skala: Guttman (Ya = 1, Tidak = 0). Kategori penerimaan: Tabel 3.1 (≥60% = Diterima).
Persentase Penerimaan = (total "Ya") / (jumlah responden × jumlah pernyataan) × 100%.

Rencana responden: 7 orang (komposisi final menyusul; usahakan memuat personel Tim LFD BSSN).

---

## A. Kuesioner

Kop: POLITEKNIK SIBER DAN SANDI NEGARA (sama seperti template).

Pengantar:
> Pengujian ini dilakukan guna memperoleh data tingkat penerimaan pengguna terhadap
> Platform Triase Forensik Memori Berbasis Volatility3 yang telah dibangun, baik dari
> kesesuaian operasional hingga pengalaman pengguna. Diharapkan mengisi kuesioner ini
> berdasarkan kondisi sebenarnya dengan memilih salah satu jawaban, "Ya" atau "Tidak",
> dengan memberikan tanda checklist (✓) pada jawaban yang dipilih. Atas waktu dan
> kesediaan Anda, saya ucapkan terima kasih.

DATA RESPONDEN: Nama · Jabatan · Instansi · Sertifikasi Keahlian · Hari/Tanggal · Tempat · Waktu

### Pernyataan (15 butir, 3 aspek)

**Aspek A — Kemudahan Penggunaan**
| No | Pernyataan | Ya | Tidak |
|----|-----------|----|-------|
| 1 | Antarmuka grafis platform mudah dipahami sehingga analisis dapat dilakukan tanpa menghafal perintah Volatility3 | | |
| 2 | Pemuatan memory dump dan proses memulai analisis mudah dilakukan melalui antarmuka | | |
| 3 | Progress bar dan status bar memudahkan pemantauan tahap analisis yang sedang berjalan | | |
| 4 | Panel Detail Indikator beserta rekomendasi investigasi mudah dibaca dan dipahami | | |
| 5 | Secara keseluruhan, platform mudah dioperasikan | | |

**Aspek B — Kegunaan Fitur**
| No | Pernyataan | Ya | Tidak |
|----|-----------|----|-------|
| 6 | Eksekusi otomatis keenam plugin Volatility3 dalam satu proses membantu menyederhanakan pekerjaan analisis | | |
| 7 | Deteksi indikator anomali (proses rogue, artefak jaringan, injeksi kode, dan objek proses) mencakup indikator yang relevan dalam analisis memori | | |
| 8 | Klasifikasi clean/suspicious membantu memfokuskan pemeriksaan pada proses yang paling memerlukan investigasi | | |
| 9 | Rekomendasi investigasi per indikator membantu menentukan langkah pemeriksaan lanjutan | | |
| 10 | Fitur ekspor hasil triase ke berkas Excel bermanfaat untuk keperluan dokumentasi dan pelaporan | | |

**Aspek C — Relevansi Output terhadap Kebutuhan Operasional Tim LFD**
| No | Pernyataan | Ya | Tidak |
|----|-----------|----|-------|
| 11 | Keluaran platform relevan dengan kebutuhan triase awal analisis memori di Tim LFD | | |
| 12 | Kemampuan platform beroperasi secara offline sesuai dengan kebutuhan lingkungan kerja forensik | | |
| 13 | Platform membantu mengurangi ketergantungan pada interpretasi keluaran mentah Volatility3 secara manual | | |
| 14 | Platform membantu mempermudah dan mempercepat alur kerja triase dibandingkan analisis manual melalui command line | | |
| 15 | Secara keseluruhan, platform layak digunakan sebagai alat bantu triase awal dalam pekerjaan Tim LFD | | |

Penutup: "Bogor, ……… 2026" + ruang tanda tangan "Responden".

> Opsi ringkas 12 butir (4 per aspek): buang No. 3, 6, dan 12.

---

## B. Responden (isi setelah pelaksanaan)

| Kode | Nama | Jabatan | Instansi | Sertifikasi |
|------|------|---------|----------|-------------|
| R-1 | | | | |
| R-2 | | | | |
| R-3 | | | | |
| R-4 | | | | |
| R-5 | | | | |
| R-6 | | | | |
| R-7 | | | | |

---

## C. Hasil UAT (isi setelah pelaksanaan)

| Kode | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | P10 | P11 | P12 | P13 | P14 | P15 |
|------|----|----|----|----|----|----|----|----|----|-----|-----|-----|-----|-----|-----|
| R-1 | | | | | | | | | | | | | | | |
| R-2 | | | | | | | | | | | | | | | |
| R-3 | | | | | | | | | | | | | | | |
| R-4 | | | | | | | | | | | | | | | |
| R-5 | | | | | | | | | | | | | | | |
| R-6 | | | | | | | | | | | | | | | |
| R-7 | | | | | | | | | | | | | | | |

Perhitungan: Total "Ya" = … dari (7 × 15 = 105) → Persentase Penerimaan = …% → Kategori (Tabel 3.1) = …

Opsional (memperkuat pembahasan): persentase per aspek —
Aspek A = (Ya A)/(7×5), Aspek B = (Ya B)/(7×5), Aspek C = (Ya C)/(7×5).

---

## D. Saran Responden (isi setelah pelaksanaan)

| Kode | Saran |
|------|-------|
| R-1 | |
| … | |

Saran-saran ini menjadi bahan langsung untuk subbab Saran di BAB VI.
