# Geolistrik CLI

Aplikasi command-line untuk menghasilkan stacking chart dan tabel pengamatan metode geolistrik (WS, WN, PP, PD, DD).

## ✅ Fitur
- Mendukung 5 konfigurasi geolistrik
- Output grafik `.png` dan data `.xlsx`
- Dapat dijalankan tanpa Python (via installer)
- CLI interaktif dengan opsi `--no-plot`, `--outdir`

---

## 💻 Cara Install

### 🪟 Windows

1. Unduh [`geolistrik_installer.exe`](https://github.com/username/geolistrik-cli/releases) dari halaman Releases.
2. Jalankan dan ikuti wizard installer.
3. Buka **CMD**, lalu jalankan:
   ```cmd
   geolistrik ws 0 100 10


<!-- nuitka --standalone --onefile --enable-plugin=pylint-warnings --enable-plugin=no-qt  --include-package=geolistrik --windows-icon-from-ico=assets/icon.ico --output-dir=build --show-modules geolistrik/__main__.py -->