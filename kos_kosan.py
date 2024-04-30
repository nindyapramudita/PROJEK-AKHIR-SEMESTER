import csv
import pwinput
from prettytable import PrettyTable
from datetime import datetime, timedelta

tabel_kamar = PrettyTable()

# untuk update data kamar ke tabel
#tanpa ini tampilan tabel akan kosong
def refresh_table_kamar():
    tabel_kamar.clear() #menghapus array dalam baris
    tabel_kamar.title = "DAFTAR KAMAR KOS MERAKYAT" #judul table. paling atas
    if user_type == "normal": #user_type normal/admin ctrl+D if adalah percabangan
        tabel_kamar.field_names = ["Nomor", "Jenis", "Harga Bulanan", "Pemilik"] #field table kamar ketika jadi pengunjung
        for kamar in data_kamar: #for adalah perulangan yang dapat ditentukan
            if kamar["ketersediaan"] == "tersedia": 
                tabel_kamar.add_row([kamar["nomor"], kamar["jenis"], format_uang(kamar["harga bulanan"]), kamar["pemilik"]]) #add row adalah tambahkan baris dalam tabel
    else: #jika user_type adalah admin
        tabel_kamar.field_names = ["Nomor", "Jenis", "Harga Bulanan", "Pemilik", "Ketersediaan"] #field table kamar ketika jadi admin
        for kamar in data_kamar: #for adalah perulangan yang dapat ditentukan
            tabel_kamar.add_row([kamar["nomor"], kamar["jenis"], kamar["harga bulanan"], kamar["pemilik"], kamar["ketersediaan"]]) #add row adalah tambahkan baris didalam tabel


# ya tanggal harini
today = datetime.now() #modul untuk mengambil data dan waktu sekarang.

# strftime =  string format time (ubah objek datetime ke bentuk string dalam format tertentu)
# Q: yg persen-persen tu apa banh?
# A: format tanggal. d=day (tgl), m=month (bulan), Y=year (tahun), H=hour (jam), M=minute (menit) // formatnya masih banyak lagi
tanggal = today.strftime("%d/%m/%Y %H:%M") #parameter(format) untuk mengonversi string tanggal waktu python.

# Q: split ni apa?
# A: misah string jadi list, contohnya nih ngubah "aku/gila" jadi ["aku","gila"]
tahun, bulan = (today.strftime("%Y/%m")).split('/')

# timedelta itu untuk nambah waktu ke tanggal, jadi yang di bawah ni tuh tanggal setelah 30 hari
tenggat = (today+timedelta(days=30)).strftime("%d/%m/%Y %H:%M")



#-----------Membuat CSV-----------#
def load_data():
    # global untuk bikin variable yang *dibuat* di dalam function (def) bisa dipakai diluar function
    global data_kamar, data_user, userpass, data_pemasukan, adminpass
    try:
        data_kamar = [] #membuat dictionary
        with open("data_kamar.csv", 'r', newline='') as file: #disuruh buat csv data_kamar
            reader = csv.reader(file) #rumus membaca file csv
            for row in reader: #for adalah perulangan yang dapat dibatasi
                data_kamar.append({"nomor": row[0], "jenis": row[1], "harga bulanan": int(row[2]), "ketersediaan": row[3], "pemilik": row[4]}) # append menambahkan item dari belakang.
    except FileNotFoundError:
        # data kamar default ketika file tidak ditemukan
        data_kamar = [ #distionary
            {"nomor": "101", "jenis": "Tunggal", "harga bulanan": 250000, "ketersediaan": "tersedia", "pemilik": ""},
            {"nomor": "102", "jenis": "Tunggal", "harga bulanan": 250000, "ketersediaan": "tersedia", "pemilik": ""},
            {"nomor": "201", "jenis": "Ganda", "harga bulanan": 400000, "ketersediaan": "tersedia", "pemilik": ""},
            {"nomor": "202", "jenis": "Ganda", "harga bulanan": 400000, "ketersediaan": "tersedia", "pemilik": ""}
        ]
        with open("data_kamar.csv", 'w', newline='') as file: #untuk menyimpan data di data_kamar.csv
            fieldnames = ["nomor", "jenis", "harga bulanan", "ketersediaan", "pemilik"] #nama field
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            for kamar in data_kamar: #for adalah perulangan yang dapat dibatasi
                writer.writerow(kamar) #writerow untuk mengambil 1 baris. writerows mengambil lebih dari satu baris.

    data_user = [] #dictionary
    try: #try except adalah jika terjadi error maka akan diberitahu errornya apa dengan bahasa kita
        with open("data_user.csv", 'r', newline='') as file: #cara membuat file csv 
            reader = csv.reader(file) #rumus membaca file csv
            for row in reader: #for adalah perulangan yang dapat dibatasi
                data_user.append({"username": row[0], "nomor kamar": row[1], "terakhir bayar": row[2], "tenggat": row[3], "lunas": row[4], "saldo": int(row[5])}) # append menambahkan item dari belakang. 
    except FileNotFoundError:
        open("data_user.csv", 'w', newline='') #menyimpan data ke file csv

    userpass = [] #dicti0nary
    try:#try except adalah jika terjadi error maka akan diberitahu errornya apa dengan bahasa kita
        with open("userpass.csv", 'r', newline='') as file: #cara membuat file csv 
            reader = csv.reader(file) #rumus membaca file csv
            for row in reader:#for adalah perulangan yang dapat dibatasi
                userpass.append({"username": row[0], "password": row[1]})
    except FileNotFoundError:
        open("userpass.csv", 'w', newline='')

    data_pemasukan = []
    try:#try except adalah jika terjadi error maka akan diberitahu errornya apa dengan bahasa kita
        with open("data_pemasukan.csv", 'r', newline='') as file: #cara membuat file csv 
            reader = csv.reader(file)#rumus membaca file csv
            for row in reader:#for adalah perulangan yang dapat dibatasi
                data_pemasukan.append({"tahun": row[0], "bulan": row[1], "pemasukan": int(row[2])}) # append menambahkan item dari belakang.
    except:
        with open("data_pemasukan.csv", 'w', newline='') as file: #menyimpan data csv
            writer = csv.writer(file)#rumus membaca file csv
            writer.writerow([tahun, bulan, 0]) #writerow dan writerows itu berbeda. writerow terdiri dari satu baris dan rows itu lebih
    
    adminpass = {}
    try:#try except adalah jika terjadi error maka akan diberitahu errornya apa dengan bahasa kita
        with open("adminpass.csv", 'r', newline='') as file: #cara membuat file csv 
            reader = csv.reader(file)#rumus membaca file csv
            for row in reader:#for adalah perulangan yang dapat dibatasi
                adminpass = {"username": row[0], "password": row[1]} #ditaruh sesuai indexnya
    except FileNotFoundError:
        # username & password admin default ketika file tidak ditemukan
        adminpass = {"username":"admin", "password":"admin86"} #dict yang berisi username dan passwort
        with open("adminpass.csv", 'w', newline='') as file: #menyimpan data csv
            fieldnames = ["username", "password"] #nama fiedl
            writer = csv.DictWriter(file, fieldnames=fieldnames) #csv.DictWriter adalah membaca filecvs berupa dictionary
            writer.writerow(adminpass) #writerow dan writerows itu berbeda. writerow terdiri dari satu baris dan rows itu lebih

#------------Simpan Data-----------#
load_data() #memanggil function tanpa perlu repot menulis program berulang ulang

# save data ke file csv
def simpan_data():
    with open("data_user.csv", 'w', newline='') as file: #untuk menyimpan data dan membuat variabel csv
        writer = csv.writer(file) #rumus menulis dan menyimpan data didalam file csv
        for user in data_user: #for adalah perulangan yang dapat dibatasi
            writer.writerow([user["username"], user["nomor kamar"], user["terakhir bayar"], user["tenggat"], user["lunas"], user["saldo"]]) #writerow dan writerows itu berbeda. writerow terdiri dari satu baris dan rows itu lebih

    with open("data_kamar.csv", 'w', newline='') as file: #untuk menyimpan data dan membuat variabel csv
        writer = csv.writer(file) #rumus menulis dan menyimpan data didalam file csv
        for kamar in data_kamar:#for adalah perulangan yang dapat dibatasi
            writer.writerow([kamar["nomor"], kamar["jenis"], kamar["harga bulanan"], kamar["ketersediaan"], kamar["pemilik"]]) #writerow dan writerows itu berbeda. writerow terdiri dari satu baris dan rows itu lebih
    
    with open("data_pemasukan.csv", 'w', newline='') as file: #untuk menyimpan data dan membuat variabel csv
        writer = csv.writer(file)#rumus menulis dan menyimpan data didalam file csv
        for data in data_pemasukan:#for adalah perulangan yang dapat dibatasi
            writer.writerow([data["tahun"], data["bulan"], data["pemasukan"]]) #writerow dan writerows itu berbeda. writerow terdiri dari satu baris dan rows itu lebih
    
    with open("userpass.csv", 'w', newline='') as file: #untuk menyimpan data dan membuat variabel csv
        writer = csv.writer(file)#rumus menulis dan menyimpan data didalam file csv
        for akun in userpass:#for adalah perulangan yang dapat dibatasi
            writer.writerow([akun["username"], akun["password"]]) #writerow dan writerows itu berbeda. writerow terdiri dari satu baris dan rows itu lebih
    
    with open("adminpass.csv", 'w', newline='') as file: #untuk menyimpan data dan membuat variabel csv
        writer = csv.writer(file)#rumus menulis dan menyimpan data didalam file csv
        writer.writerow([adminpass["username"], adminpass["password"]]) #writerow dan writerows itu berbeda. writerow terdiri dari satu baris dan rows itu lebih

simpan_data() #memanggil function tanpa perlu repot menulis program berulang ulang
load_data() #memanggil function tanpa perlu repot menulis program berulang ulang

# pengganti function input()
# - handle input biar gak error pas pencet copy di terminal
# - bisa batasi input supaya cuman bisa integer (pakai "int" di parameter 2)
# - bisa batasi input supaya cuman bisa digit (pakai "digit" di parameter 2)
# - untuk print error yg gk di handle tanpa bikin program berenti 

#----------
def inputhandler(prompt, inputtype="str"): #prompt adalah definisi paramater 1, inputtype adalah definisi parameter 2
#promt = masukkan inputan anda!
#inputtype ini kalau gak dipakai otomatis inputtype berupa str sebagai parameter 2
    while True: #while true adalah bentuk perulangan yang tidak memiliki batas
        try: #try except adalah jika terjadi error maka akan diberitahu errornya apa dengan bahasa kita
            if inputtype == "str": #merubah inputtype menjadi string
                userinput = input(prompt) #promt = masukkan inputan anda!
            elif inputtype == "int": #merubah inputtype menjadi integer
                userinput = int(input(prompt)) #promt = masukkan inputan anda!
            elif inputtype == "digit": #merubah inputtype menjadi digit. digit adalah str yang berisi angkat tanpa koma tanpa negatif. hanya angka
                userinput = input(prompt) #promt = masukkan inputan anda!
                if not userinput.isdigit(): 
                    print("Input hanya bisa berupa angka\n")
                    return inputhandler(prompt, "digit") #Return: Nilai yang dikembalikan ini bisa berupa hasil operasi dalam fungsi, nilai variabel, atau struktur data lainnya. Ketika fungsi dipanggil dalam ekspresi, fungsi tersebut akan "digantikan" oleh nilai yang dikembalikan.
            return userinput #mengembalikan nilai userinput
        except KeyboardInterrupt:
            print("\nGabisa Error!\n")
        except ValueError:
            print("Input hanya bisa berupa angka\n")
        except Exception as error:
            print(f"Error baru nih: {error}\n")


#---------Format Uang--------
def format_uang(nominal): #function format_uang untuk nambahin Rp di nominal uang
    return f"Rp{nominal:,}".replace(',','.')

# tipe user (normal/admin)
user_type = ''



#--------------Tools Admin--------------#
#---Tambah Kamar---
def tambah_kamar(): #function untuk menambah kamar (menu admin)
    while True: #while true adalah bentuk perulangan yang tidak memiliki batas
        nomor = inputhandler("Nomor kamar: ", "digit") #input dalam bentuk digit
        if any(kamar["nomor"] == nomor for kamar in data_kamar): #jika nomor yang dimasukkan sama dengan nomor kamar didalam data_kamar maka...
            print("kamar Sudah Ada!\n") 
        else:
            break #memberhentikan perulangan while
    
    print("\nJenis Kamar")
    print("[1] Tunggal")
    print("[2] Ganda")
    
    print("[3] VIP")
    while True: #while true adalah bentuk perulangan yang tidak memiliki batas
        pilihan = inputhandler("Pilihan: ") 
        if pilihan == '1':
            jenis = "Tunggal"
            break #memberhentikan perulangan while
        elif pilihan == '2':
            jenis = "Ganda"
            break #memberhentikan perulangan while
        elif pilihan == '3':
            jenis = "VIP"
            break #memberhentikan perulangan while
        else:
            print("Pilihan Tidak Ada!")
            
    harga = int(inputhandler("Harga bulanan: ", "digit")) #input harga bulanan dalam bentuk digit
    
    data_kamar.append({"nomor": nomor, "jenis": jenis, "harga bulanan": harga, "pemilik": "", "ketersediaan": "tersedia"}) # append menambahkan item dari belakang.
    # sort = urut list/dict dari angkah terkecil
    # lambda = mirip def, tapi tanpa nama function. hanya menggunakan "lambda" sudah seperti menggunakan function
    data_kamar.sort(key=lambda kamar: kamar["nomor"]) #biar urutan nomor kamar dari angka terkecil
    simpan_data()  #memanggil function tanpa perlu repot menulis program berulang ulang
    refresh_table_kamar() #memanggil function tanpa perlu repot menulis program berulang ulang
    print(tabel_kamar) #untuk memanggil tabel kamar dalam bentuk prettytable
    print(f"Berhasil menambahkan kamar {nomor} ke data kamar")

#---Edit Kamar---
def edit_kamar():
    print(tabel_kamar) #untuk memanggil tabel kamar dalam bentuk prettytable
    while True: #while true adalah bentuk perulangan yang tidak memiliki batas
        nomor = inputhandler("Nomor kamar: ", "digit") #input nomor kamar dalam bentuk digit
        if any(kamar["nomor"] == nomor for kamar in data_kamar): #jika nomor sama dengan nomo kamar yang ada didalam data_kamar
            break #untuk memberhentikan perulangan while
        else:
            print("Kamar Tidak Ada!\n")
    
    print("\nJenis Kamar")
    print("[1] Tunggal")
    print("[2] Ganda")
    print("[3] VIP")
    while True: #while true adalah bentuk perulangan yang tidak memiliki batas
        pilihan = inputhandler("Pilihan: ")
        if pilihan == '1':
            jenis = "Tunggal"
            break #untuk memberhentikan perulangan while
        elif pilihan == '2':
            jenis = "Ganda"
            break #untuk memberhentikan perulangan while
        elif pilihan == '3':
            jenis = "VIP"
            break #untuk memberhentikan perulangan while
        else:
            print("Pilihan Tidak Tersedia!")

    harga = int(inputhandler("Harga bulanan: ", "digit")) #input harga bulanan dalam bentuk digit

    for kamar in data_kamar: #for adalah perulangan yang dapat dibatasi
    #untuk kamar jika ada didalam data_kamar maka...
        if kamar["nomor"] == nomor: #jika nomor kamar sama dengan nomor yang diinputkan
            kamar["jenis"] = jenis #jenis kamar sama dengan jenis kamar yang diinputkan
            kamar["harga bulanan"] = harga #harga bulanan kamar sama dengan harga yang diinputkan
            simpan_data() #memanggil function tanpa perlu repot menulis program berulang ulang
            refresh_table_kamar() #memanggil function tanpa perlu repot menulis program berulang ulang
            print(tabel_kamar) #memanggil table_kamar dalam bentuk prettytable
            print(f"Berhasil mengubah data dari kamar {nomor}")

#---Hapus Kamar---
def hapus_kamar():
    print(tabel_kamar)
    while True: #while true adalah bentuk perulangan yang tidak memiliki batas
        nomor = inputhandler("Nomor kamar: ", "digit") #input nomor kamar dalam bentuk digit
        if any(kamar["nomor"] == nomor for kamar in data_kamar): #jika nomor sama dengan nomo kamar yang ada didalam data_kamar
            break #untuk memberhentikan perulangan while
        else:
            print("Kamar Tidak Ada!\n")
        
    for kamar in data_kamar: #for adalah perulangan yang dapat dibatasi. 
    #untuk kamar jika ada didalam data_kamar maka...
        if kamar["nomor"] == nomor: #jika nomor kamar sama dengan nomor yang diinputkan user
            if kamar["pemilik"] != '': #jika pemilik tidak sama dengan
                for user in data_user: #untuk user didalam data_user
                    if user["username"] == kamar["pemilik"]: #jika username sama dengan pemilik kamar
                        kamar["ketersediaan"] = "pending" #status kamar berubah menjadi pending karena kamar akan terhapus jika penyewa belum keluar
                        simpan_data() #memanggil function tanpa perlu repot menulis program berulang ulang
                        print("menunggu user untuk berhenti menyewa")
            else:
                data_kamar.remove(kamar) #menghapus kamar didalam data_kamar
                simpan_data() #memanggil function tanpa perlu repot menulis program berulang ulang
                refresh_table_kamar() #memanggil function tanpa perlu repot menulis program berulang ulang
                print("kamar dihapus")



#----------Menu Admin-------------
def menu_admin():
    print(f"\n{'='*10} Menu Admin {'='*10}") #judul
    while True: #while true adalah bentuk perulangan yang tidak memiliki batas
        print("[1] Lihat kamar")
        print("[2] Tools")
        print("[3] Data user")
        print("[4] Pemasukkan")
        print("[5] Pengaturan akun")
        print("[6] Keluar")
        pilihan = inputhandler("Pilihan: ")
        
        if pilihan == '1':
            print(tabel_kamar) #memanggil tabel kamar
        elif pilihan == '2':
            while True: #while true adalah bentuk perulangan yang tidak memiliki batas
                print(f"\n{'='*10} Tools {'='*10}")
                print("[1] Tambah kamar")
                print("[2] Edit data kamar")
                print("[3] Hapus data kamar")
                print("[4] Kembali")
                pilihan = inputhandler("Pilihan: ")
                if pilihan == '1':
                    tambah_kamar() #memanggil function tanpa perlu repot menulis program berulang ulang
                elif pilihan == '2':
                    edit_kamar() #memanggil function tanpa perlu repot menulis program berulang ulang
                elif pilihan == '3':
                    hapus_kamar() #memanggil function tanpa perlu repot menulis program berulang ulang
                elif pilihan == '4':
                    menu_admin() #memanggil function tanpa perlu repot menulis program berulang ulang
                    break #untuk memberhentikan perulangan while
                else:
                    print("Pilihan tidak valid!\n")

        elif pilihan == '3':
            while True: #while true adalah bentuk perulangan yang tidak memiliki batas
                print(f"\n{'='*10} Data User {'='*10}") #judul
                print("[1] Cari berdasar username")
                print("[2] Liat yang ngutang")
                print("[3] Liat yang udah bayar")
                print("[4] Kembali")
                pilihan = inputhandler("Pilihan: ")
                if pilihan == '1':
                    username = inputhandler("Siapa: ")
                    lihat_akun(username) #memanggil function tanpa perlu repot menulis program berulang ulang
                elif pilihan == '2':
                    table = PrettyTable() #tabel adalah prettytable
                    table.title = "Penunggak Hutang" #judul table
                    table.field_names = ["Nama", "Nomor kamar", "Tenggat", "Tagihan"] #field table
                    
                    ada = False #boolean
                    for user in data_user: #for adalah perulangan yang dapat dibatasi
                    #untuk user didalam data_user
                        if user["lunas"] == "belum lunas": #jika belum lunas
                            for kamar in data_kamar: #untuk nomor kamar di dalam data_kamar
                                if kamar["nomor"] == user["nomor kamar"]: #jika nomor kamar sama dengan nomor kamar
                                    table.add_row([user["username"], user["nomor kamar"], user["tenggat"], kamar["harga bulanan"]]) #tambahkan baris di tabel
                                    ada = True #boolean
                    
                    if ada:
                        print(table) #memanggil table
                    else:
                        print()
                        print("Tidak Ada Yang Berhutang!\n")
                        

                elif pilihan == '3':
                    table = PrettyTable() #tabel adalah prettytable
                    table.title = "Daftar Penyewa Yang Telah Membayar" #judul table
                    table.field_names = ["Nama", "Nomor kamar", "Tanggal bayar"] #field tabel

                    ada = False #boolean
                    for user in data_user: #untuk user didalam data_user
                        if user["lunas"] == "lunas": #jika sudah lunas
                            table.add_row([user["username"], user["nomor kamar"], user["terakhir bayar"]]) #tambahkan baris didalam tabel
                            ada = True #boolean
                    
                    if ada:
                        print(table)#memanggil table
                    else:
                        print()
                        print("Belum Ada Yang Membayar!\n")

                elif pilihan == '4':
                    menu_admin() #memanggil function tanpa perlu repot menulis program berulang ulang
                else:
                    print("Pilihan tidak valid!\n")
        elif pilihan == '4':
            while True: #while true adalah bentuk perulangan yang tidak memiliki batas
                print(f"\n{'='*10} Pemasukan {'='*10}") #judul
                print("[1] Pemasukan Tahunan")
                print("[2] Pemasukan Bulanan")
                print("[3] Pemasukan Sepanjang Masa")
                print("[4] Pemasukan Terbanyak")
                print("[5] Kembali")
                pilihan = inputhandler("Pilihan: ")
                if pilihan == '1':
                    print(f"\n{'='*10} Pemasukan Tahunan {'='*10}")
                    pemasukan = 0 #pemasukkan awal
                    for data in data_pemasukan:
                        if data["tahun"] == tahun: #Jika tahun dalam data_pemasukan sama dengan tahun
                            pemasukan += data["pemasukan"] #pemasukkan ditambahkan ke data pemasukkan
                    print(f"Pemasukan Tahun Ini: {format_uang(pemasukan)}\n")
                    while True: #while true adalah bentuk perulangan yang tidak memiliki batas
                        print("[1] Cari")
                        print("[2] Kembali")
                        pilihan = inputhandler("Pilihan: ")
                        if pilihan == '1':
                            cari = inputhandler("Tahun: ")
                            pemasukan = 0 #pemasukkan awal
                            ada =  False #boolean
                            for data in data_pemasukan: #untuk data didalam data_pemasukan
                                if data["tahun"] == cari: #jika tahun didata sama dengan tahun yang dicari
                                    pemasukan += data["pemasukan"] #pemasukkan ditambahkan ke data pemasukkan
                                    ada = True #bpplean
                            if ada:
                                print(f"pemasukan tahun {cari}: {format_uang(pemasukan)}\n")
                            else:
                                print("Data tidak tersedia\n")
                        elif pilihan == '2':
                            break #memberhentikan perulangan while
                elif pilihan == '2':
                    print(f"\n{'='*10} Pemasukan Bulanan {'='*10}") #judul
                    for data in data_pemasukan: #untuk data didalam data pemasukkan
                        if data["tahun"] == tahun and data["bulan"] == bulan: #jika tahun didalam data sama dengan tahun dan bulan didata sama dengan bulan 
                            pemasukan = data["pemasukan"] #pemasukkan adalah pemasukkan didata
                            print(f"Pemasukan Bulan Ini: {format_uang(pemasukan)}")
                            while True: #while true adalah bentuk perulangan yang tidak memiliki batas
                                print("[1] Cari")
                                print("[2] Kembali")
                                pilihan = inputhandler("Pilihan: ")
                                if pilihan == '1':
                                    ada = False #boolean
                                    while True: #while true adalah bentuk perulangan yang tidak memiliki batas
                                        tgl = inputhandler("bulan/tahun: ").split('/') # split biar bisa dipisah dengan / di csv
                                        if len(tgl) < 2: #Fungsi len() digunakan untuk mengidentifikasi dan mengetahui seberapa panjang jumlah item atau anggota pada suatu objek.
                                            print("Format input tidak valid. Contoh input yang benar: 11/2023\n")
                                        else:
                                            break #memberhentikan perulangan while
                                    for data in data_pemasukan: #untuk data didalam data pemasukan
                                        if data["tahun"] == tgl[1] and data["bulan"] == tgl[0]: #jika tahun didata sama dengan tanggal diindex 1 dan bulan didata sama dengan tanggal diindex 0
                                            pemasukan = data["pemasukan"] #pemasukan adalah data pemasukan
                                            ada = True #boolean
                                    if ada:
                                        print(f"\npemasukan {tgl[0]}/{tgl[1]}: {format_uang(pemasukan)}") #contoh output pemasukan tahun/bulan : Rp 20.000
                                    else:
                                        print("Data tidak tersedia\n")
                                elif pilihan == '2':
                                    break #memberhentikan perulangan while
                elif pilihan == '3':
                    print(f"\n{'='*10} Pemasukan Total {'='*10}")#judul
                    pemasukan = 0 #pemasukkan awal
                    for data in data_pemasukan: #untuk data didalam data pemasukkan
                        pemasukan += data["pemasukan"]#pemasukkan ditambahkan pemasukkan didalam data
                    print(f"pemasukan: {format_uang(pemasukan)}")
                elif pilihan == '4':
                    print(f"\n{'='*10} Pemasukan Terbanyak {'='*10}") #judul
                    pemasukan_tahunan = {} 
                    for data in data_pemasukan: #untuk data didalam data pemasukkan
                        pemasukan = data["pemasukan"] #pemasukan adalah data pemasukkan

                        # jika data["tahun"] ada di dalam dict pemasukan_tahunan sebagai key
                        if data["tahun"] in pemasukan_tahunan: #jika tahun didata didalam pemasukkan tahunan
                            pemasukan_tahunan[data["tahun"]] += pemasukan #pemasukkan tahunan, tahun didata ditambahkan pemasukkan
                        else:
                            pemasukan_tahunan[data["tahun"]] = pemasukan #pemasukkan tahunan, tahun didalam data adalah pemasukkan

                    # jika dict pemasukan_tahunan tidak kosong
                    if pemasukan_tahunan:
                        # max = value terbesar dari list (bisa juga dari dict)
                        # disini pakai dict
                        tahun_tertinggi = max(pemasukan_tahunan, key=pemasukan_tahunan.get)
                        pemasukan_tertinggi = pemasukan_tahunan[tahun_tertinggi]
                        print(f"Tahun dengan pemasukan tertinggi adalah {tahun_tertinggi}: {format_uang(pemasukan_tertinggi)}")
                    else:
                        print("Tidak ada data pemasukan yang tersedia.")
                    
                    pemasukan_bulanan = {}
                    for data in data_pemasukan: #untuk data didalam data pemasukkan
                        key = f"{data['bulan']}/{data['tahun']}" #key adalah bulan didata atau tahun didata
                        if key in pemasukan_bulanan: #jika bulan atau tahun didata didalam pemasukkan bulanan
                            pemasukan_bulanan[key] += data['pemasukan'] #pemasukkan bulanan [bulan/tahun] ditambahkan pemasukan didata
                        else:
                            pemasukan_bulanan[key] = data['pemasukan']#pemasukkan bulanan[bulan/tahun] adalah pemasukan didata
                    if pemasukan_bulanan:
                        bulan_tertinggi = max(pemasukan_bulanan, key=pemasukan_bulanan.get) 
                        pemasukan_tertinggi = pemasukan_bulanan[bulan_tertinggi]
                        print(f"Bulan dengan pemasukan tertinggi adalah {bulan_tertinggi}: {format_uang(pemasukan_tertinggi)}")
                    else:
                        print("Tidak ada data pemasukan yang tersedia.")
                elif pilihan == '5':
                    menu_admin() #memanggil function tanpa perlu repot menulis program berulang ulang
                    break #memberhentikan perulangan while
        elif pilihan == '5':
            print(f"\n{'='*10} Pengaturan Akun Admin {'='*10}")#judul
            while True: #while true adalah bentuk perulangan yang tidak memiliki batas
                print("[1] Ganti username")
                print("[2] Ganti password")
                print("[3] Kembali")
                pilihan = inputhandler("Pilihan: ")
                print()
                if pilihan == '1':
                    while True: #while true adalah bentuk perulangan yang tidak memiliki batas
                        username_baru = inputhandler("Username baru: ").strip() # menghapus spasi dari awal dan akhir string 
                        if len(username_baru) < 5: #Fungsi len() digunakan untuk mengidentifikasi dan mengetahui seberapa panjang jumlah item atau anggota pada suatu objek.
                            print("Minimal 5 huruf")
                        else:
                            break #memberhentikan perulangan while
                    konfirmasi = inputhandler("Apakah anda yakin? [y/n]: ")
                    # lower tu untuk bikin huruf besar jadi kecil.
                    if konfirmasi.lower() == 'y':
                        adminpass["username"] = username_baru #username adalah username baru yang diganti
                        simpan_data() #memanggil function tanpa perlu repot menulis program berulang ulang
                        print(f"\nUsername anda telah diubah ke {username_baru}")
                        break #memberhentikan perulangan while
                    else:
                        print("Berhasil dibatalkan")

                elif pilihan == '2':
                    while True: #while true adalah bentuk perulangan yang tidak memiliki batas
                        password_baru = pwinput.pwinput("Password baru: ", mask='*').strip() # menghapus spasi dari awal dan akhir string 
                        if len(password_baru) < 5: #Fungsi len() digunakan untuk mengidentifikasi dan mengetahui seberapa panjang jumlah item atau anggota pada suatu objek.
                            print("Minimal 5 huruf")
                        else:
                            break #untuk memberhentikan perulangan while
                    konfirmasi = inputhandler("Apakah anda yakin? [y/n]: ")
                    if konfirmasi.lower() == 'y': #lower digunakan biar bisa huruf besar dan kecil
                        adminpass["password"] = password_baru #password admin adalah password yang baru
                        simpan_data()#memanggil function tanpa perlu repot menulis program berulang ulang
                        print(f"\nPassword anda telah diubah")
                        break #untuk memberhentikan perulangan while
                    else:
                        print("\nBerhasil dibatalkan")
                elif pilihan == '3':
                    break #untuk memberhentikan perulangan while
                else:
                    print("Pilihan tidak valid!\n")
        elif pilihan == '6':
            menu_awal() #memanggil function tanpa perlu repot menulis program berulang ulang
        else:
            print("Pilihan tidak valid!\n")



#----------Login Admin--------
def login_admin():
    print(f"\n{'='*10} Login Sebagai Admin {'='*10}") #judul
    username = inputhandler("Username: ")
    password = pwinput.pwinput("Password: ", mask='*')

    sukses = False #boolean
    if adminpass["username"] == username and adminpass["password"] == password: #jika username yang dimasukkan sama dengan username yang didata dan password sama dengan password yang didata
            sukses = True #boolean
    
    if sukses:
        global user_type #global digunakan agar valiabel dapat digunakan diluar function
        user_type = "admin"
        print("\nSelamat Datang Admin")
        
        refresh_table_kamar() #memanggil function tanpa perlu repot menulis program berulang ulang
        menu_admin() #memanggil function tanpa perlu repot menulis program berulang ulang
    else:
        print("\nLogin gagal! Pastikan username dan password anda benar!")
#-------------------------------------#



#------------- Proses Menu Pengunjung-------------#
#---Pesan kamar---
def pesan_kamar():
    print(tabel_kamar) #menampilkan tabel kamar
    pilihan = inputhandler("Pilih nomor: ")
    kamar_ada = False #boolean
    if current_user["nomor kamar"] != "NA":
        print(f"Anda sudah memiliki kamar ('{current_user['nomor kamar']}')")
    else:
        for kamar in data_kamar: #untuk kamar didalam data kamar
            if kamar["nomor"] == pilihan: #jika nomor kamar sama dengan nomor yang diinputkan
                kamar_ada = True #maka hasilnya true (boolean)
                if kamar["pemilik"] == '': #jika pemilik sama dengan...
                    if current_user["saldo"] >= kamar["harga bulanan"]:
                        
                        current_user["terakhir bayar"] = tanggal
                        current_user["lunas"] = "lunas"
                        current_user["nomor kamar"] = pilihan
                        current_user["tenggat"] = (today + timedelta(days=30)).strftime("%d/%m/%Y %H:%M")
                        kamar["pemilik"] = current_user["username"]
                        
                        for data in data_pemasukan: #untuk data di dalam data pemasukan
                            if data["tahun"] == tahun and data["bulan"] == bulan: #jika tahun didata ssama dengan tahun dan bulan didata sama dengan bulan
                                data["pemasukan"] += kamar["harga bulanan"] #data pemasukkan ditambahkan dengan harga kamar
                                break #untuk memberhentikan perulangan while
                        else:
                            data_pemasukan.append({"tahun": tahun, "bulan": bulan, "pemasukan": kamar["harga bulanan"]}) # append menambahkan item dari belakang.

                        sisa_duid = current_user["saldo"] - kamar["harga bulanan"] 
                        invoice = PrettyTable() #invoice dalam bentuk prettytable
                        invoice.title = "Detail Pemesanan" #judul table
                        invoice.field_names = ["Nomor", "Waktu Pemesanan", "Berlaku Hingga", "Harga Bulanan"] #field tabel
                        invoice.add_rows([ #tambahkan lebih dari satu baris
                            [kamar["nomor"], tanggal, current_user["tenggat"], format_uang(kamar["harga bulanan"])],
                            ['','','-'*10,'-'*10],
                            ['','',"Saldo:", format_uang(current_user["saldo"])],
                            ['','',"Sisa Saldo:", format_uang(sisa_duid)],
                            ['','',"",""],
                            ['','',"","Terima Kasih"]
                        ])
                        current_user["saldo"] = sisa_duid
                        global kamar_user #global digunakan agar variabel dapat digunakan diluar function
                        kamar_user = kamar #kamar user adalah kamar
                        simpan_data() #memanggil function tanpa perlu repot menulis program berulang ulang

                        print(invoice) 
                        refresh_table_kamar()#memanggil function tanpa perlu repot menulis program berulang ulang
                        print() #memanggil function tanpa perlu repot menulis program berulang ulang
                        return #Return: Nilai yang dikembalikan ini bisa berupa hasil operasi dalam fungsi, nilai variabel, atau struktur data lainnya. Ketika fungsi dipanggil dalam ekspresi, fungsi tersebut akan "digantikan" oleh nilai yang dikembalikan.
                        
                    elif current_user["saldo"] == 0:
                        print("Anda tidak memiliki uang, mohon isi saldo anda\n")
                        return #Return: Nilai yang dikembalikan ini bisa berupa hasil operasi dalam fungsi, nilai variabel, atau struktur data lainnya. Ketika fungsi dipanggil dalam ekspresi, fungsi tersebut akan "digantikan" oleh nilai yang dikembalikan.
                    else:
                        print(f"Anda hanya memiliki {format_uang(current_user['saldo'])}, mohon isi saldo anda\n")
                else:
                    print("Kamar Sudah Ada Yang Punya\n")
                    return #Return: Nilai yang dikembalikan ini bisa berupa hasil operasi dalam fungsi, nilai variabel, atau struktur data lainnya. Ketika fungsi dipanggil dalam ekspresi, fungsi tersebut akan "digantikan" oleh nilai yang dikembalikan.
        if not kamar_ada: #jika tidak ada kamar
            print("Kamar Tidak Ada\n")
            return #Return: Nilai yang dikembalikan ini bisa berupa hasil operasi dalam fungsi, nilai variabel, atau struktur data lainnya. Ketika fungsi dipanggil dalam ekspresi, fungsi tersebut akan "digantikan" oleh nilai yang dikembalikan.

#---Bayar---
def bayar(bulan_dibayar):
    if current_user["saldo"] >= kamar_user["harga bulanan"]:
        current_user["terakhir bayar"] = tanggal
        parsed_tenggat = datetime.strptime(current_user["tenggat"], "%d/%m/%Y %H:%M")

        if bulan_dibayar == 2:
            current_user["tenggat"] = (parsed_tenggat+timedelta(days=60)).strftime("%d/%m/%Y %H:%M")
            current_user["lunas"] = "lunas"
        else:
            if str(parsed_tenggat.strftime("%m/%Y")) == f"{int(bulan)+1}/{tahun}":
                current_user["lunas"] = "lunas"
            else:
                current_user["tenggat"] = (parsed_tenggat+timedelta(days=30)).strftime("%d/%m/%Y %H:%M")
        
        for data in data_pemasukan:
            if data["tahun"] == tahun and data["bulan"] == bulan:
                data["pemasukan"] += kamar_user["harga bulanan"]*bulan_dibayar
                break
        else:
            data_pemasukan.append({"tahun":tahun, "bulan":bulan, "pemasukan":kamar_user["harga bulanan"]*bulan_dibayar})
        
        sisa_duid = current_user["saldo"] - kamar_user["harga bulanan"]*bulan_dibayar
        invoice = PrettyTable()
        invoice.title = "Detail Pembayaran"
        invoice.field_names = ["Nomor", "Waktu Pembayaran", "Berlaku Hingga", "Bulan", "Harga Bulanan"]
        invoice.add_rows([
            [kamar_user["nomor"], tanggal, current_user["tenggat"], bulan_dibayar, format_uang(kamar_user["harga bulanan"])],
            ['','','','-'*10,'-'*10],
            ['','','',"Saldo:", format_uang(current_user["saldo"])],
            ['','','',"sisa duid:", format_uang(sisa_duid)]
        ])
        current_user["saldo"] = sisa_duid
        simpan_data()
        print(invoice)
    elif current_user["saldo"] == 0:
        print("Anda tidak memiliki uang, mohon isi saldo anda\n")
    else:
        print(f"Anda hanya memiliki {format_uang(current_user['saldo'])}, mohon isi saldo anda\n")

#---Pengaturan Akun Pengunjung---
def setting_user():
    print(f"\n{'='*10} Pengaturan Akun {'='*10}")
    while True:
        print("[1] Ganti username")
        print("[2] Ganti password")
        print("[3] Kembali")
        pilihan = inputhandler("Pilihan: ")
        if pilihan == '1':
            while True:
                username_baru = inputhandler("Username baru: ").strip()
                if len(username_baru) < 5:
                    print("Minimal 5 huruf")
                else:
                    break
            konfirmasi = inputhandler("Apakah anda yakin? [y/n]: ")
            # lower tu untuk bikin huruf besar jadi kecil.
            if konfirmasi.lower() == 'y':
                for user in userpass:
                    if user["username"] == current_user["username"]:
                        current_user["username"] = username_baru
                        user["username"] = username_baru
                        if current_user["nomor kamar"] != "NA":
                            kamar_user["pemilik"] = username_baru

                simpan_data() #memanggil function tanpa perlu repot menulis program berulang ulang
                refresh_table_kamar() #memanggil function tanpa perlu repot menulis program berulang ulang
                print(f"\nUsername anda telah diubah ke {username_baru}")
                lihat_akun(current_user["username"])
                break
            else:
                print("Berhasil dibatalkan")

        elif pilihan == '2':
            while True:
                password_baru = pwinput.pwinput("Password baru: ", mask='*').strip()
                if len(password_baru) < 5:
                    print("Minimal 5 huruf")
                else:
                    break
            konfirmasi = inputhandler("Apakah anda yakin? [y/n]: ")
            if konfirmasi.lower() == 'y':
                for user in userpass:
                    if user["username"] == current_user["username"]:
                        user["password"] = password_baru
                        simpan_data() #memanggil function tanpa perlu repot menulis program berulang ulang
                        print(f"\nPassword anda telah diubah")
                        lihat_akun(current_user["username"])
                        break
            else:
                print("\nBerhasil dibatalkan")
        elif pilihan == '3':
            break
        else:
            print("Pilihan tidak valid!\n")

#---Status Hari---
def ket(hari):
    if hari == 0:
        keterangan = "Hari ini"
    elif hari < 0:
        keterangan = f"{-hari} hari yang lalu"
    else:
        keterangan = f"{hari} hari lagi"
    return keterangan

#---Lihat Akun Pengunjung---
def lihat_akun(username):
    print(f"\n{'='*10} Akun {'='*10}")
    for user in data_user:
        if user["username"] == username:
            print(f"Username: {user['username']}")
            print(f"Saldo: {format_uang(user['saldo'])}")

            if user["nomor kamar"] == "NA":
                print("belom punya kamar")
                if user_type != "admin":
                    while True:
                        print("[1] Pengaturan Akun")
                        print("[2] Kembali")
                        pilihan = inputhandler("Pilihan: ")
                        if pilihan == '1':
                            setting_user() #memanggil function tanpa perlu repot menulis program berulang ulang
                            break
                        elif pilihan == '2':
                            menu_user() #memanggil function tanpa perlu repot menulis program berulang ulang
                            break 
                        else:
                            print("Pilihan tidak valid!\n")
            else:
                for kamar in data_kamar:
                    if kamar["nomor"] == user["nomor kamar"]:
                        # strptime = string parse time (ubah string tanggal menjadi objek datetime)
                        tenggat = datetime.strptime(user["tenggat"], "%d/%m/%Y %H:%M")
                        sisa_hari = (tenggat - today).days
                        
                        # terakhir bayar n hari yg lalu
                        tb = (today - datetime.strptime(user['terakhir bayar'], "%d/%m/%Y %H:%M")).days
                        
                        print(f"Nomor Kamar: {user['nomor kamar']}")
                        print(f"Terakhir Bayar: {user['terakhir bayar']} ({ket(-tb)})")
                        if kamar_user["ketersediaan"] == "pending":
                            print("Peringatan: Kamar anda akan dihapus, segera keluar\n")
                            
                        if user["lunas"] == "lunas":
                            print(f"Berlaku hingga: {user['tenggat']} ({ket(sisa_hari)})")
                            print("Lunas\n")
                            if user_type != "admin":
                                while True:
                                    print("[1] Pengaturan Akun")
                                    print("[2] Kembali")
                                    pilihan = inputhandler("Pilihan: ")
                                    if pilihan == '1':
                                        setting_user() #memanggil function tanpa perlu repot menulis program berulang ulang
                                        break
                                    elif pilihan == '2':
                                        menu_user() #memanggil function tanpa perlu repot menulis program berulang ulang
                                        break
                                    else:
                                        print("Pilihan tidak valid!\n")
                        else:
                            print(f"Tenggat: {user['tenggat']} ({ket(sisa_hari)})")
                            bulan_nunggak = 1
                            if today > tenggat:
                                bulan_nunggak = 2
                                print("Belum bayar bulan lalu")
                                print(f"Sisa {5 + sisa_hari} hari lagi sebelum kepemilikan kamar dihapus!")
                            print(f"Tagihan: {format_uang(kamar['harga bulanan']*bulan_nunggak)}\n")
                            
                            # buat ngilangin tombol bayar kalo yg login itu admin
                            if user_type != 'admin':
                                while True:
                                    print("[1] Pengaturan Akun")
                                    print("[2] Bayar")
                                    print("[3] Kembali")
                                    pilihan = inputhandler("Pilihan: ")
                                    if pilihan == '1':
                                        setting_user() #memanggil function tanpa perlu repot menulis program berulang ulang
                                    elif pilihan == '2':
                                        if bulan_nunggak > 1:
                                            print("[1] Bayar 1 bulan")
                                            print("[2] Langsung lunas")
                                            print("[3] Kembali")
                                            pilihan = inputhandler("Pilihan: ")
                                            if pilihan == '1':
                                                bayar(1) #memanggil function tanpa perlu repot menulis program berulang ulang
                                            elif pilihan == '2':
                                                bayar(2) #memanggil function tanpa perlu repot menulis program berulang ulang
                                            elif pilihan== '3':
                                                return
                                            else:
                                                print("Pilihan tidak valid!\n")
                                        else:
                                            bayar(1) #memanggil function tanpa perlu repot menulis program berulang ulang
                                    elif pilihan == '3':
                                        menu_user() #memanggil function tanpa perlu repot menulis program berulang ulang
                                        return
                                    else:
                                        print("Pilihan tidak valid!\n")
                        return
            return
    print("Akun tidak ditemukan!\n")

#---Tambah Saldo---
def tambah_saldo():
        while True:
            duit = inputhandler("Masukkan Saldo Anda: ", "int")
            if duit > 0:
                current_user["saldo"] += duit
                simpan_data()
                print(f"{format_uang(duit)} berhasil ditambah ke saldo anda\n")
                break
            else:
                print("\nTidak Bisa Negatif. Harap isi dengan benar!")

#---Berhenti Menyewa---
def berhenti():
    if current_user["nomor kamar"] != "NA":
        if current_user["lunas"] == "lunas":
            konfirmasi = inputhandler(f"Apakah anda yakin ingin berhenti menyewa kamar {current_user['nomor kamar']}? [y/n]: ")
            if konfirmasi.lower() == 'y':
                print(f"Anda telah berhenti tinggal di kamar {current_user['nomor kamar']}")
                print()
                kamar_user["pemilik"] = ''
                current_user["nomor kamar"] = "NA"
                current_user["tenggat"] = "NA"
                if kamar_user["ketersediaan"] == "pending":
                    data_kamar.remove(kamar_user)
                else:
                    kamar_user["ketersediaan"] == "tersedia"
                simpan_data() #memanggil function tanpa perlu repot menulis program berulang ulang
                refresh_table_kamar() #memanggil function tanpa perlu repot menulis program berulang ulang
            else:
                print("\nBerhasil dibatalkan.")
        else:
            print("Harap bayar tunggakan terlebih dahulu!\n")
    else:
        print("Tidak menyewa\n")



#-------Tampilan Menu Pengunjung--------
def menu_user():
    print(f"\n{'='*10} Menu Utama {'='*10}")
    while True:
        print("[1] Pesan kamar")
        print("[2] Lihat akun")
        print("[3] Tambah saldo")
        print("[4] Berhenti menyewa")
        print("[5] Keluar")
        pilihan = inputhandler("Pilihan: ")
        if pilihan == '1':
            pesan_kamar() #memanggil function tanpa perlu repot menulis program berulang ulang
        elif pilihan == '2': 
            lihat_akun(current_user["username"]) #memanggil function tanpa perlu repot menulis program berulang ulang
        elif pilihan == '3':
            tambah_saldo() #memanggil function tanpa perlu repot menulis program berulang ulang
        elif pilihan == '4':
            berhenti() #memanggil function tanpa perlu repot menulis program berulang ulang
        elif pilihan == '5':
            menu_awal() #memanggil function tanpa perlu repot menulis program berulang ulang
        else:
            print("Pilihan tidak valid!\n")



#----------Register Pengunjung----------
def menu_register():
    print(f"\n{'='*10} Registrasi Akun {'='*10}")
    while True:
        username = inputhandler("Username: ").strip()
        if len(username) < 5:
            print("Minimal 5 huruf")
        else:
            break
    while True:
        try:
            password = pwinput.pwinput("Password: ", mask='*').strip()
            if len(password) < 5:
                print("Minimal 5 huruf")
            else:
                break
        except KeyboardInterrupt:
            print("Hayolo!")

    sudah_ada = False
    for akun in userpass:
        if akun["username"] == username:
            sudah_ada = True
    
    if sudah_ada:
        print("Username sudah ada")
    else:
        data_user.append({"username": username, "nomor kamar": "NA", "terakhir bayar": "NA", "tenggat": "NA", "lunas": "belum", "saldo": 0})
        simpan_data() #memanggil function tanpa perlu repot menulis program berulang ulang

        userpass.append({"username": username, "password": password})
        with open('userpass.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([username, password])

        global user_type, current_user
        user_type = "normal"
        current_user = data_user[-1]
        
        print("\nAkun berhasil dibuat")

        refresh_table_kamar() #memanggil function tanpa perlu repot menulis program berulang ulang
        menu_user() #memanggil function tanpa perlu repot menulis program berulang ulang



#---------min Sebagai Pengunjung---------
def menu_login():
    print(f"\n{'='*10} Login {'='*10}")
    username = inputhandler("Username: ")
    password = pwinput.pwinput("Password: ", mask='*')

    sukses = False
    for akun in userpass:
        if akun["username"] == username and akun["password"] == password:
            sukses = True
    
    if sukses:
        global user_type #global dipakai untuk memanggil variabel yang ada didalam function
        user_type = "normal"
        for user in data_user:
            if user["username"] == username:
                global current_user #global dipakai untuk memanggil variabel yang ada didalam function
                current_user = user
                if user["nomor kamar"] != "NA":
                    for kamar in data_kamar:
                        if kamar["pemilik"] == username:
                            global kamar_user
                            kamar_user = kamar
                    
        print("\nBerhasil login")
        
        for user in data_user:
            if user["username"] == current_user["username"] and user["tenggat"] != "NA":
                # string tenggat waktu diubah ke objek datetime
                parsed_tenggat = datetime.strptime(user["tenggat"], "%d/%m/%Y %H:%M")
                # sama, tapi untuk tanggal terakhir bayar
                parsed_tb = datetime.strptime(user["terakhir bayar"], "%d/%m/%Y %H:%M")
                # brp hari lewat dari tenggat
                lewat = (today-parsed_tenggat).days
                if today > parsed_tenggat:
                    user["lunas"] = "belum"
                    if (today - parsed_tb).days < 60:
                        user["tenggat"] = (parsed_tenggat+timedelta(days=30)).strftime("%d/%m/%Y %H:%M")
                        simpan_data()#memanggil function tanpa perlu repot menulis program berulang ulang
                    elif lewat > 0 and lewat < 5:
                        print("Cepati bayar!!!!!!!!!")
                    elif lewat >= 5:
                        kamar_user["pemilik"] = ""
                        current_user["nomor kamar"] = "NA"
                        simpan_data()#memanggil function tanpa perlu repot menulis program berulang ulang
                        print("Kamar Hilang!")

        refresh_table_kamar()#memanggil function tanpa perlu repot menulis program berulang ulang
        menu_user()#memanggil function tanpa perlu repot menulis program berulang ulang
    else:
        print("\nLogin gagal! Pastikan username dan password anda benar!")
        print()


#-----------Tampilan Awal--------
def menu_awal():
    print('='*10, "Pilih Role", '='*10)
    while True: #while true adalah bentuk perulangan yang tidak memiliki batas
        print("[1] Pengunjung")
        print("[2] Admin")
        print("[3] Selesai")
        while True: #while true adalah bentuk perulangan yang tidak memiliki batas
            try: #try except adalah jika terjadi error maka akan diberitahu errornya apa dengan bahasa kita
                pilihan = inputhandler("Pilih: ")
                break #untuk memberhentikan perulangan while
            except KeyboardInterrupt:
                print("ea\n")
        if pilihan == '1':
            pilihan = inputhandler("Apakah anda sudah memiliki akun? [y/n]: ")
            if pilihan.lower() == 'y': #lower biar bisa huruf besar dan huruf kecil
                menu_login()#memanggil function tanpa perlu repot menulis program berulang ulang
            elif pilihan.lower() == 'n': #lower biar bisa huruf besar dan huruf kecil
                menu_register()#memanggil function tanpa perlu repot menulis program berulang ulang
        elif pilihan == '2':
            login_admin()#memanggil function tanpa perlu repot menulis program berulang ulang
        elif pilihan == '3':
            print("\nTerima Kasih")
            # exit tu nutup program secara keseluruhan
            exit()#memanggil function tanpa perlu repot menulis program berulang ulang
        else:
            print("Pilihan tidak valid!\n")

print()
print("================================")
print("|         KOS MERAKYAT         |")
menu_awal()#memanggil function tanpa perlu repot menulis program berulang ulang