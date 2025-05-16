import pandas as pd
from tkinter import messagebox
from utils import ogrenci_dosyasi, fotograflar_klasoru, excel_dosyasi_yukle

# Öğrenci ekleme fonksiyonu
def ogrenci_ekle(numara, ad, soyad):
    """
    Bir öğrenci ekler ve öğrenci dosyasına kaydeder.

    Args:
        numara (str): Öğrencinin numarası.
        ad (str): Öğrencinin adı.
        soyad (str): Öğrencinin soyadı.
    """
    foto_yolu = fotograflar_klasoru / f"{numara}.jpg"
    
    # Excel dosyasını kontrol et veya oluştur
    excel_dosyasi_yukle(ogrenci_dosyasi, ['ÖğrenciNumarası', 'İsim', 'Soyisim', 'FotoğrafYolu'])
    
    # Mevcut öğrenci dosyasını oku
    df = pd.read_excel(ogrenci_dosyasi)

    # Yeni öğrenci kaydı oluştur
    new_student = pd.DataFrame({
        'ÖğrenciNumarası': [numara],
        'İsim': [ad],
        'Soyisim': [soyad],
        'FotoğrafYolu': [str(foto_yolu)]
    })

    # Yeni kaydı mevcut tabloya ekle
    df = pd.concat([df, new_student], ignore_index=True)
    
    # Güncellenmiş tabloyu dosyaya yaz
    df.to_excel(ogrenci_dosyasi, index=False)

    # Başarılı mesajı göster
    messagebox.showinfo("Başarılı", f"{ad} {soyad} başarıyla eklendi.")

# Öğrenci silme fonksiyonu
def ogrenci_sil(ogrenci_numara):
    """
    Belirtilen öğrenci numarasına göre öğrenciyi siler.

    Args:
        ogrenci_numara (str): Silinecek öğrencinin numarası.
    """
    ogrenci_numara = str(ogrenci_numara)

    # Excel dosyasını kontrol et veya oluştur
    excel_dosyasi_yukle(ogrenci_dosyasi, ['ÖğrenciNumarası', 'İsim', 'Soyisim', 'FotoğrafYolu'])
    
    # Mevcut öğrenci dosyasını oku
    df = pd.read_excel(ogrenci_dosyasi)
    df['ÖğrenciNumarası'] = df['ÖğrenciNumarası'].astype(str)

    # Öğrenci numarasını kontrol et
    if ogrenci_numara in df['ÖğrenciNumarası'].values:
        # Fotoğraf dosyasını sil
        foto_yolu = fotograflar_klasoru / f"{ogrenci_numara}.jpg"
        if foto_yolu.exists():
            foto_yolu.unlink()

        # Öğrenci kaydını sil
        df = df[df['ÖğrenciNumarası'] != ogrenci_numara]
        
        # Güncellenmiş tabloyu dosyaya yaz
        df.to_excel(ogrenci_dosyasi, index=False)
        
        # Başarılı mesajı göster
        messagebox.showinfo("Başarılı", f"Öğrenci Numarası {ogrenci_numara} başarıyla silindi.")
    else:
        # Hata mesajı göster
        messagebox.showerror("Hata", "Öğrenci bulunamadı.")