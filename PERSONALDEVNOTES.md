# Personal Notes

## Ingat ini sebelum development
1. Job drafter (`.github/workflow/release-drafter.yml`) akan bekerja membuat draft release di [Release](https://github.com/vysf/geolistrik-cli/releases) setiap ada PR yang dibuat. INGAT: masih dalam bentuk draft ya!.
2. Versioning akan bekerja dengan baik jika PR dibuat dengan label -- lihat konfigurasi drafter `.github/release-drafter.yml` -- karena saya menggunakan `RESOLVED_VERSION`, jadi jangan lupa beri label setiap PR.
3. Draft akan menumpuk semua PR di `CHANGES` yang `merge` ke `master`.
4. Selalu lakukan PR dan merge di github web karena bisa memberi label.
5. Job release (`.github/workflow/release.yml`) hanya akan berjalan apabila ada tag baru yang ditambahakan.
6. Selalu buat tag yang sama dengan draft version!.
7. Pahami dulu [Release Drafter](https://github.com/marketplace/actions/release-drafter) jangan langsung ke AI.

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

`INGAT SELALU BUAT TAG YANG SAMA DENGAN VERSI DRAFTER`.

## 6. Lanjut Fitur Baru
Tujuan fitur baru adalah membuat proses panjang yang rumit menjadi singkat nan mudah.
