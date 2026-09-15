def notu_5lik_sisteme_cevir(puan):
    if 85 <= puan <= 100:
        return 5, "Pekiyi"
    elif 70 <= puan <= 84:
        return 4, "İyi"
    elif 55 <= puan <= 69:
        return 3, "Orta"
    elif 45 <= puan <= 54:
        return 2, "Geçer"
    else:
        return 1, "Geçmez"


def puan_al():
    while True:
        try:
            puan = int(input("100 üzerinden not girin (0-100): "))
            if 0 <= puan <= 100:
                return puan
            else:
                print("⚠ Not 0 ile 100 arasında olmalı!")
        except ValueError:
            print("⚠ Lütfen geçerli bir sayı girin!")


notlar = []
ders_sayisi = int(input("Kaç ders notu gireceksiniz?: "))

for i in range(ders_sayisi):
    print(f"\n{i+1}. ders:")
    notlar.append(puan_al())

ortalama = sum(notlar) / len(notlar)
not_5lik, aciklama = notu_5lik_sisteme_cevir(int(ortalama))

print("\n--- SONUÇ ---")
print(f"Girilen notlar: {notlar}")
print(f"Ortalama: {ortalama:.2f}")
print(f"5'lik sistem karşılığı: {not_5lik} ({aciklama})")