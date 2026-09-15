# Ürünlerin Menüsü (Yapay Zeka Tarafından Oluşturuldu)
urun_fiyatlari={
    "cocacola_1l":55,
    "cocacola_1_5l":70,
    "cocacola_330ml":45,
    "pepsi_1l":57,
    "pepsi_2_5l":81,
    "fanta_1l":54,
    "sprite_1l":54,
    "schweppes_1l":79,
    "uludag_efsane_1_5l":50,
    "colaturka_2_5l":126,
    "colaturka_330ml":30,

    "eti_cikolata_100g":20,
    "eti_gofret_40g":8,
    "eti_karam":30,
    "ulker_cikturk":25,
    "ulker_populer":15,
    "ulker_cubuk_biskuvi":10,

    "torku_sut_1l":48,
    "torku_nutte":22,
    "torku_lokum":18,

    "pinar_sut_1l":42,
    "pinar_yogurt_1kg":68,
    "pinar_peynir_500g":85,
    "pinar_yumurta_12":95,

    "sek_sut_1l":40,
    "sek_yogurt_1kg":65,
    "sek_peynir_500g":80,

    "dardanel_konserve":45,
    "dardanel_lakerda":120,

    "banvit_tavuk":220,
    "lezita_tavuk":210,

    "komili_zeytinyagi_1l":300,
    "yudum_aycicek_5l":650,

    "caykur_cay_500g":90,
    "dogus_cay_500g":75,

    "tat_salca_830g":32,
    "tat_ketcap_500g":18,
    "peyman_fistik_200g":55,

    "ekmek":10,
    "simit":8,

    "nutella_350g":98,
    "nescafe_200g":145,
    "knorr_corba":18,
    "chipsy_150g":28,
    "ruffles_150g":35
}

#Sepet
sepet={}

while True:
    print("\n=== MARKET ===")
    print("1 - Ürünleri Listele")
    print("2 - Sepete Ürün Ekle")
    print("3 - Sepeti Göster")
    print("4 - Ödeme Yap")
    print("5 - Çıkış")

    secim=input("Seçimin: ")

    #Ürünleri Listele
    if secim=="1":
        print("\nÜRÜNLER:")
        for u in urun_fiyatlari:
            print(u,"-",urun_fiyatlari[u],"TL")

    #Sepete Ekle
    elif secim=="2":
        urun=input("Ürün adı: ").lower()

        if urun in urun_fiyatlari:
            adet=int(input("Kaç adet?: "))

            if adet>0:
                if urun in sepet:
                    sepet[urun]+=adet
                else:
                    sepet[urun]=adet
                print("Sepete eklendi.")
            else:
                print("Geçersiz adet!")
        else:
            print("Ürün bulunamadı!")

    #Sepeti Göster
    elif secim=="3":
        if sepet=={}:
            print("Sepet boş.")
        else:
            print("\nSEPET:")
            for u in sepet:
                print(u,"-",sepet[u],"adet")

    #Ödeme
    elif secim=="4":
        if sepet=={}:
            print("Sepet boş.")
        else:
            toplam=0
            for u in sepet:
                toplam+=urun_fiyatlari[u]*sepet[u]

            print("Toplam:",toplam,"TL")

            para=float(input("Verilen para: "))

            if para>=toplam:
                print("Ödeme alındı.")
                print("Para üstü:",para-toplam,"TL")
                sepet={}
            else:
                print("Para yetmedi!")

    #Çıkış
    elif secim=="5":
        print("Çıkış yapıldı.")
        break

    else:
        print("Hatalı seçim!")