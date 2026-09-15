def kelime_sayisi(cumle):
    kelimeler = cumle.split()
    return len(kelimeler)

cumle = input("Bir cümle girin: ")
print(f"Bu cümlede {kelime_sayisi(cumle)} kelime bulunuyor.")