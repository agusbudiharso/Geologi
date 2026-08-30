# Portal Dosen Teknik Geologi - Universitas Prisma Manado

Versi ini dibuat khusus untuk **GitHub Pages** sehingga dapat di-hosting gratis.

## Akses publik
Mahasiswa dan masyarakat umum **tidak perlu login**. Mereka hanya dapat melihat halaman dan mengunduh file yang tersedia.

## Penting
GitHub Pages adalah hosting statis. Karena itu:
- tidak ada backend Python/Flask;
- tidak ada upload langsung dari website;
- tidak ada login admin;
- penambahan RPS, bahan ajar, dan tulisan dilakukan dengan mengunggah file ke repository GitHub.

## Cara publikasi di GitHub Pages

1. Buat repository GitHub baru, misalnya `portal-dosen-geologi`.
2. Upload seluruh isi folder project ini ke repository.
3. Buka **Settings → Pages**.
4. Pada **Build and deployment**, pilih:
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/docs`
5. Klik **Save**.
6. Tunggu beberapa menit. GitHub akan memberikan alamat website gratis.

Contoh:
`https://USERNAME.github.io/portal-dosen-geologi/`

## Menambah RPS dan bahan ajar

Letakkan file pada folder:

`docs/files/NAMA-MATA-KULIAH/rps/`

atau:

`docs/files/NAMA-MATA-KULIAH/bahan-ajar/`

Kemudian tambahkan link file tersebut di `docs/mata-kuliah.html`.

Contoh:

```html
<a href="files/sig/rps/RPS_SIG_2026.pdf" download>RPS SIG 2026</a>
```

Untuk bahan ajar:

```html
<a href="files/sig/bahan-ajar/Pertemuan_01.pdf" download>Pertemuan 1</a>
```

## Menambah tulisan

Simpan file di:

`docs/files/tulisan/`

Lalu tambahkan item pada `docs/tulisan.html`.

## Informasi dosen
- Nama: Drs. Agus Santoso Budiharso, B.Sc., M.Sc.
- NIDN: 1608086501
- Email: agus.budiharso@prisma.ac.id
- SIAKAD: https://siap.prisma.ac.id/
