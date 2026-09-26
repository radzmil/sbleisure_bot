import math
import requests
from datetime import datetime

def get_engine_rules_text():
    return """
    PANDUAN LOKASI PICKUP & ENJIN HARGA:
    - Semak JADUAL HARGA TETAP LALUAN di bawah terlebih dahulu. Jika laluan wujud, GUNA HARGA TERSEBUT SEBULAT-BULATNYA DAN JANGAN UBAH:
      * Ampang ke Kajang: RM850
      * KLIA ke Kajang: RM850
      * Ampang ke Semenyih: RM850
      * KLIA ke Semenyih: RM970
      * Ampang ke Seremban: RM1,354
      * KLIA ke Seremban: RM1,300
      * Ampang ke Port Dickson: RM1,420
      * KLIA ke Port Dickson: RM1,220
      * Ampang ke Rawang: RM850
      * KLIA ke Rawang: RM990
      * Ampang ke Bukit Beruntung: RM850
      * KLIA ke Bukit Beruntung: RM1,024
      * Ampang ke Kalumpang: RM989
      * KLIA ke Kalumpang: RM1,225
      * Ampang ke Tanjung Malim: RM1,010
      * KLIA ke Tanjung Malim: RM1,250
      * Ampang ke Kuala Klawang: RM1,250
      * KLIA ke Kuala Klawang: RM1,450
      * Ampang ke Sungai Gabai: RM900
      * Ampang ke Janda Baik: RM1,000
      * KLIA ke Janda Baik: RM1,470
      * Ampang ke Bukit Tinggi: RM1,000
      * KLIA ke Bukit Tinggi: RM1,470
      * Ampang ke Genting: RM1,000
      * KLIA ke Genting: RM1,219
      * Ampang ke Bentong: RM1,220
      * KLIA ke Bentong: RM1,480
      * Ampang ke Raub: RM1,310
      * KLIA ke Raub: RM1,850
    - CAJ MENUNGGU PEMANDU: Sekiranya pelanggan lewat/menunggu, caj sebanyak RM150 dikenakan untuk setiap jam pengantara[cite: 10].
    - DESTINASI DALAM PULAU (PULAU PINANG): Tambahan surcaj RM200 bagi destinasi dalam pulau (seperti Georgetown, Batu Ferringhi, Bayan Lepas, dll) untuk caj tol jambatan dan logistik pulau[cite: 1, 2].
    - STRICT GATEKEEPING PICKUP: Hanya terima lokasi pickup di Selangor, KL, Putrajaya/Cyberjaya/KLIA. Di luar kawasan, tolak dan beri link: https://wa.link/nrmesv[cite: 1, 2].
    - NO URGENT BOOKINGS: Tempahan online HANYA untuk tarikh 8 HARI DAN KE ATAS. Jika 7 hari ke bawah, tolak dan beri link: https://wa.link/nrmesv[cite: 1, 2].
    - FORMULA TWO-WAY:
      * Return pada HARI YANG SAMA: Tambah 50% dari harga One-Way (x1.5)[cite: 1, 2].
      * Return pada HARI BERBEZA (Bermalam): Tambah 100% dari harga One-Way (x2.0)[cite: 1, 2].
    - PEMBAYARAN: Deposit 50% wajib ke akaun CIMB (SHAHRIL BASRI LEISURE ENTERPRISE) untuk lock tarikh[cite: 1, 2].
    - LARANGAN KERAS: JANGAN SEKALI-KALI sebut harga asas, formula, kadar per km, atau pecahan kos kepada pelanggan[cite: 1, 2].
    - FORMAT JAWAPAN HARGA: Terus sebut laluan (pickup ke drop-off) dan harga akhir sahaja dengan ringkas (Contoh: "Untuk sewaan dari Ampang ke Tanjung Malim, anggaran harga adalah RM1,010")[cite: 1, 2].
    - WAJIB isi borang dulu SEBELUM bagi harga dan wajib isi semua detail untuk one way atau two way[cite: 1, 2].
    """

def get_zulfa_persona():
    """Mengembalikan profil perwatakan dan arahan sistem rasmi untuk Zulfa AI"""
    return """
ANDA ADALAH ZULFA: Pembantu Khidmat Pelanggan & Perunding Tempahan Rasmi bagi SHAHRIL BASRI LEISURE ENTERPRISE.
PERWATAKAN: Mesra, profesional, sopan, sangat ringkas, dan mematuhi SOP.
- Jawab soalan secara pendek dan ringkas.
- Sentiasa belajar dari semasa ke semasa untuk menambahbaik skill.
- JANGAN pandai-pandai buat harga sendiri, ikot pada sbleisure.engine dan sop.
"""

def validasi_pickup(lokasi):
    """
    Menyemak kelayakan zon pickup (Gatekeeping).
    Memulangkan tuple (sah: bool, harga_asas: float).
    """
    if not lokasi:
        return False, 0.0

    lokasi_clean = str(lokasi).strip().lower()
    kawasan_dibenarkan = [
        "selangor", "kuala lumpur", "kl", "putrajaya", "cyberjaya", "klia",
        "ampang", "cheras", "hulu langat", "batu", "setapak", "ulu kelang", "pusat bandar",
        "bukit bintang", "chow kit", "brickfields", "bangsar", "seputeh", "kepong", "segambut",
        "sentul", "jalan ipoh", "mont kiara", "sri hartamas", "batu caves", "wangsa maju",
        "danau kota", "taman melati", "semarak", "ampang hilir", "kampung pandan", "desa pandan",
        "maluri", "airport", "damansara", "petaling", "kajang", "semenyih", "rawang", "dengkil",
        "sepang", "labu", "bukit raja", "sungai buloh", "sg buloh", "beranang", "kapar", "klang",
        "bandar", "jugra", "kelanang", "morib", "tanjong duabelas", "telok panglima garang",
        "ampang pecah", "batang kali", "buloh telor", "kalumpang", "kerling", "kuala kalumpang",
        "peretak", "rasa", "serendah", "sungai gumut", "sungai tinggi", "ulu bernam", "ulu yam",
        "api-api", "batang berjuntai", "bestari jaya", "ijok", "jeram", "kuala selangor",
        "pasangan", "tanjong karang", "ujong pematang", "ulu tinggi", "bagan nakhoda omar",
        "panchang bedena", "pasiran panjang", "sabak", "sungai panjang"
    ]
    
    sah = any(k in lokasi_clean for k in kawasan_dibenarkan)
    harga_asas = dapatkan_harga_asas_destinasi(lokasi_clean) if sah else 0.0
    return sah, harga_asas

def dapatkan_harga_asas_destinasi(destinasi):
    """Menentukan harga asas (50 km pertama) berdasarkan zon mukim destinasi mengikut struktur baru"""
    dest = str(destinasi).strip().lower()
    
    # 1. ZON SELANGOR, KL, PUTRAJAYA, CYBERJAYA, KLIA (RM700)
    zon_selangor_kl = [
        "selangor", "kuala lumpur", "kl", "putrajaya", "cyberjaya", "klia", "airport",
        "ampang", "cheras", "hulu langat", "batu", "setapak", "ulu kelang", "pusat bandar",
        "bukit bintang", "chow kit", "brickfields", "bangsar", "seputeh", "kepong", "segambut",
        "sentul", "jalan ipoh", "mont kiara", "sri hartamas", "batu caves", "wangsa maju",
        "danau kota", "taman melati", "semarak", "ampang hilir", "kampung pandan", "desa pandan",
        "maluri", "damansara", "petaling", "kajang", "semenyih", "rawang", "dengkil",
        "sepang", "labu", "bukit raja", "sungai buloh", "sg buloh", "beranang", "kapar", "klang",
        "bandar", "jugra", "kelanang", "morib", "tanjong duabelas", "telok panglima garang",
        "ampang pecah", "batang kali", "buloh telor", "kalumpang", "kerling", "kuala kalumpang",
        "peretak", "rasa", "serendah", "sungai gumut", "sungai tinggi", "ulu bernam", "ulu yam",
        "api-api", "batang berjuntai", "bestari jaya", "ijok", "jeram", "kuala selangor",
        "pasangan", "tanjong karang", "ujong pematang", "ulu tinggi", "bagan nakhoda omar",
        "panchang bedena", "pasiran panjang", "sabak", "sungai panjang"
    ]
    if any(z in dest for z in zon_selangor_kl):
        return 700.00

    # 2. ZON BENTONG (PAHANG) - RM1200
    zon_pahang_1200 = [
        "bentong", "pelangai", "sabai", "janda baik"
    ]
    if any(z in dest for z in zon_pahang_1200):
        return 1200.00

    # 3. ZON RAUB (PAHANG) - RM1300
    zon_pahang_1300 = [
        "raub", "batu talam", "dong", "gali", "sega"
    ]
    if any(z in dest for z in zon_pahang_1300):
        return 1300.00

    # 4. ZON TEMERLOH, MARAN, JERANTUT, LIPIS (PAHANG) - RM1500
    zon_pahang_1500 = [
        "temerloh", "maran", "jerantut", "lipis",
        "bangau", "guai", "kerdau", "lebak", "mentakab", "pahang tua", "sanggang", "semantan", "songsang",
        "chenor", "kertau",
        "burau", "hulu cheka", "hulu temebling", "temebling", "kangkong", "kelola", "pedah", "pulau tawar",
        "batu yon", "cheka", "gua", "jelai", "kechau", "tanum"
    ]
    if any(z in dest for z in zon_pahang_1500):
        return 1500.00

    # 5. ZON KUANTAN, PEKAN, ROMPIN, CAMERON HIGHLANDS, BERA (PAHANG) & KELANTAN & TERENGGANU - RM1600
    zon_rm1600 = [
        "kelantan", "terengganu",
        "kota bharu", "pasir mas", "tumpat", "bachok", "pasir puteh", "machang", "tanah merah", "kuala krai", "gua musang", "jeli",
        "kuala terengganu", "kuala nerus", "kemaman", "dungun", "besut", "setiu", "marang", "hulu terengganu",
        "baung", "badang", "banggu", "lundang", "panji", "kemumin", "kubang kerian", "peringat", "salor", "sering", "kadok", "kota", "limbat", "pendek",
        "lubok jong", "rantau panjang", "chetok", "bunut susu", "apam", "tok uban", "repek",
        "geting", "jal besar", "morak", "pasir pekan", "pengkalan kubor", "tawang",
        "gunong", "jelawat", "tangok", "melawi",
        "bukit abal", "jeram", "limbongan", "padang pak amat", "semerak", "jeram perdah",
        "ulu sat", "labok", "pulai chondong", "temangan",
        "kusial", "jedok", "ulu kusial", "bukit panau",
        "dabong", "olak jerai", "mengkebang", "guchil",
        "galas", "bertam", "pulai", "chiku",
        "kuala balah", "air lanas",
        "atas tol", "batu buruk", "cabang tiga", "cendering", "gelugor kedai payang", "kepong", "losong", "manir", "paloh", "pulau duyong", "pulau rusa", "rengas", "serada",
        "batu rakit", "bukit tunggal", "gong badak", "pulau redang", "seberang takir",
        "cukai", "kijal", "pasir semut", "tebak", "teluk kalong", "binjai", "banggol", "cherating", "air puteh",
        "abang", "besul", "jerangau", "kuala dungun", "paka", "pasir raja", "sura", "ullu paka",
        "keruak", "kuala besut", "lubuk kertah", "pasir akar", "pelagat", "pangkalan nyireh", "tembila", "tenang",
        "chalok", "guntong", "hulu nerus", "merang", "pak kancil", "caluk",
        "alor limbat", "bukit payong", "jerong", "merchang", "rusila", "pulau kerengga",
        "hulu berang", "jenagor", "kenerong", "kuala telemong", "tersat", "telemong",
        "kuantan", "pekan", "rompin", "cameron highlands", "bera",
        "beserah", "kuala kuantan", "penor", "ulu kuantan", "sungai karang",
        "bebar", "langgar", "lepar", "penyor", "pulau manis", "pulau rusa", "temai",
        "endau", "keratong", "tioman",
        "ringlet", "tanah rata", "ulu telom",
        "kemayan"
    ]
    if any(z in dest for z in zon_rm1600):
        return 1600.00

    # 6. ZON MELAKA & NEGERI SEMBILAN (RM1200)
    zon_melaka_ns = [
        "melaka tengah", "alor gajah", "jasin", "seremban", "port dickson", "rembau", 
        "kuala pilah", "jelebu", "jempol", "tampin",
        "alai", "ayer molek", "bachang", "balai panjang", "batu berendam", "bukit baru", 
        "bukit katil", "bukit piatu", "bukit rambai", "cheng", "duyong", "kandang", 
        "klebang besar", "klebang kecil", "krubong", "limbongan", "paya rumput", "peringgit", 
        "pernu", "semabok", "sungai baru", "sungai udang", "tangga batu", "tanjung kling", 
        "telok mas", "ujong pasir", "bertam", "padang temu", "kelewang", "ayer pa'abas", 
        "batang melaka", "belimbing", "bukit milin", "brisu", "durian tunggal", "gadek", 
        "jelatang", "kelemak", "kuala sungai baru", "kundor", "lendu", "lubok china", 
        "machap", "melekek", "padang sebang", "pegoh", "pulau sebang", "ramuan china besar", 
        "ramuan china kecil", "rembia", "sungai buloh", "taboh naning", "tampin linggi", 
        "tanjung rimau", "tebong", "tiga muka", "ayer limau", "londang", "solok", "jelai", 
        "asahan", "ayer panas", "bemban", "chohong", "chin-chin", "jus", "kesang", 
        "merlimau", "nyalas", "panchor", "rim", "sebak", "selandar", "serkam", "sebatu", 
        "tehel", "kesang pajak", "chinchin", "tedong", "lipat kajang", "ampangan", "labu", 
        "lenggeng", "pantai", "rantau", "rasah", "setul", "jimah", "linggi", "pasir panjang", 
        "si rusa", "batu kikir", "chembong", "gadong", "kota", "legong hilir", 
        "legong hulu", "mambau", "nerasau", "pedas", "pilin", "seberang", "titian bintangor", 
        "batu hampar", "gadong hilir", "ampang tinggi", "johol", "juasseh", "kepis", 
        "langkap", "seri menanti", "ulu jempol", "terachi", "parit tinggi", 
        "glami lemi", "hulu klawang", "klawang", "pertang", "peradong", "kenaboi", 
        "triang hilir", "ulu triang", "serting ilir", "serting hulu", "palong", "ayer kuning", 
        "gemencheh", "gemas", "ladang", "tampin tengah"
    ]
    if any(z in dest for z in zon_melaka_ns):
        return 1200.00

    # 7. ZON PERAK (RM1200)
    zon_perak = [
        "kinta", "larut", "matang", "selama", "manjung", "batang padang", "hilir perak", 
        "kerian", "hulu perak", "kuala kangsar", "bagan datuk", "muallim", "kampar",
        "hulu kinta", "tanjong rambutan", "sungai terap", "belanja", "asam kumbang", 
        "batu kurau", "bukit gantang", "jebong", "kamunting", "pengkalan aor", "selama", 
        "sungai limau", "taiping", "trong", "beruas", "dindings", "lumut", "sitiawan", 
        "bidor", "chenderiang", "padang rengas", "sungkai", "slim", "bagan datok", 
        "changkat jong", "durian sebatang", "labu kubong", "rungkup", "teluk anson", 
        "bagan serai", "gunong semanggol", "kuala kurau", "parit buntar", "selinsing", 
        "tanjung piandang", "belum", "gerik", "kenering", "lenggong", "pengkalan hulu", 
        "temengor", "chenderoh", "kota lama kiri", "kota lama kanan", "lubok merbau", 
        "pulau kamiri", "saiong", "sayong", "sungei siput", "hutan melintang", "behrang", 
        "ulu bernam barat", "teja", "gopeng"
    ]
    if any(z in dest for z in zon_perak):
        return 1200.00

    # 8. ZON LUAR PULAU (PULAU PINANG - SEBERANG PERAI UTARA, TENGAH, SELATAN): RM1300
    zon_pp_luar = ["seberang perai", "butterworth", "kepala batas", "tasek gelugor", "bukit mertajam", "perai", "seberang jaya", "nibong tebal", "sungai bakap", "batu kawan"]
    if any(z in dest for z in zon_pp_luar):
        return 1300.00

    # 9. ZON DALAM PULAU (PULAU PINANG - TIMUR LAUT, BARAT DAYA): RM1400
    zon_pp_dalam = ["timur laut", "barat daya", "georgetown", "george town", "batu ferringhi", "bayan lepas", "balik pulau", "batu maung", "jelutong", "ayer itam"]
    if any(z in dest for z in zon_pp_dalam):
        return 1400.00

    # 10. ZON JOHOR, PERLIS & KEDAH: RM1500
    zon_johor_perlis_kedah = [
        "johor", "perlis", "kedah", "johor bahru", "muar", "batu pahat", "kluang", "kulai", 
        "pontian", "segamat", "kota tinggi", "mersing", "tangkak", "arau", "abi", "chuping", 
        "jejawi", "kangar", "kayang", "kuala perlis", "kurong anai", "kurong batang", "oran", 
        "padang pauh", "padang siding", "paya", "sanglang", "sena", "seriab", "simpangan", 
        "simpang empat", "utan aji", "wang bintong", "titi tinggi", "beseri", "guar sanji", 
        "pauh", "kota setar", "kubang pasu", "langkawi", "padang terap", "kuala muda", "yan", 
        "pendang", "sik", "baling", "kulim", "bandar baharu", "pokok sena", "plentong", 
        "pulai", "senai", "tebrau", "tanjung kupang", "bakri", "bukit kepong", "jorak", 
        "lenga", "parit menangis", "parit jawa", "raya", "seri menanti", "sungai raya", 
        "sungai terap", "kesang", "bagan", "chaah", "kampung bahru", "linau", "minyak beku", 
        "peserai", "pt. raja", "pt. sulong", "rengit", "simpang kanan", "simpang kiri", 
        "sri gading", "tanjung semberong", "sungai punggor", "kahang", "layang-layang", 
        "machap", "nyior", "paloh", "renggam", "ulu benut", "sedenak", "bukit batu", 
        "api-api", "ayer baloi", "benut", "jeram batu", "karangan", "rimba terjun", 
        "serkat", "sungai karang", "penerok", "pulai sebatang", "bekok", "jabi", "jementah", 
        "pogoh", "sermin", "buloh kasap", "labis", "sungai segamat", "johor lama", "kambau", 
        "lenik", "pengerang", "desaru", "sedili besar", "sedili kecil", "semanggar", 
        "sungai papan", "ulu sungai johor", "tenglu", "triang", "penyabong", "jemaluang", 
        "padang endau", "pulau tinggi", "pulau sibu", "pulau aur", "pulau pemanggil", 
        "bukit serampang", "grisek", "kundang", "serom",
        "alor malai", "alor setar", "anak bukit", "derga", "gunong", "kangkong", "kubang rotan", 
        "langgar", "lepai", "limbong", "mergong", "pengkalan kundor", "sala kechil", "tajar", 
        "telok kechai", "tebengau", "ah", "asun", "bukit lada", "hosba", "jitra", "jerlun", 
        "kepayang", "kubang pasu", "malau", "naga", "padang perahu", "pering", "pelubang", 
        "tunjang", "temin", "ayer hangat", "bohor", "kedawang", "kuah", "padang matsirat", 
        "temonyong", "batang perahu", "belimbing kanan", "belimbing kiri", "kurong appendang", 
        "naka", "padang terap kanan", "padang terap kiri", "pedu", "tekai", "tualak", "bujang", 
        "gurun", "kuala merbok", "merbok", "muda", "pekan bujang", "petani", "pinang tunggal", 
        "semeling", "sidam kanan", "sungai petani", "teloi kanan", "dulang", "sala besar", 
        "singkir", "yan", "ayer puteh", "bukit panchor", "guar kepayang", "kubur panjang", 
        "padang peliang", "padang kerbau", "pendang", "tob keling", "jeneri", "kalai", "sik", 
        "sok", "bakai", "kupang", "puli", "siong", "tawar", "bagan sena", "lunas", "mahang", 
        "nesa", "padang meha", "sedim", "sungai seluang", "terap", "bagan samak", "bandar baharu", 
        "permatang pasir", "relau", "serdang", "bukit payong", "derang", "lesong", "tualang"
    ]
    if any(z in dest for z in zon_johor_perlis_kedah):
        return 1500.00

    return 700.00

# Jadual Harga Tetap Laluan Popular (Override)
JADUAL_HARGA_BAS_TETAP = {
    ("ampang", "kajang"): 850,
    ("klia", "kajang"): 850,
    ("ampang", "semenyih"): 850,
    ("klia", "semenyih"): 970,
    ("ampang", "seremban"): 1354,
    ("klia", "seremban"): 1300,
    ("ampang", "port dickson"): 1420,
    ("klia", "port dickson"): 1220,
    ("ampang", "rawang"): 850,
    ("klia", "rawang"): 990,
    ("ampang", "bukit beruntung"): 850,
    ("klia", "bukit beruntung"): 1024,
    ("ampang", "kalumpang"): 989,
    ("klia", "kalumpang"): 1225,
    ("ampang", "tanjung malim"): 1010,
    ("klia", "tanjung malim"): 1250,
    ("ampang", "kuala klawang"): 1250,
    ("klia", "kuala klawang"): 1450,
    ("ampang", "sungai gabai"): 900,
    ("ampang", "janda baik"): 1000,
    ("klia", "janda baik"): 1470,
    ("ampang", "bukit tinggi"): 1000,
    ("klia", "bukit tinggi"): 1470,
    ("ampang", "genting"): 1000,
    ("klia", "genting"): 1219,
    ("ampang", "bentong"): 1220,
    ("klia", "bentong"): 1480,
    ("ampang", "raub"): 1310,
    ("klia", "raub"): 1850,
}

def semak_jadual_tetap(pickup, dest):
    """Semakan fleksibel dua hala untuk jadual harga tetap."""
    p = pickup.strip().lower()
    d = dest.strip().lower()

    for (asal, tuju), harga in JADUAL_HARGA_BAS_TETAP.items():
        if (asal in p and tuju in d) or (tuju in p and asal in d):
            return float(harga)
    return None

def semak_kawasan_dalam_pulau_pinang(destinasi):
    """
    Mengesan sama ada destinasi berada di bahagian dalam pulau (Pulau Pinang)
    untuk caj tambahan tol jambatan / kesesakan bandar & logistik pulau (+RM200)[cite: 1, 2].
    """
    dest = str(destinasi).strip().lower()
    kawasan_pulau = [
        "georgetown", "george town", "batu ferringhi", "bayan lepas", 
        "bayan baru", "tanjung bungah", "tanjung tokoh", "teluk bahang", 
        "air itam", "ayer itam", "gelugor", "jelutong", "gurney", 
        "pulau pinang (pulau)", "penang island"
    ]
    return any(k in dest for k in kawasan_pulau)

def dapatkan_jarak_km(lokasi_asal, lokasi_tuju):
    """Mendapatkan jarak pemanduan sebenar (km) menggunakan OpenStreetMap / OSRM"""
    try:
        headers = {'User-Agent': 'SBLTransportApp/1.0'}
        url_asal = f"https://nominatim.openstreetmap.org/search?q={lokasi_asal},Malaysia&format=json&limit=1"
        url_tuju = f"https://nominatim.openstreetmap.org/search?q={lokasi_tuju},Malaysia&format=json&limit=1"
        
        res_asal = requests.get(url_asal, headers=headers, timeout=4).json()
        res_tuju = requests.get(url_tuju, headers=headers, timeout=4).json()
        
        if not res_asal or not res_tuju:
            return None
            
        lon1, lat1 = res_asal[0]['lon'], res_asal[0]['lat']
        lon2, lat2 = res_tuju[0]['lon'], res_tuju[0]['lat']
        
        osrm_url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=false"
        osrm_res = requests.get(osrm_url, timeout=4).json()
        
        if osrm_res.get('routes'):
            jarak_meter = osrm_res['routes'][0]['distance']
            return round(jarak_meter / 1000.0, 1)
    except Exception:
        return None
    return None

def bundar_ke_puluhan_atas(nilai):
    return math.ceil(nilai / 10.0) * 10

def kira_harga_bas(lokasi_pickup, destinasi, jarak_km=None, tier_jalan="normal"):
    """
    Mengira harga One-Way:
    1. Semak jadual harga tetap laluan dahulu.
    2. Jika tiada, gunakan harga asas zon destinasi (50 km pertama) + lebihan jarak (51 km ke atas) pada kadar RM3.60/km.
    3. Tambah surcaj khas RM200 jika destinasi masuk ke bahagian dalam pulau (Pulau Pinang)[cite: 1, 2].
    """
    pickup = str(lokasi_pickup).strip().lower()
    dest = str(destinasi).strip().lower()
    
    # 1. Semak Jadual Tetap
    harga_tetap = semak_jadual_tetap(pickup, dest)
    if harga_tetap is not None:
        jumlah_harga = harga_tetap
    else:
        # 2. Dapatkan Harga Asas daripada Zon Destinasi (50 km pertama)
        harga_asas = dapatkan_harga_asas_destinasi(dest)
            
        # 3. Dapatkan Jarak Sebenar jika tidak dibekalkan
        if jarak_km is None or jarak_km <= 0:
            jarak_dikesan = dapatkan_jarak_km(pickup, dest)
            jarak_km = jarak_dikesan if jarak_dikesan else 80.0
            
        # 4. Kadar Lebihan KM diseragamkan kepada RM3.60 untuk semua kawasan
        kadar_km = 3.60
            
        caj_jarak = (jarak_km - 50) * kadar_km if jarak_km > 50 else 0
        jumlah_harga = harga_asas + caj_jarak

    # 5. Surcaj Khas Bahagian Dalam Pulau (Pulau Pinang) +RM200[cite: 1, 2]
    if semak_kawasan_dalam_pulau_pinang(dest):
        jumlah_harga += 200.00
    
    # 6. Surcaj Muka Bumi (Tier Jalan)
    if tier_jalan in ["berbukit", "sempit", "pedalaman"]:
        jumlah_harga *= 1.15
        
    return float(bundar_ke_puluhan_atas(jumlah_harga))

def kira_harga_trip(lokasi_pickup, destinasi, jenis_trip="one_way", return_hari_sama=True, jarak_km=None, tier_jalan="normal"):
    """
    Mengira harga trip penuh mengikut jenis sewaan:
    - One-Way: 100% harga sehala[cite: 1, 2]
    - Two-Way Return Hari Sama: +50% (x1.5)[cite: 1, 2]
    - Two-Way Return Hari Berbeza (Bermalam): +100% (x2.0)[cite: 1, 2]
    """
    harga_one_way = kira_harga_bas(lokasi_pickup, destinasi, jarak_km=jarak_km, tier_jalan=tier_jalan)
    
    trip = str(jenis_trip).strip().lower()
    if trip in ["two_way", "two way", "pergi balik", "return"]:
        if return_hari_sama:
            jumlah_two_way = harga_one_way * 1.5
        else:
            jumlah_two_way = harga_one_way * 2.0
        return float(bundar_ke_puluhan_atas(jumlah_two_way))
        
    return float(harga_one_way)

def semak_tarikh_booking(tarikh_str):
    """Menyemak sama ada tarikh tempahan melepasi sekatan tempahan tergesa-gesa (>= 8 hari)[cite: 1, 2]"""
    try:
        tarikh_bersih = tarikh_str.strip()
        if '-' in tarikh_bersih and len(tarikh_bersih.split('-')[0]) == 4:
            tarikh_booking = datetime.strptime(tarikh_bersih, "%Y-%m-%d").date()
        else:
            tarikh_booking = datetime.strptime(tarikh_bersih, "%d-%m-%Y").date()
        
        tarikh_semasa = datetime.now().date()
        selisih_hari = (tarikh_booking - tarikh_semasa).days
        
        if selisih_hari < 0:
            return "tidak_sah", "Tarikh yang dipilih sudah lepas."
        elif selisih_hari <= 7:
            return "urgent", "Maaf, untuk tempahan dalam masa 7 hari atau kurang (urgent booking), sistem tidak boleh terima. Sila berhubung terus dengan sales team kami di pautan ini: https://wa.link/nrmesv"
        else:
            return "boleh", "Tarikh disahkan lulus untuk tempahan online."
    except ValueError:
        return "ralat", "Format tarikh tidak sah. Sila guna format YYYY-MM-DD atau DD-MM-YYYY."

def dapatkan_harga_automatik(pickup, destinasi, jenis_trip="one_way", return_hari_sama=True, tier_jalan="normal"):
    """Fungsi pembantu utama untuk mendapatkan harga automatik One-Way atau Two-Way"""
    return kira_harga_trip(lokasi_pickup, destinasi, jenis_trip=jenis_trip, return_hari_sama=return_hari_sama, jarak_km=None, tier_jalan=tier_jalan)