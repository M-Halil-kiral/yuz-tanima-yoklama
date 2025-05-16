import pandas as pd
from datetime import datetime
from utils import yoklama_dosyasi, excel_dosyasi_yukle

# Yoklama kaydetme fonksiyonu
def yoklama_kaydet(ogrenci_id):
    """
    Öğrencinin yoklama kaydını oluşturur ve Excel dosyasına kaydeder.

    Args:
        ogrenci_id (str): Yoklaması alınan öğrencinin numarası.
    """
    # Excel dosyasını kontrol et veya oluştur
    excel_dosyasi_yukle(yoklama_dosyasi, ['ÖğrenciNumarası', 'Tarih', 'Saat', 'Durum'])
    
    # Mevcut Excel dosyasını oku
    df = pd.read_excel(yoklama_dosyasi)
    
    # Tarih ve saat bilgilerini al
    tarih_saat = datetime.now()
    tarih = tarih_saat.strftime('%Y-%m-%d')
    saat = tarih_saat.strftime('%H:%M:%S')

    # Yeni yoklama kaydı oluştur
    new_record = pd.DataFrame({
        'ÖğrenciNumarası': [ogrenci_id],
        'Tarih': [tarih],
        'Saat': [saat],
        'Durum': [True]
    })

    # Yeni kaydı mevcut tabloya ekle
    df = pd.concat([df, new_record], ignore_index=True)

    # Güncellenmiş tabloyu Excel'e yaz
    df.to_excel(yoklama_dosyasi, index=False)

# Güncel yoklama durumlarını getirme
def yoklama_durumu_getir():
    """
    Bugünkü tarih için yoklaması alınan öğrencilerin numaralarını döner.

    Returns:
        set: Bugünkü tarih için yoklaması alınan öğrenci numaraları.
    """
    if yoklama_dosyasi.exists():
        df = pd.read_excel(yoklama_dosyasi)
        bugun = datetime.now().strftime('%Y-%m-%d')
        yoklamalar = df[df['Tarih'] == bugun]
        return set(yoklamalar['ÖğrenciNumarası'])
    return set()