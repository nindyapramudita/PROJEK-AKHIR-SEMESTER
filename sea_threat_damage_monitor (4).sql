-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 29 Apr 2024 pada 14.07
-- Versi server: 10.4.28-MariaDB
-- Versi PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sea_threat_damage_monitor`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `admin`
--

CREATE TABLE `admin` (
  `ID_Admin` int(20) NOT NULL,
  `nama_lengkap` varchar(40) DEFAULT NULL,
  `no_hp_admin` varchar(13) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `admin`
--

INSERT INTO `admin` (`ID_Admin`, `nama_lengkap`, `no_hp_admin`, `email`) VALUES
(2147010201, 'I Putut Gajahmada', '081239547239', 'gajahduduk@gmail.com'),
(2147010202, 'Jose Mario dos Santos Mourinho', '083210987654', 'josemourinho@gmail.com'),
(2147010208, 'admin1', '083895485325', 'nindya@gmail.com');

-- --------------------------------------------------------

--
-- Struktur dari tabel `aduan`
--

CREATE TABLE `aduan` (
  `ID_Aduan` int(40) NOT NULL,
  `ID_Masyarakat` bigint(40) DEFAULT NULL,
  `lokasi` varchar(60) NOT NULL,
  `Tanggal` date DEFAULT NULL,
  `keterangan_aduan` varchar(150) DEFAULT 'Tanpa Keterangan'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `aduan`
--

INSERT INTO `aduan` (`ID_Aduan`, `ID_Masyarakat`, `lokasi`, `Tanggal`, `keterangan_aduan`) VALUES
(29, 6472333008050138, 'Pantai Selatan', '2024-04-28', 'Terumbu karang banyak hancur karena ditabrak oleh banyaknya kapal laut'),
(30, 6472333008050198, 'Laut Selat', '2024-04-28', 'Terjadi pengebom-an ikan di banyak titik laut dan mengakibatkan ribuan ekor ikan mati'),
(32, 6472333008050225, 'Laut Timur', '2024-04-28', 'Ditemukan bangkai kapal WNA'),
(33, 6472333008050138, 'Raja Ampat', '2024-02-02', 'banyak penyu diambil orang disini, tolong ditertibkan kaka'),
(34, 6472333008050138, 'Laut Mahameru', '2024-07-03', 'banyak kapal mancing ikan pakai pukat harimau ini, saya sebagai nelayan tidak dapat ikan, terumbu karang pun hancur'),
(35, 6472333008050138, 'Kepulauan Seribu', '2024-07-19', 'Waduh di pulau seribu ini banyak sekali orang buang sampah di pesisir pantai, Tolong Ditindak lanjuti ya'),
(36, 6472333008050138, 'Laut Antapura', '2024-02-20', 'kapal kapal pelat banyak yang buang limbah minyak di laut, laut jadi kotor'),
(37, 6472333008050179, 'Sungai Sanga Sanga', '2024-03-08', 'Limbah pestisida bekas pertanian ini mengalir ke sungai'),
(38, 6472333008050179, 'Teluk Kapau', '2024-03-24', 'Kapal kapal besar yang lewat teluk kapau bikin rusak terumbu karang nih, tolong ditertibkan'),
(39, 6472333008050179, 'Laut Merah', '2024-04-08', 'Waduh saya pas mancing tadi banyak liat ada orang tangkap Hiu Massal, tolong diatasi'),
(40, 6472333008050179, 'Teluk Mawar', '2024-03-07', 'ini banyak yang ambil telur penyu kalo malam malam'),
(41, 6472333008050179, 'Perairan Sosnovka', '2024-09-04', 'banyak kapal kapal thailand pake bendera indo ini curi ikan, pakai pukat harimau lagi'),
(42, 6472333008050198, 'Laut Jawa', '2024-05-08', 'waduh mbaa ini banyak kapal kapal buang sampah sembarangan piye iki'),
(43, 6472333008050198, 'Flores', '2024-07-14', 'ini penyu penyu banyak sekali diambil orang padahal dilindungi'),
(44, 6472333008050198, 'Pulau Kerdil', '2024-03-13', 'Banyak Terumbu Karang mati ini gara gara kapal besar lewat'),
(45, 6472333008050225, 'Laut Aceh', '2024-04-01', 'Limba Minyak Banyak Dibuang Kapal'),
(46, 6472333008050225, 'Wamena', '2024-06-04', 'Banyak Orang Curi Terumbu Karang, dirusak juga habitat ikan'),
(47, 6472333008050225, 'Maratua', '2024-05-09', 'Banyak Sekali ini turis buang sampah ke laut, kotor jadi laut maratua'),
(48, 6472333008050645, 'Labuan Bajo', '2024-09-11', 'di labuan bajo ini banyak sekali ikan pari hias yang diburu untuk konsumsi'),
(49, 6472333008050645, 'Laut Pariaman', '2024-09-05', 'Orang menangkap ikan dengan menggunakan bom, membuat air tercemar'),
(50, 6472333008050645, 'Laut Papua Barat', '2024-04-11', 'saya melihat banyak kapal kapal yang membuang limba sembarangan'),
(51, 6472333008050645, 'Selat Balikpapan', '2024-11-06', 'banyak minyak yang tersebar ke laut akibat kebocoran kilang minyak'),
(52, 6472333008050645, 'Selat Malaka', '2024-09-25', 'Banyak Nelayan yang memancing ikan menggunakan Pukat Harimau'),
(53, 6472333008050666, 'Selat Sunda', '2024-12-05', 'terjadi pengeboman ikan besar besaran, membuat karang hancur'),
(54, 6472333008050666, 'Teluk Pandan', '2024-12-24', 'Pesisir pantai dipenuhi limbah minyak'),
(55, 6472333008050666, 'Selat Sangatta', '2024-08-07', 'Banyak Orang mmebuang sampah ke laut'),
(56, 6472333008050666, 'Teluk Merah', '2024-10-29', 'Limbah Pabrik mengalir dari sungai mencemari laut'),
(57, 6472333008050138, 'Teluk Hijau', '2024-10-14', 'Banyak Kapal Besar Lewat dan menurunkan jangkar menyebabkan kerusakan karang'),
(58, 6472333008050138, 'Pantai Selatan', '2024-08-06', 'Limbah Sampah Tiba tiba berdatangan, tolong diatasi'),
(59, 6472333008050138, 'Selat Jayapura', '2024-12-30', 'Terjadi penangkapan ikan dilindungi besar besaran'),
(60, 6472333008050198, 'Ujung Kulon', '2024-10-17', 'Penangkapan spesies Hiu dilindungi'),
(61, 6472333008050198, 'Banda Neira', '2024-12-12', 'Perusakan Terumbu Krang oleh turis'),
(62, 6472333008050198, 'Biduk Biduk', '2024-11-04', 'Pencemaran Limbah Kulit Kelapa ke Laut, serta sampah sampah turis'),
(63, 6472333008050225, 'Labuan Cermin', '2024-06-27', 'Penyu penyu dicuri telurnya'),
(64, 6472333008050666, 'Selat Maluku', '2024-04-11', 'Terjadi Penangkapan Hiu secara Massal'),
(65, 6472333008050225, 'Laut Sumatra', '2024-03-19', 'Pencemaran Laut dengan pembuangan limbah minyak kapal'),
(66, 6472333008050645, 'Balikpapan', '2024-02-13', 'Minyak Minyak bertebaran di laut'),
(68, 6472333008050138, 'Pulau Seribu   ', '2024-04-29', 'Perusakan terumbu karang akibat aktivitas pariwisata  ');

-- --------------------------------------------------------

--
-- Struktur dari tabel `data_kerusakan`
--

CREATE TABLE `data_kerusakan` (
  `ID_data` int(40) NOT NULL,
  `ID_Admin` int(20) DEFAULT NULL,
  `lokasi` varchar(60) NOT NULL,
  `tanggal` date DEFAULT NULL,
  `jenis_kerusakan` varchar(30) DEFAULT NULL,
  `deskripsi` varchar(100) DEFAULT NULL,
  `jumlah_kerusakan` int(10) DEFAULT NULL,
  `ID_Aduan` int(40) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `data_kerusakan`
--

INSERT INTO `data_kerusakan` (`ID_data`, `ID_Admin`, `lokasi`, `tanggal`, `jenis_kerusakan`, `deskripsi`, `jumlah_kerusakan`, `ID_Aduan`) VALUES
(28, 2147010208, 'Rawa lingu', '2024-04-28', 'Kapal laut', 'Bangkai kapal warga negara asing yang tenggelam menjadi penyebab pencemaran laut', 3, NULL),
(29, 2147010208, 'Pantai Amal', '2024-04-28', 'Limbah laut', 'Terdapat banyak tumpukan sampah dipesisir pantai akibat maraknya kunjungan masyarakat diakhir tahun', 40, NULL),
(30, 2147010208, 'Ujung Kulon', '2024-10-17', 'Hewan Laut', 'Penangkapan spesies Hiu dilindungi', 23, NULL),
(31, 2147010208, 'Banda Neira', '2024-12-12', 'Terumbu Karang', 'Perusakan Terumbu Karang oleh turis', 15, NULL),
(32, 2147010208, 'Biduk Biduk', '2024-11-04', 'Laut', 'Pencemaran Limbah Kulit Kelapa ke Laut, serta sampah turis', 40, NULL),
(33, 2147010208, 'Labuan Cermin', '2024-06-27', 'Penyu', 'Penyu dicuri telurnya', 8, NULL),
(34, 2147010208, 'Selat Maluku', '2024-04-11', 'Hewan Laut', 'Terjadi Penangkapan Hiu secara Massal', 30, NULL),
(35, 2147010208, 'Laut Sumatra', '2024-03-19', 'Laut', 'Pencemaran Laut dengan pembuangan limbah minyak kapal', 55, NULL),
(36, 2147010208, 'Balikpapan', '2024-02-13', 'Laut', 'Minyak bertebaran di laut', 10, NULL),
(37, 2147010208, 'Perairan Jawa', '2024-02-20', 'Laut', 'Penggunaan Pukat Harimau oleh para nelayan', 25, NULL),
(38, 2147010208, 'Pulau Rambut', '2024-05-05', 'Keanekaragaman Hayati', 'Perusakan habitat penyu oleh pembangunan pesisir', 12, NULL),
(39, 2147010208, 'Tanjung Layar', '2024-07-01', 'Laut', 'Pencemaran laut oleh limbah industri', 18, NULL),
(40, 2147010208, 'Pulau Seribu', '2024-08-12', 'Terumbu Karang', 'Perusakan terumbu karang akibat aktivitas pariwisata', 20, NULL),
(41, 2147010208, 'Pantai Cermin', '2024-09-29', 'Hewan Laut', 'Penangkapan ikan hiu secara berlebihan', 35, NULL),
(42, 2147010208, 'Selat Sunda', '2024-11-15', 'Laut', 'Pencemaran laut oleh limbah kimia dari kapal tanker', 28, NULL),
(43, 2147010208, 'Pulau Raja', '2024-10-02', 'Keanekaragaman Hayati', 'Perburuan liar terhadap spesies langka', 5, NULL),
(44, 2147010208, 'Teluk Benoa', '2024-12-24', 'Terumbu Karang', 'Perusakan terumbu karang oleh aktivitas kapal pesiar', 42, NULL),
(45, 2147010208, 'Tanjung Kelayang', '2024-11-08', 'Laut', 'Pencemaran laut oleh limbah plastik dari aktivitas pesisir', 60, NULL),
(46, 2147010208, 'Pulau Tidung', '2024-09-18', 'Keanekaragaman Hayati', 'Perusakan habitat penyu oleh pembangunan fasilitas pariwisata', 15, NULL),
(47, 2147010208, 'Perairan Lombok', '2024-08-05', 'Laut', 'Overfishing di perairan sekitar', 50, NULL),
(49, 2147010208, 'Teluk Kiluan', '2024-06-10', 'Terumbu Karang', 'Perusakan terumbu karang oleh kegiatan konstruksi dermaga', 25, NULL),
(50, 2147010208, 'Perairan Jawa', '2024-02-20', 'Hewan laut', 'Penggunaan Pukat Harimau Oleh para nelayan  ', 200, NULL);

-- --------------------------------------------------------

--
-- Struktur dari tabel `masyarakat`
--

CREATE TABLE `masyarakat` (
  `ID_Masyarakat` bigint(20) NOT NULL,
  `nama_lengkap` varchar(40) DEFAULT NULL,
  `alamat_rumah` varchar(60) DEFAULT NULL,
  `no_hp` varchar(13) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `masyarakat`
--

INSERT INTO `masyarakat` (`ID_Masyarakat`, `nama_lengkap`, `alamat_rumah`, `no_hp`) VALUES
(6472333008050138, 'Nindya', 'JL.M.Said', '083895485326'),
(6472333008050179, 'Epunnn', 'Jl.Jakarta', '085676498325'),
(6472333008050198, 'Diva', 'JL.M.Said', '085250699834'),
(6472333008050225, 'Sandra Wijaya', 'Jl. Anggur', '085376856553'),
(6472333008050645, 'Bambang Susilo', 'Jl.Antasari', '084537652876'),
(6472333008050666, 'Egoyyy', 'Jl.Jakarta', '083422687985');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`ID_Admin`);

--
-- Indeks untuk tabel `aduan`
--
ALTER TABLE `aduan`
  ADD PRIMARY KEY (`ID_Aduan`),
  ADD KEY `FK_ID_Masyarakat` (`ID_Masyarakat`);

--
-- Indeks untuk tabel `data_kerusakan`
--
ALTER TABLE `data_kerusakan`
  ADD PRIMARY KEY (`ID_data`),
  ADD KEY `FK_ID_Aduan` (`ID_Aduan`),
  ADD KEY `ID_Admin` (`ID_Admin`);

--
-- Indeks untuk tabel `masyarakat`
--
ALTER TABLE `masyarakat`
  ADD PRIMARY KEY (`ID_Masyarakat`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `admin`
--
ALTER TABLE `admin`
  MODIFY `ID_Admin` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2147010209;

--
-- AUTO_INCREMENT untuk tabel `aduan`
--
ALTER TABLE `aduan`
  MODIFY `ID_Aduan` int(40) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=69;

--
-- AUTO_INCREMENT untuk tabel `data_kerusakan`
--
ALTER TABLE `data_kerusakan`
  MODIFY `ID_data` int(40) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `aduan`
--
ALTER TABLE `aduan`
  ADD CONSTRAINT `FK_ID_Masyarakat` FOREIGN KEY (`ID_Masyarakat`) REFERENCES `masyarakat` (`ID_Masyarakat`),
  ADD CONSTRAINT `aduan_ibfk_1` FOREIGN KEY (`ID_Masyarakat`) REFERENCES `masyarakat` (`ID_Masyarakat`);

--
-- Ketidakleluasaan untuk tabel `data_kerusakan`
--
ALTER TABLE `data_kerusakan`
  ADD CONSTRAINT `FK_ID_Aduan` FOREIGN KEY (`ID_Aduan`) REFERENCES `aduan` (`ID_Aduan`) ON DELETE SET NULL,
  ADD CONSTRAINT `data_kerusakan_ibfk_1` FOREIGN KEY (`ID_Admin`) REFERENCES `admin` (`ID_Admin`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
