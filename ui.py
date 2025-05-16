import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar
from student_management import ogrenci_ekle, ogrenci_sil
from attendance_management import yoklama_kaydet, yoklama_durumu_getir
import cv2
from utils import fotograflar_klasoru
import pandas as pd
from utils import ogrenci_dosyasi

# Öğrenci ekleme penceresi
def ekle_penceresi(root, listbox):
    def ekle():
        numara = numara_entry.get()
        ad = ad_entry.get()
        soyad = soyad_entry.get()
        
        foto_yolu = fotograflar_klasoru / f"{numara}.jpg"

        # Kameradan fotoğraf çekme
        video_capture = cv2.VideoCapture(0)
        if video_capture.isOpened():
            ret, frame = video_capture.read()
            if ret:
                cv2.imwrite(str(foto_yolu), frame)
                ogrenci_ekle(numara, ad, soyad)
                güncellemeleri_göster(listbox)
            video_capture.release()
            cv2.destroyAllWindows()
        ekle_window.destroy()

    ekle_window = tk.Toplevel(root)
    ekle_window.title("Öğrenci Ekle")

    tk.Label(ekle_window, text="Öğrenci Numarası:").pack()
    numara_entry = tk.Entry(ekle_window)
    numara_entry.pack()

    tk.Label(ekle_window, text="Öğrenci Adı:").pack()
    ad_entry = tk.Entry(ekle_window)
    ad_entry.pack()

    tk.Label(ekle_window, text="Öğrenci Soyadı:").pack()
    soyad_entry = tk.Entry(ekle_window)
    soyad_entry.pack()

    tk.Button(ekle_window, text="Fotoğraf Çek ve Ekle", command=ekle).pack()

# Öğrenci silme penceresi
def sil_penceresi(root, listbox):
    def sil():
        ogrenci_id = id_entry.get()
        if ogrenci_id:
            ogrenci_sil(ogrenci_id)
            güncellemeleri_göster(listbox)
            sil_window.destroy()
        else:
            messagebox.showerror("Hata", "Lütfen geçerli bir öğrenci numarası girin.")

    sil_window = tk.Toplevel(root)
    sil_window.title("Öğrenci Sil")

    tk.Label(sil_window, text="Silinecek Öğrenci Numarası:").pack()
    id_entry = tk.Entry(sil_window)
    id_entry.pack()

    tk.Button(sil_window, text="Sil", command=sil).pack()

def yoklama_al():
    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        messagebox.showerror("Hata", "Kamera açılamadı!")
        return

    # Bugünkü tarih için yoklaması alınan öğrencileri al
    yoklama_alinanlar = yoklama_durumu_getir()

    try:
        while True:
            ret, frame = video_capture.read()
            if not ret:
                messagebox.showerror("Hata", "Kamera bağlantısı başarısız!")
                break

            # Geçici bir resim dosyası oluştur
            temp_path = fotograflar_klasoru / "temp.jpg"
            cv2.imwrite(str(temp_path), frame)

            identified = False
            person_name = "Bilinmiyor"
            ogrenci_id = None

            # Öğrenci kayıtlarını kontrol et
            df = pd.read_excel(ogrenci_dosyasi)
            for _, row in df.iterrows():
                ogrenci_num = str(row['ÖğrenciNumarası'])
                isim = row['İsim']
                soyisim = row['Soyisim']
                foto_yolu = row['FotoğrafYolu']

                # Referans resim okuma
                ref_image = cv2.imread(foto_yolu)
                if ref_image is not None:
                    # DeepFace ile yüz karşılaştırma
                    from deepface import DeepFace
                    result = DeepFace.verify(str(temp_path), str(foto_yolu), enforce_detection=False)

                    if result["verified"]:
                        identified = True
                        person_name = f"{isim} {soyisim}"
                        ogrenci_id = ogrenci_num

                        # Eğer yoklaması alınmadıysa kaydet
                        if ogrenci_id not in yoklama_alinanlar:
                            yoklama_kaydet(ogrenci_id)  # Yoklamayı kaydet
                            yoklama_alinanlar.add(ogrenci_id)  # Kümede sakla
                        break

            # Ekrana görüntü ekleme
            color = (0, 255, 0) if identified else (0, 0, 255)
            cv2.putText(frame, f"Kişi: {person_name}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.imshow('Kamera - Yüz Tanıma', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q' tuşuna basıldığında çıkış
                break
    finally:
        video_capture.release()
        cv2.destroyAllWindows()

# Yoklamaları listeleme
def güncellemeleri_göster(listbox):
    listbox.delete(0, tk.END)
    yoklama_alinanlar = yoklama_durumu_getir()
    for ogrenci_id in yoklama_alinanlar:
        listbox.insert(tk.END, f"{ogrenci_id}")

# Ana arayüz
def arayuz():
    root = tk.Tk()
    root.title("Yüz Tanıma Sistemi")
    root.geometry("500x600")
    root.configure(bg="black")

    # Listeleme kutusu
    frame = tk.Frame(root, bg="black")
    frame.pack(pady=10)

    column_titles = ["Numara", "İsim", "Soyisim"]
    for i, title in enumerate(column_titles):
        label = tk.Label(frame, text=title, width=15, bg="black", fg="white")
        label.grid(row=0, column=i)

    listbox_frame = tk.Frame(frame)
    listbox_frame.grid(row=1, column=0, columnspan=3)

    listbox = Listbox(listbox_frame, width=50, height=10)
    listbox.pack(side=tk.LEFT)

    scrollbar = Scrollbar(listbox_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    # Butonlar
    button_frame = tk.Frame(root, bg="black")
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Yoklama Al", width=30, bg="#007BFF", fg="white", command=yoklama_al).pack(pady=5)
    tk.Button(button_frame, text="Listeyi Güncelle", width=30, bg="#28A745", fg="white",
              command=lambda: güncellemeleri_göster(listbox)).pack(pady=5)
    tk.Button(root, text="Öğrenci Ekle", command=lambda: ekle_penceresi(root, listbox), width=30, bg="#28A745",
              fg="white").pack(pady=5)
    tk.Button(root, text="Öğrenci Sil", command=lambda: sil_penceresi(root, listbox), width=30, bg="#DC3545",
              fg="white").pack(pady=5)

    # Başlangıçta listeyi güncelle
    güncellemeleri_göster(listbox)

    root.mainloop()