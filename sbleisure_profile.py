# ==========================================
# FILE: sbleisure_profile.py
# Modul Profil Syarikat SBLEISURE
# ==========================================

def get_company_identity():
    """Mengembalikan maklumat rasmi identiti dan pendaftaran syarikat SBLeisure Transport."""
    profile = {
        "nama_jenama": "SBLeisure Transport",
        "nama_syarikat": "Shahril Basri Leisure Enterprise (SBLeisure Transport)",
        "ssm_no": "202203168334 (003413019-W)",
        "tahun_mula_operasi": 2017,
        "tahun_daftar_ssm": 2022,
        "alamat": "No. 8-1, 9-1, First Floor, Laman Niaga@Ampang Waterfront, Jalan AWF 3A, Ampang Waterfront, 68000, Ampang, Selangor",
        "google_maps": "https://maps.app.goo.gl/jSJHUNXjZdhiLDRbA",
        "emel": "sbltransport.my@gmail.com",
        "telefon": ["013-243 4200", "016-260 1885"],
        "facebook": "https://www.facebook.com/sewabaspersiaranmurah",
        "whatsapp_sales": "https://wa.link/nrmesv"
    }
    return profile

def get_payment_link():
    """Mengembalikan maklumat akaun bank rasmi untuk urusan deposit/pembayaran."""
    payment_info = {
        "bank": "CIMB Bank Berhad",
        "no_akaun": "860 5247 780",
        "nama_pemegang_akaun": "Shahril Basri Leisure Enterprise",
        "toyyibpay": "https://toyyibpay.com/sbl-online"
    }
    return payment_info

def get_fleet_and_services():
    """Senarai kenderaan dan perkhidmatan pengangkutan yang ditawarkan."""
    services = {
        "kenderaan": [
            "Bas Persiaran (44 Seater / Executive)",
            "Van Persiaran (Hiace / Urvan)",
            "MPV Mewah (Toyota Vellfire, Innova)",
            "Van Bagasi & Lori Logistik"
        ],
        "cakupan": "Seluruh Semenanjung Malaysia serta perjalanan rentas sempadan ke Singapura dan Thailand",
        "kategori_pelanggan": [
            "Sektor Korporat",
            "Agensi Kerajaan & Kementerian",
            "Institusi Pendidikan (Sekolah / IPTA / IPTS)",
            "Pelanggan Individu, Rombongan Keluarga & Perkahwinan"
        ]
    }
    return services

def get_experience_and_clients():
    """Rekod pengalaman dan senarai klien utama syarikat."""
    experience = {
        "klien_kerajaan": [
            "Jabatan Muzium Malaysia",
            "Kementerian Pendidikan Malaysia (KPM)",
            "Kementerian Dalam Negeri (KDN)",
            "Akademi Binaan Malaysia (ABM)"
        ],
        "pengkhususan_khas": [
            "Sokongan logistik ketenteraan (Operasi MALBATT)",
            "Pengangkutan persidangan, seminar, dan delegasi rasmi"
        ]
    }
    return experience

def get_profile_text():
    """Menggabungkan maklumat profil menjadi teks ringkas untuk rujukan konteks Zulfa AI."""
    p = get_company_identity()
    f = get_fleet_and_services()
    e = get_experience_and_clients()
    b = get_payment_link()
    
    return f"""
    Nama Jenama: {p['nama_jenama']}
    Nama Pendaftaran: {p['nama_syarikat']}
    No. Pendaftaran SSM: {p['ssm_no']}
    Alamat Pejabat Operasi: {p['alamat']}
    Pautan Lokasi Peta: {p['google_maps']}
    Talian Hotline/WhatsApp: {', '.join(p['telefon'])}
    Emel Rasmi: {p['emel']}
    Facebook: {p['facebook']}
    Pautan WhatsApp Sales: {p['whatsapp_sales']}
    
    Fleet Kenderaan: {', '.join(f['kenderaan'])}
    Kawasan Liputan: {f['cakupan']}
    Klien Utama: {', '.join(e['klien_kerajaan'])}
    Akaun Bank Rasmi: {b['bank']} - {b['no_akaun']} ({b['nama_pemegang_akaun']})
    """