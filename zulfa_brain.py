# ==========================================
# FAIL: zulfa_brain.py (DIKEMASKINI)
# MODUL UTAMA OTAK AI ZULFA (GEMINI)
# ==========================================
import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

import tempat_menarik
import info_jalan
import sbleisure_profile
import sop_payment
import sbleisure_engine

# Konfigurasi Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

load_dotenv()

# Setup Client Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

# Pangkalan Data Memori Pelanggan (JSON)
MEMORY_FILE = "zulfa_customers_memory.json"

# ==========================================
# 1. PENGURUSAN MEMORI PELANGGAN
# ==========================================

def muat_memori():
    """Membaca rekod memori pelanggan dari fail JSON."""
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Ralat membaca fail memori: {e}")
            return {}
    return {}

def simpan_memori(data):
    """Menyimpan rekod memori pelanggan ke fail JSON."""
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logging.error(f"Ralat menyimpan fail memori: {e}")

def dapatkan_konteks_pelanggan(no_telefon):
    """Mengambil konteks atau sejarah perbualan pelanggan berdasarkan nombor telefon."""
    memori = muat_memori()
    return memori.get(no_telefon, {
        "nama": "",
        "status_tempahan": "baru",
        "sejarah_mesej": []
    })

def kemaskini_konteks_pelanggan(no_telefon, mesej_user, mesej_zulfa, nama=None):
    """Menyimpan perbualan baharu ke dalam memori pelanggan."""
    memori = muat_memori()
    if no_telefon not in memori:
        memori[no_telefon] = {
            "nama": nama or "",
            "status_tempahan": "baru",
            "sejarah_mesej": []
        }
    
    if nama:
        memori[no_telefon]["nama"] = nama

    sejarah = memori[no_telefon]["sejarah_mesej"]
    sejarah.append({"role": "user", "content": mesej_user, "timestamp": datetime.now().isoformat()})
    sejarah.append({"role": "assistant", "content": mesej_zulfa, "timestamp": datetime.now().isoformat()})
    
    if len(sejarah) > 20:  
        sejarah = sejarah[-20:]
        
    memori[no_telefon]["sejarah_mesej"] = sejarah
    simpan_memori(memori)

# ==========================================
# 2. SYSTEM INSTRUCTION & INTEGRASI GEMINI
# ==========================================

def get_zulfa_persona():
    return "ANDA ADALAH ZULFA: Pembantu Khidmat Pelanggan & Perunding Tempahan Rasmi bagi SHAHRIL BASRI LEISURE ENTERPRISE. PERWATAKAN: Mesra, profesional, sopan, namun SANGAT TEGAS dalam mematuhi SOP syarikat. PANDUAN PENILAIAN INFRASTRUKTUR & TIER JALAN: Apabila pelanggan memberikan destinasi, nilai bentuk mukabumi dan laluan secara bijak (JALAN BERBUKIT: kawasan tinggi/pendakian; JALAN SEMPIT: perkampungan pedalaman/chalet tepi sungai; JALAN NORMAL: lebuh raya/bandar). Caj tambahan 15% hanya untuk Berbukit & Sempit. Jangan beritahu formula kepada pelanggan."

def bina_system_instruction():
    """Membina System Instruction dinamik daripada pelbagai modul tempatan."""
    profil_text = sbleisure_profile.get_profile_text() if hasattr(sbleisure_profile, 'get_profile_text') else ""
    sop_text = sop_payment.get_sop_text() if hasattr(sop_payment, 'get_sop_text') else ""
    engine_rules = sbleisure_engine.get_engine_rules_text() if hasattr(sbleisure_engine, 'get_engine_rules_text') else ""
    persona_text = get_zulfa_persona()

    admin_notes = ""
    if os.path.exists("admin_memory.txt"):
        with open("admin_memory.txt", "r", encoding="utf-8") as f:
            admin_notes = f.read()

    arahan_khas_portal = ""
    if os.path.exists("custom_instructions.txt"):
        with open("custom_instructions.txt", "r", encoding="utf-8") as f:
            arahan_khas_portal = f.read()

    try:
        import pytz
        tz_malaysia = pytz.timezone('Asia/Kuala_Lumpur')
        sekarang = datetime.now(tz_malaysia)
    except Exception:
        sekarang = datetime.now()

    hari_ini = sekarang.strftime('%A') 
    jam_semasa = sekarang.strftime('%H:%M')
    angka_hari = sekarang.weekday() 
    jam_angka = sekarang.hour

    is_waktu_pejabat = True
    if angka_hari >= 5: 
        is_waktu_pejabat = False
    elif jam_angka < 8 or jam_angka >= 17: 
        is_waktu_pejabat = False

    status_waktu = "DALAM WAKTU PEJABAT (Isnin-Jumaat, 8pg-5ptg)" if is_waktu_pejabat else "DI LUAR WAKTU PEJABAT / CUTI (Sabtu/Ahad atau selepas 5ptg)"

    system_prompt = f"""
    Nama anda ialah zulfa, Pegawai Khidmat Pelanggan dari SB Leisure Transport.
    Tugas utama anda ialah membantu pelanggan membuat sewaan bas, menjawab pertanyaan harga, dan memberikan khidmat pelanggan yang mesra, sopan, dan profesional.

    === STATUS MASA SEMASA (REAL-TIME) ===
    - Hari & Masa: {hari_ini}, {jam_semasa} (Waktu Malaysia)
    - Status: {status_waktu}

    === MAKLUMAT SYARIKAT & PROFIL ===
    {profil_text}

    === SOP PEMBAYARAN & REKOD ===
    {sop_text}

    === PERATURAN & ENJIN PENGIRAAN HARGA ===
    {engine_rules}

    === PERSONA & PANDUAN PENILAIAN ===
    {persona_text}
    
    === PANDUAN NADA & PERILAKU ===
    1. Anda Zulfa. Balas dalam bahasa Melayu Malaysia yang mesra, sopan, natural dan ringkas untuk WhatsApp. Elakkan jawapan berjela atau skrip jualan yang tidak berkaitan.
    2. Kenal pasti soalan terkini dan fakta dalam sejarah dahulu. Jawab soalan pelanggan sebelum memulakan proses tempahan. Jika sekadar salam, tanya apa yang diperlukan. Jika kabur, tanya SATU soalan penjelasan khusus.
    3. Jangan ulang jawapan atau soalan terdahulu. Jangan minta semula jenis kenderaan, jenis trip atau butiran lain yang sudah diberikan. Tanya hanya maklumat yang masih kurang; jika soalan diulang, jawab secara relevan dan ringkas.
    4. Tempahan online hanya untuk bas. Untuk Van, MPV, SUV atau pakej Tour, arahkan kepada sales team: https://wa.link/nrmesv.
    5. Untuk sewaan bas, apabila pelanggan sudah memilih one way atau two way, berikan borang yang sepadan SEKALI sahaja. Gunakan jawapan yang sudah diberi dan jangan hantar semula borang lengkap jika hanya beberapa butiran kurang.
    6. Jawab soalan umum tanpa memaksa borang. Sebelum sebut harga, pastikan borang lengkap termasuk pickup, destinasi, tarikh pergi, tarikh balik jika dua hala dan jumlah pax; patuhi enjin harga di atas. Jangan teka atau ubah harga. Jika pelanggan mahu tawar-menawar, arahkan kepada sales team: https://wa.link/nrmesv.
    7. Jika pelanggan bersedia membayar, tanya pilihan QR DuitNow atau Online Banking (https://toyyibpay.com/sbl-online) dan Deposit 50% atau Bayaran Penuh. Ikut SOP pembayaran di atas sebelum memberikan butiran bayaran.
    8. Jika pelanggan semak tempahan sedia ada, gunakan sejarah yang tersedia; jangan reka status. Jika meminta gambar kenderaan, rujuk https://www.facebook.com/sewabaspersiaranmurah.
    
    === NOTA KHAS & ARAHAN TERKINI DARIPADA ADMIN ===
    {admin_notes}

    === ARAHAN KHAS TAMBAHAN DARI PORTAL SETTING ===
    {arahan_khas_portal}

    === BORANG ONE WAY ===
    Terima kasih kerana berminat dengan perkhidmatan sewaan Mpv/Van/Bas persiaran   
    *SB Leisure* 🚎

    ➡️Mohon Tuan/Puan isi :

    📝BORANG MAKLUMAT SEWAAN

    Syarikat : 
    Alamat : 

    Nama : 
    No. tel : 
    Tarikh : 
    Masa : 
    Pick-up point : 
    Drop-off point : 
    Pax : 

    ➡️Jenis sewaan (Mpv/Van/Bas) : BAS

    📌HARGA SEWAAN TERTAKLUK KEPADA JARAK DAN MASA PERJALANAN YANG DIBERIKAN📍

    T.KASIH 😊

    === BORANG TWO WAY ===

    Terima kasih kerana berminat dengan perkhidmatan sewaan Mpv/Van/Bas persiaran
    🚎 *SB Leisure* 🚎

    ➡️Mohon Tuan/Puan isi :

    📝BORANG MAKLUMAT SEWAAN

    Syarikat : 
    Alamat : 

    Nama : 
    No. tel : 
    Tarikh : 
    Masa : 
    Pick-up point : 
    Drop-off point : 
    Pax : 

    ➡️Jenis sewaan (Mpv/Van/Bas) : 

    🔄Maklumat untuk RETURN trip :-

    Tarikh : 
    Masa : 
    Pick-up point : 
    Drop-off point : 
    Pax : 

    📌HARGA SEWAAN TERTAKLUK KEPADA JARAK DAN MASA PERJALANAN YANG DIBERIKAN📍

    T.KASIH 😊
    """
    return system_prompt

def proses_mesej(no_telefon, mesej_user, nama_pelanggan=None):
    """Menerima mesej daripada pelanggan dan memulangkan respons Zulfa menggunakan Gemini."""
    if not client:
        return "Ralat: GEMINI_API_KEY tidak dikonfigurasikan dengan betul."

    # 1. Dapatkan sejarah perbualan pelanggan
    data_pelanggan = dapatkan_konteks_pelanggan(no_telefon)
    sejarah = data_pelanggan.get("sejarah_mesej", [])

    # 2. Bina pesanan perbualan untuk Gemini API
    contents = []
    for h in sejarah:
        contents.append(types.Content(
            role="model" if h["role"] in ("assistant", "model") else "user",
            parts=[types.Part.from_text(text=h["content"])]
        ))
    
    contents.append(types.Content(
        role="user",
        parts=[types.Part.from_text(text=mesej_user)]
    ))

    # 3. Tetapkan Konfigurasi LLM
    system_instruction = bina_system_instruction()
    jawapan_terakhir = next((h["content"] for h in reversed(sejarah) if h.get("role") in ("assistant", "model")), "")
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.3,
        max_output_tokens=1000
    )

    try:
        # 4. Panggil model Gemini
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=contents,
            config=config
        )
        
        jawapan_zulfa = (response.text or "").strip()
        if jawapan_zulfa and jawapan_terakhir and jawapan_zulfa.casefold() == jawapan_terakhir.strip().casefold():
            # Regenerate once using the same context; do not expose the internal correction.
            pembetulan = contents + [
                types.Content(role="model", parts=[types.Part.from_text(text=jawapan_zulfa)]),
                types.Content(role="user", parts=[types.Part.from_text(
                    text="Jawapan draf itu mengulang jawapan terdahulu. Jawab soalan terkini secara khusus dan ringkas. Jangan ulang soalan atau minta maklumat yang telah diberi. Jika tiada perkara baru untuk ditambah, nyatakan secara ringkas bahawa maklumat sudah diberikan.")]),
            ]
            response = client.models.generate_content(model="gemini-3.5-flash-lite", contents=pembetulan, config=config)
            jawapan_zulfa = (response.text or "").strip()
        if not jawapan_zulfa or (jawapan_terakhir and jawapan_zulfa.casefold() == jawapan_terakhir.strip().casefold()):
            jawapan_zulfa = "Saya dah kongsikan maklumat itu tadi. Jika ada perkara lain yang ingin disemak, boleh beritahu saya."

        # 5. Kemaskini memori perbualan
        kemaskini_konteks_pelanggan(no_telefon, mesej_user, jawapan_zulfa, nama=nama_pelanggan)

        return jawapan_zulfa

    except Exception as e:
        logging.error(f"Ralat semasa memproses mesej Gemini: {e}")
        return "Maaf, sistem mengalami sedikit gangguan teknikal. Sila cuba sebentar lagi atau hubungi pegawai kami."

def jana_jawapan(no_telefon, mesej_user, nama_pelanggan=None):
    """Alias fungsi untuk keserasian dengan app.py"""
    return proses_mesej(no_telefon, mesej_user, nama_pelanggan=nama_pelanggan)