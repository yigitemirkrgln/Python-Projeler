# HATIRLATMA PROGRAMI

import tkinter as tk
from tkinter import messagebox, filedialog
from plyer import notification
import schedule
import time
import threading
import json
import datetime
import winsound
import os

DOSYA = "hatirlatmalar.json"
AYAR_DOSYA = "ayarlar.json"

# Varsayılan Ayarlar
ayarlar = {
    "ses_acik": True,
    "ses_dosya": None,
    "tema": "acik",  # acik / karanlik
    "otomatik_sil": True
}

# Açılış Ekranı
def acilis_ekrani():
    splash = tk.Toplevel()
    splash.overrideredirect(True)
    splash.geometry("400x200+500+300")
    tk.Label(splash, text="HATIRLATMA PRO", font=("Arial", 20, "bold")).pack(pady=30)
    tk.Label(splash, text="Yükleniyor...", font=("Arial", 12)).pack()
    splash.after(2000, splash.destroy)

# Ayar Yükle / Kaydet
def ayar_yukle():
    global ayarlar
    if os.path.exists(AYAR_DOSYA):
        with open(AYAR_DOSYA, "r", encoding="utf-8") as f:
            ayarlar.update(json.load(f))


def ayar_kaydet():
    with open(AYAR_DOSYA, "w", encoding="utf-8") as f:
        json.dump(ayarlar, f, ensure_ascii=False, indent=4)

# Bildirim
def bildirim_gonder(mesaj, index=None):
    if ayarlar["ses_acik"]:
        if ayarlar["ses_dosya"] and os.path.exists(ayarlar["ses_dosya"]):
            winsound.PlaySound(ayarlar["ses_dosya"], winsound.SND_FILENAME | winsound.SND_ASYNC)
        else:
            winsound.Beep(1000, 600)

    notification.notify(title="🔔 Hatırlatma", message=mesaj, timeout=10)

    if ayarlar["otomatik_sil"] and index is not None:
        try:
            liste.delete(index)
            h = yukle()
            h.pop(index)
            kaydet(h)
        except:
            pass

# JSON
def yukle():
    try:
        with open(DOSYA, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def kaydet(liste):
    with open(DOSYA, "w", encoding="utf-8") as f:
        json.dump(liste, f, ensure_ascii=False, indent=4)

# Scheduler
def scheduler_baslat():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Tema
def tema_uygula():
    if ayarlar["tema"] == "karanlik":
        bg, fg = "#1e1e1e", "white"
    else:
        bg, fg = "white", "black"

    root.configure(bg=bg)
    for w in root.winfo_children():
        try:
            w.configure(bg=bg, fg=fg)
        except:
            pass


def tema_degistir():
    ayarlar["tema"] = "karanlik" if ayarlar["tema"] == "acik" else "acik"
    ayar_kaydet()
    tema_uygula()

# Ayarlar Penceresi
def ayarlar_penceresi():
    win = tk.Toplevel(root)
    win.title("Ayarlar")
    win.geometry("300x250")

    ses_var = tk.BooleanVar(value=ayarlar["ses_acik"])
    oto_var = tk.BooleanVar(value=ayarlar["otomatik_sil"])

    def kaydet_local():
        ayarlar["ses_acik"] = ses_var.get()
        ayarlar["otomatik_sil"] = oto_var.get()
        ayar_kaydet()
        win.destroy()

    tk.Checkbutton(win, text="Ses Açık", variable=ses_var).pack(pady=5)
    tk.Checkbutton(win, text="Hatırlatma sonrası otomatik sil", variable=oto_var).pack(pady=5)

    def ses_sec():
        yol = filedialog.askopenfilename(filetypes=[("WAV Dosyası", "*.wav")])
        if yol:
            ayarlar["ses_dosya"] = yol
            ayar_kaydet()

    tk.Button(win, text="Ses Dosyası Seç", command=ses_sec).pack(pady=5)
    tk.Button(win, text="Kaydet", command=kaydet_local).pack(pady=10)

# Hatırlatma Ekle
def hatirlatma_ekle():
    tarih = tarih_entry.get()
    saat = saat_entry.get()
    mesaj = mesaj_entry.get()

    if not tarih or not saat or not mesaj:
        messagebox.showerror("Hata", "Tüm alanları doldurun")
        return

    h = yukle()
    index = len(h)
    schedule.every().day.at(saat).do(bildirim_gonder, mesaj, index)

    h.append({"tarih": tarih, "saat": saat, "mesaj": mesaj})
    kaydet(h)

    liste.insert(tk.END, f"{tarih} {saat} - {mesaj}")

# ANA UI
root = tk.Tk()
root.title("Hatırlatma Programı Yiğit Tarafından")
root.geometry("600x600")

acilis_ekrani()
ayar_yukle()

tk.Button(root, text="Ayarlar", command=ayarlar_penceresi).pack(pady=5)
tk.Button(root, text="Açık / Karanlık Tema", command=tema_degistir).pack(pady=5)

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Tarih (YYYY-AA-GG)").grid(row=0, column=0)
tarih_entry = tk.Entry(frame)
tarih_entry.grid(row=0, column=1)

tk.Label(frame, text="Saat (SS:DD)").grid(row=1, column=0)
saat_entry = tk.Entry(frame)
saat_entry.grid(row=1, column=1)

tk.Label(frame, text="Mesaj").grid(row=2, column=0)
mesaj_entry = tk.Entry(frame)
mesaj_entry.grid(row=2, column=1)

# Buton
tk.Button(root, text="Hatırlatma Ekle", command=hatirlatma_ekle).pack(pady=10)

# Liste
liste = tk.Listbox(root, width=70)
liste.pack(pady=10)

threading.Thread(target=scheduler_baslat, daemon=True).start()
tema_uygula()
root.mainloop()
