dogum_tarihi_str = input("Doğum tarihinizi (gg.aa.yyyy) Formatında Giriniz: ")
dogum_gun, dogum_ay, dogum_yil = map(int, dogum_tarihi_str.split('.'))
hesaplama_gun = 1
hesaplama_ay = 12
hesaplama_yil = 2025
yas_yil = hesaplama_yil - dogum_yil
yas_ay = hesaplama_ay - dogum_ay
yas_gun = hesaplama_gun - dogum_gun
print("Kullanıcı", yas_yil,"Yıl",yas_ay,"Ay",yas_gun,"Gün","Yaşındadır.")
