import os
import shutil
from ultralytics import YOLO

# 1. Modeli Yüklüyoruz
model = YOLO('yolov8s.pt')

# 2. Eğitimi Başlatıyoruz (Yaml dosyasını direkt ana dizinden çekiyoruz)
model.train(
    data='/content/data.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    patience=20,
    name='atik_modeli_v8s'
)

# 3. Drive'a Otomatik Aktarma
kaynak_yolu = '/content/runs/detect/atik_modeli_v8s'
hedef_yolu = '/content/drive/MyDrive/Atik_Projesi_Yedek'

if os.path.exists(kaynak_yolu):
    if os.path.exists(hedef_yolu):
        shutil.rmtree(hedef_yolu)
    
    shutil.copytree(kaynak_yolu, hedef_yolu)
    print("\nEğitim bitti ve dosyalar Drive'a başarıyla yedeklendi.")
else:
    print("\nHATA: Eğitim klasörü bulunamadı!")