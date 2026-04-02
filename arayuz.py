import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from ultralytics import YOLO

class AtikTanimaUygulamasi:
    def __init__(self, pencere):
        self.pencere = pencere
        self.pencere.title("Akıllı Atık Ayrıştırma Sistemi")
        self.pencere.geometry("600x650")
        self.pencere.configure(bg="#f4f4f4")
        
        # Dosya direkt kodun yanında olduğu için sadece ismini yazıyoruz
        self.model_yolu = "best.pt"
        if os.path.exists(self.model_yolu):
            self.model = YOLO(self.model_yolu)
        else:
            messagebox.showerror("Hata", f"'{self.model_yolu}' dosyası bu klasörde bulunamadı!\nLütfen 'best.pt' dosyasını bu kodun yanına kopyalayın.")
            sys.exit()

        # Arayüz Elemanları
        self.baslik = tk.Label(pencere, text="ATIK TANIMA SİSTEMİ", font=("Helvetica", 18, "bold"), bg="#f4f4f4", fg="#333")
        self.baslik.pack(pady=15)
        
        self.resim_alani = tk.Label(pencere, text="Henüz bir görsel seçilmedi", bg="#ddd", width=50, height=20)
        self.resim_alani.pack(pady=10)
        
        self.sonuc_etiketi = tk.Label(pencere, text="Tespit Edilen Sınıflar: -", font=("Helvetica", 12, "bold"), bg="#f4f4f4", fg="#005b96")
        self.sonuc_etiketi.pack(pady=15)
        
        self.btn_sec = tk.Button(pencere, text="Görsel Seç ve Tanı", command=self.gorsel_islem, font=("Helvetica", 11, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5)
        self.btn_sec.pack(pady=5)
        
        self.btn_cikis = tk.Button(pencere, text="Çıkış", command=pencere.quit, font=("Helvetica", 11), bg="#f44336", fg="white", padx=15)
        self.btn_cikis.pack(pady=5)

    def gorsel_islem(self):
        dosya_yolu = filedialog.askopenfilename(filetypes=[("Resim Dosyaları", "*.jpg *.jpeg *.png *.bmp")])
        if not dosya_yolu:
            return
            
        # Görseli arayüzde göster
        img = Image.open(dosya_yolu)
        img.thumbnail((400, 400))
        img_tk = ImageTk.PhotoImage(img)
        self.resim_alani.config(image=img_tk, text="")
        self.resim_alani.image = img_tk
        
        # Modeli çalıştır
        results = self.model.predict(source=dosya_yolu, conf=0.5)
        
        tespitler = []
        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                cls_name = self.model.names[cls_id]
                conf = float(box.conf[0]) * 100
                tespitler.append(f"{cls_name.upper()} (%{conf:.1f})")
                
        if tespitler:
            self.sonuc_etiketi.config(text="Tespit Edilen Sınıflar:\n" + ", ".join(tespitler))
            results[0].show() # Tespit kutulu görseli dışarıda açar
        else:
            self.sonuc_etiketi.config(text="Tespit Edilen Sınıflar: Hiçbir atık bulunamadı.")

if __name__ == "__main__":
    kok = tk.Tk()
    uygulama = AtikTanimaUygulamasi(kok)
    kok.mainloop()