# Revisi TA — Edit CARI/GANTI (Abstrak + BAB IV + BAB V.1/V.2)

Sumber kebenaran: regresi final `regression_test.py` (8 Juli 2026) —
1127 PID, TP=7, FP=1, FN=0, TN=1119. Recall=100%, Accuracy=99,91%, FPR=0,09%, Precision=87,5%.
FP tunggal: `PaintStudio.Vi` (Paint 3D) di clean_baseline, kena R2 (telemetri Microsoft/Azure 48.209.133.15:443).

Kalimat kanonik (pakai konsisten): *"Platform mengimplementasikan enam aturan deteksi yang
terorganisasi dalam empat kelompok indikator SANS dan ditopang oleh enam plugin Volatility3."*

Keputusan: judul subbab BAB V mengikuti BAB III persis → **Pengujian Fungsional / Pengujian Non-Fungsional / User Acceptance Test (UAT)** (alpha/beta dibuang).
Metrik Abstrak: **Recall + FPR** (keduanya terdefinisi di III.3.4.b).

> V.3 (UAT) dan BAB VI menyusul setelah angka UAT riil diberikan.

---

## BAGIAN A — ABSTRAK

### A1. Abstrak Indonesia — kalimat metrik (hal. vi)
**CARI:**
> Hasil pengujian performa menunjukkan sensitivitas deteksi sebesar 100% dan spesifisitas sebesar 99,91%, sejalan dengan desain platform yang memprioritaskan minimnya ancaman yang terlewat.

**GANTI:**
> Hasil pengujian non-fungsional menunjukkan Recall (sensitivitas) deteksi sebesar 100% dengan False Positive Rate sebesar 0,09%, sejalan dengan desain platform yang memprioritaskan minimnya ancaman yang terlewat.

### A2. Abstrak Indonesia — kata "pengujian performa" di kalimat validasi (hal. vi)
**CARI:**
> Validasi platform dilakukan melalui pengujian fungsional, pengujian performa terhadap 1.127 proses dari tujuh skenario serangan terkontrol, serta User Acceptance Test (UAT) bersama Tim LFD BSSN.

**GANTI:**
> Validasi platform dilakukan melalui pengujian fungsional, pengujian non-fungsional terhadap 1.127 proses dari tujuh skenario serangan terkontrol, serta User Acceptance Test (UAT) bersama Tim LFD BSSN.

### A3. Abstrak Indonesia — placeholder halaman & titik ganda (hal. vi)
**CARI:**
> …ser ta mendukung konsistensi alur kerja analisis forensik memori pada Tim LFD BSSN..
>
>    +   halaman +   lampiran (2026)
> Kata kunci : Forensik Memori (1), Triase (2), open-source (3), Otomatisasi (4), Volatility3 (5)

**GANTI:**
> …serta mendukung konsistensi alur kerja analisis forensik memori pada Tim LFD BSSN.
>
> xiii + 76 halaman + 2 lampiran (2026)
> Kata kunci: Forensik Memori (1), Triase (2), Open-Source (3), Otomatisasi (4), Volatility3 (5)

> Catatan: sesuaikan "76 halaman" dengan jumlah halaman final setelah revisi (samakan dengan versi Inggris).

### A4. Abstract Inggris — REGENERASI TOTAL (hal. vii)
Ganti seluruh isi paragraf Abstract dengan berikut (buang ISO/IEC 27042, "four indicators"→six rules, tambah non-functional testing + UAT + angka):

**GANTI (seluruh badan Abstract):**
> The difficulty in handling large-scale cyber incidents is often caused by the limited time available to analyze volatile evidence in Random Access Memory (RAM). Delays in the triage process can have fatal consequences, including the loss of critical artifacts such as encryption keys and network connection traces when the system is shut down. Therefore, a platform capable of rapidly automating memory analysis is required to support the digital evidence analysis workflow of the Digital Forensics Laboratory (LFD) Team of the National Cyber and Crypto Agency (BSSN). This research produced a memory forensics triage platform based on the Volatility3 framework, built using the Python programming language with a Tkinter-based graphical interface. The platform implements six heuristic detection rules organized into four of the six steps of the SANS Memory Forensics Methodology, namely the identification of rogue processes, the review of network artifacts, the detection of code injection, and the analysis of process objects. The platform was developed using the Design Research Methodology (DRM) framework with a Prototyping model, enabling systematic development based on the real operational needs of the LFD BSSN users. Platform validation was carried out through functional testing, non-functional testing against 1,127 processes from seven controlled attack scenarios, and a User Acceptance Test (UAT) with the LFD BSSN Team. The non-functional testing yielded a detection Recall of 100% with a False Positive Rate of 0.09%, consistent with the platform's design that prioritizes minimizing missed threats. The resulting platform is expected to reduce reliance on the manual interpretation of raw Volatility3 output and to support the consistency of the memory forensics analysis workflow within the LFD BSSN Team.
>
> xiii + 76 pages + 2 attachments (2026)
> Keywords: Memory Forensics (1), Triage (2), Open-Source (3), Automation (4), Volatility3 (5)

> Tambahkan satu kalimat hasil UAT setelah kalimat FPR begitu angka UAT final (mis. "The UAT resulted in an acceptance level of NN%, categorized as …").

---

## BAGIAN B — BAB IV

### B1. Caption "Tabel Tabel" (hal. 32, 33, 34)
**CARI:** `Tabel 4.1 Tabel Software Requirement Specification (SRS) Platform`
**GANTI:** `Tabel 4.1 Software Requirement Specification (SRS) Platform`

**CARI:** `Tabel 4.2 Tabel Kebutuhan Fungsional`
**GANTI:** `Tabel 4.2 Kebutuhan Fungsional`

**CARI:** `Tabel 4.3 Tabel Kebutuhan Non-fungsional`
**GANTI:** `Tabel 4.3 Kebutuhan Non-fungsional`

### B2. Narasi "skala prioritas" (hal. 31–32, kolom prioritas sudah dihapus)
**CARI:**
> Berdasarkan hasil wawancara, diperoleh pula tabel Software Requirement Specification (SRS) yang merangkum seluruh kebutuhan platform beserta skala prioritas dan solusi teknis yang diusulkan, sebagaimana ditunjukkan pada Tabel 4.1.

**GANTI:**
> Berdasarkan hasil wawancara, diperoleh pula tabel Software Requirement Specification (SRS) yang merangkum seluruh kebutuhan platform beserta solusi teknis yang diusulkan, sebagaimana ditunjukkan pada Tabel 4.1.

### B3. Tabel 4.1 baris 2 — "empat plugin" vs "6 plugin" (hal. 32)
**CARI (kolom Deskripsi Kebutuhan):** `Eksekusi otomatis empat plugin Volatility3 dalam satu kali proses`
**GANTI:** `Eksekusi otomatis enam plugin Volatility3 dalam satu kali proses`

**CARI (kolom Solusi):** `Integrasi Volatility3 sebagai engine analisis melalui pemanggilan modul Python, yang menjalankan 6 plugin secara berurutan terhadap satu memory dump`
**GANTI:** `Integrasi Volatility3 sebagai engine analisis melalui pemanggilan modul Python, yang menjalankan enam plugin secara berurutan terhadap satu memory dump`

### B4. Flowchart hal. 37 — "keenam plugin" tapi daftar 4; "keempat heuristic rule"
**CARI:**
> Setelah validasi berhasil, pengguna memulai analisis dan platform mengeksekusi keenam plugin Volatility3 secara sekuensial, windows.pslist, windows.pstree, windows.netscan, dan windows.malware.malfind, dengan indikator progres yang ditampilkan secara real-time di antarmuka. Seluruh PID unik yang ditemukan kemudian dikumpulkan dan dievaluasi satu per satu melalui keempat heuristic rule.

**GANTI:**
> Setelah validasi berhasil, pengguna memulai analisis dan platform mengeksekusi keenam plugin Volatility3 secara sekuensial, yaitu windows.pslist, windows.pstree, windows.netscan, windows.malware.malfind, windows.dlllist, dan windows.handles, dengan indikator progres yang ditampilkan secara real-time di antarmuka. Seluruh PID unik yang ditemukan kemudian dikumpulkan dan dievaluasi satu per satu melalui enam aturan deteksi yang terorganisasi dalam empat kelompok indikator SANS.

### B5. Sequence diagram hal. 37–38 — hapus nama fungsi Python; seragamkan
**CARI:**
> Interaksi dimulai dari pemuatan file oleh Analis melalui app.py, yang kemudian mendelegasikan eksekusi analisis ke main.py melalui pemanggilan fungsi run_analysis(). main.py selanjutnya memanggil runner.py untuk mengeksekusi keenam plugin Volatility3 secara sekuensial dan mengembalikan hasil mentah dalam format JSON. Hasil tersebut diteruskan ke analyzer.py melalui fungsi classify_all di mana setiap PID dievaluasi secara internal melalui keenam heuristic rule. Klasifikasi yang dihasilkan kemudian dikembalikan ke main.py dan diteruskan ke app.py untuk ditampilkan di GUI. Pada tahap akhir, ketika pengguna memilih untuk mengekspor hasil, app.py memanggil reporter.py melalui fungsi export_all() yang menghasilkan file Excel (.xlsx) menggunakan pustaka openpyxl.

**GANTI:**
> Interaksi dimulai dari pemuatan file oleh analis melalui app.py, yang kemudian mendelegasikan eksekusi analisis kepada main.py. Modul main.py selanjutnya memanggil runner.py untuk mengeksekusi keenam plugin Volatility3 secara sekuensial dan mengembalikan hasil mentah dalam format JSON. Hasil tersebut diteruskan kepada analyzer.py, tempat setiap PID dievaluasi secara internal melalui enam aturan deteksi dalam empat kelompok indikator SANS. Klasifikasi yang dihasilkan kemudian dikembalikan kepada main.py dan diteruskan kepada app.py untuk ditampilkan di GUI. Pada tahap akhir, ketika pengguna memilih untuk mengekspor hasil, app.py mendelegasikan penulisan berkas kepada reporter.py yang menghasilkan file Excel (.xlsx) menggunakan pustaka openpyxl.

### B6. Arsitektur hal. 38 — "keempat heuristic rule"
**CARI:**
> analyzer.py yang mengimplementasikan keempat heuristic rule secara mandiri tanpa ketergantungan modul eksternal
**GANTI:**
> analyzer.py yang mengimplementasikan keenam aturan deteksi (dalam empat kelompok indikator SANS) secara mandiri tanpa ketergantungan modul eksternal

### B7. hal. 38 — "Tabel 4.1" seharusnya "Tabel 4.2"
**CARI:**
> Implementasi dari kedelapan kebutuhan fungsional yang dirumuskan pada Tabel 4.1, yaitu F01 hingga F08, diuraikan pada subbab-subbab berikut
**GANTI:**
> Implementasi dari kedelapan kebutuhan fungsional yang dirumuskan pada Tabel 4.2, yaitu F01 hingga F08, diuraikan pada subbab-subbab berikut

### B8. hal. 40 — deskripsi kolom tabel & "tingkat risiko"
**CARI:**
> Hasil klasifikasi disajikan dalam tabel yang memuat delapan kolom, yaitu PID, Nama Proses, Path Eksekusi, Status, serta empat kolom R1 hingga R4. Empat kolom terakhir menandakan aturan heuristik yang terpicu pada proses bersangkutan, di mana karakter (✓) menunjukkan aturan terpicu dan karakter (·) menunjukkan aturan tidak terpicu. Setiap baris diberi warna latar sesuai tingkat risikonya, yaitu merah untuk suspicious dan hijau untuk clean, sehingga analis dapat dengan cepat mengenali proses yang paling memerlukan investigasi.

**GANTI:**
> Hasil klasifikasi disajikan dalam tabel yang memuat delapan kolom, yaitu PID, Nama Proses, Path Eksekusi, Status, serta empat kolom R1 hingga R4 yang mewakili empat kelompok indikator SANS (Identify Rogue Processes, Review Network Artifacts, Look for Evidence of Code Injection, dan Analyze Process Objects). Sebuah kolom kelompok ditandai terpicu apabila salah satu aturan di dalamnya terpenuhi, di mana karakter (✓) menunjukkan kelompok terpicu dan karakter (·) menunjukkan tidak terpicu. Setiap baris diberi warna latar sesuai status klasifikasinya, yaitu oranye untuk suspicious dan hijau untuk clean, sehingga analis dapat dengan cepat mengenali proses yang paling memerlukan investigasi.

### B9. IV.4.1 butir 3 (F03) — REWRITE TOTAL (Rogue = R1a masquerade + R1b induk-anak)
Ganti seluruh butir 3 (mulai "3. Deteksi rogue processes…" sampai sebelum Gambar 4.8 / butir 4).

**GANTI (seluruh butir 3):**
> **3. Deteksi rogue processes berdasarkan penyamaran nama/path dan ketidakwajaran relasi induk-anak (F03)**
>
> Fitur ini diimplementasikan dalam modul analyzer.py sebagai kelompok aturan pertama (Rule 1) yang memetakan langkah Identify Rogue Processes. Kelompok ini terdiri atas dua aturan yang masing-masing dapat memicu indikator secara mandiri, yaitu R1a yang mendeteksi proses menyamar melalui kemiripan nama dan kewajaran path eksekusi, serta R1b yang mendeteksi relasi induk-anak yang menyimpang dari pola eksekusi normal Windows. Kolom R1 pada tabel hasil ditandai terpicu apabila salah satu dari kedua aturan tersebut terpenuhi.
>
> Aturan R1a memeriksa nama dan path proses melalui dua sub-pengujian. Sub-pengujian pertama mendeteksi typosquatting, yaitu teknik penyamaran proses berbahaya menggunakan nama yang mirip dengan proses sistem Windows yang sah, misalnya svch0st.exe (huruf "o" diganti angka "0") yang menyerupai svchost.exe. Pengujian dilakukan dengan membandingkan nama proses terhadap daftar proses sistem Windows yang sah, kemudian menghitung jarak edit Levenshtein antara nama proses dengan setiap nama pada whitelist. Apabila nama proses tidak persis sama dengan salah satu nama pada whitelist namun memiliki jarak edit kurang dari atau sama dengan dua karakter, proses tersebut diidentifikasi sebagai indikasi typosquatting. Pengecekan keanggotaan whitelist secara persis dilakukan sebelum perhitungan jarak edit untuk mencegah proses sistem yang sah keliru ditandai karena kemiripan dengan proses lain pada whitelist, misalnya lsass.exe terhadap lsaiso.exe. Sub-pengujian kedua mendeteksi kewajaran path eksekusi. Proses sistem Windows yang sah pada umumnya dieksekusi dari direktori standar seperti C:\Windows\System32\ atau C:\Program Files\, sedangkan proses berbahaya cenderung diluncurkan dari direktori sementara atau lokasi yang dapat ditulisi pengguna seperti \Temp\, \AppData\Local\Temp\, \Users\Public\, \Downloads\, atau \Desktop\. Apabila path eksekusi tidak diawali oleh prefix direktori sistem yang sah dan mengandung salah satu kata kunci direktori mencurigakan, path tersebut diidentifikasi sebagai indikasi rogue process.
>
> Aturan R1b memeriksa relasi induk-anak yang tertangkap oleh plugin windows.pstree melalui dua sub-pengujian. Sub-pengujian pertama membandingkan proses terhadap baseline relasi induk yang konsisten pada Windows normal; beberapa proses sistem memiliki induk yang sangat spesifik, misalnya services.exe dan lsass.exe yang selalu dijalankan oleh wininit.exe, csrss.exe oleh smss.exe, serta svchost.exe oleh services.exe. Apabila proses tersebut ditemukan memiliki induk yang berbeda dari yang seharusnya, hal ini mengindikasikan adanya proses palsu yang menyamar menggunakan nama proses sistem yang sah. Sub-pengujian kedua mendeteksi pola suspicious spawner, yaitu proses yang dalam operasi normalnya tidak meluncurkan shell atau interpreter, mencakup aplikasi perkantoran (winword.exe, excel.exe, outlook.exe), suite perkantoran alternatif (soffice.bin), peramban modern (chrome.exe, msedge.exe, firefox.exe), serta aplikasi yang umum dijadikan target living-off-the-land seperti notepad.exe dan mspaint.exe. Apabila salah satu proses tersebut terdeteksi meluncurkan shell atau interpreter seperti cmd.exe, powershell.exe, wscript.exe, atau cscript.exe — maupun utilitas administratif yang sering disalahgunakan seperti wmic.exe, regsvr32.exe, dan rundll32.exe — R1b dipicu dengan mencatat nama dan PID proses induk beserta proses anaknya. Seluruh whitelist proses sistem, direktori standar, baseline relasi induk-anak, dan daftar suspicious spawner disusun mengacu pada SANS DFIR Cheat Sheet, SANS FOR508, dan dokumentasi resmi Microsoft. Kemunculan salah satu sub-pengujian saja sudah cukup untuk menandai Rule 1 sebagai terpenuhi (R1 = ✓).
>
> Implementasi R1a diverifikasi dengan menganalisis berkas infected_r1a_masquerade.raw, sebuah memory dump yang dihasilkan dengan menanamkan payload meterpreter yang dinamai svch0st.exe dan dijalankan dari direktori C:\Users\Public\. Hasil analisis platform menandai proses svch0st.exe dengan PID 4988 sebagai suspicious. Pada panel Detail Indikator, kedua sub-pengujian R1a terpicu: sub-pengujian typosquatting mengidentifikasi kemiripan nama svch0st.exe dengan svchost.exe (jarak edit satu karakter), sementara sub-pengujian path mengidentifikasi keberadaan kata kunci \users\public\ pada direktori eksekusi. Proses yang sama juga terpicu pada seluruh kelompok indikator lainnya (R2, R3, dan R4) karena payload meterpreter tunggal ini sekaligus membuka koneksi keluar aktif, meninggalkan segmen memori tersuntik, dan memuat modul dari path mencurigakan — sebuah ilustrasi bahwa satu proses berbahaya dapat memenuhi beberapa indikator secara bersamaan. Tampilan hasil analisis pada infected_r1a_masquerade.raw dapat dilihat pada Gambar 4.7.
>
> Implementasi R1b diverifikasi dengan menganalisis berkas infected_r1b_parentchild.raw, sebuah memory dump yang dihasilkan dari eksekusi makro LibreOffice Basic yang memanggil COM automation sehingga soffice.bin meluncurkan powershell.exe secara langsung sebagai proses anak. Hasil analisis platform menandai proses soffice.bin dengan PID 9140 sebagai suspicious. Pada panel Detail Indikator, R1b terpicu dengan pesan [Rule1] Spawn mencurigakan: 'soffice.bin' (PID=9140) -> 'powershell.exe' (PID=10120), menandakan bahwa suite perkantoran yang dalam operasi normalnya tidak pernah meluncurkan interpreter telah menjalankan powershell.exe sebagai anak langsung. Proses anak powershell.exe (PID 10120) turut ditandai suspicious melalui kelompok indikator lain karena memegang koneksi reverse shell aktif dan meninggalkan segmen memori tersuntik.

> Catatan gambar: Gambar 4.7 sebaiknya menampilkan hasil infected_r1a_masquerade.raw (svch0st.exe PID 4988). Jika Anda ingin memisahkan bukti R1b, tambahkan satu gambar baru untuk infected_r1b_parentchild.raw (soffice.bin PID 9140) dan sesuaikan penomoran gambar berikutnya di seluruh bab & Daftar Gambar.

### B10. IV.4.1 butir 4 (F04 / R2) — perbarui verifikasi ke dataset final
**CARI:**
> Fitur ini diimplementasikan dalam modul analyzer.py sebagai aturan kedua (Rule 2) dari empat heuristik. Rule 2 mengevaluasi setiap proses berdasarkan jejak koneksi jaringan yang tertangkap oleh plugin windows.netscan
**GANTI:**
> Fitur ini diimplementasikan dalam modul analyzer.py sebagai kelompok aturan kedua (Rule 2) yang memetakan langkah Review Network Artifacts. Rule 2 mengevaluasi setiap proses berdasarkan jejak koneksi jaringan yang tertangkap oleh plugin windows.netscan

**CARI (paragraf verifikasi butir 4 — seluruhnya):**
> Implementasi Rule 2 diverifikasi dengan menganalisis berkas infected_network.raw, sebuah memory dump yang dihasilkan dari simulasi serangan dengan menjalankan payload Meterpreter yang membuka reverse connection ke mesin penyerang. Hasil analisis platform menampilkan tiga proses bertanda suspicious, di antaranya update.exe dengan PID 10876 yang ditandai sebagai suspicious. Pada panel Detail Indikator, Rule 2 terpicu dengan pesan [Rule2] Koneksi outbound abnormal: 'update.exe' -> 192.168.70.131:4444 (TCPv4, ESTABLISHED), menandakan bahwa proses update.exe, yang bukan merupakan proses jaringan yang dikenal, sedang memegang koneksi aktif ke mesin penyerang. Dua proses suspicious lainnya pada memory dump yang sama, yaitu notepad.exe dan powershell.exe, terdeteksi melalui Rule 3 yang akan dibahas pada bagian berikutnya. Hasil deteksi Rule 2 dengan baris update.exe dipilih dapat dilihat pada Gambar 4.8.

**GANTI:**
> Implementasi Rule 2 diverifikasi dengan menganalisis berkas infected_r2_network.raw, sebuah memory dump yang dihasilkan dari implan C2 framework Sliver yang membuka koneksi keluar aktif ke mesin penyerang. Skenario ini secara khusus memilih implan Sliver berbasis Go karena tidak meninggalkan region memori RWX, sehingga membuktikan bahwa Rule 2 mampu menangkap kanal C2 yang tidak terjangkau oleh Rule 1, Rule 3, maupun Rule 4. Hasil analisis platform menandai proses AtlasAgent.exe dengan PID 8732 sebagai satu-satunya proses suspicious. Pada panel Detail Indikator, Rule 2 terpicu dengan pesan [Rule2] Koneksi outbound abnormal: 'AtlasAgent.exe' -> 192.168.70.131:8443 (TCPv4, ESTABLISHED), menandakan bahwa proses AtlasAgent.exe, yang bukan merupakan proses jaringan yang dikenal, sedang memegang koneksi aktif ke mesin penyerang, sementara ketiga kelompok indikator lainnya membaca False. Hasil deteksi Rule 2 dengan baris AtlasAgent.exe dipilih dapat dilihat pada Gambar 4.8.

### B11. IV.4.1 butir 5 (F05 / R3) — perbarui verifikasi ke dataset final
**CARI:**
> Fitur ini diimplementasikan dalam modul analyzer.py sebagai aturan ketiga (Rule 3) dari empat heuristik. Rule 3 mengevaluasi setiap proses berdasarkan jejak region memori yang ditemukan oleh plugin windows.malware.malfind
**GANTI:**
> Fitur ini diimplementasikan dalam modul analyzer.py sebagai kelompok aturan ketiga (Rule 3) yang memetakan langkah Look for Evidence of Code Injection. Rule 3 mengevaluasi setiap proses berdasarkan jejak region memori yang ditemukan oleh plugin windows.malware.malfind

**CARI (paragraf verifikasi butir 5 — seluruhnya):**
> Implementasi Rule 3 diverifikasi dengan menganalisis berkas infected_injection.raw, sebuah memory dump yang dihasilkan dari simulasi serangan dengan menjalankan payload Meterpreter yang kemudian melakukan migration ke dalam proses svchost.exe. Hasil analisis platform menampilkan empat proses bertanda suspicious, di antaranya svchost.exe dengan PID 676 yang ditandai sebagai suspicious. Pada panel Detail Indikator, Rule 3 terpicu sebanyak dua kali pada proses yang sama, yaitu pada region memori beralamat 1932527534080 dan 1932561285120, yang menandakan keberadaan lebih dari satu segmen memori yang disuntikkan oleh payload. Proses powershell.exe pada memory dump yang sama juga terdeteksi oleh Rule 3 dengan pola serupa, sementara dua proses suspicious lainnya (MicrosoftEdgeUpdate.exe dan update.exe) terdeteksi melalui Rule 2 karena masing-masing memegang koneksi outbound aktif ke alamat eksternal. Hasil deteksi Rule 3 dengan baris svchost.exe dipilih dapat dilihat pada Gambar 4.9.

**GANTI:**
> Implementasi Rule 3 diverifikasi dengan menganalisis berkas infected_r3_injection.raw, sebuah memory dump yang dihasilkan dengan menyuntikkan kode meterpreter reflective DLL ke dalam proses sah notepad.exe melalui teknik migration. Berbeda dengan skenario Rule 2, koneksi C2 pada skenario ini sengaja disenyapkan sebelum akuisisi sehingga proses target tampak sah dari sisi jaringan dan hanya terbongkar melalui artefak injeksi memorinya. Hasil analisis platform menandai proses notepad.exe dengan PID 3404 sebagai satu-satunya proses suspicious. Pada panel Detail Indikator, Rule 3 terpicu sebanyak dua kali pada proses yang sama, yaitu pada dua region memori dengan kombinasi PAGE_EXECUTE_READWRITE dan PrivateMemory beralamat 0x22319910000 dan 0x22319950000, yang menandakan sisa segmen reflective loader hasil injeksi, sementara ketiga kelompok indikator lainnya membaca False. Hasil deteksi Rule 3 dengan baris notepad.exe dipilih dapat dilihat pada Gambar 4.9.

### B12. IV.4.1 butir 6 (F06) — REWRITE TOTAL (Process Objects = R4a DLL + R4b LSASS)
Ganti seluruh butir 6 (mulai "6. Deteksi anomali pada process objects…" sampai sebelum Gambar 4.10 / butir 7). Konten induk-anak lama DIPINDAH ke butir 3 (lihat B9), jadi butir 6 sepenuhnya diisi R4a + R4b.

**GANTI (seluruh butir 6):**
> **6. Deteksi anomali pada process objects berdasarkan pemuatan DLL mencurigakan dan akses ke LSASS (F06)**
>
> Fitur ini diimplementasikan dalam modul analyzer.py sebagai kelompok aturan keempat (Rule 4) yang memetakan langkah Analyze Process Objects. Kelompok ini terdiri atas dua aturan yang masing-masing dapat memicu indikator secara mandiri, yaitu R4a yang memeriksa asal pemuatan Dynamic Link Library (DLL) melalui plugin windows.dlllist, serta R4b yang memeriksa keabsahan akses antarproses terhadap Local Security Authority Subsystem Service (LSASS) melalui plugin windows.handles. Kolom R4 pada tabel hasil ditandai terpicu apabila salah satu dari kedua aturan tersebut terpenuhi.
>
> Aturan R4a mengevaluasi setiap modul DLL yang dimuat oleh sebuah proses. Proses yang sah pada umumnya memuat DLL dari direktori instalasi resmi seperti C:\Windows\System32\ atau C:\Program Files\, sedangkan teknik DLL side-loading maupun DLL search-order hijacking cenderung memuat modul dari lokasi yang dapat ditulisi pengguna. Apabila sebuah DLL dimuat dari path yang mengandung kata kunci direktori mencurigakan seperti \Users\Public\, \Temp\, \AppData\, atau \Downloads\ dan berada di luar direktori instalasi yang sah, R4a dipicu dengan mencatat nama proses, nama modul DLL, serta path pemuatannya.
>
> Aturan R4b mengevaluasi handle antarproses yang menunjuk ke proses lsass.exe. Teknik credential dumping (misalnya menggunakan Mimikatz) umumnya meminta hak akses yang mencakup bit PROCESS_VM_READ (0x0010) terhadap lsass.exe untuk membaca memori kredensial. Platform memeriksa setiap handle bertipe Process yang menunjuk ke lsass.exe; apabila access mask yang diberikan mengandung bit PROCESS_VM_READ dan proses pemegang handle tidak termasuk dalam daftar proses yang secara wajar mengakses LSASS (LEGIT_LSASS_ACCESSORS, misalnya wininit.exe, services.exe, dan lsass.exe itu sendiri), R4b dipicu dengan mencatat nama proses pemegang handle, target LSASS beserta PID-nya, dan nilai GrantedAccess. Daftar direktori sah maupun daftar accessor LSASS yang sah disusun mengacu pada SANS DFIR Cheat Sheet, MITRE ATT&CK, dan dokumentasi resmi Microsoft.
>
> Implementasi R4a diverifikasi dengan menganalisis berkas infected_r4a_dll.raw, sebuah memory dump yang dihasilkan dengan menanamkan sebuah DLL (evil.dll) di direktori C:\Users\Public\ lalu memuatnya melalui rundll32.exe, sebuah LOLBin Windows yang sah. Penggunaan rundll32 sebagai pemuat dipilih agar hanya path DLL yang bersifat anomali, sementara proses pemuatnya tetap sah. Hasil analisis platform menandai proses rundll32.exe dengan PID 8392 sebagai suspicious. Pada panel Detail Indikator, R4a terpicu dengan pesan [Rule4] DLL path mencurigakan: 'rundll32.exe' memuat 'evil.dll' dari 'C:\Users\Public\evil.dll' (mengandung '\users\public\'), sementara ketiga kelompok indikator lainnya membaca False. Hasil deteksi R4a dapat dilihat pada Gambar 4.10.
>
> Implementasi R4b diverifikasi dengan menganalisis berkas infected_r4b_lsass.raw, sebuah memory dump yang dihasilkan dari eksekusi Mimikatz (privilege::debug diikuti sekurlsa::logonpasswords) terhadap lsass.exe, dengan mimikatz dijalankan dari path yang sah agar hanya R4b yang terisolasi. Hasil analisis platform menandai proses mimikatz.exe dengan PID 8 sebagai suspicious. Pada panel Detail Indikator, R4b terpicu dengan pesan [Rule4] Akses mencurigakan ke LSASS: 'mimikatz.exe' memegang handle ke 'lsass.exe pid 688' dengan GrantedAccess=4112 (mengandung PROCESS_VM_READ), menandakan upaya pembacaan memori LSASS, sementara ketiga kelompok indikator lainnya membaca False.

> Catatan gambar: Gambar 4.10 sebaiknya menampilkan hasil infected_r4a_dll.raw (rundll32.exe PID 8392). Untuk bukti R4b, tambahkan satu gambar baru untuk infected_r4b_lsass.raw (mimikatz.exe PID 8) dan sesuaikan penomoran gambar & Daftar Gambar.

### B13. IV.4.1 butir 7 (F07) — perbarui rujukan & contoh dataset
**CARI:**
> Fitur ini merupakan tahap akhir dari pipeline analisis dan diimplementasikan dalam modul analyzer.py sebagai logika klasifikasi yang menggabungkan hasil keempat aturan heuristik menjadi keputusan akhir per proses. Setiap proses pada memory dump yang telah dievaluasi oleh Rule 1, Rule 2, Rule 3, dan Rule 4 akan menerima status klasifikasi biner sebagai keluaran akhir yang ditampilkan kepada analis.
>
> Status klasifikasi ditentukan berdasarkan pemenuhan aturan heuristik. Apabila salah satu dari keempat aturan terpicu, proses ditandai sebagai suspicious; apabila tidak satu pun aturan terpicu, proses ditandai sebagai clean.

**GANTI:**
> Fitur ini merupakan tahap akhir dari pipeline analisis dan diimplementasikan dalam modul analyzer.py sebagai logika klasifikasi yang menggabungkan hasil keenam aturan deteksi — yang terorganisasi dalam empat kelompok indikator (Rule 1 hingga Rule 4) — menjadi keputusan akhir per proses. Setiap proses pada memory dump yang telah dievaluasi oleh keempat kelompok indikator tersebut akan menerima status klasifikasi biner sebagai keluaran akhir yang ditampilkan kepada analis.
>
> Status klasifikasi ditentukan berdasarkan pemenuhan aturan deteksi. Apabila salah satu dari keenam aturan terpicu, proses ditandai sebagai suspicious; apabila tidak satu pun aturan terpicu, proses ditandai sebagai clean.

**CARI (paragraf validasi dua skenario butir 7):**
> Penerapan logika klasifikasi divalidasi melalui dua skenario yang saling melengkapi. Pada skenario pertama, analisis terhadap infected_rogue.raw menghasilkan satu proses suspicious, yaitu svch0st.exe, sementara 169 proses lainnya diklasifikasikan sebagai clean, sebagaimana ditunjukkan pada Gambar 4.11. Skenario ini memverifikasi bahwa stats panel merangkum hasil secara akurat, skema warna bekerja sesuai status klasifikasi, dan proses suspicious diurutkan ke atas tabel secara otomatis. Pada skenario kedua, baris MicrosoftEdgeUpdate.exe pada memory dump infected_injection.raw dipilih untuk memverifikasi panel Detail Indikator, sebagaimana ditunjukkan pada Gambar 4.12. Panel menampilkan pesan anomali Rule 2 beserta rekomendasi investigasi spesifik yang dapat dijadikan acuan tindak lanjut oleh analis.

**GANTI:**
> Penerapan logika klasifikasi divalidasi melalui dua skenario yang saling melengkapi. Pada skenario pertama, analisis terhadap infected_r1a_masquerade.raw menghasilkan satu proses suspicious, yaitu svch0st.exe (PID 4988), sementara 159 proses lainnya diklasifikasikan sebagai clean, sebagaimana ditunjukkan pada Gambar 4.11. Skenario ini memverifikasi bahwa panel statistik merangkum hasil secara akurat, skema warna bekerja sesuai status klasifikasi, dan proses suspicious diurutkan ke atas tabel secara otomatis. Pada skenario kedua, baris AtlasAgent.exe pada memory dump infected_r2_network.raw dipilih untuk memverifikasi panel Detail Indikator, sebagaimana ditunjukkan pada Gambar 4.12. Panel menampilkan pesan anomali Rule 2 beserta rekomendasi investigasi spesifik yang dapat dijadikan acuan tindak lanjut oleh analis.

### B14. IV.4.1 butir 8 (F08) — lima sheet → tujuh sheet
**CARI:**
> Berkas results disusun ke dalam lima sheet yang mempertahankan baik hasil keluaran mentah keenam plugin Volatility3 maupun keputusan klasifikasi akhir yang dihasilkan platform. Sheet pertama hingga keempat masing-masing menyajikan output mentah dari plugin windows.pslist, windows.pstree, windows.netscan, dan windows.malware.malfind, sedangkan sheet kelima yang berlabel Klasifikasi menyajikan hasil triase platform per proses.

**GANTI:**
> Berkas results disusun ke dalam tujuh sheet yang mempertahankan baik hasil keluaran mentah keenam plugin Volatility3 maupun keputusan klasifikasi akhir yang dihasilkan platform. Sheet pertama hingga keenam masing-masing menyajikan output mentah dari plugin windows.pslist, windows.pstree, windows.netscan, windows.malware.malfind, windows.dlllist, dan windows.handles, sedangkan sheet ketujuh yang berlabel Klasifikasi menyajikan hasil triase platform per proses.

**CARI (kolom sheet Klasifikasi):**
> Sheet Klasifikasi memuat sembilan kolom yang merangkum seluruh hasil evaluasi per proses, yaitu PID, Name, Path, Status, empat kolom boolean yang menandakan aturan mana yang terpicu (Rule1_Rogue, Rule2_Network, Rule3_Injection, Rule4_ProcObj), serta kolom Reasons yang memuat pesan indikator anomali.

**GANTI:**
> Sheet Klasifikasi memuat sembilan kolom yang merangkum seluruh hasil evaluasi per proses, yaitu PID, Name, Path, Status, empat kolom boolean yang menandakan kelompok indikator mana yang terpicu (Rule1_Rogue, Rule2_Network, Rule3_Injection, Rule4_ProcObj), serta kolom Reasons yang memuat pesan indikator anomali. Empat kolom boolean tersebut mewakili empat kelompok SANS; sebuah kolom bernilai benar apabila salah satu aturan di dalam kelompoknya terpenuhi, sedangkan rincian aturan spesifik yang terpicu (termasuk pembeda R1a/R1b dan R4a/R4b) tercantum lengkap pada kolom Reasons.

**CARI (warna & summary lima dataset):**
> dengan warna merah atau oranye untuk suspicious dan hijau muda untuk clean, mengikuti skema warna yang digunakan pada antarmuka GUI
**GANTI:**
> dengan warna oranye untuk suspicious dan hijau muda untuk clean, mengikuti skema warna yang digunakan pada antarmuka GUI

**CARI:**
> Pada Performance Testing di BAB V, ringkasan dari kelima dataset dapat digabungkan dengan cepat menjadi satu tabel untuk perhitungan Recall, Accuracy, dan False Positive Rate.
**GANTI:**
> Pada Pengujian Non-Fungsional di BAB V, ringkasan dari ketujuh dataset dapat digabungkan dengan cepat menjadi satu tabel untuk perhitungan Recall, Accuracy, dan False Positive Rate.

### B15. IV.4.2 NF03 (hal. 52) — kelima → ketujuh
**CARI:**
> Pada tahap konstruksi, kelima memory dump yang digunakan, yang masing-masing berukuran 5 GB, seluruhnya berhasil diproses oleh platform hingga menghasilkan klasifikasi tanpa kendala kehabisan memori maupun kegagalan pemrosesan
**GANTI:**
> Pada tahap konstruksi, ketujuh memory dump yang digunakan, yang masing-masing berukuran 5 GB, seluruhnya berhasil diproses oleh platform hingga menghasilkan klasifikasi tanpa kendala kehabisan memori maupun kegagalan pemrosesan

### B16. hal. 52–53 — penutup IV.4: keempat indikator → enam aturan
**CARI:**
> Realisasi kedelapan kebutuhan fungsional pada tahap ini secara kolektif membentuk satu alur kerja triase yang utuh, mulai dari pemuatan memory dump, eksekusi otomatis enam plugin Volatility3, evaluasi keempat indikator anomali, klasifikasi biner clean/suspicious, hingga ekspor hasil ke berkas Excel.
**GANTI:**
> Realisasi kedelapan kebutuhan fungsional pada tahap ini secara kolektif membentuk satu alur kerja triase yang utuh, mulai dari pemuatan memory dump, eksekusi otomatis enam plugin Volatility3, evaluasi enam aturan anomali dalam empat kelompok indikator SANS, klasifikasi biner clean/suspicious, hingga ekspor hasil ke berkas Excel.

### B17. hal. 53 — kutip Rumusan Masalah apa adanya + hapus "maka" + sitasi [9]
**CARI:**
> Keterpaduan alur inilah yang menjadi dasar platform dalam menjawab rumusan masalah pertama, yaitu bagaimana platform dapat mempercepat alur kerja analisis bukti digital melalui deteksi indikator anomali secara otomatis.

**GANTI:**
> Keterpaduan alur inilah yang menjadi dasar platform dalam menjawab rumusan masalah pertama, yaitu bagaimana merancang dan membangun platform triase forensik memori berbasis Volatility3 yang dapat mengotomatisasi deteksi indikator anomali pada proses sesuai kebutuhan Tim Laboratorium Forensik Digital.

**CARI:**
> Kedua, klasifikasi biner mempersempit ruang pemeriksaan awal, di mana dari seluruh proses yang ditemukan pada sebuah memory dump maka platform secara otomatis menyaringnya menjadi sejumlah kecil proses berstatus suspicious yang ditempatkan pada urutan teratas tabel
**GANTI:**
> Kedua, klasifikasi biner mempersempit ruang pemeriksaan awal, di mana dari seluruh proses yang ditemukan pada sebuah memory dump platform secara otomatis menyaringnya menjadi sejumlah kecil proses berstatus suspicious yang ditempatkan pada urutan teratas tabel

**CARI:**
> serta dengan prinsip bahwa otomatisasi dapat mengurangi beban kerja dan konsumsi waktu dalam proses forensik digital [13].
**GANTI:**
> serta dengan prinsip bahwa otomatisasi dapat mengurangi beban kerja dan konsumsi waktu dalam proses forensik digital [9].

> Alasan: klaim identik di hal. 2 ("otomatisasi… mengurangi beban kerja, menekan konsumsi waktu") dikutip [9] (Michelet dkk., tentang otomatisasi forensik). [13] (Shakhsheer dkk.) adalah studi analisis memori Volatility, bukan sumber klaim beban kerja. Verifikasi ke kedua paper.

### B19. hal. 53 (penutup IV.4) — "beta testing" → UAT
**CARI:**
> sedangkan penilaian terhadap percepatan dan kemudahan penggunaan dari perspektif pengguna akhir diperoleh melalui beta testing yang dibahas pada BAB V.

**GANTI:**
> sedangkan penilaian terhadap percepatan dan kemudahan penggunaan dari perspektif pengguna akhir diperoleh melalui User Acceptance Test (UAT) yang dibahas pada BAB V.

### B20. hal. 53 (IV.5 Deployment) — "beta testing" → UAT
**CARI:**
> Adapun evaluasi dari perspektif pengguna akhir, yaitu personel Tim Laboratorium Forensik Digital, dilaksanakan secara terpisah melalui beta testing sebagaimana diuraikan pada BAB V.

**GANTI:**
> Adapun evaluasi dari perspektif pengguna akhir, yaitu personel Tim Laboratorium Forensik Digital, dilaksanakan secara terpisah melalui User Acceptance Test (UAT) sebagaimana diuraikan pada BAB V.

### B18. Tabel 4.6 butir 3 — FP contoh disesuaikan ke hasil final
**CARI:**
> False positive MicrosoftEdgeUpdate.exe pada sampel infected_injection.raw didokumentasikan sebagai keterbatasan platform, karena aturan heuristik statis tidak dapat membedakan konteks koneksi keluar yang sah dari sebuah proses sistem dengan aktivitas berbahaya
**GANTI:**
> False positive PaintStudio.Vi (komponen Paint 3D) pada sampel clean_baseline.raw didokumentasikan sebagai keterbatasan platform, karena aturan heuristik statis tidak dapat membedakan konteks koneksi keluar yang sah ke layanan telemetri Microsoft dari sebuah proses sistem dengan aktivitas berbahaya

---

## BAGIAN C — BAB V.1 & V.2

### C1. Pengantar BAB V (hal. 55) — hapus alpha/beta
**CARI:**
> Pengujian dilaksanakan secara berurutan melalui tiga jenis pengujian yang saling melengkapi, yaitu alpha testing untuk memverifikasi kesesuaian fungsional platform terhadap spesifikasi yang telah ditetapkan, performance testing untuk mengukur akurasi deteksi indikator anomali terhadap ground truth yang telah diketahui, serta beta testing untuk memperoleh penilaian penerimaan pengguna dari perspektif personel Tim Laboratorium Forensik Digital.

**GANTI:**
> Pengujian dilaksanakan secara berurutan melalui tiga jenis pengujian yang saling melengkapi, yaitu pengujian fungsional untuk memverifikasi kesesuaian fungsional platform terhadap spesifikasi yang telah ditetapkan, pengujian non-fungsional untuk mengukur akurasi deteksi indikator anomali terhadap ground truth yang telah diketahui, serta User Acceptance Test (UAT) untuk memperoleh penilaian penerimaan pengguna dari perspektif personel Tim Laboratorium Forensik Digital.

### C2. Judul & isi V.1 (hal. 55)
**CARI:** `V.1 ALPHA TESTING`
**GANTI:** `V.1 PENGUJIAN FUNGSIONAL`

**CARI:**
> Alpha testing dilaksanakan menggunakan metode black box testing yang bertujuan untuk memverifikasi bahwa seluruh fungsi utama platform berjalan sesuai dengan spesifikasi yang telah ditetapkan tanpa melibatkan pemeriksaan terhadap kode sumber.
**GANTI:**
> Pengujian fungsional dilaksanakan menggunakan metode black box testing yang bertujuan untuk memverifikasi bahwa seluruh fungsi utama platform berjalan sesuai dengan spesifikasi yang telah ditetapkan tanpa melibatkan pemeriksaan terhadap kode sumber.

**CARI:**
> sehingga alpha testing pada subbab ini berperan sebagai formalisasi verifikasi tersebut ke dalam rangkaian test case yang terstruktur.
**GANTI:**
> sehingga pengujian fungsional pada subbab ini berperan sebagai formalisasi verifikasi tersebut ke dalam rangkaian test case yang terstruktur.

### C3. Tabel 5.1 F02 (hal. 56) — lengkapi daftar plugin
**CARI:**
> Setelah memilih memory dump, pengguna menekan tombol Mulai Analisis dan mengamati eksekusi keenam plugin (windows.pslist, windows.pstree, windows.netscan, windows.malware.malfind)
**GANTI:**
> Setelah memilih memory dump, pengguna menekan tombol Mulai Analisis dan mengamati eksekusi keenam plugin (windows.pslist, windows.pstree, windows.netscan, windows.malware.malfind, windows.dlllist, windows.handles)

### C4. Tabel 5.1 F03 (hal. 56) — dataset & path final
**CARI (kolom Skenario):**
> Sampel infected_rogue.raw dianalisis untuk memverifikasi deteksi typosquatting nama proses (svch0st.exe) dan kewajaran path eksekusi pada direktori tidak wajar (C:\Temp)
**GANTI:**
> Sampel infected_r1a_masquerade.raw dianalisis untuk memverifikasi deteksi typosquatting nama proses (svch0st.exe) dan kewajaran path eksekusi pada direktori tidak wajar (C:\Users\Public\); sampel infected_r1b_parentchild.raw dianalisis untuk memverifikasi deteksi relasi induk-anak menyimpang (soffice.bin meluncurkan powershell.exe)

**CARI (kolom Expected Result):**
> Proses svch0st.exe ditandai suspicious dengan Rule 1 terpicu, dan panel Detail Indikator menampilkan kemiripan nama dengan svchost.exe (jarak edit 1) serta keberadaan kata kunci direktori \temp\
**GANTI:**
> Proses svch0st.exe dan soffice.bin ditandai suspicious dengan Rule 1 terpicu, dan panel Detail Indikator menampilkan kemiripan nama dengan svchost.exe (jarak edit 1) beserta kata kunci direktori \users\public\ untuk R1a, serta relasi induk-anak soffice.bin → powershell.exe untuk R1b

### C5. Tabel 5.1 F04 (hal. 57) — dataset final
**CARI (Skenario):**
> Sampel infected_network.raw dianalisis untuk memverifikasi deteksi koneksi outbound aktif dari proses non-jaringan (update.exe)
**GANTI:**
> Sampel infected_r2_network.raw dianalisis untuk memverifikasi deteksi koneksi outbound aktif dari proses non-jaringan (AtlasAgent.exe)

**CARI (Expected Result):**
> Proses update.exe ditandai suspicious dengan Rule 2 terpicu, dan panel Detail Indikator menampilkan koneksi ke 192.168.70.131:4444 (TCPv4, ESTABLISHED)
**GANTI:**
> Proses AtlasAgent.exe ditandai suspicious dengan Rule 2 terpicu, dan panel Detail Indikator menampilkan koneksi ke 192.168.70.131:8443 (TCPv4, ESTABLISHED)

### C6. Tabel 5.1 F05 (hal. 57) — dataset final
**CARI (Skenario):**
> Sampel infected_injection.raw dianalisis untuk memverifikasi deteksi region memori dengan kombinasi PAGE_EXECUTE_READWRITE dan PrivateMemory pada proses target migration (svchost.exe)
**GANTI:**
> Sampel infected_r3_injection.raw dianalisis untuk memverifikasi deteksi region memori dengan kombinasi PAGE_EXECUTE_READWRITE dan PrivateMemory pada proses target migration (notepad.exe)

**CARI (Expected Result):**
> Proses svchost.exe ditandai suspicious dengan Rule 3 terpicu, dan panel Detail Indikator menampilkan alamat region memori yang anomali
**GANTI:**
> Proses notepad.exe ditandai suspicious dengan Rule 3 terpicu, dan panel Detail Indikator menampilkan alamat region memori yang anomali

### C7. Tabel 5.1 F06 (hal. 57) — GANTI dari induk-anak ke DLL + LSASS
**CARI (Skenario):**
> Sampel infected_procobj.raw dianalisis untuk memverifikasi deteksi relasi parent-child yang menyimpang, yaitu mspaint.exe yang meluncurkan cmd.exe
**GANTI:**
> Sampel infected_r4a_dll.raw dianalisis untuk memverifikasi deteksi pemuatan DLL dari path mencurigakan (rundll32.exe memuat evil.dll dari C:\Users\Public\); sampel infected_r4b_lsass.raw dianalisis untuk memverifikasi deteksi akses mencurigakan ke LSASS (mimikatz.exe memegang handle ke lsass.exe)

**CARI (Expected Result):**
> Proses mspaint.exe ditandai suspicious dengan Rule 4 terpicu, dan panel Detail Indikator menampilkan relasi mspaint.exe (PID 10480) terhadap cmd.exe (PID 11280)
**GANTI:**
> Proses rundll32.exe dan mimikatz.exe ditandai suspicious dengan Rule 4 terpicu; panel Detail Indikator menampilkan pemuatan evil.dll dari C:\Users\Public\ untuk R4a, serta handle ke lsass.exe pid 688 dengan GrantedAccess=4112 (mengandung PROCESS_VM_READ) untuk R4b

### C8. Tabel 5.1 F08 (hal. 58) — lima → tujuh sheet
**CARI:**
> Berkas Excel berhasil dibuat dan memuat lima sheet (PSList, PSTree, NetScan, Malfind, dan Klasifikasi), dengan sheet Klasifikasi memuat status dan kolom rule per proses serta skema warna yang konsisten dengan tampilan GUI
**GANTI:**
> Berkas Excel berhasil dibuat dan memuat tujuh sheet (PSList, PSTree, NetScan, Malfind, DllList, Handles, dan Klasifikasi), dengan sheet Klasifikasi memuat status dan kolom kelompok indikator per proses serta skema warna yang konsisten dengan tampilan GUI

### C9. Penutup V.1 (hal. 59) — keempat → keenam plugin/aturan
**CARI:**
> yang menunjukkan bahwa setiap fungsi utama, mulai dari pemuatan memory dump, eksekusi otomatis keempat plugin Volatility3, deteksi keempat indikator anomali, klasifikasi biner clean/suspicious beserta panel detail dan rekomendasi investigasi, hingga ekspor hasil ke berkas Excel, berjalan sesuai dengan spesifikasi yang telah ditetapkan tanpa kegagalan. Dengan terpenuhinya seluruh fungsi tersebut, platform dinyatakan lolos alpha testing dan dapat dilanjutkan ke tahap performance testing untuk mengukur akurasi deteksinya.

**GANTI:**
> yang menunjukkan bahwa setiap fungsi utama, mulai dari pemuatan memory dump, eksekusi otomatis keenam plugin Volatility3, deteksi enam aturan anomali dalam empat kelompok indikator SANS, klasifikasi biner clean/suspicious beserta panel detail dan rekomendasi investigasi, hingga ekspor hasil ke berkas Excel, berjalan sesuai dengan spesifikasi yang telah ditetapkan tanpa kegagalan. Dengan terpenuhinya seluruh fungsi tersebut, platform dinyatakan lolos pengujian fungsional dan dapat dilanjutkan ke tahap pengujian non-fungsional untuk mengukur akurasi deteksinya.

### C10. Judul & intro V.2 (hal. 59) — nama + tujuh sampel
**CARI:** `V.2 PERFORMANCE TESTING`
**GANTI:** `V.2 PENGUJIAN NON-FUNGSIONAL`

**CARI:**
> Performance testing dilaksanakan untuk mengukur kemampuan platform dalam mendeteksi indikator anomali secara akurat terhadap sejumlah memory dump yang kondisinya telah diketahui secara pasti. Pengujian ini menggunakan lima sampel memory dump yang dibuat sendiri dalam lingkungan terkontrol sebagaimana telah diuraikan pada subbab III.3.4, yang terdiri dari satu sampel baseline pada kondisi sistem bersih (clean_baseline.raw) dan empat sampel pada kondisi terinfeksi yang masing-masing terutama menargetkan salah satu dari empat indikator yang diadopsi.

**GANTI:**
> Pengujian non-fungsional dilaksanakan untuk mengukur kemampuan platform dalam mendeteksi indikator anomali secara akurat terhadap sejumlah memory dump yang kondisinya telah diketahui secara pasti. Pengujian ini menggunakan tujuh sampel memory dump yang dibuat sendiri dalam lingkungan terkontrol sebagaimana telah diuraikan pada subbab III.3.4, yang terdiri dari satu sampel baseline pada kondisi sistem bersih (clean_baseline.raw) dan enam sampel pada kondisi terinfeksi yang masing-masing dirancang untuk mengisolasi salah satu dari enam aturan deteksi, sehingga aturan-aturan lain membaca False pada sampel tersebut.

### C11. Paragraf pengelompokan confusion matrix (hal. 59) — "empat kategori" tetap; tidak diubah
(Tidak ada perubahan; empat kategori TP/TN/FP/FN benar.)

### C12. Tabel 5.2 — ISI SELURUH SEL (hal. 59–60)
Isi baris sesuai regresi final:

| Nama Dump | Total PID | GT Suspicious | TP | FP | FN | TN |
|---|---|---|---|---|---|---|
| clean_baseline.raw | 179 | 0 | 0 | 1 | 0 | 178 |
| infected_r1a_masquerade.raw | 160 | 1 | 1 | 0 | 0 | 159 |
| infected_r1b_parentchild.raw | 169 | 2 | 2 | 0 | 0 | 167 |
| infected_r2_network.raw | 154 | 1 | 1 | 0 | 0 | 153 |
| infected_r3_injection.raw | 147 | 1 | 1 | 0 | 0 | 146 |
| infected_r4a_dll.raw | 160 | 1 | 1 | 0 | 0 | 159 |
| infected_r4b_lsass.raw | 158 | 1 | 1 | 0 | 0 | 157 |
| **Total** | **1127** | **7** | **7** | **1** | **0** | **1119** |

### C13. Narasi pasca-Tabel 5.2 (hal. 60) — angka final
**CARI:**
> Berdasarkan Tabel 5.2, sampel clean_baseline.raw yang merepresentasikan kondisi sistem bersih tidak menghasilkan satu pun proses suspicious, sehingga seluruh 165 proses terklasifikasi sebagai True Negative dan memverifikasi bahwa platform tidak menghasilkan deteksi palsu pada kondisi normal. Pada keempat sampel terinfeksi, seluruh proses yang ground truth-nya bersifat suspicious berhasil terdeteksi tanpa terkecuali, sebagaimana ditunjukkan oleh nilai False Negative yang bernilai nol pada seluruh sampel. Terdapat satu kasus False Positive yang muncul pada sampel infected_injection.raw, di mana satu proses yang sebenarnya sah keliru ditandai sebagai suspicious, sementara empat sampel lainnya tidak menghasilkan False Positive sama sekali.

**GANTI:**
> Berdasarkan Tabel 5.2, sampel clean_baseline.raw yang merepresentasikan kondisi sistem bersih menghasilkan satu proses yang keliru ditandai suspicious, sehingga 178 dari 179 proses terklasifikasi sebagai True Negative. Pada keenam sampel terinfeksi, seluruh proses yang ground truth-nya bersifat suspicious berhasil terdeteksi tanpa terkecuali, sebagaimana ditunjukkan oleh nilai False Negative yang bernilai nol pada seluruh sampel. Satu-satunya kasus False Positive justru muncul pada sampel clean_baseline.raw, di mana satu proses sistem yang sah keliru ditandai sebagai suspicious, sementara keenam sampel terinfeksi tidak menghasilkan False Positive sama sekali.

### C14. Paragraf metrik agregat (hal. 60) — angka final
**CARI:**
> Dari akumulasi keseluruhan nilai pada Tabel 5.2, diperoleh total 10 True Positive, 1 False Positive, 0 False Negative, dan 834 True Negative dari keseluruhan 845 proses yang dievaluasi. Berdasarkan nilai tersebut, dihitung tiga metrik evaluasi yang saling melengkapi. Metrik utama, yaitu Recall, dihitung melalui pembagian jumlah True Positive terhadap jumlah seluruh proses yang ground truth-nya suspicious, dengan hasil Recall = TP / (TP + FN) = 10 / (10 + 0) = 100%. Sebagai metrik pendukung, Accuracy dihitung melalui pembagian jumlah klasifikasi yang benar terhadap keseluruhan proses, dengan hasil Accuracy = (TP + TN) / Total = (10 + 834) / 845 = 99,88%. Adapun False Positive Rate (FPR) dihitung pada proses yang sebenarnya bersih sebagai sanity check, dengan hasil FPR = FP / (FP + TN) = 1 / (1 + 834) = 0,12%.

**GANTI:**
> Dari akumulasi keseluruhan nilai pada Tabel 5.2, diperoleh total 7 True Positive, 1 False Positive, 0 False Negative, dan 1.119 True Negative dari keseluruhan 1.127 proses yang dievaluasi. Berdasarkan nilai tersebut, dihitung tiga metrik evaluasi yang saling melengkapi. Metrik utama, yaitu Recall, dihitung melalui pembagian jumlah True Positive terhadap jumlah seluruh proses yang ground truth-nya suspicious, dengan hasil Recall = TP / (TP + FN) = 7 / (7 + 0) = 100%. Sebagai metrik pendukung, Accuracy dihitung melalui pembagian jumlah klasifikasi yang benar terhadap keseluruhan proses, dengan hasil Accuracy = (TP + TN) / Total = (7 + 1.119) / 1.127 = 99,91%. Adapun False Positive Rate (FPR) dihitung pada proses yang sebenarnya bersih sebagai sanity check, dengan hasil FPR = FP / (FP + TN) = 1 / (1 + 1.119) = 0,09%.

### C15. Paragraf Recall (hal. 60) — tidak ada angka lama; hanya sinkron kalimat
(Boleh dibiarkan; Recall 100% & target ≥80% masih benar. Tidak ada perubahan wajib.)

### C16. Paragraf Accuracy (hal. 60–61) — angka distribusi kelas
**CARI:**
> Meskipun nilai Accuracy yang diperoleh mencapai 99,88%, nilai ini tidak dapat dibaca sebagai indikator performa utama platform karena distribusi kelas pada pengujian ini sangat tidak seimbang. Dari keseluruhan 845 proses yang dievaluasi, sebanyak 835 proses (sekitar 98,8%) merupakan proses yang ground truth-nya bersih, sehingga nilai Accuracy didominasi oleh keberhasilan platform mengklasifikasikan proses bersih yang jumlahnya jauh lebih banyak. Sebagai ilustrasi, sebuah pengklasifikasi naif yang menandai seluruh proses sebagai clean tanpa melakukan analisis apa pun akan tetap memperoleh nilai Accuracy yang setara tinggi, yaitu sekitar 98,8%, namun dengan Recall sebesar 0% karena gagal menangkap seluruh proses berbahaya.

**GANTI:**
> Meskipun nilai Accuracy yang diperoleh mencapai 99,91%, nilai ini tidak dapat dibaca sebagai indikator performa utama platform karena distribusi kelas pada pengujian ini sangat tidak seimbang. Dari keseluruhan 1.127 proses yang dievaluasi, sebanyak 1.120 proses (sekitar 99,4%) merupakan proses yang ground truth-nya bersih, sehingga nilai Accuracy didominasi oleh keberhasilan platform mengklasifikasikan proses bersih yang jumlahnya jauh lebih banyak. Sebagai ilustrasi, sebuah pengklasifikasi naif yang menandai seluruh proses sebagai clean tanpa melakukan analisis apa pun akan tetap memperoleh nilai Accuracy yang setara tinggi, yaitu sekitar 99,4%, namun dengan Recall sebesar 0% karena gagal menangkap seluruh proses berbahaya.

### C17. Paragraf FPR + FP tunggal (hal. 61) — angka & proses FP final
**CARI:**
> Nilai False Positive Rate sebesar 0,12% berada jauh di bawah ambang batas maksimal 15% yang telah ditetapkan, yang menunjukkan bahwa platform tetap praktis digunakan tanpa membanjiri analis dengan peringatan palsu pada proses sistem yang sah. Satu-satunya False Positive yang muncul berasal dari proses MicrosoftEdgeUpdate.exe pada sampel infected_injection.raw, yang ditandai oleh Rule 2 karena memegang koneksi keluar yang sah ke server pembaruan Microsoft dan bukan merupakan bagian dari skenario serangan yang disimulasikan.

**GANTI:**
> Nilai False Positive Rate sebesar 0,09% berada jauh di bawah ambang batas maksimal 15% yang telah ditetapkan, yang menunjukkan bahwa platform tetap praktis digunakan tanpa membanjiri analis dengan peringatan palsu pada proses sistem yang sah. Satu-satunya False Positive yang muncul berasal dari proses PaintStudio.Vi (komponen Paint 3D) pada sampel clean_baseline.raw, yang ditandai oleh Rule 2 karena memegang koneksi keluar yang sah ke alamat telemetri Microsoft/Azure (48.209.133.15:443) dan bukan merupakan bagian dari skenario serangan yang disimulasikan.

### C18. Tabel 5.3 — ISI (6 baris per aturan) (hal. 61)
Ganti header & isi Tabel 5.3 menjadi per aturan (bukan per kelompok):

| Aturan Deteksi | Dataset Penguji | GT | TP | FN | Recall |
|---|---|---|---|---|---|
| R1a — Masquerading (nama/path) | infected_r1a_masquerade.raw | 1 | 1 | 0 | 100% |
| R1b — Relasi Induk-Anak Anomali | infected_r1b_parentchild.raw | 1 | 1 | 0 | 100% |
| R2 — Koneksi Jaringan Keluar Anomali | infected_r2_network.raw | 1 | 1 | 0 | 100% |
| R3 — Injeksi Kode (RWX + PrivateMemory) | infected_r3_injection.raw | 1 | 1 | 0 | 100% |
| R4a — Pemuatan DLL dari Path Mencurigakan | infected_r4a_dll.raw | 1 | 1 | 0 | 100% |
| R4b — Akses LSASS (PROCESS_VM_READ) | infected_r4b_lsass.raw | 1 | 1 | 0 | 100% |
| **Total** | | **6** | **6** | **0** | **100%** |

> Catatan judul: bila Anda memilih "Recall per Indikator Anomali" tetap sebagai judul Tabel 5.3, itu masih akurat. Kolom "Dataset Penguji" opsional — boleh dihapus bila tabel terlalu lebar.

### C19. Rekonsiliasi pasca-Tabel 5.3 (hal. 61–62) — REWRITE (7 proses vs 6 target aturan)
**CARI:**
> Perlu dicatat bahwa penjumlahan kolom Ground Truth pada Tabel 5.3, yaitu sebanyak 13 pemicuan, lebih besar daripada total 10 proses suspicious yang tercatat pada Tabel 5.2. Perbedaan ini bukan merupakan ketidaksesuaian, melainkan disebabkan oleh perbedaan satuan penghitungan di antara kedua tabel. Tabel 5.2 menghitung pada level proses, di mana setiap proses dihitung satu kali terlepas dari jumlah indikator yang dipicunya, sedangkan Tabel 5.3 menghitung pada level pemicuan rule, di mana satu proses suspicious dapat memicu lebih dari satu indikator secara bersamaan sehingga turut dihitung pada beberapa indikator sekaligus. Sebagai contoh sebagaimana telah diuraikan pada BAB IV, proses svch0st.exe pada sampel infected_rogue.raw memicu tiga indikator sekaligus (Rule 1, Rule 2, dan Rule 3), sementara proses mspaint.exe pada sampel infected_procobj.raw memicu dua indikator sekaligus (Rule 3 dan Rule 4), sehingga jumlah pemicuan rule secara keseluruhan melampaui jumlah proses suspicious.

**GANTI:**
> Perlu dicatat bahwa penjumlahan kolom Ground Truth pada Tabel 5.3, yaitu sebanyak enam target aturan, berbeda dari total tujuh proses suspicious yang tercatat pada Tabel 5.2. Perbedaan ini bukan merupakan ketidaksesuaian, melainkan disebabkan oleh perbedaan satuan penghitungan di antara kedua tabel. Tabel 5.2 menghitung pada level proses, di mana setiap proses berbahaya yang ditanamkan dihitung satu kali, sedangkan Tabel 5.3 menghitung pada level aturan yang diisolasi, di mana setiap dataset terinfeksi dirancang untuk menargetkan tepat satu aturan sehingga menghasilkan enam target aturan. Selisih satu proses berasal dari sampel infected_r1b_parentchild.raw yang, selain menanamkan proses induk soffice.bin sebagai target utama R1b, turut menghasilkan proses anak powershell.exe sebagai konsekuensi alami rantai serangan; proses anak tersebut dihitung sebagai satu proses suspicious tambahan pada Tabel 5.2 namun tidak menambah baris pada Tabel 5.3 karena bukan target isolasi aturan. Perlu ditegaskan pula bahwa beberapa proses memicu lebih dari satu aturan secara bersamaan; sebagaimana diuraikan pada BAB IV, proses svch0st.exe pada sampel infected_r1a_masquerade.raw memicu keempat kelompok indikator sekaligus (Rule 1 hingga Rule 4) karena payload meterpreter tunggalnya sekaligus menyamar, membuka koneksi keluar, meninggalkan segmen memori tersuntik, dan memuat modul dari path mencurigakan. Pemicuan berlapis semacam ini tidak memengaruhi perhitungan Recall per aturan pada Tabel 5.3, yang mengukur keberhasilan setiap aturan menangkap target isolasinya masing-masing.

### C20. Paragraf akhir V.2 (hal. 62) — keempat indikator & "tujuh pemicuan R3"
**CARI:**
> Berdasarkan Tabel 5.3, keempat indikator anomali memperoleh nilai Recall sebesar 100%, yang menunjukkan bahwa setiap rule berhasil menangkap seluruh pemicuan yang ground truth-nya memang seharusnya terdeteksi pada masing-masing indikator. Indikator Look for Evidence of Code Injection (Rule 3) tercatat memiliki jumlah pemicuan terbanyak, yaitu tujuh pemicuan, yang mencerminkan bahwa teknik injeksi kode melalui migration payload merupakan karakteristik yang paling sering muncul di seluruh skenario serangan yang disimulasikan, sementara ketiga indikator lainnya terpicu sesuai dengan skenario utama masing-masing sampel.

**GANTI:**
> Berdasarkan Tabel 5.3, keenam aturan deteksi memperoleh nilai Recall sebesar 100%, yang menunjukkan bahwa setiap aturan berhasil menangkap target isolasi yang ground truth-nya memang seharusnya terdeteksi pada masing-masing dataset. Capaian ini membuktikan bahwa keenam aturan — baik yang berada pada peringkat prevalensi global tinggi seperti injeksi kode dan koneksi C2, maupun yang lebih spesifik pada kebutuhan operasional Tim LFD seperti pemuatan DLL mencurigakan dan akses LSASS — seluruhnya bekerja sesuai rancangan pada skenario serangan nyata yang disimulasikan.

### C21. Penutup V.2 (hal. 62) — tidak wajib diubah
(Paragraf "Secara keseluruhan, hasil… Recall sempurna… satu False Positive" masih akurat; hanya pastikan tidak menyebut angka lama. Frasa "performance testing" di dalamnya → ganti "pengujian non-fungsional".)

**CARI:** `Secara keseluruhan, hasil performance testing membuktikan bahwa pipeline deteksi platform bekerja sesuai dengan rancangan`
**GANTI:** `Secara keseluruhan, hasil pengujian non-fungsional membuktikan bahwa pipeline deteksi platform bekerja sesuai dengan rancangan`

---

## MENYUSUL (butuh angka UAT)
- V.3 USER ACCEPTANCE TEST (UAT) — tulis hasil dari data riil.
- BAB VI KESIMPULAN DAN SARAN (keterbatasan menyatu di VI.2).
- Abstrak: sisipkan kalimat hasil UAT (ID & EN).
- Daftar Isi: tambah I.5, BAB VI; Daftar Gambar: sinkron caption "Enam Plugin".
