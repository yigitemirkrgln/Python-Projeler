import random

def oyun():
    secenekler = ["taş", "kağıt", "makas"]
    bilgisayar = random.choice(secenekler)
    oyuncu = input("Taş, kağıt veya makas?: ").lower()

    print("Bilgisayar:", bilgisayar)

    if oyuncu == bilgisayar:
        print("Berabere!")
    elif (oyuncu == "taş" and bilgisayar == "makas") or \
         (oyuncu == "kağıt" and bilgisayar == "taş") or \
         (oyuncu == "makas" and bilgisayar == "kağıt"):
        print("Kazandın!")
    else:
        print("Kaybettin!")

oyun()