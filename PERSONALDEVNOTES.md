# Personal Notes

## Tentang SemVer (`MAJOR.MINOR.PATCH`)
### 1. `patch`
- Deskripsi: Perubahan kecil, bugfix, atau perbaikan minor yang tidak mengubah fitur atau breaking API.
- Kapan memberi label ini:
  - Memperbaiki bug yang sudah ada.
  - Mengubah dokumentasi, komentar, atau README.
  - Memperbaiki typo atau masalah minor yang tidak berpengaruh pada behavior utama.
- Contoh:
  - `Fix typo in CLI help message` → label: `patch`
  - `Correct error handling in Linux update` → label: `patch`

### 2. `minor`
- Deskripsi: Menambahkan fitur baru secara backward-compatible tanpa merusak fungsi lama.
- Kapan memberi label ini:
  - Menambahkan command baru, opsi CLI baru.
  - Menambahkan parameter baru pada fungsi, tapi fungsi lama tetap berjalan.
  - Peningkatan performa, refactor, atau optimasi yang tidak merubah API.
- Contoh:
  - `Add --version flag to update command` → label: `minor`
  - `Improve download progress bar in CLI` → label: `minor`

### 3. `major`
- Deskripsi: Perubahan besar, breaking change, atau migrasi yang tidak kompatibel dengan versi sebelumnya.
- Kapan memberi label ini:
  - Perubahan struktur folder, executable format, atau cara update CLI yang lama tidak bisa langsung upgrade.
  - Hilangnya fitur lama atau API berubah.
  - Perubahan cara pengguna install/update, misal dari `--onefile` ke `--one-dir` (future plan).
- Contoh:
  - `Migrate update system to one-dir deployment` → label: `major`
  - `Drop support for version 1 users` → label: `major`

### 💡 Tips praktis untuk GitHub Actions & RESOLVED_VERSION

- Kalau PR diberi label `patch` → action otomatis tingkatkan patch: `1.0.0` → `1.0.1`.
- Kalau PR diberi label `minor` → action otomatis tingkatkan minor, reset patch: `1.0.1` → `1.1.0`.
- Kalau PR diberi label `major` → action otomatis tingkatkan major, reset minor & patch: `1.1.0` → `2.0.0`.

GitHub Action baca label PR dan update RESOLVED_VERSION otomatis.

---

## Ingat ini sebelum development
1. Job drafter (`.github/workflow/release-drafter.yml`) akan bekerja membuat draft release di [Release](https://github.com/vysf/geolistrik-cli/releases) setiap ada PR yang dibuat. INGAT: masih dalam bentuk draft ya!.
2. Versioning akan bekerja dengan baik jika PR dibuat dengan label -- lihat konfigurasi drafter `.github/release-drafter.yml` -- karena saya menggunakan `RESOLVED_VERSION`, jadi jangan lupa beri label setiap PR.
3. Draft akan menumpuk semua PR di `CHANGES` yang `merge` ke `master`.
4. Selalu lakukan PR dan merge di github web karena bisa memberi label.
5. Job release (`.github/workflow/release.yml`) hanya akan berjalan apabila ada tag baru yang ditambahakan.
6. Selalu buat tag yang sama dengan draft version!.
7. Pahami dulu [Release Drafter](https://github.com/marketplace/actions/release-drafter) jangan langsung ke AI.
8. Testing menggunakan pytest dan coverage, bisa jalankan:
    ```
    pytest
    ```
    untuk liat keberhasilan test. \
    atau 
    ```
    pytest --cov=geolistrik/domain --cov-report=term-missing
    ```
    untuk liat keberhasilan dan coverage nya juga. 
    Bisa ubah `--cov` jadi `geolistrik` untuk semua folder di sana. \
    sepertinya kita bisa pertimbangkan ini untuk CI
    ```
    pytest --cov=geolistrik/domain --cov-fail-under=90
    ```
    Arti command
    | Command                                                    | Artinya                              |
    | ---------------------------------------------------------- | ------------------------------------ |
    | `pytest`                                                   | test saja                            |
    | `pytest --cov=geolistrik/domain`                           | test + hitung coverage               |
    | `pytest --cov=geolistrik/domain --cov-report=term`         | tampilkan % di terminal              |
    | `pytest --cov=geolistrik/domain --cov-report=term-missing` | tampilkan % + baris yang belum dites |
    | `pytest --cov=geolistrik/domain --cov-report=html`         | bikin laporan HTML                   |


---

# Development Flow
## 1. Buat branch baru
Setiap akan melakukan development, selalu buat branch baru mengikuti pe-label-an yang ada di konfigurasi drafter, contoh `feat/ves-method`, `fix/lazy-load` dan lain-lain.
```
git chackout -b <branch>
```
`-b` artinya create and change branch. Kalo mau pindah branch cukup hilangkan `-b`.

## 2. Buat pesan commit
Selalu buat pesan commit yang jelas serta beri label drafter.
```
git commit -m "fix: typo on generate variable"
```

## 3. Buat Pull Request
Selalu lakukan PR di `web`. Tujuanya adalah untuk memberikan label `RESOLVED_VERSION` agar penamaan versi konsisten dan tujuan perubahan juga konsisten (major, minor, patch).

Selain itu juga beri pesan dengan label drafter agar pada drafter menumpuk pesan pengembangan yang rapi.

## 4. Buat Merge
Sebaiknya merge dilakukan juga di `web` yaitu setelah proses PR selesai. Meskipun kita dapat melakukanya di terminal dengan memastikan bahwa kita di branch parent. Misal di branch `feat/update-smothing`. pindah ke `dev` dulu baru lakukan merge.
```
git checkout dev
git merge feat/update-smothing
git push origin dev
```
Setelah selesai merge, maka kita sudah bisa hapus branch di lokal dana remote
```
git branch -d <branch>
git push origin --delete <branch>
```
Dimana proses hapus branch ini dilakukan itu opsional ya, bisa dihapus secepatanya atau setelah rilis.

## 5. Buat Tag
Setelah selesai PR dan merge, maka kita bisa buat tag untuk memicu rilis aplikasi
```
git pull origin master
git tag vx.x.x
git push origin masater --tags
```
Jangan takut gagal. Kalo gagal, hentikan dulu action di `web` lalu balik lagi ke terminal, hapus tag lama lalu buat ulang tag yang mau dirilis
```
git tag -d vx.x.x
git push origin --delete vx.x.x
```
Lalu tunggu sampai rilis...

`INGAT SELALU BUAT TAG YANG SAMA DENGAN VERSI DRAFTER`.

## 6. Lanjut Fitur Baru
Tujuan fitur baru adalah membuat proses panjang yang rumit menjadi singkat nan mudah.

---

# Prioritas Saat Ini
1. Stabilkan update CLI & installer → on progress.
2. Pastikan user tidak bisa memilih folder → minimalkan risiko overwrite atau path salah.
3. Setelah itu baru fokus ke optimasi startup speed dan penambahan fitur minor.
4. Unit test & integrasi test bisa ditunda sebentar, tapi jangan diabaikan sepenuhnya.

---

# NEXT UPDATE
1. Lakukan testing
2. Perbaikan arsitektur kode
3. Implementasi lazy load untuk percepatan akses program (opsi: Dependency Injection)

### Mulai berat mungkin jadi versi 3

4. command nuitkan diubah dari --onefile menjadi --one-dir. Strategi upgrade dan downgrade perlu diperbaiki, replace folder ketimbang replace file artinya copy seluruh folder.
5. strategi setup setelah install: windows cukup copy folder. linux perlu copy folder dan sysmlink. buat lebih ux friendly.
6. Sesuaikan kembali `update_cli.py` dan `geolistrik_setup.iss`

## UPDATE POIN 1,2,3

```
geolistrik/
├── __main__.py              # Composition root (lazy load dimulai di sini)
├── __init__.py

├── cli/                     # Interface Adapter (CLI layer)
│   ├── __init__.py
│   ├── app.py               # CLI dispatcher / router
│   ├── commands/            # Setiap command CLI
│   │   ├── __init__.py
│   │   ├── wenner.py
│   │   ├── schlumberger.py
│   │   ├── dipole_dipole.py
│   │   └── help.py
│   └── args.py              # argparse / click config

├── usecases/                # Application business rules
│   ├── __init__.py
│   ├── generate_config.py   # Use case: generate konfigurasi elektroda
│   ├── generate_stack.py    # Use case: stacking data
│   └── plot_result.py       # Orkestrasi plotting (tanpa matplotlib langsung)

├── domain/                  # Enterprise business rules (PURE)
│   ├── __init__.py
│   ├── electrode.py         # Entity
│   ├── array_type.py        # Wenner, Schlumberger, Dipole
│   ├── geometry.py          # Perhitungan jarak & posisi
│   └── formula.py           # Rumus resistivitas (tanpa numpy!)

├── infrastructure/          # Frameworks & drivers
│   ├── __init__.py
│   ├── plotting/
│   │   ├── __init__.py
│   │   └── matplotlib_plotter.py
│   ├── export/
│   │   ├── __init__.py
│   │   ├── csv_exporter.py
│   │   └── image_exporter.py
│   └── numeric/
│       ├── __init__.py
│       └── numpy_backend.py

├── factories/               # Dependency wiring (lazy)
│   ├── __init__.py
│   ├── plotter_factory.py
│   └── numeric_factory.py

└── utils/                   # Helper ringan
    ├── __init__.py
    └── validation.py
```

| Folder         | Deskripsi                                                                 | Lazy-load | Dependency ke layer lain |
|----------------|---------------------------------------------------------------------------|-----------|--------------------------|
| domain         | Pure business rules: elektroda, geometri, formula resistivitas (tanpa lib eksternal) | Tidak relevan | Tidak (paling dalam) |
| usecases       | Application logic: orkestrasi domain + interface (bukan implementasi)      | Tidak     | Ke domain + abstraction |
| cli            | Interface Adapter: parsing arg & trigger usecase                           | Ya        | Ke usecases + factories |
| infrastructure | Implementasi teknis (numpy, matplotlib, file, OS, network)                | Ya        | Ke domain abstractions |
| factories      | Dependency wiring & lazy creation                                          | Ya        | Ke infrastructure |
| utils          | Helper ringan & murni (validasi, formatting, mapping sederhana)            | Tidak     | Minimal / netral |
