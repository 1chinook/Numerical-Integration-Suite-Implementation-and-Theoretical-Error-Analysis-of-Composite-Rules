# Numerical Integration Suite

Bileşik yamuk, Simpson 1/3 ve Simpson 3/8 kurallarını karşılaştıran Python terminal aracı.

## Kurulum ve çalıştırma

```sh
python -m pip install -r requirements.txt
python numerikPython.py
```

## Kullanım

Alt ve üst sınırı ve pozitif alt aralık sayısını girin. Simpson 1/3 için sayı çift, Simpson 3/8 için üçün katı olmalıdır. Üç yöntemi aynı anda karşılaştırmak için örneğin `0`, `1`, `12` girin. Program analitik integralden hesapladığı referans değeri ve mutlak hataları gösterir. İkinci ve dördüncü türevler 101 noktada örneklenir, dolayısıyla bunlarla hesaplanan teorik sınır ifadeleri örneklemeye dayalı tahminlerdir.

## Proje yapısı

- `numerikPython.py` — yöntemler, hata analizi ve terminal arayüzü. Örnek fonksiyon `f_sym` olarak tanımlıdır.
- `requirements.txt` — SymPy bağımlılığı.
