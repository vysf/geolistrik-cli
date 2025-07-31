<p align="center">
<img src="https://raw.githubusercontent.com/vysf/geolistrik-cli/master/docs/icon.png" width="128">
</p>

<h1 align="center">Geolistrik CLI</h1>
<p align="center">
Generate geoelectrical stacking chart and observation tables from the terminal, without Python.
</p>

<p align="center">
<a href="https://github.com/vysf/geolistrik-cli/blob/master/README.md">English</a> |
<a href="https://github.com/vysf/geolistrik-cli/blob/master/docs/indonesian.md">Bahasa Indonesia</a>
</p>


---

## 📑 Table of Contents

- [Perkenalan](#perkenalan)
- [Fitur](#fitur)
- [Cara Instalasi](#cara-instalasi)
  - [Windows](#windows)
  - [Linux](#linux)
- [Contoh Penggunaan](#contoh-penggunaan)
- [Pengembangan Lokal](#pengembangan-lokal)
- [Kontribusi](#kontribusi)

---
## Perkenalan

**Geolistrik CLI** adalah aplikasi berbasis terminal untuk menghasilkan **stacking chart** dan **tabel konfigurasi elektroda** dari metode geolistrik umum:

- Wenner-Schlumberger (`ws`)
- Wenner (`wn`)
- Pole-Pole (`pp`)
- Pole-Dipole (`pd`)
- Dipole-Dipole (`dd`)

Hasil disimpan dalam `.png` dan `.txt`, dan tidak butuh Python untuk dijalankan.

---

### Fitur:

- Mendukung 5 konfigurasi elektroda
- CLI dengan opsi `--no-plot`, `--outdir`
- Ekspor grafik `.png` dan data `.txt`
- Bisa digunakan di Windows & Linux tanpa instalasi Python

---

### Cara Instalasi

#### Windows

📦 [Download Installer](https://github.com/vysf/geolistrik-cli/releases)

1. Jalankan installer, ikuti petunjuk. 
2. Setelah intalaso selesai, tambahkan folder:
  ```
  C:\Program Files\Geolistrik 1.0.0   
  ```
  ke **system PATH** secara manual.
3. Buka CMD dan ketik:
   ```cmd
   geolistrik
   ```
   Kamu akan melihat welcome banner:
   ![welcome](welcome-message.png)
4. Untuk uninstall:
   - uninstall lewat **Control Panel → Uninstall a Program**
   - Hapus path yang path dari **system environment**

#### Linux

📦 [Download Linux binary](https://github.com/vysf/geolistrik-cli/releases)

```bash
chmod +x geolistrik-linux
sudo mv geolistrik-linux /usr/local/bin/geolistrik
```

Kemudian gunakan CLI dimana saja:
```bash
geolistrik ws 0 100 10 --outdir results/
```

---

### Contoh Penggunaan

```bash
geolistrik [config] [min] [max] [spacing] [--outdir DIR] [--no-plot]
```

### Kode Konfigurasi:

| Code | Configuration        |
|------|----------------------|
| ws   | Wenner-Schlumberger |
| wn   | Wenner              |
| pp   | Pole-Pole           |
| pd   | Pole-Dipole         |
| dd   | Dipole-Dipole       |

### Options:

| Option       | Description                                |
|--------------|--------------------------------------------|
| `--outdir`   | Set output directory for files             |
| `--no-plot`  | Skip plotting `.png`, just generate data   |
| `--version`  | Show app version                           |
| `--about`    | Show app metadata                          |

---

### Pengembangan Lokal

1. Clone repositori ini:
   ```bash
   git clone https://github.com/vysf/geolistrik-cli
   cd geolistrik-cli
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run secara lokal:
   ```bash
   python -m geolistrik --help
   ```

4. Build dengan Nuitka:
   See `build.bat` or use:

   ```bash
   nuitka --standalone --onefile --include-package=geolistrik --output-dir=build geolistrik/__main__.py
   ```

5. kompilasi Windows Installer:
   - Requires [Inno Setup](https://jrsoftware.org/isinfo.php)
   - Run:
     ```bash
     ISCC geolistrik_setup.iss
     ```

---

### Kontribusi

Kami menerima kontribusi dalam bentuk:
- Perbaikan bug
- Penambahan fitur
- Dokumentasi
- Terjemahan

Silakan buka *Issue* atau *Pull Request* untuk memulai.

---

📫 Kontak: **Yusuf Umar Al Hakim**  
✉️ yusufumaralhakim@fmipa.untan.ac.id.com  
🌐 [GitHub Project](https://github.com/vysf/geolistrik-cli)
