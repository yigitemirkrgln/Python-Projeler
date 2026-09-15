yıl = int(input("Doğum yılınızı Giriniz : "))
ay = int(input("Doğum ayınızı Giriniz : "))
gün = int(input("Doğum Gününüzü Giriniz : "))
dogum = (gün,"/",ay,"/",yıl)
bugün_yıl = 2025
bugün_ay = 12
bugün_gün = 1
bugün = (bugün_gün,"/",bugün_ay,"/",bugün_yıl)
yaş_yıl = bugün_yıl - yıl
yaş_ay = bugün_ay - ay
yaş_gün = bugün_gün - gün
yaş = (yaş_gün,yaş_ay,yaş_yıl)
print("yaşınız",yaş)
