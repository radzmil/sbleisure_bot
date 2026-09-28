# ==========================================
# FAIL: sop_payment.py
# MODUL SOP PAYMENT, TERMA SYARAT & NOTIFIKASI
# ==========================================
import os
import smtplib
import logging
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

GROUP_ADMIN_NUMBER = os.getenv("GROUP_ADMIN_NUMBER", "601123687357")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "radzmil@gmail.com")
TOYYIBPAY_LINK = "https://toyyibpay.com/sbl-online"
QR_CODE_DIRECT_LINK = "https://i.ibb.co/YTP80GLk/Whats-App-Image-2026-08-19-at-9-27-28-PM.jpg"

def get_sop_text():
    """Mengembalikan teks lengkap polisi & SOP pembayaran untuk rujukan model AI."""
    return """
SOP & POLISI PEMBAYARAN (SBLeisure Transport):

1. STRUKTUR & CARA PEMBAYARAN:
- Pilihan Pembayaran: Pelanggan boleh memilih sama ada membuat Deposit 50% atau Bayaran Penuh (Full Payment).
- Kaedah 1 (QR Code DuitNow): Imbas kod QR CIMB rasmi SHAHRIL BASRI LEISURE ENTERPRISE. 
  * PENTING: Sila letakkan nombor telefon pelanggan sebagai Rujukan / Ref semasa membuat transaksi pemindahan online.
- Kaedah 2 (Online Banking ToyyibPay): Pautan rasmi https://toyyibpay.com/sbl-online.
- Baki 50% (jika pilih deposit): Wajib dijelaskan sekurang-kurangnya 2 hari sebelum tarikh perjalanan.

2. POLISI PEMBATALAN OLEH PELANGGAN:
- Lebih 14 hari sebelum tarikh perjalanan: Refund 90% daripada deposit (10% yuran pentadbiran).
- 7 hingga 14 hari sebelum tarikh perjalanan: Refund 50% daripada deposit.
- Kurang daripada 2 hari (<2 hari): Deposit hangus 100%.
- Gagal melunaskan baki 2 hari sebelum trip: Tempahan terbatal secara automatik dan deposit hangus.

3. POLISI PENUNDAAN TARIKH (POSTPONEMENT):
- Dibenarkan 1 kali dengan notis minimum 7 hari sebelum tarikh asal.
- Caj penundaan RM200 dikenakan jika notis kurang 7 hari.

4. PEMBATALAN OLEH PIHAK SYARIKAT:
- Bayaran dikembalikan 100% penuh dalam tempoh 7 hari bekerja.
"""

def get_sop_payment_text():
    """Alias tambahan bagi mengekalkan keserasian modul lama."""
    return get_sop_text()

def paparkan_terma_pembayaran_ringkas():
    """Teks ringkas untuk dihantar terus ke pelanggan dalam WhatsApp."""
    return (
        "**RINGKASAN POLISI PEMBAYARAN & DEPOSIT**\n\n"
        "• **Pilihan Bayaran**: Deposit 50% atau Bayaran Penuh (Full Payment).\n"
        "• **Kaedah Bayaran**: QR Code DuitNow CIMB atau ToyyibPay.\n"
        "• **Rujukan Pemindahan (Ref)**: Sila letak **nombor telefon** anda.\n"
        "• **Baki Bayaran**: Dijelaskan selewat-lewatnya 2 hari sebelum perjalanan.\n\n"
        "Sila balas **'Setuju'** untuk meneruskan pengesahan tempahan anda."
    )

def format_admin_notification(data):
    """Format mesej pemberitahuan pantas untuk Admin WhatsApp & Emel."""
    harga = data.get("harga", 0)

    try:
        harga = float(harga)
    except (TypeError, ValueError):
        harga = 0.0

    return (
        f"🚨 *NOTIFIKASI TEMPAHAN / PEMBAYARAN BAHARU* 🚨\n\n"
        f"• *ID Tempahan:* {data.get('ref_id', '-')}\n"
        f"• *Nama Pelanggan:* {data.get('nama', '-')}\n"
        f"• *No. Telefon:* {data.get('no_tel', '-')}\n"
        f"• *Tarikh Perjalanan:* {data.get('tarikh', '-')}\n"
        f"• *Lokasi Pickup:* {data.get('pickup', '-')}\n"
        f"• *Destinasi:* {data.get('dropoff', '-')}\n"
        f"• *Jumlah Harga:* RM{harga:.2f}\n"
        f"• *Status:* {data.get('status_bayaran', 'Resit Dihantar / Menunggu Semakan')}\n\n"
        f"Sila buat semakan pada akaun CIMB atau portal ToyyibPay berpandukan nombor telefon pelanggan."
    )

def hantar_emel_admin(data_tempahan):
    """Menghantar salinan maklumat tempahan dan pengesahan QR ke emel pentadbiran rasmi."""
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    sender_email = os.getenv("SMTP_EMAIL", "radzmil@gmail.com")
    sender_password = os.getenv("SMTP_PASSWORD")

    if not sender_password:
        logging.warning(
            "Penghantaran emel dibatalkan: SMTP_PASSWORD tidak ditetapkan dalam .env"
        )
        return False

    subjek = f"🔔 Tempahan & Pengesahan QR Baharu - Ref: {data_tempahan.get('ref_id', 'SB-LEISURE')}"
    isi_mesej = format_admin_notification(data_tempahan)

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ADMIN_EMAIL
    msg['Subject'] = subjek
    msg.attach(MIMEText(isi_mesej, 'plain', 'utf-8'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, ADMIN_EMAIL, msg.as_string())
        server.quit()
        logging.info(f"Emel pengesahan tempahan & QR berjaya dihantar ke {ADMIN_EMAIL}")
        return True
    except Exception as e:
        logging.error(f"Ralat menghantar emel notifikasi admin: {e}")
        return False