
print("\n           TATLILAR \n ______________________________________ \n |BAKLAVA FISTIKLI(No : 1) = 400TL/Kg | \n |BAKLAVA CEVİZLİ(No : 2) = 250TL/Kg  | \n |ŞÖBİYET(No : 3) = 200TL/Kg          | \n |KADAYIF(No : 4) = 200TL/Kg          | \n |ŞEKERPARE(No : 5) = 175TL/Kg        | \n |TRİLEÇE(No : 6) = 150TL/Kg          |\n |MAGNOLYA(No : 7) = 50TL/Adet        | \n |____________________________________|")
secim = str(input("Alacağınız Tatlının Numarasını Giriniz : "))
kilo = float(input("Kaç Kilo Alacaksınız : "))

if secim == "1":
    ucret = 1000
elif secim == "2":
    ucret = 500
elif secim == "3":
    ucret = 300
elif secim == "4":
    ucret = 250
elif secim == "5":
    ucret =  200
elif secim == "6":
    ucret = 200
elif secim == "7":
    ucret = 50 
fiyat = kilo * ucret
def fis():
    if secim == "1":
        isim = "Baklava Fıstıklı"
        
    elif secim == "2":
        isim = "Baklava Cevizli"
    elif secim == "3":
        isim = "Şöbiyet"
    elif secim == "4":
        isim = "Kadayıf"
    elif secim == "5":
        isim = "Şekerpare"
    elif secim == "6":
        isim = "Trileçe"
    elif secim == "7":
        isim = "Magnolya"
    print("\n              FİŞİNİZ             \n __________________________________  \n Alınan Tatlı :",isim, "\n Alınan Miktar : ",kilo,"Kg/Adet","\n Alınan Ücret : ",fiyat,"TL","\n Bizi Tercih Ettiğiniz İçin Teşekkür Ederiz :) ","\n ________________________________")

def secim1():

    fis()

def secim2():

    fis()


def secim3():    

    fis()

def secim4():

    fis()

def secim5():   

    fis()

def secim6():
    
    fis()
def secim7():
    
    fis()

if secim == "1":
    secim1()
if secim == "2":
    secim2()
if secim == "3":
    secim3()
if secim == "4":
    secim4()
if secim == "5":
    secim5()
if secim == "6":
    secim6()
if secim == "7":
    secim7()
