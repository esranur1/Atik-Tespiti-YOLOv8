# Akıllı Atık Tespiti ve Sınıflandırma (YOLOv8)
Tokat Gaziosmanpaşa Üniversitesi - Bilgisayar Programcılığı
Geliştirici: Esranur Uçal 

Bu proje, görüntü ve videolardaki atıkları türlerine göre (Cam, Kağıt, Metal, Plastik) tespit eden, YOLOv8 tabanlı bir derin öğrenme uygulamasıdır. Proje, model eğitiminin yanı sıra kullanıcı dostu bir arayüz ile test ve görsel çıktı alma imkanı sunmaktadır.

## 1. Veri Seti Oluşturma ve Ön İşleme
**Sınıflar: Modelimiz;** cam, kagit, metal ve plastik olmak üzere 4 farklı geri dönüştürülebilir atık türünü tanımaktadır.
**Veri Toplama ve Çeşitlilik:** Veri seti Roboflow üzerinden hazırlandı ve yaklaşık 6000 adet görüntüden oluşturulmuştur. Modelin gerçek hayat senaryolarında (farklı açılar, değişen ışık koşulları, karmaşık arka planlar ve farklı ölçekler) başarılı olması için veri çeşitliliğine maksimum özen gösterilmiştir.
**Etiketleme (Bounding Box):** Görüntülerdeki atıklar yüksek doğrulukla ve tutarlı sınırlayıcı kutular (bounding box) ile etiketlenmiştir.
**Ön İşleme & Ayrım:** Veri seti train (eğitim), val (doğrulama) ve test olmak üzere üç alt kümeye ayrılmıştır. Eğitim öncesi eksik veya hatalı görüntüler temizlenmiş ve modelin genelleme yeteneğini artırmak için veri artırma (augmentation) teknikleri uygulanmıştır.

## 2. Model Seçimi ve Mimari
Projede hız ve doğruluk dengesi sebebiyle son teknoloji nesne tespiti modellerinden YOLOv8s (Small) tercih edilmiştir. Modelin temel görsel algılama yetenekleri (Pre-trained weights) kullanılmış, ancak model tamamen bana ait olan 6000 görsellik özel atık veri setiyle eğitilerek projeye özgü hale getirilmiştir. Bu Transfer Learning yöntemiyle eğitim sürecinin verimliliği artırılmıştır.

## 3. Eğitim (Training) ve Performans
Eğitim süreci Google Colab üzerinde 100 epoch olarak planlanmış ve patience=20 (erken durdurma) parametresi eklenmiştir.
Eğitim sürecine ait tüm kayıp (loss) metrikleri, mAP, Precision ve Recall grafikleri runs/detect/ dizini altında saklanmaktadır.
**Sonuç Analizi:** Test sonuçları incelendiğinde modelin Plastik, Metal ve Kağıt atıkları oldukça yüksek bir doğruluk oranıyla başarıyla tespit ettiği görülmüştür. Cam atıklarda ise saydamlık ve ışık yansımaları nedeniyle diğer sınıflara kıyasla daha düşük bir başarı oranı elde edilmiş olup, bu durum gelecekteki çalışmalar için bir iyileştirme alanı olarak kaydedilmiştir.

Kullanım ve Çalışır Sistem (Arayüz Özellikleri)
Projede tespit süreçlerini test etmek ve videoları işlemek için Python scriptleri hazırlanmıştır.

Gerekli Kütüphanelerin Kurulumu:
pip install ultralytics opencv-python

## 4. Uygulama Modülleri:
**Görsel Arayüz Modu (arayuz.py):** Python'ın Tkinter kütüphanesiyle hazırlanmış özel bir pencere açar ve nesne tanımasını bu arayüz üzerinden gerçekleştirir.
**Video Analiz Modu (video_arayuz.py):** Yine Tkinter kütüphanesiyle hazırlanan bu modül, bilgisayardan bir video seçilmesini sağlar. Seçilen video üzerinde analiz yaptıktan sonra, nesne tespiti yapılmış sonuçlandırılmış videoyu çıktı olarak doğrudan klasöre kaydeder.

Dosya Yapısı

**runs/detect/:** Eğitim sürecine ait performans grafikleri, matrisler ve metrikler.

**best.pt:** Eğitim sonucu elde edilen en başarılı ve optimize model ağırlık dosyası.

**data.yaml:** Veri seti sınıflarını ve dosya yollarını barındıran yapılandırma dosyası.

**egitim_kodu.py:** Colab üzerinde çalıştırdığımız eğitim scripti.
