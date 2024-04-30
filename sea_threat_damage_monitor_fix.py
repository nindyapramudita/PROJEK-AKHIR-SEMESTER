import mysql.connector #ini namanya modul. buat sambungkan program dengan database mysql
from prettytable import PrettyTable #ini modul untuk buat tabel cantik :3
import matplotlib.pyplot as plt #ini modul buat bikin diagram-diagram gitu
from datetime import datetime #ini modul untuk tanggal dan waktu menyesuaikan dengan yang ada dilaptop
import os #ini modul untuk biar bisa gunain os.system dibawah 

# ini fungsinya membersihkan layar konsol. layar diatas terminal yang ganggu itu!
os.system('cls')

#==========KONEKSI ANTAR PROGRAM DAN DATABASENYA============
def buat_koneksi(): #ini fungsi yang dikasi nama buat_koneksi. fungsinya yah buat koneksi antara program dan mysql. tanpa ini gak bisa tersambung
    return mysql.connector.connect( # buat memanggil fungsi conector() dari mysql.connector
        host="localhost", #semua ini parameter yang disesuaikan untuk disambungkan ke database. anggaplah kita catat alamatnya.
        user="root",
        password="",
        database="sea_threat_damage_monitor", #ini disesuaikan sama nama database di phpmyadmin. harus sama namanya!
        autocommit=True #ini biar commit otomatis gitu. biar setai program gak perlu tulis commit terus! contoh mydb.commit()
    )

#==================BLUEPRINT USER==========================
class User: #class user untuk buat blueprint user. mendefinisikan nanti usernya itu admin atau masyarakat.
    def __init__(self, nama_lengkap, no_hp,): #def didalam class itu namanya method. tapi ini methodnya spesial. karena didalamnya ada konstruktor
        self.nama_lengkap = nama_lengkap #ini namanya atribut
        self.no_hp = no_hp 

#==========BLUEPRINT ADMIN DAN PROSES MENUNYA==============
class Admin(User): #class admin untuk buat blueprint pengguna admin. nah admin ini mewarisi sifat sifat dari class user
    def __init__(self, ID_Admin, nama_lengkap, no_hp): #ini konstruktor admin
        super().__init__(nama_lengkap, no_hp) #ini atribut yang mewarisi class user
        self.nama_lengkap = nama_lengkap
        self.ID_Admin = ID_Admin

    #ini proses perbandingan!
    @staticmethod #ini statis method. gunanya untuk mendeklarasikan si def merge sama merge_sort dibawahnya. biar mereka itu dapat dipanggil gitu loh di class admin tanpa harus buat objek baru di class.
    def merge(left, right, key, reverse=False): #ini fungsi merge dan parameternya. left pertama digabungkan, right yang kedua digabungkan, key kunci berdasarkan elemen mana dalam daftar yang akan dibandingkan. reverse itu argumen opsional buat nentuin apa penggabungannya dilakukan secara terbalik atau tidak? nilai defaultnya false
        result = [] #ini tempat untuk nyimpen hasil penggabungan. daftar kosong
        i = j = 0 #Inisialisasi dua variabel i dan j dengan nilai 0.
        while i < len(left) and j < len(right): #nah disini i itu sebelah kiri dan j itu sebelah kanan dengan nilai masing masing 0
            if not reverse: #Pengecekan apakah argumen reverse adalah False. Jika ya, penggabungan akan dilakukan secara normal.
                if left[i][key] < right[j][key]: #disini membandingkan nilai kunci kiri apa lebih kecil dari yang kanan? kalau lebih kecil akan ditambahkan ke result[]
                    result.append(left[i]) #ini nambahkan nilai kunci sebelah kiri ke result[]
                    i += 1 #nilai i yang dari awal 0 di tambah 1
                else:
                    result.append(right[j]) #kalau nilai sebelah kiri gak lebih kecil dari yang kanan maka nilai kunci kanan yang dimasukkan ke result[]
                    j += 1 #nilai j yang dari awal 0 ditambah 1
            else: #ini jika pengecekan apakah argumen reverse adalah selain false. penggabungan dilakukan tidak secara normal
                if left[i][key] > right[j][key]: #jika nilai key sebelah kiri lebih besar maka dia masuk ke result[]
                    result.append(left[i]) #nilai i atau nilai kiri dimasukkan ke result[]
                    i += 1 #nilai i yang dari awal 0 di tambah 1
                else:
                    result.append(right[j]) #nilai j atau nilai kanan dimasukkan ke result[] kalau nilai key kanan yang lebih besar
                    j += 1 #nilai j yang dari awal 0 di tambah 1
        result.extend(left[i:]) #Menambahkan sisa elemen dari daftar left (jika ada) ke result.
        result.extend(right[j:]) #Menambahkan sisa elemen dari daftar right (jika ada) ke result.
        return result #menggabungkan hasil penggabungan dari left dan right dalam bentuk daftar baru

    #ini proses pengurutan!
    @staticmethod #ini statis method. gunanya untuk mendeklarasikan si def merge sama merge_sort dibawahnya. biar mereka itu dapat dipanggil gitu loh di class admin tanpa harus buat objek baru di class.
    def merge_sort(arr, key, reverse=False): #ini fungsi merge dan parameternya. arr it daftar yang akan diurutkan, key itu kunci berdasarkan elemen mana dalam daftar yang akan diurutkan, reverse itu argumen opsional buat nentuin apa pengurutannya dilakukan secara terbalik atau tidak? nilai defaultnya false
        if len(arr) <= 1: #ini pengecekan apakah panjang daftar arr kurang atau sama dengan 1
            return arr #kalau iya maka return arr
        mid = len(arr) // 2 #menghitung index tengah(mid) dari daftar arr. buat bagi daftar jadi dua bagian yang hampir sama besar 
        left = Admin.merge_sort(arr[:mid], key, reverse) #manggil fungsi merge_sort untuk mengurutkan setengah pertama dari daftar arr. arr[:mid] ini nanti digunakan untuk ngambil setengah pertama dari daftar.
        right = Admin.merge_sort(arr[mid:], key, reverse) #manggil fungsi merge_sort untuk mengurutkan setengah kedua dari daftar arr. arr[:mid] ini nanti digunakan untuk ngambil setengah kedua dari daftar.
        return Admin.merge(left, right, key, reverse) #menggabungkan dan mengurutkan dua bagian terurut dari daftar arr yaitu left dan right nya menggunakan fungsi merge.

    def sort_merge_data_kerusakan(self, conn, key, reverse=False): #ini fungsi untuk mengurutkan data kerusakan. self itu merujuk ke class yang memanggil method, conn ini koneksi database untuk eksekusi query, key Kunci berdasarkan mana data kerusakan akan diurutkan kayak id, lokasi tanggal, Argumen opsional yang menentukan apakah pengurutan akan dilakukan secara terbalik atau tidak. Nilainya default adalah False
        cursor = conn.cursor() #Membuat objek cursor dari koneksi database yang diberikan.
        try: #Memulai blok try untuk menangani eksekusi query.
            cursor.execute(
                "SELECT ID_data, lokasi, DATE_FORMAT(Tanggal, '%d %M %Y'), jenis_kerusakan, deskripsi, jumlah_kerusakan FROM data_kerusakan" #eksekusi query untuk mengambil atau select data kerusakan dari table data kerusakan
            )
            data_kerusakan = cursor.fetchall() #Mengambil semua baris hasil query dan menyimpannya dalam variabel

            sorted_data = self.merge_sort(data_kerusakan, key=key, reverse=reverse) #memanggil fungsi merge_sort untuk mengurutkan data kerusakanberdasarkan key yang diinginkan pengguna.  Pengurutan dapat dilakukan secara terbalik jika reverse disetel sebagai True.

            # Membuat objek PrettyTable
            table = PrettyTable() #buat prettytable
            table.field_names = ["ID_data", "Lokasi", "Tanggal", "Jenis Kerusakan", "Deskripsi", "Jumlah Kerusakan"] #ini buat nama nama di kolom table

            # Menambahkan baris data yang sudah diurutkan ke dalam tabel
            for data in sorted_data: #perulangan untuk sorted_data satu per satu. nilainya akan disimpan dalam variabel data.
                table.add_row(data) #ini menambahkan baris dan menampilkan tabel dengan baris sesuai isi variabel data

            # Mencetak tabel yang sudah diurutkan
            print(f"\nData Kerusakan:") #output
            table.max_width["Deskripsi"] = 80 #ini untuk biar table dengan nama kolom "deksripsi" isinya banyak. bakal akan langsung kepotong dan dilanjutkan ke baris bawah. biar gak KEPANJANGAN!
            print(table) #tampilkan table

        except mysql.connector.Error as err: #ini kalau error querynya bisa dikasih tau errornya karena apa
            print("Gagal mengambil data kerusakan:", err) #ini nanti outputnya kalau error
        finally: #untuk menutup objek cursor
            cursor.close() #tutup cursor

    def menu_sorting_data_kerusakan(self): #ini fungsi untuk manggil semua proses sortingan sesuai mau user. key dari fungsi diatas berasal dari sini
        choice = input("\nIngin Sorting Berdasarkan Apa? (Lokasi/Tanggal): ").lower() #ini user akan input mau sorting berdasarkan lokasi apa tanggal?
        conn = buat_koneksi() #Membuat koneksi baru ke database menggunakan fungsi buat_koneksi().
        if choice == "lokasi": #ini proses jika user pilih lokasi
            self.sort_merge_data_kerusakan(conn, key=1) #dia akan langsung memanggil methode sort_merge_data_kerusakan untuk mengurutkan berdasarkan lokasi. Argumen key=1 digunakan untuk menentukan bahwa pengurutan akan dilakukan berdasarkan kolom "Lokasi" (kolom ke-2 dalam definisi tabel).
        elif choice == "tanggal": #ini proses jika user pilih tanggal
            self.sort_merge_data_kerusakan(conn, key=2) #dia akan langsung memanggil methode sort_merge_data_kerusakan untuk mengurutkan berdasarkan tanggal. Argumen key=2 digunakan untuk menentukan bahwa pengurutan akan dilakukan berdasarkan kolom "tanggal" (kolom ke-3 dalam definisi tabel).
        else:
            print("Pilihan Tidak Ada!") #output jika user memilih selain lokasi atau tanggal
        conn.close() #tutup koneksi

    def sort_merge_aduan(self, conn, key, reverse=False): #ini fungsi untuk mengurutkan daftar aduan. self itu merujuk ke class yang memanggil method, conn ini koneksi database untuk eksekusi query, key Kunci berdasarkan mana daftar aduan akan diurutkan kayak id, lokasi, tanggal, Argumen opsional yang menentukan apakah pengurutan akan dilakukan secara terbalik atau tidak. Nilainya default adalah False
        cursor = conn.cursor()  #Membuat objek cursor dari koneksi database yang diberikan.
        try: #Memulai blok try untuk menangani eksekusi query.
            cursor.execute("SELECT * FROM aduan") #eksekusi query untuk mengambil atau select daftar aduan dari table aduan
            aduan = cursor.fetchall()  #Mengambil semua baris hasil query dan menyimpannya dalam variable aduan

            sorted_data = self.merge_sort(aduan, key=key, reverse=reverse) #memanggil fungsi merge_sort untuk mengurutkan data kerusakan berdasarkan key yang diinginkan pengguna. Pengurutan dapat dilakukan secara terbalik jika reverse disetel sebagai True.

            # Membuat objek PrettyTable
            table = PrettyTable() #buat prettytable
            table.field_names = ["ID Aduan", "ID Masyarakat", "Lokasi", "Tanggal", "Keterangan"] #ini buat nama nama di kolom table

            # Menambahkan baris data yang sudah diurutkan ke dalam tabel
            for data in sorted_data: #perulangan untuk sorted_data satu per satu. nilainya akan disimpan dalam variabel data.
                table.add_row(data) #ini menambahkan baris dan menampilkan tabel dengan baris sesuai isi variabel data

            # Mencetak tabel yang sudah diurutkan
            print(f"\nData Aduan Masyarakat (Diurutkan berdasarkan {key}):") #output berdasarkan key atau kemauan user
            table.max_width["Keterangan"] = 80 #ini untuk biar table dengan nama kolom "keterangan" isinya banyak. bakal akan langsung kepotong dan dilanjutkan ke baris bawah. biar gak KEPANJANGAN!
            print(table) #tampilkan table

        except mysql.connector.Error as err: #ini kalau error querynya bisa dikasih tau errornya karena apa
            print("Gagal mengambil data aduan masyarakat:", err)
        finally: #untuk menutup objek cursor
            cursor.close() #tutup cursor
            conn.close() #tutup koneksi

    def menu_sorting_aduan(self): #ini fungsi untuk manggil semua proses sortingan sesuai mau user. key dari fungsi diatas berasal dari sini
        choice = input("\nIngin Sorting Berdasarkan Apa? (Lokasi/Tanggal): ").lower() #ini user akan input mau sorting berdasarkan lokasi apa tanggal?
        conn = buat_koneksi() #Membuat objek cursor dari koneksi database yang diberikan.
        if  choice == "lokasi":  #ini proses jika user pilih lokasi
            self.sort_merge_aduan(conn, key=2) #dia akan langsung memanggil methode sort_merge_aduan untuk mengurutkan berdasarkan lokasi. Argumen key=2 digunakan untuk menentukan bahwa pengurutan akan dilakukan berdasarkan kolom "Lokasi" (kolom ke-3 dalam definisi tabel).
        elif choice == "tanggal":
            self.sort_merge_aduan(conn, key=3) #dia akan langsung memanggil methode sort_merge_aduan untuk mengurutkan berdasarkan lokasi. Argumen key=3 digunakan untuk menentukan bahwa pengurutan akan dilakukan berdasarkan kolom "tanggal" (kolom ke-4 dalam definisi tabel).
        else:
            print("Pilihan Tidak Ada!") #output jika user memilih selain lokasi atau tanggal

    def fibonacci_search(self, arr, x, key): #ini fungsi fibbonaci search dan parameternya. self, merujuk pada class yang memanggil metode, arr daftar yang dicari, x nilai yang dicari didalam daftar
        fibMMm2 = 0  #ini bilangan primitif dari fibonacci
        fibMMm1 = 1  #ini bilangan primitif dari fibonacci
        fibM = fibMMm2 + fibMMm1  #bilangan primitif selalu ditambah dengan bilangan sebelumnya. contoh 0+1=1 1+1=2 2+1=3 3+1=4

        # fibM menjadi terbesar Fibonacci yang <= panjang array
        while (fibM < len(arr)): #perulangan dimana hasil penjumlahan bilangan primitif dibandingkan apakah lebih kecil dari panjang array
            fibMMm2 = fibMMm1 #kalau lebih kecil, fibMMm2 yang awalnya nilainya 0 diisi dengan fibMMm1 yang bernilai 1
            fibMMm1 = fibM #fibMMm1 yang awalnya nilainya 1 diubah menjadi jumlah dari penjumlahan bilangan primitif yang pertama fibM.
            fibM = fibMMm2 + fibMMm1 #fibM kembali diisi dengan hasil penjumlahan fibMMm2 + fibMMm1 atau 1+1=2

        offset = -1 #Variabel offset diinisialisasi dengan nilai -1. Ini akan digunakan untuk menandai posisi saat mencari di dalam daftar.

        while (fibM > 1): #ini perulangan dimana hasil penjumlahan fibMMm2 + fibMMm1 atau variabel fibM dibandingkan apakah lebih besar dari 1 atau ngga?
            i = min(offset + fibMMm2, len(arr) - 1) #kalau lebih besar dari 1 maka, i adalah nilai minimum dari offset + fibMMm2 dan len(rr) - 1 atau panjang dari daftar arr dikurangi 1. karena index di pyton itu mulai dari 0.

            # Jika elemen lebih kecil dari x, geser ke bawah Fibonacci satu kali lebih banyak
            if (arr[i][key] < x): #Jika nilai elemen dalam arr[i] kurang dari nilai yang dicari (x), maka nilai Fibonacci dikurangi untuk menggeser pencarian ke bawah dan variabel offset diperbarui ke i.
                fibM = fibMMm1 #memperbarui variabel
                fibMMm1 = fibMMm2
                fibMMm2 = fibM - fibMMm1 #fibMMm2 adalah hasil dari penjumlahan fibM - fibMMm1
                offset = i #memperbarui variabel offser

            # Jika elemen lebih besar dari x, geser ke bawah Fibonacci dua kali lebih banyak
            elif (arr[i][key] > x): #Jika nilai elemen dalam arr[i] lebih besar dari nilai yang dicari (x), maka nilai Fibonacci dikurangi lebih banyak lagi untuk menggeser pencarian ke bawah.
                fibM = fibMMm2 #memperbarui variabel
                fibMMm1 = fibMMm1 - fibMMm2 
                fibMMm2 = fibM - fibMMm1

            # Jika ditemukan, return indeksnya
            else:
                return i #Jika nilai elemen dalam arr[i] sama dengan nilai yang dicari (x), maka kembalikan indeks i.

        # Memeriksa elemen terakhir
        if (fibMMm1 and arr[offset + 1][key] == x): #ini memeriksa apakah  elemen terakhir dalam urutan Fibonacci apa cocok dengan nilai yang dicari (x). Jika cocok, kembalikan indeksnya.
            return offset + 1

        # Jika tidak ada yang cocok, kembalikan -1
        return -1 #Jika tidak ada elemen dalam daftar yang cocok dengan nilai yang dicari, kembalikan -1.

    def menu_search_data_kerusakan(self, key, value): #ini adalah fungsi search data kerusakan. dimana ada parameter didalamnya.  Fungsi ini adalah metode dari kelas Admin, karena memiliki parameter self. key itu buat pas usernya pilih search berdasarkan id atau lokasi atau juga tanggal. value Nilai yang akan dicari dalam kolom yang sesuai dengan key. 
        conn = buat_koneksi() #Membuat koneksi baru ke database menggunakan fungsi buat_koneksi().
        cursor = conn.cursor()#Membuat objek cursor dari koneksi database yang diberikan.
        try: #Memulai blok try untuk menangani eksekusi query.
            cursor.execute(
                "SELECT ID_data, lokasi, DATE_FORMAT(Tanggal, '%d %M %Y'), jenis_kerusakan, deskripsi, jumlah_kerusakan FROM data_kerusakan"
            )#eksekusi query untuk mengambil atau select data kerusakan dari table data_kerusakan
            data_kerusakan = cursor.fetchall()#Mengambil semua baris hasil query dan menyimpannya dalam variable data kerusakan

            # Membuat objek PrettyTable untuk hasil pencarian
            search_table = PrettyTable() #buat prettytable
            search_table.field_names = ["ID Data", "Lokasi", "Tanggal", "Jenis Kerusakan", "Deskripsi", "Jumlah Kerusakan"] #ini buat nama nama di kolom table

            # Mencari data berdasarkan key dan value
            if key == "ID_data": #ini memeriksa apakah key sama dengan id_data?
                # jika iya lanjut untuk menemukan data berdasarkan ID
                found = False #variabel found bernilai false
                for data in data_kerusakan: #perulangan untuk setiap baris data dalam data_kerusakan.
                    if str(data[0]) == value: #jika data[0] atau id_data sama dengan nilai yang dicari atau valuenya. atau data ditemukan!
                        search_table.add_row(data) #maka baris data tersebut ditambahkan ke dalam objek PrettyTable yang digunakan untuk menampilkan hasil pencarian.
                        found = True #memperbarui variabel found menjadi true
                        break #menghentikan perulangan
                if not found: #jika data tidak ditemukan!
                    print(f"Tidak ada data dengan ID {value}.") #maka print output seperti disamping
                    return #fungsi mengembalikan hasil
            elif key == "lokasi": #ini memeriksa apakah key sama dengan id_data?
                # Menemukan data berdasarkan lokasi (spesifik) bukan yang berdasarkan mirip-mirip
                found = False  #variabel found bernilai false
                for data in data_kerusakan: #perulangan untuk setiap baris data dalam data_kerusakan.
                    if data[1].strip().lower() == value.lower():  # penggunaan lower() untuk membandingkan tanpa memperdulikan huruf besar atau kecil. jika data[1] atau lokasi sama dengan valuenya. atau ditemukan!
                        search_table.add_row(data) #maka baris data tersebut ditambahkan ke dalam objek PrettyTable yang digunakan untuk menampilkan hasil pencarian.
                        found = True #memperbarui variabel found menjadi true
                        break   #menghentikan perulangan
                if not found: #jika data tidak ditemukan!
                    print(f"Tidak ada data dengan lokasi {value}.") #maka print output seperti disamping
                    return #fungsi mengembalikan hasil
            elif key == "tanggal": #ini memeriksa apakah key sama dengan id_data?
                # Ubah format tanggal yang dimasukkan pengguna menjadi objek tanggal
                value = datetime.strptime(value, '%d-%m-%Y').strftime('%d %B %Y') # digunakan untuk mengurai string tanggal ke dalam objek datetime, kemudian strftime() digunakan untuk mengonversi objek datetime kembali ke dalam string dengan format yang diinginkan.

                # Menemukan data berdasarkan tanggal
                found = False#variabel found bernilai false
                for data in data_kerusakan: #perulangan untuk setiap baris data dalam data_kerusakan.
                    if data[2] == value:#jika data[2] atau tanggal sama dengan nilai yang dicari atau valuenya. atau data ditemukan!
                        search_table.add_row(data)#maka baris data tersebut ditambahkan ke dalam objek PrettyTable yang digunakan untuk menampilkan hasil pencarian.
                        found = True #memperbarui variabel found menjadi true
                if not found:  #jika data tidak ditemukan!
                    print(f"Tidak ada data pada tanggal {value}.") #maka print output seperti disamping
                    return #fungsi mengembalikan hasil
            else:
                print("Key tidak valid. Silakan coba lagi.") #jika key yang dipilih user tidak ada dari ketika key diatas maka akan mengeluarkan output seperti disamping
                return

            # Batasi lebar maksimum untuk kolom Deskripsi agar tidak terlalu lebar
            search_table.max_width["Deskripsi"] = 80 #ini untuk biar table dengan nama kolom "deksripsi" isinya banyak. bakal akan langsung kepotong dan dilanjutkan ke baris bawah. biar gak KEPANJANGAN!

            # Cetak tabel hasil pencarian
            print("Pencarian ditemukan!")
            print(f"\nHasil Pencarian (Berdasarkan {key}):")
            print(search_table) #menampilkan tabel yang dicari berdasarkan key

        except mysql.connector.Error as err: #ini kalau error querynya bisa dikasih tau errornya karena apa
            print("Gagal melakukan pencarian data kerusakan:", err)
        finally:
            cursor.close() #tutup cursor
            conn.close() #tutup koneksi

    def menu_search_aduan(self, key, value): #ini adalah fungsi search daftar aduan. dimana ada parameter didalamnya. Fungsi ini adalah metode dari kelas Admin, karena memiliki parameter self. key itu buat pas usernya pilih search berdasarkan id atau lokasi atau juga tanggal. value Nilai yang akan dicari dalam kolom yang sesuai dengan key. 
        conn = buat_koneksi() #Membuat koneksi baru ke database menggunakan fungsi buat_koneksi().
        cursor = conn.cursor() #Membuat objek cursor dari koneksi database yang diberikan.
        try: #Memulai blok try untuk menangani eksekusi query.
            cursor.execute("SELECT * FROM aduan") #eksekusi query untuk mengambil atau select daftar aduan dari table aduan
            aduan_masyarakat = cursor.fetchall() #Mengambil semua baris hasil query dan menyimpannya dalam variable aduan_masyarakat

            # Membuat objek PrettyTable untuk hasil pencarian
            search_table = PrettyTable() #buat prettytable
            search_table.field_names = ["IDAduan", "ID Masyarakat", "Lokasi", "Tanggal", "Keterangan"] #ini buat nama nama di kolom table

            # Mencari data berdasarkan key dan value
            if key == "ID Aduan": #ini memeriksa apakah key sama dengan id_aduan?
                # Menemukan data berdasarkan ID Aduan
                found = False #variabel found bernilai false
                for aduan in aduan_masyarakat: #perulangan untuk setiap baris aduan dalam aduan_masyarakat.
                    if str(aduan[0]) == value: #jika data[0] atau id_aduan sama dengan nilai yang dicari atau valuenya. atau data ditemukan!
                        search_table.add_row(aduan) #maka baris aduan tersebut ditambahkan ke dalam objek PrettyTable yang digunakan untuk menampilkan hasil pencarian.
                        found = True #memperbarui variabel found menjadi true
                        break #menghentikan perulangan
                if not found:  #jika data tidak ditemukan!
                    print(f"Tidak ada aduan dengan ID {value}.") #maka print output seperti disamping
                    return #fungsi mengembalikan hasil
            elif key == "lokasi": #ini memeriksa apakah key sama dengan lokasi?
                # Menemukan data berdasarkan lokasi (spesifik) bukan yang berdasarkan mirip-mirip
                found = False #variabel found bernilai fals
                for aduan in aduan_masyarakat:
                    if aduan[2].strip().lower() == value.strip().lower():  #jika data[2] atau lokasi sama dengan nilai yang dicari atau valuenya. atau data ditemukan!
                        search_table.add_row(aduan) #maka baris aduan tersebut ditambahkan ke dalam objek PrettyTable yang digunakan untuk menampilkan hasil pencarian.
                        found = True #memperbarui variabel found menjadi true
                        break  # Hentikan pencarian setelah menemukan satu hasil
                if not found: #jika data tidak ditemukan!
                    print(f"Tidak ada aduan dengan lokasi {value}.")  #maka print output seperti disamping
                    return #fungsi mengembalikan hasil
            elif key == "tanggal":  #ini memeriksa apakah key sama dengan tanggal?
                # Menemukan data berdasarkan tanggal
                found = False #variabel found bernilai false
                for aduan in aduan_masyarakat:  #perulangan untuk setiap baris aduan dalam aduan_masyarakat.
                    if aduan[3].strftime('%Y-%m-%d') == value: #jika data[3] atau tanggal sama dengan nilai yang dicari atau valuenya. atau data ditemukan!
                        search_table.add_row(aduan) #maka baris aduan tersebut ditambahkan ke dalam objek PrettyTable yang digunakan untuk menampilkan hasil pencarian.
                        found = True #memperbarui variabel found menjadi true
                if not found: #jika data tidak ditemukan!
                    print(f"Tidak ada aduan pada tanggal {value}.")  #maka print output seperti disamping
                    return #fungsi mengembalikan hasil
            else:
                print("Key tidak valid. Silakan coba lagi.") #jika key yang dipilih user tidak ada dari ketika key diatas maka akan mengeluarkan output seperti disamping
                return

            search_table.max_width["Keterangan"] = 80 #ini untuk biar table dengan nama kolom "keterangan" isinya banyak. bakal akan langsung kepotong dan dilanjutkan ke baris bawah. biar gak KEPANJANGAN!

            # Cetak tabel hasil pencarian
            print(f"\nHasil Pencarian (Berdasarkan {key}):")
            print(search_table)  #menampilkan tabel yang dicari berdasarkan key

        except mysql.connector.Error as err: #ini kalau error querynya bisa dikasih tau errornya karena apa
            print("Gagal melakukan pencarian aduan masyarakat:", err)
        finally:
            cursor.close() #tutup cursor
            conn.close() #tutup koneksi

    def menu_search_masyarakat(self, field, value): #ini adalah fungsi search akun masyarakat. dimana ada parameter didalamnya. Fungsi ini adalah metode dari kelas Admin, karena memiliki parameter self. value itu nilai yang dicari user
        conn = buat_koneksi() #Membuat koneksi baru ke database menggunakan fungsi buat_koneksi().
        cursor = conn.cursor()#Membuat objek cursor dari koneksi database yang diberikan.
        try: #Memulai blok try untuk menangani eksekusi query.
            cursor.execute(f"SELECT * FROM masyarakat WHERE `ID_Masyarakat` = %s", (value,)) #eksekusi query untuk mengambil atau select akun masyarakat dari table masyarakat berdasarkan id_masyarakat yang dicari(value)
            masyarakat = cursor.fetchone() #Mengambil satu baris hasil query dan menyimpannya dalam variabel masyarakat. Fungsi fetchone() digunakan untuk mengambil satu baris hasil dari query yang dieksekusi sebelumnya. Jika tidak ada baris yang cocok, variabel masyarakat akan bernilai None.

            if masyarakat: #Setelah mendapatkan data akun masyarakat dari database, blok kode berikutnya menggunakan kondisi if masyarakat:
                print("\nInformasi Akun Masyarakat:")
                print("ID Masyarakat:", masyarakat[0]) #mengambil posisi table masyarakat di index 0 atau id_masyarakat
                print("Nama:", masyarakat[1]) #mengambil posisi table masyarakat di index 1 atau nama_lengkap
                print("Alamat:", masyarakat[2]) #mengambil posisi table masyarakat di index 2 atau alamat_rumah
                print("Nomor Telepon:", masyarakat[3]) #mengambil posisi table masyarakat di index 3 atau no_hp

                # Tampilkan aduan yang pernah dibuat oleh masyarakat
                cursor.execute("SELECT * FROM aduan WHERE ID_Masyarakat = %s", (value,))  #eksekusi query untuk mengambil atau select akun masyarakat dari table aduan berdasarkan id_masyarakat yang dicari(value)
                aduan_masyarakat = cursor.fetchall() #Mengambil semua baris hasil query dan menyimpannya dalam variable aduan_masyarakat

                if aduan_masyarakat: 
                    # Buat objek PrettyTable untuk menampilkan aduan
                    table_aduan = PrettyTable() #buat prettytable
                    table_aduan.field_names = ["ID Aduan", "ID_Masyarakat", "Lokasi", "Tanggal", "Keterangan"] #nama kolom prettytable

                    # Tambahkan baris data aduan ke tabel
                    for aduan in aduan_masyarakat: #perulangan untuk setiap baris aduan dalam aduan_masyarakat.
                        table_aduan.add_row(aduan[0:5])  # Ambil hanya kolom pertama hingga kelima

                    # Set lebar maksimum untuk kolom keterangan agar menyesuaikan dengan konten
                    table_aduan.max_width["Keterangan"] = 80 #ini untuk biar table dengan nama kolom "keterangan" isinya banyak. bakal akan langsung kepotong dan dilanjutkan ke baris bawah. biar gak KEPANJANGAN!
                    print("\nDaftar Aduan Masyarakat Yang  Dibuat:")
                    print(table_aduan)  #menampilkan tabel yang dicari berdasarkan key
                else:
                    print("\nMasyarakat ini belum membuat aduan!")

            else:
                print("Masyarakat dengan ID tersebut tidak ditemukan.")

        except mysql.connector.Error as err: #ini kalau error querynya bisa dikasih tau errornya karena apa
            print("Gagal mencari akun masyarakat:", err)
        finally:
            cursor.close() #tutup cursor
            conn.close() #tutup koneksi


    def lihat_data_kerusakan(self): #fungsi untuk melihat data kerusakan
        conn = buat_koneksi() #Membuat koneksi baru ke database menggunakan fungsi buat_koneksi().
        cursor = conn.cursor() #Membuat objek cursor dari koneksi database yang diberikan.
        try: #Memulai blok try untuk menangani eksekusi query.
            cursor.execute("SELECT ID_data, lokasi, DATE_FORMAT(Tanggal, '%d %M %Y'), jenis_kerusakan, deskripsi, jumlah_kerusakan FROM data_kerusakan") #eksekusi query untuk mengambil atau select data kerusakan dari table data_kerusakan
            data_kerusakan = cursor.fetchall() #Mengambil semua baris hasil query dan menyimpannya dalam variable data_kerusakan

            # Buat objek PrettyTable
            table = PrettyTable() #membuat pretty tabel
            table.field_names = ["ID Data", "Lokasi", "Tanggal", "Jenis Kerusakan", "Deskripsi", "Jumlah Kerusakan"] #nama kolom setiap prettytable

            # Tambahkan baris data ke tabel
            for data in data_kerusakan: #perulangan untuk setiap baris data dalam data_kerusakan
                table.add_row(data) #maka baris data tersebut ditambahkan ke dalam objek PrettyTable yang digunakan untuk menampilkan hasil pencarian.

            # Batasi lebar maksimum untuk kolom Deskripsi agar tidak terlalu lebar
            table.max_width["Deskripsi"] = 80 #ini untuk biar table dengan nama kolom "deskripsi" isinya banyak. bakal akan langsung kepotong dan dilanjutkan ke baris bawah. biar gak KEPANJANGAN!

            # Cetak tabel
            print("\nData Kerusakan:")
            print(table) 

        except mysql.connector.Error as err: #ini kalau error querynya bisa dikasih tau errornya karena apa
            print("Gagal mengambil data kerusakan:", err)
        finally:
            cursor.close() #tutup cursor
            conn.close() #tutup koneksi

    def hapus_data_kerusakan(self, id_data):
        conn = buat_koneksi() #Membuat koneksi baru ke database menggunakan fungsi buat_koneksi().
        cursor = conn.cursor() #Membuat objek cursor dari koneksi database yang diberikan.
        try: #Memulai blok try untuk menangani eksekusi query.
            # Periksa apakah data dengan ID yang diberikan ada dalam database
            cursor.execute("SELECT ID_data FROM data_kerusakan WHERE ID_data = %s", (id_data,)) #eksekusi query untuk mengambil atau select data kerusakan dari table data_kerusakan berdasarkan id_data
            result = cursor.fetchone() #Mengambil satu baris hasil query dan menyimpannya dalam variabel result. Fungsi fetchone() digunakan untuk mengambil satu baris hasil dari query yang dieksekusi sebelumnya. Jika tidak ada baris yang cocok, variabel masyarakat akan bernilai None.

            if result:
                # Data ditemukan, maka hapus data dari database
                query = "DELETE FROM data_kerusakan WHERE ID_data = %s" #eksekusi query untuk menghapus data kerusakan dari table data_kerusakan berdasarkan id_data
                cursor.execute(query, (id_data,)) #untuk eksekusi querynya melewati id_data. ada koma dibelakang id_data biar dia jadi tuple satu elemen
                conn.commit() #mengkonfirmasi bahwa perubahan yang dibuat bakal disimpan di database
                print("Data kerusakan berhasil dihapus.")
            else:
                # Data tidak ditemukan, berikan pesan kesalahan
                print(f"Tidak ada data kerusakan dengan ID {id_data}.")

            # Perbarui tampilan tabel data kerusakan
            self.lihat_data_kerusakan() #memanggil fungsi lihat data kerusakan

        except mysql.connector.Error as err: #ini kalau error querynya bisa dikasih tau errornya karena apa
            print("Gagal menghapus data kerusakan:", err)
        finally:
            cursor.close() #tutup cursor
            conn.close() #tutup koneksi

    def pindahkan_ke_data_kerusakan(self, cursor, id_aduan, id_admin): #ini fungsi pas update data kerusakan akan menggunakan fungsi pindahkan. agar data dari daftar aduan pindah ke data kerusakan
        try: #Memulai blok try untuk menangani eksekusi query.
            # Mendapatkan informasi aduan dan informasi aduan berdasarkan ID
            query = """
                SELECT aduan.lokasi, aduan.Tanggal, aduan.keterangan_aduan, data_kerusakan.jenis_kerusakan
                FROM aduan
                LEFT JOIN data_kerusakan ON aduan.ID_Aduan = data_kerusakan.ID_Aduan
                WHERE aduan.ID_Aduan = %s 
            """ #ini menggabungkan kedua tabel, table aduan dan table data kerusakan. 
            #Operasi LEFT JOIN digunakan untuk menggabungkan kedua tabel berdasarkan kunci yang diberikan (ID_Aduan), dengan semua baris dari tabel kiri (aduan) ditampilkan bahkan jika tidak ada yang cocok di tabel kanan (data_kerusakan).
            cursor.execute(query, (id_aduan,)) #untuk eksekusi querynya melewati id_aduan. ada koma dibelakang id_aduan biar dia jadi tuple satu elemen
            aduan_info = cursor.fetchone() #Mengambil satu baris hasil query dan menyimpannya dalam variabel aduan_info. Fungsi fetchone() digunakan untuk mengambil satu baris hasil dari query yang dieksekusi sebelumnya.

            if aduan_info: #jika aduan_info ini nilainya tidak none/kosong. artinya informasi aduan telah ditemukan.
                lokasi, tanggal, keterangan_aduan, jenis_kerusakan = aduan_info  #Di sini menetapkan nilai-nilai dalam tuple aduan_info ke dalam variabel lokasi, tanggal, keterangan_aduan, dan jenis_kerusakan dengan terpisah dan juga set sat set
                print(f"\n[Informasi Aduan!]\nLokasi: {lokasi}\nTanggal: {tanggal}\nKeterangan: {keterangan_aduan}")

                # Meminta informasi tambahan untuk data kerusakan
                #nah disini masih manual. jangan tanya kenapa ga buat yang otomatis. BINGUNG! harus buat db khusus kategorinya sendiri. 
                print("Pilih jenis kerusakan:")
                print("1. Hewan laut")
                print("2. Terumbu karang")
                print("3. Limbah laut")
                print("4. Kapal laut")
                print("5. Lainnya")
                jenis_kerusakan_input = input("Silahkan Pilih jenis kerusakan: ") 
                if jenis_kerusakan_input == "1": #ini memeriksa seperti biasayanya sesuai yang user mau. harus angka!
                    jenis_kerusakan = "Hewan laut" 
                elif jenis_kerusakan_input == "2":
                    jenis_kerusakan = "Terumbu karang"
                elif jenis_kerusakan_input == "3":
                    jenis_kerusakan = "Limbah laut"
                elif jenis_kerusakan_input == "4":
                    jenis_kerusakan = "Kapal laut"
                elif jenis_kerusakan_input == "5":
                    jenis_kerusakan = "Lainnya"
                else:
                    print("Pilihan kategori tidak valid.")

                if jenis_kerusakan_input in {"1", "2", "3", "4", "5"}: #ini biar gak satu satu. Himpunan string "1", "2", "3", "4", dan "5", yang mewakili jenis kerusakan.
                    # Memastikan deskripsi kerusakan hanya angka saja
                    deskripsi_kerusakan = input("Perbarui Keterangan: ") #ini memperbarui keterangan biar adminnya bisa saring bahasa dari masyrakat ke bahasa yang lebih baku dan lengkap

                    # Memastikan jumlah kerusakan hanya angka saja
                    while True: #perulangan while
                        jumlah_kerusakan = input("Masukan Jumlah Kerusakan: ") #ini untuk keperluan penyajian data dalam bentuk diagram
                        if jumlah_kerusakan.isdigit():  # Memeriksa apakah input adalah angka
                            jumlah_kerusakan = int(jumlah_kerusakan)  # Mengonversi input menjadi integer
                            break
                        else:
                            print("Masukan harus berupa angka. Silakan coba lagi.")

                # Menambahkan aduan ke data kerusakan
                query_insert = """
                    INSERT INTO data_kerusakan (ID_Admin, lokasi, tanggal, jenis_kerusakan, deskripsi, jumlah_kerusakan, ID_Aduan)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """ #ini perintah untuk memasukan data ke table data_kerusakan
                cursor.execute(query_insert, (id_admin, lokasi, tanggal, jenis_kerusakan, deskripsi_kerusakan, jumlah_kerusakan, id_aduan)) #untuk eksekusi querynya.

                print("Aduan berhasil dipindahkan ke data kerusakan.")
                query_delete = "DELETE FROM aduan WHERE ID_Aduan = %s" #kalau data berhasil dipindahkan ke data kerusakan. langsung hapus di bagian daftar aduan masyarakat
                cursor.execute(query_delete, (id_aduan,)) #untuk eksekusi querynya.
            else:
                print("ID Aduan tidak ditemukan. ID harus berupa angka!")

        except mysql.connector.Error as err: #ini kalau error querynya bisa dikasih tau errornya karena apa
            print("Gagal memindahkan aduan ke data kerusakan:", err)

    def update_data_kerusakan(self): #nah ini fungsi untuk updatenya bakal berkaitan dengan fungsi pindah_ke_data_kerusakan
        conn = buat_koneksi() #Membuat koneksi baru ke database menggunakan fungsi buat_koneksi().
        cursor = conn.cursor() #Membuat objek cursor dari koneksi database yang diberikan.
        try: #Memulai blok try untuk menangani eksekusi query.
            cursor.execute("SELECT ID_Aduan, ID_Masyarakat, lokasi, Tanggal, keterangan_aduan FROM aduan") #eksekusi query untuk mengambil atau select daftar aduan dari table aduan
            aduan_masyarakat = cursor.fetchall() #Mengambil semua baris hasil query dan menyimpannya dalam variable aduan_masyarakat

            # Buat objek PrettyTable
            table = PrettyTable() #buat prettytable
            table.field_names = ["ID Aduan", "ID Masyarakat", "Lokasi", "Tanggal", "Keterangan"] #buat namain kolom-kolom setiap prettytabel

            # Tambahkan baris data ke tabel
            for aduan in aduan_masyarakat: #perulangan untuk setiap baris aduan dalam aduan_masyarakat
                table.add_row(aduan)  #maka baris aduan tersebut ditambahkan ke dalam objek PrettyTable yang digunakan untuk menampilkan hasil pencarian.

            # Cetak tabel
            print("\nDaftar Aduan Masyarakat:")
            table.max_width["Keterangan"] = 80 #ini untuk biar table dengan nama kolom "keterangan" isinya banyak. bakal akan langsung kepotong dan dilanjutkan ke baris bawah. biar gak KEPANJANGAN!
            print(table)

            id_aduan = input("\nPilih ID_aduan aduan --> data kerusakan(kosongkan untuk kembali): ")
            if id_aduan:
                # Panggil metode pindahkan_ke_data_kerusakan dengan menyediakan nilai id_admin
                result = self.pindahkan_ke_data_kerusakan(cursor, id_aduan, self.ID_Admin)

        except mysql.connector.Error as err: #ini kalau error querynya bisa dikasih tau errornya karena apa
            print("Gagal mengambil daftar aduan:", err)
        finally:
            cursor.close() #tutup cursor
            conn.close() #tutup koneksi

    def lihat_aduan_masyarakat(self):
        conn = buat_koneksi() #Membuat koneksi baru ke database menggunakan fungsi buat_koneksi().
        cursor = conn.cursor() #Membuat objek cursor dari koneksi database yang diberikan.
        try: #Memulai blok try untuk menangani eksekusi query.
            cursor.execute("SELECT * FROM aduan") #eksekusi query untuk mengambil atau select daftar aduan dari table aduan
            aduan_masyarakat = cursor.fetchall() #Mengambil semua baris hasil query dan menyimpannya dalam variable aduan_masyarakat

            # Buat objek PrettyTable
            table = PrettyTable()  #buat prettytable
            table.field_names = ["ID Aduan", "ID Masyarakat", "Lokasi", "Tanggal", "Keterangan"] #buat namain kolom-kolom setiap prettytabel

            # Tambahkan baris data ke tabel
            for aduan in aduan_masyarakat: #perulangan untuk setiap baris aduan dalam aduan_masyarakat
                table.add_row(aduan) #maka baris aduan tersebut ditambahkan ke dalam objek PrettyTable yang digunakan untuk menampilkan hasil pencarian.

            # Cetak tabel
            print("\nDaftar Aduan Masyarakat:")
            # Set lebar maksimum untuk kolom keterangan agar menyesuaikan dengan konten
            table.max_width["Keterangan"] = 80 #ini untuk biar table dengan nama kolom "keterangan" isinya banyak. bakal akan langsung kepotong dan dilanjutkan ke baris bawah. biar gak KEPANJANGAN!
            print(table) #tampilin tablenya

        except mysql.connector.Error as err: #ini kalau error querynya bisa dikasih tau errornya karena apa
            print("Gagal mengambil daftar aduan:", err)
        finally:
            cursor.close() #tutup cursor
            conn.close() #tutup koneksi

    def hapus_aduan(self, id_aduan):
        # Validasi bahwa id_aduan hanya berisi angka
        if not id_aduan.isdigit(): #ini memeriksa apakah id_aduan yang user masukkan itu angka apa ngga? HARUS ANGKA!
            print("ID aduan harus berupa angka.")
            return
        conn = buat_koneksi() #Membuat koneksi baru ke database menggunakan fungsi buat_koneksi().
        cursor = conn.cursor() #Membuat objek cursor dari koneksi database yang diberikan.
        try: #Memulai blok try untuk menangani eksekusi query.
            # Periksa apakah aduan dengan ID yang diberikan ada dalam database
            cursor.execute("SELECT ID_Aduan FROM aduan WHERE ID_Aduan = %s", (id_aduan,)) #eksekusi query untuk mengambil atau select daftar aduan dari table aduan berdasarkan id_aduan
            result = cursor.fetchone() #Mengambil satu baris hasil query dan menyimpannya dalam variabel result. Fungsi fetchone() digunakan untuk mengambil satu baris hasil dari query yang dieksekusi sebelumnya.

            if result: #jika result ini nilainya tidak none/kosong. artinya informasi aduan telah ditemukan.
                # Aduan ditemukan, maka hapus aduan dari database
                query = "DELETE FROM aduan WHERE ID_Aduan = %s" #eksekusi query untuk menghapus daftar aduan dari table aduan berdasarkan id_aduan
                cursor.execute(query, (id_aduan,)) #buat eksekusi querynya.
                conn.commit() #biasa dikasih pas ada query hapus data, tugasnya memastikan bahwa perubahan tersebut diterapkan secara permanen pada database.

                print("Aduan berhasil dihapus.")
            else:
                # Aduan tidak ditemukan, berikan pesan kesalahan
                print(f"Tidak ada aduan dengan ID {id_aduan}.")

        except mysql.connector.Error as err: #ini kalau error querynya bisa dikasih tau errornya karena apa
            print("Gagal menghapus aduan:", err)
        finally:
            cursor.close() #tutup cursor
            conn.close() #tutup koneksi

    def lihat_akun_masyarakat(self):
        conn = buat_koneksi() #Membuat koneksi baru ke database menggunakan fungsi buat_koneksi().
        cursor = conn.cursor() #Membuat objek cursor dari koneksi database yang diberikan.
        try: #Memulai blok try untuk menangani eksekusi query.
            cursor.execute("""
                SELECT m.ID_Masyarakat, m.Nama_Lengkap, m.Alamat_Rumah, m.No_HP, 
                    COUNT(a.ID_Aduan) AS jumlah_aduan
                FROM masyarakat m
                LEFT JOIN aduan a ON m.ID_Masyarakat = a.ID_Masyarakat 
                GROUP BY m.ID_Masyarakat
            """) #memastikan bahwa semua baris dari tabel masyarakat tetap termasuk dalam hasil, bahkan jika tidak ada yang cocok di tabel aduan.
            #menggunakan klausa GROUP BY untuk mengelompokkan hasil berdasarkan nilai ID_Masyarakat.

            akun_masyarakat = cursor.fetchall() #Mengambil semua baris hasil query dan menyimpannya dalam variable akun_masyarakat

            # Buat objek PrettyTable
            table = PrettyTable() #buat prettytable
            table.field_names = ["ID Masyarakat", "Nama Lengkap", "Alamat Rumah", "Nomor HP", "Jumlah Aduan"] #buat namain kolom-kolom setiap prettytabel

            # Tambahkan baris data ke tabel
            for akun in akun_masyarakat: #perulangan untuk setiap baris akun dalam akun_masyarakat
                table.add_row(akun) #maka baris akun tersebut ditambahkan ke dalam objek PrettyTable yang digunakan untuk menampilkan hasil pencarian

            # Cetak tabel
            print("\nDaftar Akun Masyarakat:")
            print(table) #tampilkan table

        except mysql.connector.Error as err: #ini kalau error querynya bisa dikasih tau errornya karena apa
            print("Gagal mengambil daftar akun masyarakat:", err)
        finally:
            cursor.close() #tutup cursor
            conn.close() #tutup koneksi







#==========BLUEPRINT MASYARAKAT DAN PROSES MENUNYA==============
class Masyarakat(User):  #class masyarakat untuk buat blueprint pengguna masyarakat. nah masyarakat ini mewarisi sifat sifat dari class user
    def __init__(self, ID_Masyarakat, nama_lengkap, no_hp, alamat_rumah): #ini konstruktor masyarakat
        super().__init__(nama_lengkap, no_hp)  #ini atribut yang mewarisi class user
        self.ID_Masyarakat = ID_Masyarakat
        self.alamat_rumah = alamat_rumah
        self.nomor_hp = no_hp
        self.no_ktp = ID_Masyarakat

    def tampilkan_informasi_akun(self):   #ini fungsi untuk menampilkan fungsi pemilik akun yang sedang login
        # Tampilkan informasi akun masyarakat
        print("\n============INFORMASI AKUN===============")
        print("Nomor KTP: ",self.no_ktp)  #panggil atributnya dari class masyarakat
        print("Nama Lengkap:", self.nama_lengkap)  
        print("Alamat:", self.alamat_rumah) 
        print("Nomor HP:", self.nomor_hp)  

    def edit_informasi_akun(self):  #ini fungsi untuk mengedit informasi akun diatas. tapi cuma bisa edit nomor hape sama alamat. yang lain gak boleh!
        # Mengedit informasi akun masyarakat
        print("\nEdit Informasi Akun:")
        alamat_baru = input("Masukkan alamat baru: ") #masukkan alamat baru dulu
        
        # Validasi nomor HP agar hanya berisi angka
        while True: #perulangan
            nomor_hp_baru = input("Masukkan nomor HP baru: ") #terus masukkan nomor hape baru
            if nomor_hp_baru.isdigit(): #nomor hape yang baru harus angka! kalau ngga gak boleh!
                break
            else:
                print("Nomor HP hanya boleh berisi angka. Silakan coba lagi.")

        # Lakukan validasi data yang dimasukkan sebelum melakukan pembaruan di database
        if alamat_baru.strip() == "" or nomor_hp_baru.strip() == "": #alamat baru dikasi strip() biar kalau ada spasi spasi gak jelas otomatis dihapus otomatis. nomor hape juga. kodisi mereka berdua gak boleh juga kosong
            print("Alamat dan nomor HP tidak boleh kosong. Silakan coba lagi.")
        else:
            # Lakukan pembaruan data di database
            conn = buat_koneksi() #Membuat koneksi baru ke database menggunakan fungsi buat_koneksi().
            cursor = conn.cursor() #Membuat objek cursor dari koneksi database yang diberikan.
            try:
                cursor.execute("UPDATE masyarakat SET alamat_rumah = %s, no_hp = %s WHERE ID_Masyarakat = %s",
                            (alamat_baru, nomor_hp_baru, self.ID_Masyarakat)) #eksekusi query untuk mengupdate akun masyarakat dari table masyarakat
                conn.commit() #biasa dikasih pas ada query update data, tugasnya memastikan bahwa perubahan tersebut diterapkan secara permanen pada database.
                print("Informasi akun berhasil diperbarui.")
                self.alamat_rumah = alamat_baru  #nilai atribut diperbarui
                self.nomor_hp = nomor_hp_baru  
            except mysql.connector.Error as err: #ini kalau error querynya bisa dikasih tau errornya karena apa
                print("Gagal memperbarui informasi akun:", err)
            finally:
                cursor.close() #tutup cursor
                conn.close() #tutup koneksi

    def lihat_dan_edit_informasi_akun(self):  #nah ini buat nampilin fungsi menu edit akun diatas tadi
        while True: #perulangan while
            self.tampilkan_informasi_akun()  #memanggil fungsi tampilkan akun

            print("\n\033[0m\033[91m1.\033[0m Edit Informasi Akun")
            print("\033[0m\033[91m2.\033[0m Kembali ke Menu Utama")

            pilihan = input("Masukkan pilihan Anda: ")

            if pilihan == "1":
                # Panggil fungsi untuk mengedit informasi akun
                self.edit_informasi_akun() 
            elif pilihan == "2":
                # Kembali ke menu utama
                break #memberhentikan perulangan
            else:
                print("Pilihan tidak valid. Silakan pilih opsi yang valid.")

    #ini proses perbandingan!
    @staticmethod #ini statis method. gunanya untuk mendeklarasikan si def merge sama merge_sort dibawahnya. biar mereka itu dapat dipanggil gitu loh di class admin tanpa harus buat objek baru di class.
    def merge(left, right, key, reverse=False): #ini fungsi merge dan parameternya. left pertama digabungkan, right yang kedua digabungkan, key kunci berdasarkan elemen mana dalam daftar yang akan dibandingkan. reverse itu argumen opsional buat nentuin apa penggabungannya dilakukan secara terbalik atau tidak? nilai defaultnya false
        result = [] #ini tempat untuk nyimpen hasil penggabungan. daftar kosong
        i = j = 0 #Inisialisasi dua variabel i dan j dengan nilai 0.
        while i < len(left) and j < len(right): #nah disini i itu sebelah kiri dan j itu sebelah kanan dengan nilai masing masing 0
            if not reverse: #Pengecekan apakah argumen reverse adalah False. Jika ya, penggabungan akan dilakukan secara normal.
                if left[i][key] < right[j][key]: #disini membandingkan nilai kunci kiri apa lebih kecil dari yang kanan? kalau lebih kecil akan ditambahkan ke result[]
                    result.append(left[i]) #ini nambahkan nilai kunci sebelah kiri ke result[]
                    i += 1 #nilai i yang dari awal 0 di tambah 1
                else:
                    result.append(right[j]) #kalau nilai sebelah kiri gak lebih kecil dari yang kanan maka nilai kunci kanan yang dimasukkan ke result[]
                    j += 1 #nilai j yang dari awal 0 ditambah 1
            else: #ini jika pengecekan apakah argumen reverse adalah selain false. penggabungan dilakukan tidak secara normal
                if left[i][key] > right[j][key]: #jika nilai key sebelah kiri lebih besar maka dia masuk ke result[]
                    result.append(left[i]) #nilai i atau nilai kiri dimasukkan ke result[]
                    i += 1 #nilai i yang dari awal 0 di tambah 1
                else:
                    result.append(right[j]) #nilai j atau nilai kanan dimasukkan ke result[] kalau nilai key kanan yang lebih besar
                    j += 1 #nilai j yang dari awal 0 di tambah 1
        result.extend(left[i:]) #Menambahkan sisa elemen dari daftar left (jika ada) ke result.
        result.extend(right[j:]) #Menambahkan sisa elemen dari daftar right (jika ada) ke result.
        return result #menggabungkan hasil penggabungan dari left dan right dalam bentuk daftar baru

    #ini proses pengurutan!
    @staticmethod #ini statis method. gunanya untuk mendeklarasikan si def merge sama merge_sort dibawahnya. biar mereka itu dapat dipanggil gitu loh di class admin tanpa harus buat objek baru di class.
    def merge_sort(arr, key, reverse=False): #ini fungsi merge dan parameternya. arr it daftar yang akan diurutkan, key itu kunci berdasarkan elemen mana dalam daftar yang akan diurutkan, reverse itu argumen opsional buat nentuin apa pengurutannya dilakukan secara terbalik atau tidak? nilai defaultnya false
        if len(arr) <= 1: #ini pengecekan apakah panjang daftar arr kurang atau sama dengan 1
            return arr #kalau iya maka return arr
        mid = len(arr) // 2 #menghitung index tengah(mid) dari daftar arr. buat bagi daftar jadi dua bagian yang hampir sama besar 
        left = Admin.merge_sort(arr[:mid], key, reverse) #manggil fungsi merge_sort untuk mengurutkan setengah pertama dari daftar arr. arr[:mid] ini nanti digunakan untuk ngambil setengah pertama dari daftar.
        right = Admin.merge_sort(arr[mid:], key, reverse) #manggil fungsi merge_sort untuk mengurutkan setengah kedua dari daftar arr. arr[:mid] ini nanti digunakan untuk ngambil setengah kedua dari daftar.
        return Admin.merge(left, right, key, reverse) #menggabungkan dan mengurutkan dua bagian terurut dari daftar arr yaitu left dan right nya menggunakan fungsi merge.


    def sort_merge_data_kerusakan(self, conn, key, reverse=False): #ini fungsi untuk mengurutkan data kerusakan. self itu merujuk ke class yang memanggil method, conn ini koneksi database untuk eksekusi query, key Kunci berdasarkan mana data kerusakan akan diurutkan kayak id, lokasi tanggal, Argumen opsional yang menentukan apakah pengurutan akan dilakukan secara terbalik atau tidak. Nilainya default adalah False
        cursor = conn.cursor() #Membuat objek cursor dari koneksi database yang diberikan.
        try: #Memulai blok try untuk menangani eksekusi query.
            cursor.execute(
                "SELECT ID_data, lokasi, DATE_FORMAT(Tanggal, '%d %M %Y'), jenis_kerusakan, deskripsi, jumlah_kerusakan FROM data_kerusakan" #eksekusi query untuk mengambil atau select data kerusakan dari table data_kerusakan
            ) #eksekusi query untuk mengambil atau select data kerusakan dari table data kerusakan
            data_kerusakan = cursor.fetchall() #Mengambil semua baris hasil query dan menyimpannya dalam variabel

            sorted_data = self.merge_sort(data_kerusakan, key=key, reverse=reverse) #memanggil fungsi merge_sort untuk mengurutkan data kerusakanberdasarkan key yang diinginkan pengguna.  Pengurutan dapat dilakukan secara terbalik jika reverse disetel sebagai True.

            # Membuat objek PrettyTable
            table = PrettyTable()  #buat prettytable
            table.field_names = ["ID_data", "Lokasi", "Tanggal", "Jenis Kerusakan", "Deskripsi", "Jumlah Kerusakan"] #ini buat nama nama di kolom table

            # Menambahkan baris data yang sudah diurutkan ke dalam tabel
            for data in sorted_data: #perulangan untuk sorted_data satu per satu. nilainya akan disimpan dalam variabel data.
                table.add_row(data)  #ini menambahkan baris dan menampilkan tabel dengan baris sesuai isi variabel data

            # Mencetak tabel yang sudah diurutkan
            print(f"\nData Kerusakan:")
            table.max_width["Deskripsi"] = 80 #ini untuk biar table dengan nama kolom "deskripsi" isinya banyak. bakal akan langsung kepotong dan dilanjutkan ke baris bawah. biar gak KEPANJANGAN!
            print(table) #tampilkan table

        except mysql.connector.Error as err: #ini kalau error querynya bisa dikasih tau errornya karena apa
            print("Gagal mengambil data kerusakan:", err)
        finally:
            cursor.close() #tutup cursor

    def menu_sorting_data_kerusakan(self): #ini fungsi untuk manggil semua proses sortingan sesuai mau user. key dari fungsi diatas berasal dari sini
        choice = input("\nIngin Sorting Berdasarkan Apa? (Lokasi/Tanggal): ").lower() #ini user akan input mau sorting berdasarkan lokasi apa tanggal?
        conn = buat_koneksi() #Membuat koneksi baru ke database menggunakan fungsi buat_koneksi().
        if choice == "lokasi": #ini proses jika user pilih lokasi
            self.sort_merge_data_kerusakan(conn, key=1)  #dia akan langsung memanggil methode sort_merge_data_kerusakan untuk mengurutkan berdasarkan lokasi. Argumen key=1 digunakan untuk menentukan bahwa pengurutan akan dilakukan berdasarkan kolom "Lokasi" (kolom ke-2 dalam definisi tabel).
        elif choice == "tanggal":  #ini proses jika user pilih tanggal
            self.sort_merge_data_kerusakan(conn, key=2) #dia akan langsung memanggil methode sort_merge_data_kerusakan untuk mengurutkan berdasarkan tanggal. Argumen key=2 digunakan untuk menentukan bahwa pengurutan akan dilakukan berdasarkan kolom "tanggal" (kolom ke-3 dalam definisi tabel).
        else:
            print("Pilihan Tidak Ada!") #output jika user memilih selain lokasi atau tanggal
        conn.close() #tutup koneksi


    def fibonacci_search(self, arr, x, key): #ini fungsi fibbonaci search dan parameternya. self, merujuk pada class yang memanggil metode, arr daftar yang dicari, x nilai yang dicari didalam daftar
            fibMMm2 = 0   #ini bilangan primitif dari fibonacci
            fibMMm1 = 1   #ini bilangan primitif dari fibonacci
            fibM = fibMMm2 + fibMMm1  #bilangan primitif selalu ditambah dengan bilangan sebelumnya. contoh 0+1=1 1+1=2 2+1=3 3+1=4

            # fibM menjadi terbesar Fibonacci yang <= panjang array
            while (fibM < len(arr)): #perulangan dimana hasil penjumlahan bilangan primitif dibandingkan apakah lebih kecil dari panjang array
                fibMMm2 = fibMMm1 #kalau lebih kecil, fibMMm2 yang awalnya nilainya 0 diisi dengan fibMMm1 yang bernilai 1
                fibMMm1 = fibM #fibMMm1 yang awalnya nilainya 1 diubah menjadi jumlah dari penjumlahan bilangan primitif yang pertama fibM.
                fibM = fibMMm2 + fibMMm1 #fibM kembali diisi dengan hasil penjumlahan fibMMm2 + fibMMm1 atau 1+1=2

            offset = -1 #Variabel offset diinisialisasi dengan nilai -1. Ini akan digunakan untuk menandai posisi saat mencari di dalam daftar.

            while (fibM > 1): #ini perulangan dimana hasil penjumlahan fibMMm2 + fibMMm1 atau variabel fibM dibandingkan apakah lebih besar dari 1 atau ngga?
                i = min(offset + fibMMm2, len(arr) - 1) #kalau lebih besar dari 1 maka, i adalah nilai minimum dari offset + fibMMm2 dan len(rr) - 1 atau panjang dari daftar arr dikurangi 1. karena index di pyton itu mulai dari 0.

                # Jika elemen lebih kecil dari x, geser ke bawah Fibonacci satu kali lebih banyak
                if (arr[i][key] < x): #Jika nilai elemen dalam arr[i] kurang dari nilai yang dicari (x), maka nilai Fibonacci dikurangi untuk menggeser pencarian ke bawah dan variabel offset diperbarui ke i.
                    fibM = fibMMm1 #memperbarui variabel
                    fibMMm1 = fibMMm2
                    fibMMm2 = fibM - fibMMm1 #fibMMm2 adalah hasil dari penjumlahan fibM - fibMMm1
                    offset = i #memperbarui variabel offser

                # Jika elemen lebih besar dari x, geser ke bawah Fibonacci dua kali lebih banyak
                elif (arr[i][key] > x): #Jika nilai elemen dalam arr[i] lebih besar dari nilai yang dicari (x), maka nilai Fibonacci dikurangi lebih banyak lagi untuk menggeser pencarian ke bawah.
                    fibM = fibMMm2 #memperbarui variabel
                    fibMMm1 = fibMMm1 - fibMMm2 
                    fibMMm2 = fibM - fibMMm1

                # Jika ditemukan, return indeksnya
                else:
                    return i #Jika nilai elemen dalam arr[i] sama dengan nilai yang dicari (x), maka kembalikan indeks i.

            # Memeriksa elemen terakhir
            if (fibMMm1 and arr[offset + 1][key] == x): #ini memeriksa apakah  elemen terakhir dalam urutan Fibonacci apa cocok dengan nilai yang dicari (x). Jika cocok, kembalikan indeksnya.
                return offset + 1

            # Jika tidak ada yang cocok, kembalikan -1
            return -1 #Jika tidak ada elemen dalam daftar yang cocok dengan nilai yang dicari, kembalikan -1.

    def menu_search_data_kerusakan(self, key, value): #ini adalah fungsi search data kerusakan. dimana ada parameter didalamnya.  Fungsi ini adalah metode dari kelas Admin, karena memiliki parameter self. key itu buat pas usernya pilih search berdasarkan id atau lokasi atau juga tanggal. value Nilai yang akan dicari dalam kolom yang sesuai dengan key. 
        conn = buat_koneksi() #Membuat koneksi baru ke database menggunakan fungsi buat_koneksi().
        cursor = conn.cursor()#Membuat objek cursor dari koneksi database yang diberikan.
        try: #Memulai blok try untuk menangani eksekusi query.
            cursor.execute(
                "SELECT ID_data, lokasi, DATE_FORMAT(Tanggal, '%d %M %Y'), jenis_kerusakan, deskripsi, jumlah_kerusakan FROM data_kerusakan"
            )#eksekusi query untuk mengambil atau select data kerusakan dari table data_kerusakan
            data_kerusakan = cursor.fetchall()#Mengambil semua baris hasil query dan menyimpannya dalam variable data kerusakan

            # Membuat objek PrettyTable untuk hasil pencarian
            search_table = PrettyTable() #buat prettytable
            search_table.field_names = ["ID Data", "Lokasi", "Tanggal", "Jenis Kerusakan", "Deskripsi", "Jumlah Kerusakan"] #ini buat nama nama di kolom table

            # Mencari data berdasarkan key dan value
            if key == "ID_data": #ini memeriksa apakah key sama dengan id_data?
                # jika iya lanjut untuk menemukan data berdasarkan ID
                found = False #variabel found bernilai false
                for data in data_kerusakan: #perulangan untuk setiap baris data dalam data_kerusakan.
                    if str(data[0]) == value: #jika data[0] atau id_data sama dengan nilai yang dicari atau valuenya. atau data ditemukan!
                        search_table.add_row(data) #maka baris data tersebut ditambahkan ke dalam objek PrettyTable yang digunakan untuk menampilkan hasil pencarian.
                        found = True #memperbarui variabel found menjadi true
                        break #menghentikan perulangan
                if not found: #jika data tidak ditemukan!
                    print(f"Tidak ada data dengan ID {value}.") #maka print output seperti disamping
                    return #fungsi mengembalikan hasil
            elif key == "lokasi": #ini memeriksa apakah key sama dengan id_data?
                # Menemukan data berdasarkan lokasi (spesifik) bukan yang berdasarkan mirip-mirip
                found = False  #variabel found bernilai false
                for data in data_kerusakan: #perulangan untuk setiap baris data dalam data_kerusakan.
                    if data[1].strip().lower() == value.lower():  # penggunaan lower() untuk membandingkan tanpa memperdulikan huruf besar atau kecil. jika data[1] atau lokasi sama dengan valuenya. atau ditemukan!
                        search_table.add_row(data) #maka baris data tersebut ditambahkan ke dalam objek PrettyTable yang digunakan untuk menampilkan hasil pencarian.
                        found = True #memperbarui variabel found menjadi true
                        break   #menghentikan perulangan
                if not found: #jika data tidak ditemukan!
                    print(f"Tidak ada data dengan lokasi {value}.") #maka print output seperti disamping
                    return #fungsi mengembalikan hasil
            elif key == "tanggal": #ini memeriksa apakah key sama dengan id_data?
                # Ubah format tanggal yang dimasukkan pengguna menjadi objek tanggal
                value = datetime.strptime(value, '%d-%m-%Y').strftime('%d %B %Y') # digunakan untuk mengurai string tanggal ke dalam objek datetime, kemudian strftime() digunakan untuk mengonversi objek datetime kembali ke dalam string dengan format yang diinginkan.

                # Menemukan data berdasarkan tanggal
                found = False#variabel found bernilai false
                for data in data_kerusakan: #perulangan untuk setiap baris data dalam data_kerusakan.
                    if data[2] == value:#jika data[2] atau tanggal sama dengan nilai yang dicari atau valuenya. atau data ditemukan!
                        search_table.add_row(data)#maka baris data tersebut ditambahkan ke dalam objek PrettyTable yang digunakan untuk menampilkan hasil pencarian.
                        found = True #memperbarui variabel found menjadi true
                if not found:  #jika data tidak ditemukan!
                    print(f"Tidak ada data pada tanggal {value}.") #maka print output seperti disamping
                    return #fungsi mengembalikan hasil
            else:
                print("Key tidak valid. Silakan coba lagi.") #jika key yang dipilih user tidak ada dari ketika key diatas maka akan mengeluarkan output seperti disamping
                return

            # Batasi lebar maksimum untuk kolom Deskripsi agar tidak terlalu lebar
            search_table.max_width["Deskripsi"] = 80 #ini untuk biar table dengan nama kolom "deksripsi" isinya banyak. bakal akan langsung kepotong dan dilanjutkan ke baris bawah. biar gak KEPANJANGAN!

            # Cetak tabel hasil pencarian
            print("Pencarian ditemukan!")
            print(f"\nHasil Pencarian (Berdasarkan {key}):")
            print(search_table) #menampilkan tabel yang dicari berdasarkan key

        except mysql.connector.Error as err: #ini kalau error querynya bisa dikasih tau errornya karena apa
            print("Gagal melakukan pencarian data kerusakan:", err)
        finally:
            cursor.close() #tutup cursor
            conn.close() #tutup koneksi


    def lihat_data_kerusakan(self): #fungsi untuk melihat data kerusakan
        conn = buat_koneksi() #Membuat koneksi baru ke database menggunakan fungsi buat_koneksi().
        cursor = conn.cursor() #Membuat objek cursor dari koneksi database yang diberikan.
        try: #Memulai blok try untuk menangani eksekusi query.
            cursor.execute("SELECT ID_data, lokasi, DATE_FORMAT(Tanggal, '%d %M %Y'), jenis_kerusakan, deskripsi, jumlah_kerusakan FROM data_kerusakan") #eksekusi query untuk mengambil atau select data kerusakan dari table data_kerusakan
            data_kerusakan = cursor.fetchall() #Mengambil semua baris hasil query dan menyimpannya dalam variable data_kerusakan

            # Buat objek PrettyTable
            table = PrettyTable() #membuat pretty tabel
            table.field_names = ["ID Data", "Lokasi", "Tanggal", "Jenis Kerusakan", "Deskripsi", "Jumlah Kerusakan"] #nama kolom setiap prettytable

            # Tambahkan baris data ke tabel
            for data in data_kerusakan: #perulangan untuk setiap baris data dalam data_kerusakan
                table.add_row(data) #maka baris data tersebut ditambahkan ke dalam objek PrettyTable yang digunakan untuk menampilkan hasil pencarian.

            # Batasi lebar maksimum untuk kolom Deskripsi agar tidak terlalu lebar
            table.max_width["Deskripsi"] = 80 #ini untuk biar table dengan nama kolom "deskripsi" isinya banyak. bakal akan langsung kepotong dan dilanjutkan ke baris bawah. biar gak KEPANJANGAN!

            # Cetak tabel
            print("\nData Kerusakan:")
            print(table) 

        except mysql.connector.Error as err: #ini kalau error querynya bisa dikasih tau errornya karena apa
            print("Gagal mengambil data kerusakan:", err)
        finally:
            cursor.close() #tutup cursor
            conn.close() #tutup koneksi
    
    def lihat_diagram_kerusakan_bar(self, cursor=None, conn=None): #ini untuk membuat diagram batang. cursor dan conn adalah parameter opsional yang digunakan untuk menerima objek kursor dan koneksi database. Jika tidak diberikan, mereka akan diinisialisasi dengan nilai default None
        conn = buat_koneksi() #Membuat koneksi baru ke database menggunakan fungsi buat_koneksi().
        cursor = conn.cursor() #Membuat objek cursor dari koneksi database yang diberikan.
        try: #Memulai blok try untuk menangani eksekusi query.
            cursor.execute("SELECT jenis_kerusakan, SUM(jumlah_kerusakan) FROM data_kerusakan GROUP BY jenis_kerusakan") #eksekusi query untuk mengambil atau select data kerusakan dari table data_kerusakan
            jumlah_kerusakan = cursor.fetchall() #Mengambil semua baris hasil query dan menyimpannya dalam variable jumlah_kerusakan

            # Memisahkan data ke dalam dua list: jenis kerusakan dan jumlah kerusakan
            jenis_kerusakan = [item[0] for item in jumlah_kerusakan]
            jumlah = [item[1] for item in jumlah_kerusakan]

            # Membuat diagram batang
            plt.bar(jenis_kerusakan, jumlah) # Ini adalah panggilan fungsi bar dari library matplotlib.pyplot (biasanya diimpor sebagai plt). Fungsi ini digunakan untuk membuat diagram batang.
            plt.xlabel('Jenis Kerusakan') #Parameter pertama adalah kumpulan data yang akan digunakan sebagai sumbu x dalam diagram batang.
            plt.ylabel('Jumlah Kerusakan') #Parameter kedua adalah kumpulan data yang akan digunakan sebagai tinggi dari batang dalam diagram.
            plt.title('Diagram Batang Jumlah Kerusakan Berdasarkan Jenis Kerusakan')
            plt.xticks(rotation=45) #Parameter rotation digunakan untuk menentukan sudut rotasi. nilai 45 menunjukkan bahwa label-label tersebut akan diputar sebesar 45 derajat ke arah searah jarum jam.
            plt.show() #menampilkan diagram batangnya

        except mysql.connector.Error as err: #ini kalau error querynya bisa dikasih tau errornya karena apa
            print("Gagal mengambil data jumlah kerusakan:", err)
        finally:
            cursor.close() #tutup cursor
            conn.close() #tutup koneksi
    
    def lihat_diagram_kerusakan_pie(self, cursor=None, conn=None): #ini untuk membuat diagram pie. cursor dan conn adalah parameter opsional yang digunakan untuk menerima objek kursor dan koneksi database. Jika tidak diberikan, mereka akan diinisialisasi dengan nilai default None
        conn = buat_koneksi() #Membuat koneksi baru ke database menggunakan fungsi buat_koneksi().
        cursor = conn.cursor() #Membuat objek cursor dari koneksi database yang diberikan.
        try: #Memulai blok try untuk menangani eksekusi query
            cursor.execute("SELECT jenis_kerusakan, SUM(jumlah_kerusakan) FROM data_kerusakan GROUP BY jenis_kerusakan") #eksekusi query untuk mengambil atau select data kerusakan dari table data_kerusakan
            jumlah_kerusakan = cursor.fetchall() #Mengambil semua baris hasil query dan menyimpannya dalam variable jumlah_kerusakan

            # Memisahkan data ke dalam dua list: jenis kerusakan dan jumlah kerusakan
            jenis_kerusakan = [item[0] for item in jumlah_kerusakan]
            jumlah = [item[1] for item in jumlah_kerusakan]

            # Membuat diagram bundar (pie chart)
            plt.pie(jumlah, labels=jenis_kerusakan, autopct='%1.1f%%') #autopct itu untuk nampilin datanya berdasarkan persentase
            plt.title('Diagram Pie Jumlah Kerusakan Berdasarkan Jenis Kerusakan')
            plt.axis('equal')  # Untuk memastikan diagram bundar
            plt.show() #menampilkan diagram pie nya

        except mysql.connector.Error as err: #ini kalau error querynya bisa dikasih tau errornya karena apa
            print("Gagal mengambil data jumlah kerusakan:", err)
        finally:
            cursor.close() #tutup cursor
            conn.close() #tutup koneksi

    def lihat_diagram_kerusakan_garis(self, cursor=None, conn=None): #ini untuk membuat diagram garis. cursor dan conn adalah parameter opsional yang digunakan untuk menerima objek kursor dan koneksi database. Jika tidak diberikan, mereka akan diinisialisasi dengan nilai default None
        conn = buat_koneksi() #Membuat koneksi baru ke database menggunakan fungsi buat_koneksi().
        cursor = conn.cursor() #Membuat objek cursor dari koneksi database yang diberikan.
        try: #Memulai blok try untuk menangani eksekusi query
            cursor.execute("SELECT jenis_kerusakan, SUM(jumlah_kerusakan) FROM data_kerusakan GROUP BY jenis_kerusakan") #eksekusi query untuk mengambil atau select data kerusakan dari table data_kerusakan
            jumlah_kerusakan = cursor.fetchall() #Mengambil semua baris hasil query dan menyimpannya dalam variable jumlah_kerusakan

            # Memisahkan data ke dalam dua list: jenis kerusakan dan jumlah kerusakan
            jenis_kerusakan = [item[0] for item in jumlah_kerusakan]
            jumlah = [item[1] for item in jumlah_kerusakan]

            plt.plot(jenis_kerusakan, jumlah, marker='o', linestyle='-')
            plt.xlabel('Jenis Kerusakan') #Parameter pertama adalah kumpulan data yang akan digunakan sebagai sumbu x dalam diagram batang.
            plt.ylabel('Jumlah Kerusakan') #Parameter kedua adalah kumpulan data yang akan digunakan sebagai tinggi dari batang dalam diagram.
            plt.title('Diagram Garis Jumlah Kerusakan Berdasarkan Jenis Kerusakan')
            plt.xticks(rotation=45)  #Parameter rotation digunakan untuk menentukan sudut rotasi. nilai 45 menunjukkan bahwa label-label tersebut akan diputar sebesar 45 derajat ke arah searah jarum jam.
            plt.grid(True)  # Menambah grid pada diagram
            plt.show() #nampilin diagram garisnya

        except mysql.connector.Error as err: #ini kalau error querynya bisa dikasih tau errornya karena apa
            print("Gagal mengambil data jumlah kerusakan:", err)
        finally:
            cursor.close() #tutup cursor
            conn.close() #tutup koneksi


    def buat_aduan(self, lokasi, keterangan_aduan): #ini proses buat aduan masyarakat, parameternya ada lokasi dama keterangan aduan. karena itu doang yang bakal dipakai
        conn = buat_koneksi() #Membuat koneksi baru ke database menggunakan fungsi buat_koneksi().
        cursor = conn.cursor() #Membuat objek cursor dari koneksi database yang diberikan.
        try:
            query = "INSERT INTO aduan (ID_Masyarakat, lokasi, Tanggal, keterangan_aduan) VALUES (%s, %s, NOW(), %s)" #eksekusi query untuk memasukkan daftar aduan ke table aduan
            cursor.execute(query, (self.ID_Masyarakat, lokasi, keterangan_aduan)) #buat eksekusi querynya
            conn.commit()  #mengkonfirmasi bahwa perubahan yang dibuat bakal disimpan di database
            print("Aduan berhasil dibuat.")
        except mysql.connector.Error as err: #ini kalau error querynya bisa dikasih tau errornya karena apa
            print("Gagal membuat aduan:", err)
        finally:
            cursor.close() #tutup cursor
            conn.close() #tutup koneksi







#==============TAMPILAN ADMIN DAN  MENUNYA================
def menu_admin(admin): #ini fungsi menu_admin dan masih memiliki kaitan dengan class admin
    while True: #perulangan while
        #tampilan menu admin
        print("\n\033[0m\033[91mMenu Admin:\033[0m")
        print("\033[0m\033[91m1.\033[0m Mengurus Data Kerusakan")
        print("\033[0m\033[91m2.\033[0m Mengurus Data Aduan")
        print("\033[0m\033[91m3.\033[0m Mengurus Akun Masyarakat") 
        print("\033[0m\033[91m4.\033[0m Keluar")

        pilihan = input("Silahkan Pilih Menu(1/2/3/4): ")

        if pilihan == "1":
            while True:
                print("\n=======TOOLS TABLE DATA KERUSAKAN=======")
                print("\033[0m\033[91m1.\033[0m Lihat Table Data Kerusakan")
                print("\033[0m\033[91m2.\033[0m Hapus Table Data Kerusakan")
                print("\033[0m\033[91m3.\033[0m Update Table Data Kerusakan") 
                print("\033[0m\033[91m4.\033[0m Kembali Ke Menu Admin")

                sub_pilihan = input("Silahkan Pilih Menu(1/2/3/4): ")

                if sub_pilihan == "1":
                    admin.lihat_data_kerusakan() #memanggil fungsi lihat data dari class admin
                    choice = input("\nIngin Sorting atau Searching Data Kerusakan? (Sort/Search): ").lower()
                    if choice == "sort":
                        admin.menu_sorting_data_kerusakan() #memanggil fungsi menu sorting data kerusakan dari class admin
                    elif choice == "search":
                        sub_choice = input("Ingin mencari berdasarkan ID atau Lokasi? (ID/Lokasi/Tanggal): ").lower()
                        if sub_choice == "id":
                            id_data = input("Masukkan ID data yang ingin dicari: ")
                            if id_data.isdigit(): #memastikan lagi kalau id_data yang dimasukkan user adalah angka.
                                admin.menu_search_data_kerusakan("ID_data", id_data) #memanggil fungsi menu searching data kerusakan dari class admin berdasarkan id yang dicari
                            else:
                                print("ID harus berupa angka. Silakan coba lagi.")
                        elif sub_choice == "lokasi":
                            lokasi = input("Masukkan nama lokasi yang ingin dicari: ")
                            admin.menu_search_data_kerusakan("lokasi", lokasi) #memanggil fungsi menu searching data kerusakan dari class admin berdasarkan lokasi yang dicari
                        elif sub_choice == "tanggal":
                            tanggal = input("Masukkan tanggal yang ingin dicari (Format: DD-MM-YYYY): ")
                            admin.menu_search_data_kerusakan("tanggal", tanggal) #memanggil fungsi menu searching data kerusakan dari class admin berdasarkan tanggal yang dicari
                        else:
                            print("Pilihan tidak valid. Silakan coba lagi.")
                    else:
                        print("Pilihan tidak ada!")
                elif sub_pilihan == "2":
                    admin.lihat_data_kerusakan() #memanggil fungsi lihat data dari class admin
                    id_data = input("Masukkan ID data yang ingin dihapus: ")
                    if id_data.isdigit(): #memastikan lagi kalau id_data yang dimasukkan berupa angka
                        admin.hapus_data_kerusakan(id_data)  #memanggil fungsi hapus data kerusakan dari class admin
                    else:
                        print("ID harus berupa angka. Silakan coba lagi.")
                    
                elif sub_pilihan == "3":
                    admin.update_data_kerusakan()  #memanggil fungsi update data kerusakan dari class admin
                elif sub_pilihan == "4":
                    
                    break
                else:
                    print("Pilihan Tidak Ada!")
                
        elif pilihan == "2":
            while True:
                print("\n=======TOOLS DATA ADUAN MASYARAKAT=======")
                print("\033[0m\033[91m1.\033[0m Lihat Aduan Masyarakat")
                print("\033[0m\033[91m2.\033[0m Hapus Aduan Masyarakat")
                print("\033[0m\033[91m3.\033[0m Kembali Ke Menu Admin")

                sub_pilihan = input("Silahkan Pilih Menu(1/2/3): ")

                if sub_pilihan == "1":
                    admin.lihat_aduan_masyarakat() #memanggil fungsi lihat aduan masyarakat dari class admin
                    choice = input("\nIngin Sorting atau Searching Data Aduan? (Sort/Search): ").lower()
                    if choice == "sort":
                        admin.menu_sorting_aduan()  #memanggil fungsi menu sorting daftar aduan dari class admin
                    elif choice == "search":
                        sub_choice = input("Ingin mencari berdasarkan ID atau Lokasi? (ID/Lokasi/Tanggal): ").lower()
                        if sub_choice == "id":
                            id_data = input("Masukkan ID data yang ingin dicari: ")
                            if id_data.isdigit(): #memastikan lagi kalau id yang dimasukkan adalah angka
                                admin.menu_search_aduan("ID Aduan", id_data) #memanggil fungsi menu searching daftar aduan dari class admin berdasarkan id yang dicari
                            else:
                                print("ID Aduan tidak ditemukan. ID harus berupa angka!")
                        elif sub_choice == "lokasi":
                            lokasi = input("Masukkan nama lokasi yang ingin dicari: ")
                            admin. menu_search_aduan("lokasi", lokasi) #memanggil fungsi menu searching daftar aduan dari class admin berdasarkan lokasi yang dicari
                        elif sub_choice == "tanggal":
                            tanggal = input("Masukkan tanggal yang ingin dicari (Format: YYYY-MM-DD): ")
                            admin.menu_search_aduan("tanggal", tanggal) #memanggil fungsi menu searching daftar aduan dari class admin berdasarkan tanggal yang dicari
                        else:
                            print("Pilihan tidak valid. Silakan coba lagi.")
                    else:
                        print("Pilihan tidak ada!")
                elif sub_pilihan == "2":
                    admin.lihat_aduan_masyarakat() #memanggil fungsi lihat aduan masyarakat dari class admin
                    id_aduan = input("Masukkan ID aduan yang ingin dihapus: ")
                    admin.hapus_aduan(id_aduan) #memanggil fungsi hapus aduan masyarakat dari class admin
                elif sub_pilihan == "3":
                    break
                else:
                    print("Pilihan Tidak Ada!")
                
        elif pilihan == "3":
            admin.lihat_akun_masyarakat() #memanggil fungsi lihat akun masyarakat dari class admin
            while True:
                choice = input("\nIngin Searching Akun Masyarakat? (Y/N): ").lower()
                if choice == "y":
                    key = input("Masukkan ID Masyarakat: ")
                    # Validasi bahwa ID Masyarakat hanya berisi angka
                    if not key.isdigit(): #memastikan lagi kalau id_masyarakat berupa angka
                        print("ID Masyarakat harus berupa angka.")
                        continue
                    
                    # Menampilkan informasi akun masyarakat
                    admin.menu_search_masyarakat("ID Masyarakat", key) #memanggil fungsi searching akun masyarakat  dari class admin
                elif choice == "n":
                    break
                else:
                    print("Pilihan tidak valid. Silakan masukkan Y atau N.")


        elif pilihan == "4":
            print("Keluar dari Menu Admin.")
            main()
            break
            
        else:
            print("Pilihan Tidak Ada!")



#==============PEMBUATAN AKUN MASYARAKAT================
def buat_akun_masyarakat(): #fungsi untuk membuat akun masyarakat
    conn = buat_koneksi() #Membuat koneksi baru ke database menggunakan fungsi buat_koneksi().
    cursor = conn.cursor() #Membuat objek cursor dari koneksi database yang diberikan.
    try: #Memulai blok try untuk menangani eksekusi query
        ID_Masyarakat = input("Masukkan No KTP Anda:")
        # Memastikan bahwa No KTP hanya berisi angka
        if not ID_Masyarakat.isdigit(): #memastikan lagi kalau id_masyarakatnya adalah angka
            raise ValueError("No KTP harus berupa angka.")
        
        nama_lengkap = input("Masukkan nama lengkap Anda: ")
        alamat_rumah = input("Masukkan alamat rumah Anda: ")
        
        no_hp = input("Masukkan nomor HP Anda:")
        # Memastikan bahwa nomor HP hanya berisi angka
        if not no_hp.isdigit(): #memastikan lagi kalau nomor hape sudah berupa angka
            raise ValueError("Nomor HP harus berupa angka.")

        query = "INSERT INTO masyarakat (ID_Masyarakat, nama_lengkap, alamat_rumah, no_hp) VALUES (%s, %s, %s, %s)" #perintah untuk memasukkan data masyarakat
        cursor.execute(query, (ID_Masyarakat, nama_lengkap, alamat_rumah, no_hp)) #eksekusi query
        conn.commit()  #mengkonfirmasi bahwa perubahan yang dibuat bakal disimpan di database

        print("Akun masyarakat berhasil dibuat.")
        main()
    except ValueError as ve: #Blok ini menangkap pengecualian yang dihasilkan jika terjadi kesalahan dalam pemrosesan nilai, ve dicetak dalam pesan yang mengindikasikan bahwa ada kesalahan dalam membuat akun masyarakat.
        print("Gagal membuat akun masyarakat:", ve)
    except mysql.connector.Error as err: #ini kalau error querynya bisa dikasih tau errornya karena apa
        print("Gagal membuat akun masyarakat:", err)
    finally:
        cursor.close() #tutup cursor
        conn.close() #tutup koneksi







#==============TAMPILAN MASYARAKAT DAN  MENUNYA================
def menu_masyarakat(masyarakat):  #ini fungsi menu_masyarakat dan masih memiliki kaitan dengan class masyarakat
    while True: #perulagan while
        #tampilan menu masyarakat
        print("\n\033[0m\033[91mMenu Masyarakat:\033[0m")
        print("\033[0m\033[91m1.\033[0m Lihat Data Kerusakan")
        print("\033[0m\033[91m2.\033[0m Lihat Diagram Data")
        print("\033[0m\033[91m3.\033[0m Buat Aduan")
        print("\033[0m\033[91m4.\033[0m Informasi Akun")
        print("\033[0m\033[91m5.\033[0m Keluar")

        pilihan = input("Silahkan Pilih Menu(1/2/3/4/5): ")

        if pilihan == "1":
            masyarakat.lihat_data_kerusakan() #memanggil fungsi lihat data dari class masyarakat
            choice = input("\nIngin Sorting atau Searching Data Kerusakan? (Sort/Search): ").lower()
            if choice == "sort":
                masyarakat.menu_sorting_data_kerusakan() #memanggil fungsi menu sorting data dari class masyarakat
            elif choice == "search":
                sub_choice = input("Ingin mencari berdasarkan ID atau Lokasi? (ID/Lokasi): ").lower()
                if sub_choice == "id":
                    id_data = input("Masukkan ID data yang ingin dicari: ")
                    if id_data.isdigit(): #memastikan lagi kalau id_data yang dimasukkan user adalah angka.
                        masyarakat.menu_search_data_kerusakan("ID_data", id_data) #memanggil fungsi menu searching data kerusakan dari class masyarakat berdasarkan id yang dicari
                    else:
                        print("ID harus berupa angka. Silakan coba lagi.")
                elif sub_choice == "lokasi":
                    lokasi = input("Masukkan nama lokasi yang ingin dicari: ")
                    masyarakat.menu_search_data_kerusakan("lokasi", lokasi) #memanggil fungsi menu searching data kerusakan dari class masyarakat berdasarkan lokasi yang dicari
                else:
                    print("Pilihan tidak valid. Silakan coba lagi.")
            else:
                print("Pilihan tidak ada!")
        elif pilihan == "2":
            print("\nPilih Ingin Disajikan dalam bentuk apa:")
            print("\033[0m\033[91m1.\033[0m Diagram batang")
            print("\033[0m\033[91m2.\033[0m Diagram Pie")
            print("\033[0m\033[91m3.\033[0m Diagram Garis")
            pilihan = input("Silahkan Pilih Diagram (1/2/3): ")
            if pilihan == "1":
                masyarakat.lihat_diagram_kerusakan_bar() #memanggil fungsi lihat diagram bar dari class masyarakat
            elif pilihan == "2":
                masyarakat.lihat_diagram_kerusakan_pie() #memanggil fungsi lihat diagram pie dari class masyarakat
            elif pilihan == "3":
                masyarakat.lihat_diagram_kerusakan_garis() #memanggil fungsi lihat diagram garis dari class masyarakat
            else:
                print("Pilihan tidak ada!")
        elif pilihan == "3":
            lokasi = input("Masukkan lokasi kerusakan: ")
            keterangan_aduan = input("Masukkan deskripsi aduan: ")
            if not lokasi or not keterangan_aduan:  # Memeriksa apakah lokasi atau keterangan aduan kosong
                print("Lokasi dan deskripsi aduan harus diisi!. Gagal membuat aduan.")
            else:
                masyarakat.buat_aduan(lokasi, keterangan_aduan) #memanggil fungsi buat aduan dari class masyarakat
        elif pilihan == "4":
            masyarakat.lihat_dan_edit_informasi_akun() #memanggil fungsi lihat dan edit informasi akun dari class masyarakat
            print("\n")
        elif pilihan == "5":
            print("Keluar dari Menu Masyarakat.")
            main()
            break
        else:
            print("Pilihan Tidak Ada!")

def ambil_info_admin(username): #ini fungsi untuk ambil info admin
    conn = buat_koneksi() #Membuat koneksi baru ke database menggunakan fungsi buat_koneksi().
    cursor = conn.cursor() #Membuat objek cursor dari koneksi database yang diberikan.
    try: #Memulai blok try untuk menangani eksekusi query
        cursor.execute("SELECT * FROM admin WHERE nama_lengkap = %s", (username,)) #ini perintah untuk mengambil atau select admin berdasarkan username
        admin_data = cursor.fetchone() #Mengambil satu baris hasil query dan menyimpannya dalam variabel admin_data. Fungsi fetchone() digunakan untuk mengambil satu baris hasil dari query yang dieksekusi sebelumnya.

        if admin_data: #jika admin_data ini nilainya tidak none/kosong. artinya informasi data telah ditemukan.
            return Admin(admin_data[0],admin_data[1], admin_data[2]) #ambil data admin data[0] atau id_admin, data[1] nama_lengkap, data[2] nomor hape
        else:
            return None
    except mysql.connector.Error as err: #ini kalau error querynya bisa dikasih tau errornya karena apa
        print("Nama admin tidak ada!", err)
    finally:
        cursor.close() #tutup cursor
        conn.close() #tutup koneksi

def ambil_info_masyarakat(username): #ini fungsi untuk ambil info masyarakat
    conn = buat_koneksi() #Membuat koneksi baru ke database menggunakan fungsi buat_koneksi().
    cursor = conn.cursor() #Membuat objek cursor dari koneksi database yang diberikan.
    try: #Memulai blok try untuk menangani eksekusi query
        cursor.execute("SELECT * FROM masyarakat WHERE LOWER(nama_lengkap) = LOWER(%s)", (username,)) #ini perintah untuk mengambil atau select masyarakat berdasarkan username
        masyarakat = cursor.fetchone()  #Mengambil satu baris hasil query dan menyimpannya dalam variabel masyarakat. Fungsi fetchone() digunakan untuk mengambil satu baris hasil dari query yang dieksekusi sebelumnya.
        if masyarakat: #jika masyarakat ini nilainya tidak none/kosong. artinya informasi data telah ditemukan.
            return Masyarakat(masyarakat[0], masyarakat[1], masyarakat[3], masyarakat[2]) #ambil data masyarakat data[0] atau id_masyarakat, data[1] nama_lengkap, data[2] nomor hape
        else:
            return None
    except mysql.connector.Error as err: #ini kalau error querynya bisa dikasih tau errornya karena apa
        print("Gagal mengambil info admin:", err)
    finally:
        cursor.close() #tutup cursor
        conn.close() #tutup koneksi

def cek_login(username, password):
    # Fungsi untuk memeriksa login pengguna
    conn = buat_koneksi() #Membuat koneksi baru ke database menggunakan fungsi buat_koneksi().
    cursor = conn.cursor() #Membuat objek cursor dari koneksi database yang diberikan.
    try: #Memulai blok try untuk menangani eksekusi query
        cursor.execute("SELECT * FROM admin WHERE nama_lengkap = %s AND ID_Admin = %s", (username, password)) #ini perintah untuk mengambil atau select admin berdasarkan username dan password(id_admin)
        admin = cursor.fetchone()  #Mengambil satu baris hasil query dan menyimpannya dalam variabel admin. Fungsi fetchone() digunakan untuk mengambil satu baris hasil dari query yang dieksekusi sebelumnya.

        if admin: #Jika admin tidak None, artinya data pengguna ditemukan dan login berhasil sebagai pengguna dari kalangan admin.
            return "admin" #fungsi akan mengembalikan string admin.
        else:
            cursor.execute("SELECT * FROM masyarakat WHERE nama_lengkap = %s AND ID_Masyarakat = %s", (username, password)) #ini perintah untuk mengambil atau select masyarakat berdasarkan username dan password(id_masyarakat)
            masyarakat = cursor.fetchone()  #Mengambil satu baris hasil query dan menyimpannya dalam variabel masyarakat. Fungsi fetchone() digunakan untuk mengambil satu baris hasil dari query yang dieksekusi sebelumnya.

            if masyarakat: #Jika masyarakat tidak None, artinya data pengguna ditemukan dan login berhasil sebagai pengguna dari kalangan masyarakat.
                return "masyarakat" #fungsi akan mengembalikan string masyarakat.
            else:
                main()
    except mysql.connector.Error as err:  #ini kalau error querynya bisa dikasih tau errornya karena apa
        print("Gagal melakukan pengecekan login:", err)
    finally:
        cursor.close() #tutup cursor
        conn.close() #tutup koneksi



#==================TAMPILAN SELAMAT DATANG===================
def main():
    print("")
    print("================WELOCOME================")
    print("     APLIKASI PENGADUAN MASYARAKAT      ")
    print("        KERUSAKAN EKOSISTEM LAUT        ")
    print("========================================")    
    print("\nSilahkan pilih menu:")
    print("\033[0m\033[91m1.\033[0m Login")
    print("\033[0m\033[91m2.\033[0m Registrasi")

    while True:
        pilihan = input("Masukkan pilihan Anda (1/2): ")
        if pilihan.lower() == "1":
            print("")
            print("==================LOGIN=================")
            username = input("Masukkan Username Anda: ")
            password = input("Masukkan Password/NIK Anda: ")

            # Cek apakah pengguna terdaftar sebagai admin atau masyarakat
            user_type = cek_login(username, password) #ini memanggil fungsi cek_login
            if user_type == "admin": #kalau user typenya adalah admin
                admin = ambil_info_admin(username) #maka ambil info admin dari fungsi ambil info admin berdasarkan usernamenya
                if admin: #Jika admin tidak None, artinya data pengguna ditemukan dan login berhasil sebagai pengguna dari kalangan admin.
                    print("Login berhasil sebagai admin!.")
                    menu_admin(admin) #panggil fungsi menu_admin
                    break
            elif user_type == "masyarakat": #kalau user typenya adalah masyarakat
                masyarakat = ambil_info_masyarakat(username) #maka ambil info masyarakat dari fungsi ambil info masyarakat berdasarkan usernamenya
                if masyarakat: #Jika masyarakat tidak None, artinya data pengguna ditemukan dan login berhasil sebagai pengguna dari kalangan masyarakat.
                    print("Login berhasil sebagai masyarakat!.")
                    menu_masyarakat(masyarakat)  #panggil fungsi menu_masyarakat
                    break
            else:
                print("Nama pengguna atau kata sandi salah. Silakan coba lagi!")

        elif pilihan.lower() == "2":
            buat_akun_masyarakat() #panggil fungsi untuk buat akun masyarakat

        else:
            print("Pilihan tidak ada!")

if __name__ == "__main__": #untuk mengeksekusi kode tertentu hanya jika skrip Python dieksekusi langsung, bukan diimpor sebagai modul oleh skrip lain.
    main() #tampilkan fungsi main() atau tampilan utama
