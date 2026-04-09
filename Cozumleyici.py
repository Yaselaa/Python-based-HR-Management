import tkinter as tk

# Kütüphane (Buradaki veriler büyük olsa bile program şıklaştıracak)
kutuphane = {
    "ABD": "ASLI BÜŞRA DEMİRBAŞ", "AFD": "ALİ FURKAN DAYI", "AB": "AYKUT BÜRME","AMH":"ARSLAN MUSTAFA HOT" ,"EYA":"EMRE YİĞİT ARAS","AY":"ATİKE YELTEPE",
    "ACS": "AYŞENUR CEREN SEYHUN", "AU": "ALPEREN ÜREY", "BA": "BUKET ASLANER",
    "BEK": "BERK KAYALI", "BB": "BURAK BAYRAKTAR",
    "BO": "BURAK ÖKTEN", "DC": "DURALİ ÇAM", "DS": "DERYA SABANCI",
    "DT": "DOĞAN TÜRE", "EA": "ENES ARSLAN", "EAR": "EMRE ARTIK",
    "EAT": "ERKAM ATA", "ET": "EMRE TAMER", "EEE": "ENSAR EMİN ERSOY",
    "EE": "ENES EROL", "FC": "FURKAN CENKIŞ", "FS": "FADİME ŞAHİN",
    "FE": "FERHAT ERSAN", "GK": "GÜLER KOLLAYAN", "GOS": "GAMZE OCAK ŞENOL",
    "İBC": "İREM BETÜL CENGE", "İO": "İSMAİL ÖLÇER", "İEB": "İSMAİL ENES BİLGİN",
    "KUO": "KENAN UMUT OLPAK", "MK": "MEHMET KOLLAYAN", "MBT": "MUSTAFA BURAK TOKSOY",
    "MEY": "MUHAMMED EMİN YÜCEL", "MMK": "MUHAMMED MUSTAFA KÖSE",
    "MTT": "MEHMET TUĞBERK TÜRKOĞLU", "MOV": "MUSTAFA OVACIKLI", "MOZ": "MEHMET ÖZTÜRK",
    "NBY": "NECATİ BERKAY YEDİLER", "NGA": "NURAY GENÇER AYDIN", "NT": "NİYAZİ TUNÇ",
    "OA": "ÖZLEM ARSLAN", "OK": "OĞUZHAN KARABAL", "PS": "PINAR SÖNMEZ",
    "RC": "RUMEYSA COŞGUNYÜREK", "SA": "SAMET AYDEMİR", "SS": "SERKAN ŞEN","KBC":"KADİR BUĞRA CENGİZ",
    "TK": "TUNCAY KOÇAK", "TU": "TÜLAY ÜNAL", "UB": "UĞUR BOZKIR", "UO": "UĞUR ÖZBEN","HS":"HASAN ŞENER"
}

def sorgula(event=None):
    anahtar = entry.get().strip().upper()
    
    if anahtar in kutuphane:
        # .title() metodu her kelimenin ilk harfini büyük, diğerlerini küçük yapar
        ham_isim = kutuphane[anahtar]
        sik_isim = ham_isim.title() 
        
        label_sonuc.config(text=sik_isim, fg="#06173B")
    else:
        label_sonuc.config(text="Kısaltma bulunamadı!", fg="#06173B")

# --- Arayüz Tasarımı ---
root = tk.Tk()
root.title("İsim Kayıt Sistemi")
root.geometry("400x300")
root.configure(bg="#C3C4D6")

# Başlık
tk.Label(root, text="Kısaltma Sorgulama", font=("Helvetica", 14, "bold"), bg="#C3C4D6", fg="#06173B").pack(pady=20)

# Giriş Kutusu
entry = tk.Entry(root, font=("Helvetica", 14), justify="center", bd=1, relief="solid")
entry.pack(pady=10, padx=40, ipady=5)
entry.focus_set()
entry.bind("<Return>", sorgula)

# Buton
btn = tk.Button(root, text="Sorgula", command=sorgula, font=("Helvetica", 10, "bold"), 
                bg="#06173B", fg="#C3C4D6", width=20, relief="flat", cursor="hand2")
btn.pack(pady=15)

# Sonuç Alanı
label_sonuc = tk.Label(root, text="", font=("Helvetica", 14, "italic"), 
                       bg="#C3C4D6",fg="#06173B", wraplength=350)
label_sonuc.pack(pady=20)

root.mainloop()