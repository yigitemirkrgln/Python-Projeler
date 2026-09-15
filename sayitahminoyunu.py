import random
sayi= random.randint(1,100)
while True:
    tahmin=int(input("Tahmin: "))
    if tahmin < sayi :
     print("Daha Büyük!")
    elif tahmin > sayi :
     print("Daha Küçük!")
    else:
     print("Doğru Tahmin!")
    break 