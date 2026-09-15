kısa_kenar = int(input("Kısa Kenarı Giriniz : "))
uzun_kenar = int(input("Uzun Kenarı Giriniz : "))
if kısa_kenar > uzun_kenar:
    print("kısa kenar uzun kenardan büyük olamaz!!")
else:
    alan = kısa_kenar * uzun_kenar
    çevre = (kısa_kenar + uzun_kenar) * 2
    print("alanımız : ",alan,"çevremiz : ",çevre)