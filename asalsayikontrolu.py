def asal_mi(sayi):
    if sayi <= 1:
        return False
    for i in range(2, int(sayi ** 0.5) + 1):
        if sayi % i == 0:
            return False
    return True

sayi = int(input("Bir sayı girin: "))
if asal_mi(sayi):
    print(f"{sayi} asal bir sayıdır.")
else:
    print(f"{sayi} asal bir sayı değildir.")
