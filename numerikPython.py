import math
import os
import sympy as sp

def terminali_temizle():
    os.system('cls' if os.name == 'nt' else 'clear') # Her işlemde terminal temizliği #


x = sp.symbols('x')  # türevini alabilmemiz için x'i sembolik hale getiriyoruz #

f_sym = sp.exp(x) * sp.cos(x) ###################- FONKSİYONUMUZUN TANIMLANACAĞI SATIR -###################

### Örnek Değerler : x ** 3 + 2*x**2 - 5*x + 10 &&&& sp.exp(x) * sp.cos(x) &&&& sp.log(x**2 + 1) &&&& 1 / sp.sqrt(1+x**2)
                      


f = sp.lambdify(x, f_sym, 'math')  # Sembolik ifadeyi sayısal hesaplamalar için fonksiyon haline getiriyoruz. #

def hata_hesapla(yaklasik, gercek):  
    if yaklasik is None or gercek is None:  # Eğer yaklaşık veya gerçek değer hesaplanmadıysa hiçbir şey döndürme #
        return None
    return abs(gercek - yaklasik)   # Hesaplandıysa ikisi arasındaki mutlak değeri geri döndür #


def yamuk_yöntemi(a, b, n):       # Alt sınır, üst sınır ve alt aralık sayısını alıyoruz. # 
    h = (b - a) / n               # Adım sayısını hesaplıyoruz. #
    toplam = (f(a) + f(b)) / 2.0  # Ortalama yükseklik değerini hesaplıyoruz. #

    for i in range(1, n):          
        toplam += f(a + i * h)   # Aralıktaki tüm noktaların fonksiyon değerlerini hesaplıyoruz. #
        
    return h * toplam            # Alanı bulmak için h ile çarpıyoruz. #

def simpson_1_3(a, b, n):        # Alt sınır, üst sınır ve alt aralık sayısını alıyoruz. # 

    if n % 2 != 0:               # 1/3 kuralına göre n'in, 2'nin katı olması gerekiyor. (Değilse sonuç döndürmüyor) # 
        return None
    
    h = (b - a) / n                 # Adım sayısını hesaplıyoruz. #
    toplam = f(a) + f(b)            # Toplamı hesaplıyoruz. #
     
    for i in range(1, n):           # Noktaların fonksiyon değerlerini hesaplamaya başlıyoruz #
        x_i = a + i * h             # Kaçıncı adımda olduğumuza bağlı olarak mevcut x_indis değerini hesaplıyoruz #
        if i % 2 == 1:              # Simpson 1/3 formülüne göre eğer indis tek sayı ise katsayı 4 olur. #
            toplam += 4 * f(x_i)    # 4 ile çarpıyoruz. #
        else:                       # Simpson 1/3 formülüne göre eğer indis çift sayı ise katsayı 2 olur. #                   
            toplam += 2 * f(x_i)    # 2 ile çarpıyoruz. #
            
    return (h / 3.0) * toplam       # (i=1 den başladığımız için ve n'e kadar gittiği için baştaki ve sondaki değerlerin katsayısı 1 olarak kaldı!) #

def simpson_3_8(a, b, n):           # Alt sınır, üst sınır ve alt aralık sayısını alıyoruz. # 

    if n % 3 != 0:                  # 3/8 kuralına göre n'in, 3'ün katı olması gerekiyor. (Değilse sonuç döndürmüyor) # 
        return None
    
    h = (b - a) / n                 # Adım sayısını hesaplıyoruz. #
    toplam = f(a) + f(b)            # Toplamı hesaplıyoruz. #
    
    for i in range(1, n):           # Noktaların fonksiyon değerlerini hesaplamaya başlıyoruz #
        x_i = a + i * h             # Kaçıncı adımda olduğumuza bağlı olarak mevcut x_indis değerini hesaplıyoruz #
        if i % 3 == 0:              # 3. dereceden interpolasyon polinomu gereği 3'ün katı olan düğüm noktalarının katsayısı 2'dir #    
            toplam += 2 * f(x_i)  
        else:                       # 3. dereceden interpolasyon polinomu gereği indis 3'ün katı değilse katsayı 3 olur. #    
            toplam += 3 * f(x_i)  
            
    return (3 * h / 8.0) * toplam       # Formüle göre değerimizi hesaplıyoruz. #    
 
def hata_ust_siniri_hesapla(a_deger, b_deger, n_deger):  # Hata üst sınırı hesaplamak için alt, üst ve n değerlerini alıyoruz #
    x = sp.symbols('x')                                  # x değişkeni sembolik olarak tanımlanıyor (türev alabilmek için) #
    
    h = (b_deger - a_deger) / n_deger                    # h değerini hesaplıyoruz #  
    aralik = (a_deger, b_deger)                          # aralığı alıyoruz # 

    f_prime2 = sp.diff(f_sym, x, 2)     # 2. Türev Hesabı #
    noktalar = [abs(f_prime2.subs(x, a_deger + i * (b_deger - a_deger) / 100)) for i in range(101)]  # Tüm türevlere bakıyoruz #
    M2 = max(noktalar)                                                  # En yüksek olan türevi alıyoruz #
    hata_ust_yamuk = ((b_deger - a_deger) * (h**2) / 12) * M2           # Formülde herşeyi yerine koyuyoruz #

    f_prime4 = sp.diff(f_sym, x, 4)     # 4. Türev Hesabı #
    noktalar_4 = [abs(f_prime4.subs(x, a_deger + i * (b_deger - a_deger) / 100)) for i in range(101)] # Tüm türevlere bakıyoruz #
    M4 = max(noktalar_4)                     # En yüksek olan türevi alıyoruz #
    
    hata_ust_s13 = ((b_deger - a_deger) * (h**4) / 180) * M4  # Simpson 1/3 için formüle yazıyoruz #
    hata_ust_s38 = ((b_deger - a_deger) * (h**4) / 80) * M4   # Simpson 3/8 için formüle yazıyoruz #

    return hata_ust_yamuk, hata_ust_s13, hata_ust_s38      # Değerleri geri döndürüyoruz #

try:

    terminali_temizle()

    a = float(input("Alt sınır değerini giriniz: ")) # Alt değeri kullanıcıdan alıyoruz #
    b = float(input("Üst sınır değerini giriniz: ")) # Üst değeri kullanıcıdan alıyoruz #
    n = int(input("Alt aralık sayısını giriniz: "))  # Alt aralık sayısını kullanıcıdan alıyoruz #

    sonuc_yamuk = yamuk_yöntemi(a, b, n) # Yamuk yöntemini kullanarak yaklaşık değeri alıyoruz. #
    sonuc_s13 = simpson_1_3(a, b, n)     # Simpson 1/3 yöntemini kullanarak yaklaşık değeri alıyoruz. #    
    sonuc_s38 = simpson_3_8(a, b, n)     # Simpson 3/8 yöntemini kullanarak yaklaşık değeri alıyoruz. #   

    referans_deger = sonuc_s13 if sonuc_s13 is not None else sonuc_yamuk  # Referans değer olarak değeri olanı al #
    hata_yamuk = hata_hesapla(sonuc_yamuk, referans_deger)                # Yamuk değeri için hata hesapla #
    hata_s38 = hata_hesapla(sonuc_s38, referans_deger)                    # 3/8 için hata hesapla #



    print("\n" + "=" * 60)                            # Görsel Düzenlemeler # 
    print(f"{'YÖNTEM':<30} | {'YAKLAŞIK DEĞER':<25}") # Görsel Düzenlemeler # 
    print("-" * 60)                                   # Görsel Düzenlemeler #   

    print(f"Bileşik Yamuk Sonucu:       {sonuc_yamuk:.8f}")                # Yamuk yöntemiyle sonuç (8 digitli) #    

    if sonuc_s13 is not None:                                              # Fonksiyondan bir değer gelip gelmediğini kontrol ediyoruz #
        print(f"Bileşik Simpson 1/3 Sonucu: {sonuc_s13:.8f}")              # Simpson 1/3 yöntemiyle sonuç (8 digitli) #
    else:
        print("Bileşik Simpson 1/3 Sonucu: Hesaplanamadı (n çift olmalı)") # eğer n çift değilse hata veriyor #

    if sonuc_s38 is not None:                                              # Fonksiyondan bir değer gelip gelmediğini kontrol ediyoruz #         
        print(f"Bileşik Simpson 3/8 Sonucu: {sonuc_s38:.8f}")              # Simpson 3/8 yöntemiyle sonuç (8 digitli) #
    else:
        print("Bileşik Simpson 3/8 Sonucu: Hesaplanamadı (n, 3'ün katı olmalı)") # eğer n 3'ün katı değilse hata veriyor #

    print(f"Yamuk Yöntemi Mutlak Hata Tahmini: {hata_yamuk:.10f}")               # Yamuk yöntemi hata tahmini #
    if hata_s38 is not None:
        print(f"Simpson 3/8 vs 1/3 Farkı:       {hata_s38:.10f}")                # Simpson hata farkı # 


    print("-" * 60)
    h_yamuk, h_s13, h_s38 = hata_ust_siniri_hesapla(a, b, n) # Hata üst sınırı hesaplama girdileri #

    print(f"--- Teorik Hata Üst Sınırları (n={n}) ---")     # Görsel Girdiler #
    print(f"Yamuk Üst Sınır    : {h_yamuk:.10f}")           # Hata Hesaplamaları #   
    print(f"Simpson 1/3 Üst Sınır: {h_s13:.10f}")           # Hata Hesaplamaları #   
    print(f"Simpson 3/8 Üst Sınır: {h_s38:.10f}")           # Hata Hesaplamaları #   

    print("-" * 60)
    print(f"Analiz Aralığı: [{a}, {b}] | Alt Aralık Sayısı: {n}\n")        # Analiz aralığını ve alt aralık sayısını belirtiyoruz. #  
    

except Exception as e:
    print(f"Hata Oluştu: {e}")      # Olası bir hataya karşı önlem # 