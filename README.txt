PORTAL DOSEN TEKNIK GEOLOGI
Universitas Prisma Manado
==============================================

FITUR
-----
1. Profil dosen.
2. Email resmi:
   agus.budiharso@prisma.ac.id
3. Link SIAKAD Prisma:
   https://siap.prisma.ac.id/
4. Enam halaman mata kuliah.
5. Upload RPS per mata kuliah.
6. Upload bahan ajar per mata kuliah.
7. Download RPS dan bahan ajar oleh mahasiswa.
8. Halaman Tulisan & Publikasi.
9. Upload tulisan/artikel/makalah/buku.
10. Login admin sederhana untuk melindungi fungsi upload.

CARA MENJALANKAN
----------------
A. Pertama kali:
   Klik INSTALL_WEB.bat

B. Penggunaan biasa:
   Klik JALANKAN_WEB.bat

C. Bila ingin menggunakan password admin sendiri setiap kali menjalankan:
   Klik JALANKAN_DENGAN_PASSWORD.bat

Alamat web:
http://127.0.0.1:5000

LOGIN ADMIN
-----------
Alamat:
http://127.0.0.1:5000/admin/login

Password awal:
PrismaGeologi2026

CATATAN PENTING
---------------
Password awal hanya untuk penggunaan lokal/testing.
Sebelum web ditempatkan di internet/public hosting,
gunakan password pribadi melalui environment variable ADMIN_PASSWORD
atau gunakan JALANKAN_DENGAN_PASSWORD.bat.

FILE YANG BISA DIUPLOAD
-----------------------
PDF, DOC, DOCX, PPT, PPTX, XLS, XLSX,
ZIP, RAR, TXT, JPG, JPEG, PNG.

DATA DAN FILE
-------------
Metadata upload disimpan di:
data/portal_data.json

RPS:
uploads/rps/

Bahan ajar:
uploads/materials/

Tulisan:
uploads/writings/

Jika folder project dipindahkan ke komputer lain,
salin seluruh folder agar data dan dokumen tetap ikut.