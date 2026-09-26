# ==========================================
# FAIL: tempat_menarik.py
# MODUL PENGKALAN DATA DESTINASI PELANCONGAN & CADANGAN LOKASI
# ==========================================

DESTINASI_SEMENANJUNG = {
    "johor": [
        "Legoland Malaysia, Iskandar Puteri",
        "Desaru Coast & Pantai Desaru",
        "Taman Negara Johor Endau-Rompin",
        "Bandar Raya Johor Bahru (Danga Bay / Bazar Karat)",
        "Kukup & Tanjung Piai (Penghujung Benua Asia)"
    ],
    "kedah": [
        "Jeti Kuala Kedah (Laluan Feri ke Langkawi)",
        "Gunung Jerai Geopark, Yan",
        "Pekan Rabu, Alor Setar",
        "Menara Alor Setar & Masjid Zahir",
        "Sedim Riverside (Tree Top Walk)"
    ],
    "kelantan": [
        "Pasar Siti Khadijah, Kota Bharu",
        "Pantai Irama, Bachok",
        "Rantau Panjang (Zon Bebas Cukai)",
        "Pengkalan Kubor, Tumpat",
        "Masjid Muhammadi & Muzium Negeri Kelantan"
    ],
    "melaka": [
        "Bandar Hilir, Kota A Famosa & Menara Taming Sari",
        "Jonker Walk Night Market",
        "Masjid Selat Melaka (Pulau Melaka)",
        "Ayer Keroh (Zoo Melaka, Taman Buaya & Taman Botanikal)",
        "Pantai Pengkalan Balak, Masjid Tanah"
    ],
    "negeri sembilan": [
        "Pantai Teluk Kemang, Port Dickson",
        "Pantai Tanjung Biru (Blue Lagoon), Port Dickson",
        "Muzium Diraja Seri Menanti, Kuala Pilah",
        "Hutan Lipur Ulu Bendul, Seremban",
        "Pusat Ibadah & Falak Baitul Hilal, Teluk Kemang"
    ],
    "pahang": [
        "Genting Highlands (SkyAvenue & SkyWorlds)",
        "Cameron Highlands (Kea Farm, Ladang Teh BOH, Bharat Tea)",
        "Janda Baik & Bukit Tinggi (Colmar Tropicale)",
        "Teluk Cempedak & Cherating, Kuantan",
        "Taman Negara Kuala Tahan, Jerantut"
    ],
    "perak": [
        "Lost World of Tambun, Ipoh",
        "Pekan Lama Ipoh (Concubine Lane & Restoran Halal Popular)",
        "Gua Tempurung, Gopeng",
        "Jeti Marina Island / Lumut (Pintu Masuk Pulau Pangkor)",
        "Kellie's Castle, Batu Gajah",
        "Menara Condong Teluk Intan"
    ],
    "perlis": [
        "Gua Kelam, Kaki Bukit",
        "Wang Kelian Viewpoint",
        "Taman Herba Perlis & Tasik Timah Tasoh",
        "Padang Besar (Pusat Beli-belah Sempadan)"
    ],
    "pulau pinang": [
        "Georgetown UNESCO World Heritage Site",
        "Bukit Bendera (Penang Hill)",
        "Batu Ferringhi & Padang Kota Lama (Esplanade)",
        "Taman Tema ESCAPE & Entopia, Teluk Bahang"
    ],
    "selangor": [
        "i-City Theme Park, Shah Alam",
        "Bukit Melawati & Taman Kelip-Kelip, Kuala Selangor",
        "Sky Mirror Sasaran, Kuala Selangor",
        "Batu Caves (Kuil & Kawasan Gua Batu Kapur)",
        "Pantai Morib & Pantai Bagan Lalang, Sepang",
        "FRIM Kepong & Hutan Lipur Kanching, Rawang"
    ],
    "terengganu": [
        "Jeti Merang / Besut (Pintu Masuk Pulau Redang & Perhentian)",
        "Pasar Payang & Kampung Cina, Kuala Terengganu",
        "Masjid Kristal & Taman Tamadun Islam",
        "Pantai Batu Buruk, Kuala Terengganu",
        "Tasik Kenyir, Hulu Terengganu"
    ],
    "kuala lumpur": [
        "Menara Berkembar PETRONAS (KLCC) & Menara KL",
        "Merdeka 118 & Dataran Merdeka",
        "Bukit Bintang, Pavilion & Lalaport BBCC",
        "Taman Tasik Perdana (Botanical Gardens) & Taman Tasik Titiwangsa",
        "Pasar Seni (Central Market) & Petaling Street"
    ],
    "putrajaya": [
        "Masjid Putra & Dataran Putra",
        "Tasik Putrajaya (Cruise Tasik Putrajaya)",
        "Taman Saujana Hijau & Taman Botani Putrajaya",
        "Masjid Tuanku Mizan Zainal Abidin (Masjid Besi)",
        "IOI City Mall Putrajaya"
    ]
}

def get_tempat_menarik():
    """Mengembalikan keseluruhan pengkalan data tempat menarik."""
    return DESTINASI_SEMENANJUNG

def cari_tempat_menarik(query):
    """
    Mencari senarai tarikan popular berdasarkan nama negeri atau kata kunci lokasi.
    Contoh: cari_tempat_menarik('pahang') atau cari_tempat_menarik('cameron')
    """
    if not query:
        return None, []

    q = str(query).strip().lower()

    # 1. Semakan nama negeri secara langsung
    for negeri, senarai in DESTINASI_SEMENANJUNG.items():
        if negeri in q:
            return negeri.title(), senarai

    # 2. Semakan mengikut nama destinasi/tempat
    jumpaan = []
    negeri_terlibat = set()
    for negeri, senarai in DESTINASI_SEMENANJUNG.items():
        for tempat in senarai:
            if q in tempat.lower():
                jumpaan.append(tempat)
                negeri_terlibat.add(negeri.title())

    if jumpaan:
        label = ", ".join(negeri_terlibat)
        return label, jumpaan

    return None, []

def senaraikan_semua_negeri():
    """Mengembalikan senarai nama negeri yang disokong."""
    return [n.title() for n in DESTINASI_SEMENANJUNG.keys()]