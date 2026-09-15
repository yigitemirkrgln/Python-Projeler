import tkinter as tk
from tkinter import ttk
import math

# ---------------- HESAPLAMA ----------------
def hesapla():
    try:
        v = [float(e.get()) for e in entries]
        s = secim.get()

        if s == "Kare":
            a = v[0]
            alan = a * a
            cevre = 4 * a

        elif s == "Dikdörtgen":
            a, b = v
            alan = a * b
            cevre = 2 * (a + b)

        elif s == "Üçgen":
            taban, h, a, b, c = v
            alan = (taban * h) / 2
            cevre = a + b + c

        elif s == "Daire":
            r = v[0]
            alan = math.pi * r * r
            cevre = 2 * math.pi * r

        elif s == "Paralelkenar":
            taban, h, yan = v
            alan = taban * h
            cevre = 2 * (taban + yan)

        elif s == "Yamuk":
            a, b, h, c, d = v
            alan = (a + b) * h / 2
            cevre = a + b + c + d

        elif s == "Eşkenar Üçgen":
            a = v[0]
            alan = (math.sqrt(3) / 4) * a * a
            cevre = 3 * a

        elif s == "Dik Üçgen":
            a, b = v
            c = math.sqrt(a*a + b*b)
            alan = (a * b) / 2
            cevre = a + b + c

        elif s == "Elips":
            a, b = v
            alan = math.pi * a * b
            cevre = 2 * math.pi * math.sqrt((a*a + b*b) / 2)

        elif s == "Beşgen":
            a = v[0]
            alan = (5 * a * a) / (4 * math.tan(math.pi / 5))
            cevre = 5 * a

        sonuc.set(f"Alan: {alan:.2f}\nÇevre: {cevre:.2f}")

    except:
        sonuc.set("❌ Hatalı veya eksik giriş!")

# ---------------- DİNAMİK ALANLAR ----------------
def alanlari_guncelle(*args):
    for w in alan_frame.winfo_children():
        w.destroy()
    entries.clear()

    alanlar = {
        "Kare": ["Kenar"],
        "Dikdörtgen": ["Kısa Kenar", "Uzun Kenar"],
        "Üçgen": ["Taban", "Yükseklik", "1.Kenar", "2.Kenar", "3.Kenar"],
        "Daire": ["Yarıçap"],
        "Paralelkenar": ["Taban", "Yükseklik", "Yan Kenar"],
        "Yamuk": ["Alt Taban", "Üst Taban", "Yükseklik", "Sol Kenar", "Sağ Kenar"],
        "Eşkenar Üçgen": ["Kenar"],
        "Dik Üçgen": ["1. Dik Kenar", "2. Dik Kenar"],
        "Elips": ["Büyük Yarıçap", "Küçük Yarıçap"],
        "Beşgen": ["Kenar"]
    }

    for a in alanlar[secim.get()]:
        tk.Label(
            alan_frame,
            text=a,
            bg="#f0f8ff",
            fg="#003366",
            font=("Arial", 10, "bold")
        ).pack(pady=2)

        e = tk.Entry(
            alan_frame,
            bg="#fffacd",
            fg="#000000",
            justify="center"
        )
        e.pack(pady=2)
        entries.append(e)

# ---------------- PENCERE ----------------
root = tk.Tk()
root.title("Geometrik Şekil Alan & Çevre")
root.geometry("380x600")
root.configure(bg="#f0f8ff")

# Başlık
tk.Label(
    root,
    text="📐 Geometrik Şekil Hesaplama",
    font=("Arial", 14, "bold"),
    bg="#4682b4",
    fg="white",
    pady=10
).pack(fill="x")

# Şekil seçimi
tk.Label(
    root,
    text="Şekil Seçiniz",
    bg="#f0f8ff",
    font=("Arial", 11)
).pack(pady=5)

secim = tk.StringVar()
combo = ttk.Combobox(
    root,
    values=[
        "Kare", "Dikdörtgen", "Üçgen", "Daire",
        "Paralelkenar", "Yamuk", "Eşkenar Üçgen",
        "Dik Üçgen", "Elips", "Beşgen"
    ],
    textvariable=secim,
    state="readonly"
)
combo.pack()

combo.bind("<<ComboboxSelected>>", alanlari_guncelle)

alan_frame = tk.Frame(root, bg="#f0f8ff")
alan_frame.pack(pady=10)

entries = []

# Hesapla Butonu
tk.Button(
    root,
    text="HESAPLA",
    command=hesapla,
    bg="#32cd32",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=20,
    pady=5
).pack(pady=10)

# Sonuç
sonuc = tk.StringVar()
tk.Label(
    root,
    textvariable=sonuc,
    bg="#e6e6fa",
    fg="#4b0082",
    font=("Arial", 12),
    relief="ridge",
    width=25,
    height=3
).pack(pady=10)

root.mainloop()
