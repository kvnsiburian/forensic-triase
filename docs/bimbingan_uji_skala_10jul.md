# Status Uji Skala Ukuran Dump (dokumen kerja, dimutakhirkan)

**Nama:** Kevin Armando Siburian
**Program:** D-IV Rekayasa Keamanan Siber
**Asal:** catatan bimbingan Pak Rahmat 10 Juli 2026, lalu dimutakhirkan mengikuti
hasil capture 11 Juli dan keputusan ruang lingkup.

> Catatan penting: dokumen ini SUDAH direvisi dari versi 10 Juli. Versi lama
> memakai ukuran 5/12/20 GB dan mengklaim dump 12 & 20 GB berhasil di-capture.
> Itu keliru. Dump 12 & 20 GB via DumpIt ternyata rusak dan dibuang. Ukuran
> final berubah jadi 5/10/16 GB lewat .vmem. Isi di bawah ini yang berlaku.

---

## 1. Latar belakang (kenapa uji ini ada)

Uji ini menjawab masukan analis Lab Forensik Digital (LFD) BSSN saat sesi
demo/diskusi: minta ada pengujian pada beberapa ukuran dump, karena salah satu
plugin (malfind) diperkirakan melambat saat RAM yang dipindai membesar.

Uji ini bersifat tambahan/pelengkap, bukan syarat kelulusan. Jalur kritis tetap
UAT + penulisan bab. Uji ini memperkuat bab Hasil dan Pembahasan.

---

## 2. Apa yang sebenarnya dijawab uji ini (framing terkini)

**A. Kesanggupan memproses dump besar + karakterisasi durasi.**
Apakah platform sanggup memproses dump sampai 16 GB tanpa gagal, dan bagaimana
durasi tiap plugin berperilaku. Deteksi Rule 3 (code injection) harus tetap
benar (TP) di ketiga ukuran.

Catatan jujur ruang lingkup: ini uji "kesanggupan memproses dump besar", BUKAN
"uji beban RAM padat". RAM VM cuma dinaikkan alokasinya (5/10/16 GB), tapi isinya
tetap Windows diam + notepad, jadi RAM tambahan sebagian besar kosong. Karena itu
jumlah region malfind tidak membengkak, dan durasi tidak ikut meledak. Analis LFD
benar bahwa malfind melambat pada RAM besar yang padat aktivitas. Temuan kita
tidak membantah itu, cuma berada di sebelahnya. Uji RAM besar yang benar-benar
terisi penuh ditaruh sebagai saran penelitian lanjutan.

**B. Nilai otomasi platform (framing DIUBAH, lihat bagian 3).**
Versi lama mengukur "waktu platform vs waktu manual" pakai stopwatch. Ini
dibuang. Penggantinya di bagian 3.

---

## 3. Perubahan framing "nilai otomasi" (keputusan penting)

Versi lama mau membuktikan "platform lebih cepat dari kerja manual" pakai
stopwatch peneliti sendiri. Ini dibatalkan karena dua alasan yang jujur:

1. **Hasilnya sudah bisa ditebak.** Otomasi vs baca manual, jelas otomasi menang.
   Mengukur sesuatu yang jawabannya sudah pasti itu lemah secara penelitian.
2. **Tidak apple-to-apple.** Peneliti menanam malware sendiri, jadi sudah tahu
   notepad mana yang jahat. Stopwatch "manual" peneliti tidak jujur secara alami,
   dan penguji gampang merobohkannya.

**Gantinya, nilai platform ditunjukkan lewat ukuran yang objektif, bukan
stopwatch:**

- **Volume baca yang dipangkas.** Untuk satu dump, analis manual harus menyisir
  puluhan ribu baris output (contoh handles ~52 ribu baris, ditambah dlllist
  ribuan baris, netscan, malfind, dst). Platform memangkas itu jadi satu
  ringkasan proses mencurigakan. Angka baris ini objektif, tidak tergantung siapa
  yang mengukur, tidak bisa dituduh "curang karena tahu jawaban".
- **Keandalan dan kelengkapan.** Manual bergantung fokus dan stamina analis, bisa
  capek, bisa skip satu baris dari puluhan ribu. Platform menjalankan enam aturan
  yang sama persis setiap kali. Nilai jualnya bukan detik, tapi "seragam dan tidak
  ada yang terlewat". Di forensik ini justru yang penting.

Jadi klaim geser dari "lebih cepat" (lemah, sudah jelas, tidak adil) ke
"menghilangkan beban baca yang terukur besar + konsisten tanpa terlewat" (objektif,
kuat).

**Klaim yang tetap DIHINDARI (biar tak diserang penguji):**
- "Mesin platform lebih cepat dari Volatility3" — SALAH, mesin pemindainya sama.
- Menyeret angka percepatan multiprocessing ke klaim laporan — bukan basis uji ini.

---

## 4. Desain eksperimen (isolasi satu variabel: ukuran)

- **Variabel bebas:** ukuran dump (5 / 10 / 16 GB).
- **Yang dikunci:** skenario ancaman (r3 injection identik di ketiga ukuran),
  build OS, kode/analyzer (dibekukan), laptop pengukur, mode berurutan (bukan
  paralel, biar durasi per-plugin bersih dan bisa dibandingkan antar titik).

| Titik | RAM VM | Sumber dump | Format | Isi |
|---|---|---|---|---|
| 1 | 5 GB | `infected_r3_injection.raw` (sudah ada dari Dataset 5) | RAW (DumpIt) | r3 injection |
| 2 | 10 GB | `infected_r3_injection_10gb.vmem` (capture baru) | .vmem (suspend VM) | r3 injection (sama) |
| 3 | 16 GB | `infected_r3_injection_16gb.vmem` (capture baru) | .vmem (suspend VM) | r3 injection (sama) |

**Kenapa r3 injection:** sekalian membuktikan deteksi Rule 3 tetap benar (TP) di
5/10/16 GB, aturan tak jebol saat dump membesar.

**Kenapa 3 ukuran, bukan 18 (6 dataset x 3 ukuran):** durasi ditentukan oleh apa
yang dipindai, bukan jenis ancaman. 18 dump = mengukur variabel yang sama
berulang + mencampur dua variabel sekaligus (tidak bersih).

**Kenapa 5/10/16 GB:** host 31,7 GB. VM 16 GB menyisakan ~15,7 GB untuk host =
aman dari swap/crash. Ukuran lebih besar dari itu terlalu mepet, ditolak.

**Kenapa ada RAW (5 GB) dan ada .vmem (10/16 GB):** titik 5 GB pakai ulang dump
lama yang memang RAW dari DumpIt. Dua titik baru diambil lewat suspend VM (.vmem)
karena percobaan DumpIt untuk ukuran besar gagal (lihat bagian 6). Bagi Volatility3,
RAW dan .vmem dibaca sama; format bukan penyebab beda durasi.

Sikap penulisan (diputuskan Kevin 12 Jul): TULIS TERUS TERANG + alasan. Bahan
kalimat siap-pakai (dipasang saat menulis bab uji skala, belum masuk Word):

> Kalimat bab: "Titik uji 5 GB menggunakan berkas berformat RAW hasil akuisisi
> DumpIt, sedangkan titik 10 GB dan 16 GB menggunakan berkas berformat .vmem
> hasil suspend mesin virtual VMware. Kedua format merupakan citra mentah isi RAM
> dan dibaca oleh Volatility3 melalui layer pembaca masing-masing, sehingga hasil
> analisisnya setara dan tetap dapat diperbandingkan. Deteksi Rule 3 pada notepad
> terinjeksi tetap benar (True Positive) pada ketiga berkas, yang menunjukkan
> perbedaan format tidak memengaruhi keluaran deteksi."

> Kalimat Keterbatasan: "Titik uji 5 GB berformat RAW karena memanfaatkan dump
> yang telah tersedia, sementara titik 10 GB dan 16 GB berformat .vmem karena
> akuisisi langsung pada ukuran tersebut tidak stabil sehingga citra memori
> diambil melalui mekanisme suspend mesin virtual. Perbedaan sumber ini disebutkan
> apa adanya; bagi Volatility3 kedua format setara."

Catatan: di Keterbatasan sengaja pakai "akuisisi langsung tidak stabil", BUKAN
"DumpIt rusak/gagal" yang vulgar. Jujur tapi tak membuka luka lebar. Jawaban lisan
sidang kalau dikejar: sama isinya, tekankan yang menentukan durasi adalah jumlah
objek dipindai, bukan format. Nyambung ke catatan penguji Jeckson #8 (asal dump).

**Skenario r3 injection (identik 3 ukuran):** payload meterpreter reflective DLL
di-`migrate` ke proses sah `notepad.exe` (nama asli, path System32, induk
explorer.exe). Ini meninggalkan segmen PAGE_EXECUTE_READWRITE + PrivateMemory =
artefak yang dideteksi Rule 3. Koneksi C2 disenyapkan (`sleep 300`) sebelum
capture, sehingga Rule 2 (network) tetap diam. Hasilnya isolasi Rule 3 murni.

---

## 5. Cara mengukur

**Sisi PLATFORM:** satu kali analisis (mode berurutan). Durasi diambil dari timer
internal (`--timing`), bukan stopwatch tangan. Sudah mencakup Volatility3 +
analisis + export.

**Sisi "beban manual" (pengganti stopwatch):** tidak pakai stopwatch. Cukup catat
berapa banyak baris output yang harus dibaca analis kalau menjalankan 6 plugin
Volatility3 mentah (jumlah baris handles, dlllist, dst), lalu bandingkan dengan
satu ringkasan yang disajikan platform. Ini bukti volume, bukan lomba waktu.

---

## 6. Status pengerjaan (dimutakhirkan 11 Juli 2026)

### 6.1 SUDAH SELESAI

**a. Instrumentasi timer di kode (commit `2562dbd`, sudah di-push):**
- `core/runner.py`: `run_plugin_timed()` membungkus eksekusi plugin dengan
  `time.perf_counter` (murni pengukur, tidak mengubah hasil).
- `main.py`: flag CLI `--timing` yang mencetak tabel durasi per-plugin + total dan
  menulis berkas `<dump>_timing.csv`.
- Diverifikasi tidak mengubah deteksi: regression tetap TP=7 / FP=1 / FN=0.

**b. Percobaan DumpIt 12 & 20 GB GAGAL, dump dibuang.**
Percobaan awal memakai DumpIt untuk 12 & 20 GB. Kedua dump ternyata rusak:
live-capture tidak konsisten pada dump besar, DTB tak cocok isi RAM, malfind 0,
R3 tidak menyala. Dibuktikan dari pslist patah (hanya 24/5 proses vs ~179 sehat),
psscan tetap penuh (83), memmap notepad hilang ~47%. Kedua dump dibuang. Solusi:
pindah ke .vmem (suspend VM). Inilah alasan ukuran final jadi 5/10/16 GB, bukan
5/12/20 GB.

**c. Capture 10 & 16 GB via .vmem BERHASIL dan terverifikasi (11 Jul).**
Tersimpan di `/mnt/d/forensic_triase/dataset_update/`. Wajib pasangan .vmem +
.vmss dengan nama cocok di folder sama; kalau .vmss hilang Vol3 gagal memetakan
(pslist jeblok, notepad hilang). Hasil verifikasi sehat + R3 TP:
- 5 GB .raw: pslist 147 proses, notepad TP.
- 10 GB .vmem: pslist 137 proses, notepad PID 6236, malfind PAGE_EXECUTE_READWRITE -> TP.
- 16 GB .vmem: pslist 146 proses, notepad PID 7704, malfind PAGE_EXECUTE_READWRITE -> TP.

### 6.2 Tabel A lengkap (durasi platform per-plugin, mode berurutan, detik)

| Plugin | 5 GB | 10 GB | 16 GB |
|---|---|---|---|
| pslist | 1,37 | 1,42 | 1,38 |
| pstree | 3,14 | 2,98 | 4,35 |
| netscan | 42,81 | 62,31 | 45,93 |
| **malfind** | **134,47** | **113,60** | **113,07** |
| dlllist | 39,32 | 30,65 | 32,18 |
| handles | 107,46 | 102,86 | 116,56 |
| **Total** | **328,57** | **313,81** | **313,46** |

Ketiga ukuran: notepad R3 = TP. netscan dan export xlsx tidak crash (fix af1d436
jalan).

### 6.3 Temuan kunci (durasi ikut jumlah objek, bukan ukuran dump)

| | 5 GB | 10 GB | 16 GB |
|---|---|---|---|
| region malfind | 100 | 95 | 90 |
| durasi malfind (dtk) | 134,47 | 113,60 | 113,07 |
| handles (objek) | 52206 | 46852 | 50938 |

Ukuran dump NAIK tapi region malfind TURUN, dan durasi malfind ikut turun (searah
region, lawan ukuran). Total stabil 313-329 detik walau dump membesar. Ini jawaban
untuk penguji kalau bertanya "kok 5 GB malah paling lambat": bukan karena format
.raw, tapi karena region malfind-nya paling banyak (100). Jangan salah bilang
".raw lebih lambat"; bagi Vol3 .raw dan .vmem sama.

### 6.4 BELUM

- Tulis narasi Hasil, Pembahasan, dan Keterbatasan dengan framing baru (bagian 3).
- Selesaikan diskusi satu per satu: RAW vs .vmem (cara menulis di laporan),
  fileless yang dilewati, dan isi persis rumusan masalah setelah perbandingan
  manual dibuang.

---

## 7. Bentuk penyajian hasil yang dituju (terkini)

**Tabel A — durasi platform per-plugin vs ukuran (detik):** sudah lengkap di 6.2.

**Tabel B (platform vs manual, stopwatch): DIBUANG.** Diganti penyajian volume
baca yang dipangkas (jumlah baris output yang tidak perlu lagi dibaca analis) +
argumen keandalan/kelengkapan (aturan sama tiap kali, tidak ada yang terlewat).
Lihat bagian 3.

---

## 8. Keterbatasan yang ditulis jujur (memperkuat kredibilitas)

1. RAM VM dinaikkan alokasi (5/10/16 GB) tapi beban kerja isinya tetap ringan,
   jadi ini uji kesanggupan memproses dump besar, bukan uji RAM padat aktivitas.
   Uji RAM besar terisi penuh = saran penelitian lanjutan.
2. Pengukuran durasi dari satu laptop, satu kali jalan per titik. Idealnya banyak
   ulangan. Pengakuan ini memperkuat kredibilitas, bukan melemahkan.
3. Titik 5 GB berformat RAW, dua titik lain .vmem. Bagi Vol3 sama, tapi perbedaan
   sumber ini disebut apa adanya.

---

## 9. Hal yang masih perlu diputuskan / didiskusikan

1. Isi persis rumusan masalah setelah perbandingan manual (stopwatch) dibuang.
2. Cara menuliskan alasan RAW (5 GB) vs .vmem (10/16 GB) di laporan.
3. Apakah menyinggung fileless vs filebased atau tidak.
4. Penempatan uji ini di laporan: sub-bab Hasil tersendiri atau digabung dengan
   pengujian deteksi.
