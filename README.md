
# 1. Alur ketika pengguna membuka halaman portofolio baru

Ketika pengguna membuka halaman portofolio baru, alur dimulai saat browser
mengirimkan HTTP request ke server Django.

1. Request pertama kali diterima oleh `urls.py` pada tingkat proyek.
   File ini berfungsi sebagai URL dispatcher utama yang mengarahkan request
   ke URL aplikasi yang sesuai.

2. `urls.py` pada aplikasi kemudian mencocokkan URL yang diterima dengan pola
   URL yang tersedia dan mengarahkannya ke fungsi atau class view yang sesuai.

3. View menerima request tersebut dan menjalankan logika yang diperlukan.
   Jika data portofolio disimpan dalam database, view akan meminta data
   melalui model.

4. Model berfungsi sebagai representasi data dan penghubung antara aplikasi
   Django dengan database. Model mengambil data portofolio yang diperlukan,
   misalnya judul, deskripsi, gambar, dan tautan proyek.

5. Setelah data diperoleh, view mengirimkan data tersebut ke template
   menggunakan context.

6. Template menggunakan data dari context untuk membentuk halaman HTML.
   Django kemudian mengembalikan HTML tersebut sebagai HTTP response
   kepada browser.

7. Browser menerima response, memproses HTML, CSS, dan aset lainnya,
   kemudian menampilkan halaman portofolio kepada pengguna.

Secara sederhana, alurnya adalah:

Browser → urls.py proyek → urls.py aplikasi → View → Model/Database
→ View → Template → HTML Response → Browser

#### 2. Alasan data portofolio disimpan pada model

Data portofolio sebaiknya disimpan pada model, bukan ditulis langsung
di dalam template, karena model berfungsi untuk mengelola dan
merepresentasikan data aplikasi secara terstruktur.

Jika data ditulis langsung di dalam template, setiap perubahan seperti
mengganti judul proyek, deskripsi, atau menambahkan portofolio baru
mengharuskan developer mengubah kode HTML/template secara manual.
Hal ini membuat pemeliharaan menjadi lebih sulit, terutama ketika
jumlah data semakin banyak.

Dengan menyimpan data pada model, template hanya bertugas menampilkan
data yang diberikan oleh view. Data dapat diubah melalui database,
admin Django, atau fitur aplikasi tanpa harus mengubah struktur
template.

Pendekatan ini memberikan beberapa keuntungan:
- Memisahkan logika data dari tampilan.
- Memudahkan pemeliharaan dan pembaruan data.
- Memungkinkan penambahan portofolio tanpa menyalin template baru.
- Membuat aplikasi lebih mudah dikembangkan dan digunakan kembali.
- Memudahkan integrasi dengan fitur lain, seperti pencarian, filter,
  dan pengelolaan data melalui Django Admin.

Dengan demikian, penggunaan model membuat aplikasi lebih terstruktur,
fleksibel, dan mudah dikembangkan.

# 3. Perbedaan makemigrations dan migrate

`makemigrations` dan `migrate` merupakan dua perintah Django yang
berhubungan dengan perubahan struktur database, tetapi memiliki
fungsi yang berbeda.

- `python manage.py makemigrations`

  Perintah ini digunakan untuk mendeteksi perubahan pada model dan
  membuat file migration yang berisi instruksi perubahan struktur
  database. Perintah ini belum langsung menerapkan perubahan tersebut
  ke database.

- `python manage.py migrate`

  Perintah ini digunakan untuk menjalankan migration yang telah dibuat
  dan menerapkan perubahan struktur database yang diperlukan.

