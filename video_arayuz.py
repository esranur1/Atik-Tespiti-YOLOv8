import os
import sys
from datetime import datetime  # <-- Tarih eklemek için bunu ekledik
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from ultralytics import YOLO

class VideoTanimaUygulamasi:
    def __init__(self, pencere):
        self.pencere = pencere
        self.pencere.title("Atık Tanıma Sistemi - Video Analizi")
        self.pencere.geometry("500x350")
        self.pencere.configure(bg="#f4f4f4")
        
        self.model_yolu = "best.pt"
        if os.path.exists(self.model_yolu):
            self.model = YOLO(self.model_yolu)
        else:
            messagebox.showerror("Hata", f"'{self.model_yolu}' dosyası bulunamadı!\nLütfen 'best.pt' dosyasını bu kodun yanına koyun.")
            sys.exit()

        self.baslik = tk.Label(pencere, text="VİDEO ATIK ANALİZİ", font=("Helvetica", 16, "bold"), bg="#f4f4f4", fg="#333")
        self.baslik.pack(pady=20)
        
        self.bilgi_etiketi = tk.Label(
            pencere, 
            text="Lütfen analiz etmek istediğiniz videoyu seçin.\nİşlem bitince işlenmiş video klasöre kaydedilecektir.", 
            font=("Helvetica", 10), bg="#f4f4f4", fg="#666"
        )
        self.bilgi_etiketi.pack(pady=10)
        
        self.durum_etiketi = tk.Label(pencere, text="Durum: Bekleniyor...", font=("Helvetica", 11, "bold"), bg="#f4f4f4", fg="#005b96")
        self.durum_etiketi.pack(pady=20)
        
        self.btn_sec = tk.Button(pencere, text="Video Seç ve İşle", command=self.video_islem, font=("Helvetica", 11, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5)
        self.btn_sec.pack(pady=5)
        
        self.btn_cikis = tk.Button(pencere, text="Çıkış", command=pencere.quit, font=("Helvetica", 11), bg="#f44336", fg="white", padx=15)
        self.btn_cikis.pack(pady=5)

    def video_islem(self):
        video_yolu = filedialog.askopenfilename(filetypes=[("Video Dosyaları", "*.mp4 *.avi *.mov *.mkv")])
        if not video_yolu:
            return
            
        self.durum_etiketi.config(text="Durum: Video işleniyor, lütfen bekleyin...", fg="#ff9800")
        self.pencere.update()
        
        try:
            cap = cv2.VideoCapture(video_yolu)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            su_anki_klasor = os.path.dirname(os.path.abspath(__file__))
            
            # --- DEĞİŞİKLİK BURADA BAŞLIYOR ---
            # Dosya adının sonuna YılAyGün_SaatDakikaSaniye ekliyoruz
            zaman_damgasi = datetime.now().strftime("%Y%m%d_%H%M%S")
            video_adi = f"islenmis_atik_videosu_{zaman_damgasi}.mp4"
            output_yolu = os.path.join(su_anki_klasor, video_adi)
            # --- DEĞİŞİKLİK BURADA BİTİYOR ---
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_yolu, fourcc, fps, (width, height))
            
            kalinlik = 5          
            font_boyutu = 2.0     
            font_kalinligi = 4    

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                    
                results = self.model.predict(source=frame, conf=0.20, verbose=False)
                
                for result in results:
                    for box in result.boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        conf = float(box.conf[0])
                        cls_id = int(box.cls[0])
                        cls_name = self.model.names[cls_id].lower()
                        
                        if (x2 - x1) > (width * 0.9) or (y2 - y1) > (height * 0.9):
                            continue

                        gecerli_mi = False
                        if cls_name == "plastik" and conf >= 0.70:
                            gecerli_mi = True
                        elif cls_name in ["cam", "metal"] and conf >= 0.30:
                            gecerli_mi = True
                        elif cls_name not in ["plastik", "cam", "metal"] and conf >= 0.50:
                            gecerli_mi = True

                        if gecerli_mi:
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), kalinlik)
                            yuzde_metni = f"{cls_name.upper()} %{int(conf * 100)}"
                            
                            (w, h_text), _ = cv2.getTextSize(yuzde_metni, cv2.FONT_HERSHEY_SIMPLEX, font_boyutu, font_kalinligi)
                            
                            cv2.rectangle(frame, (x1, y1 - int(h_text * 1.5)), (x1 + w, y1), (0, 0, 0), -1)
                            
                            cv2.putText(frame, yuzde_metni, (x1, y1 - int(h_text * 0.3)), 
                                        cv2.FONT_HERSHEY_SIMPLEX, font_boyutu, (255, 255, 255), font_kalinligi)
                
                out.write(frame)
                
            cap.release()
            out.release()
            
            self.durum_etiketi.config(text="Durum: İşlem Tamamlandı!", fg="#4CAF50")
            messagebox.showinfo(
                "Başarılı", 
                f"Video başarıyla analiz edildi!\nKaydedilen dosya:\n{video_adi}"
            )
            
        except Exception as e:
            self.durum_etiketi.config(text="Durum: Hata Oluştu!", fg="#f44336")
            messagebox.showerror("Hata", f"Video işlenirken bir hata oluştu:\n{str(e)}")

if __name__ == "__main__":
    kok = tk.Tk()
    uygulama = VideoTanimaUygulamasi(kok)
    kok.mainloop()