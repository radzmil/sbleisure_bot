# ==========================================
# FAIL: info_jalan.py
# MODUL PENGESANAN STRUKTUR JALAN & INFRASTRUKTUR
# ==========================================

LALUAN_KHAS = {
    "berbukit": {
        "kategori": "Jalan Berbukit & Kawasan Tanah Tinggi",
        "keywords": ["cameron", "genting", "fraser", "bukit tinggi", "bukit larut", "gunung jerai", "tanah tinggi"],
        "contoh_lokasi": "Cameron Highlands, Genting Highlands, Bukit Tinggi",
        "panduan_bas": "Perjalanan memerlukan bas berkuasa tinggi (enjin euro spesifikasi bukit), brek retarder yang diservis rapi, serta pemandu berpengalaman di laluan cerun curam."
    },
    "sempit": {
        "kategori": "Jalan Sempit, Pedalaman & Luar Bandar",
        "keywords": ["kampung", "pedalaman", "felda", "sempit", "jambatan kayu", "lorong", "chalet tepi sungai", "hulu"],
        "contoh_lokasi": "Chalet pedalaman, perkampungan tradisi, perkhemahan tepi sungai",
        "panduan_bas": "Kelebaran laluan dan jejambat perlu disemak terlebih dahulu; bas bersaiz 40-44 kerusi mungkin perlu digantikan dengan bas mini atau van persiaran mengikut kesesuaian jalan."
    },
    "sungai_rekreasi": {
        "kategori": "Kawasan Rekreasi Air Terjun & Hutan Lipur",
        "keywords": ["sungai", "air terjun", "riadah", "rekreasi", "hutan lipur", "sungai gabai", "ulu yam", "janda baik", "chiling"],
        "contoh_lokasi": "Sungai Gabai, Janda Baik, Hutan Lipur Kanching, Ulu Yam",
        "panduan_bas": "Akses laluan masuk selalunya berbatu, berlopak atau mempunyai selekoh tajam. Perlu semakan tempat letak kenderaan berat/bas persiaran di tapak rekreasi."
    }
}

def semak_struktur_jalan_khas(mesej):
    """
    Menyemak teks pelanggan untuk mengesan sama ada destinasi/lokasi
    melibatkan bentuk muka bumi mencabar (berbukit, sempit, rekreasi).
    """
    if not mesej:
        return None

    teks = mesej.lower()

    for jenis, data in LALUAN_KHAS.items():
        if any(kata in teks for kata in data["keywords"]):
            return {
                "kategori": data["kategori"],
                "contoh_lokasi": data["contoh_lokasi"],
                "panduan_bas": data["panduan_bas"]
            }

    return None