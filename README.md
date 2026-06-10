# 🧋 Boba Barokah - Web Pesen Boba Paling Enak!

Halo teman-teman! 👋 
Ini adalah website **Boba Barokah** buatan kita. Di sini, kamu bisa pilih dan pesen minuman boba yang kenyal-kenyal dan manis banget secara online. Terus nanti pesenannya langsung dikirim lewat WhatsApp. Gampang banget kan? 

---

## 😋 Menu Boba yang Bikin Ngiler
Di website ini ada banyak rasa boba yang enak-enak, lho! Sekarang kita juga bisa menambah dan menghapus menu boba dengan mudah menggunakan aplikasi pengelola boba.

---

## 🎮 Cara Pesennya (Gampang Banget!)
Ikuti langkah-langkah mainnya ya:
1. **Pilih Boba**: Cari gambar boba yang kamu pengen, terus klik tombol **"Tambah"** yang warna krem itu.
2. **Lihat Keranjang**: Klik tas belanjaan di kanan atas buat liat boba apa aja yang udah kamu pilih.
3. **Tulis Nama & Alamat**: Jangan lupa tulis nama kamu sama alamat rumah kamu ya, biar abang kurirnya ga nyasar pas nganter bobanya! 🏠
4. **Kirim via WhatsApp**: Klik tombol hijau besar yang tulisannya **"Checkout via WhatsApp"**. Nanti websitenya otomatis buka WhatsApp dan ngirim pesan pesanan kamu ke penjualnya. Tinggal tunggu deh bobanya dateng!

---

## 🛠️ Mainan di Belakang Layar (Bahan Pembuatan)
Web ini dibuat dengan struktur file berikut biar rapi:
* 📄 **index.html** - Ini kerangka websitenya, buat nampilin tulisan, tombol, dan kotak pesanan.
* 🎨 **style.css** - Ini buat warnain websitenya biar cantik, ada warna krem, cokelat, dan tombol hijau yang estetik.
* 🗃️ **products.js** - Berisi daftar/database produk boba dalam bentuk data JavaScript. Dipisah agar bisa diedit dengan mudah oleh program Python.
* ⚡ **script.js** - Ini otak websitenya! Buat ngitung harga boba, nyimpen belanjaan kamu, dan ngubungin ke WhatsApp abang penjual boba.
* 📂 **images/** - Folder tempat menyimpan file gambar produk yang diunggah secara lokal.

---

## 💻 Aplikasi Pengelola Produk Python (GUI Desktop)
Untuk memudahkan menambah atau menghapus menu boba, kita sekarang punya aplikasi pembantu berbasis desktop yang dibuat menggunakan **Python** dengan pustaka bawaan `tkinter`.

### Fitur Aplikasi:
1. **Daftar Produk Real-time**: Menampilkan seluruh menu boba yang ada saat ini.
2. **Tambah Produk**: Form mudah untuk memasukkan Nama, Deskripsi, Harga, dan Gambar (bisa URL gambar web atau file gambar lokal dari komputer Anda). Jika Anda memilih gambar dari komputer Anda, gambar akan otomatis disalin ke folder `images/`.
3. **Hapus Produk**: Tinggal pilih produk dari tabel dan klik tombol hapus. File gambar lokal yang tidak terpakai juga akan otomatis dibersihkan.
4. **Buka Website**: Tombol pintas untuk langsung membuka website `index.html` di browser default untuk melihat perubahan Anda.

### Cara Menjalankan Aplikasi Pengelola:
1. Pastikan komputer Anda sudah terinstal **Python 3**.
2. Buka Command Prompt / PowerShell / Terminal di direktori proyek ini.
3. Jalankan perintah:
   ```powershell
   python manage_products.py
   ```
4. Aplikasi GUI Boba Barokah akan terbuka dan siap digunakan!

Selamat mencoba pesen boba ya teman-teman! Jangan lupa sikat gigi abis minum yang manis-manis! 🪥🦷😋
