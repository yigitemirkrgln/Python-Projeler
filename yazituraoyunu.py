import random 
tahmin=str(input("Yazı mı yoksa Tura mı? "))

sonuc=random.choice("Yazı""Tura")
if tahmin==sonuc:
 print("Kazandınız!")
else:
 print("Maalesef Kazanamadınız...")
