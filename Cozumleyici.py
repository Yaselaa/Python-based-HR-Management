import tkinter as tk

# Kütüphane (Buradaki veriler büyük olsa bile program şıklaştıracak)
kutuphane = {
    "isim kısaltmasını ekleyin":"isim açılımını ekleyin"
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
