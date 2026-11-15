"""Bileşik integral kurallarını ve yaklaşım hatalarını karşılaştırır."""

import math

import sympy as sp

x = sp.symbols("x", real=True)
f_sym = sp.exp(x) * sp.cos(x)
f = sp.lambdify(x, f_sym, "math")


def yamuk_yöntemi(a, b, n):
    """Bileşik yamuk kuralını uygula."""
    h = (b - a) / n
    ic_toplam = math.fsum(f(a + i * h) for i in range(1, n))
    return h * ((f(a) + f(b)) / 2 + ic_toplam)


def simpson_1_3(a, b, n):
    """Çift sayıda alt aralık için bileşik Simpson 1/3 kuralını uygula."""
    if n % 2:
        return None
    h = (b - a) / n
    ic_toplam = math.fsum((4 if i % 2 else 2) * f(a + i * h) for i in range(1, n))
    return (h / 3) * (f(a) + ic_toplam + f(b))


def simpson_3_8(a, b, n):
    """Üçün katı sayıda alt aralık için bileşik Simpson 3/8 kuralını uygula."""
    if n % 3:
        return None
    h = (b - a) / n
    ic_toplam = math.fsum((3 if i % 3 else 2) * f(a + i * h) for i in range(1, n))
    return (3 * h / 8) * (f(a) + ic_toplam + f(b))


def orneklemli_hata_sinirlari(a, b, n):
    """Denklemlerdeki türev maksimumlarını 101 noktada yaklaşık hesapla."""
    uzunluk = abs(b - a)
    h = uzunluk / n
    noktalar = [a + (b - a) * i / 100 for i in range(101)]
    ikinci_turev = sp.lambdify(x, sp.diff(f_sym, x, 2), "math")
    dorduncu_turev = sp.lambdify(x, sp.diff(f_sym, x, 4), "math")
    m2 = max(abs(ikinci_turev(nokta)) for nokta in noktalar)
    m4 = max(abs(dorduncu_turev(nokta)) for nokta in noktalar)
    return (uzunluk * h**2 * m2 / 12, uzunluk * h**4 * m4 / 180,
            uzunluk * h**4 * m4 / 80)


def main():
    try:
        a = float(input("Alt sınır: "))
        b = float(input("Üst sınır: "))
        n = int(input("Alt aralık sayısı: "))
        if not math.isfinite(a) or not math.isfinite(b) or n < 1:
            raise ValueError("Sınırlar sonlu, alt aralık sayısı pozitif olmalıdır.")

        referans = float(sp.integrate(f_sym, (x, a, b)).evalf())
        sonuc = (yamuk_yöntemi(a, b, n), simpson_1_3(a, b, n), simpson_3_8(a, b, n))
        sinirlar = orneklemli_hata_sinirlari(a, b, n)
    except (EOFError, ArithmeticError, ValueError, TypeError) as hata:
        print(f"Hesaplama yapılamadı: {hata}")
        return

    yontemler = ("Bileşik Yamuk", "Bileşik Simpson 1/3", "Bileşik Simpson 3/8")
    kosullar = ("", "n çift olmalı", "n üçün katı olmalı")
    print(f"\nReferans integral: {referans:.10f}")
    for ad, deger, sinir, kosul in zip(yontemler, sonuc, sinirlar, kosullar):
        if deger is None:
            print(f"{ad}: Hesaplanamadı ({kosul})")
            continue
        mutlak_hata = abs(deger - referans)
        print(f"{ad}: {deger:.10f} | Mutlak hata: {mutlak_hata:.3g} "
              f"| Örneklemli sınır tahmini: {sinir:.3g}")


if __name__ == "__main__":
    main()
