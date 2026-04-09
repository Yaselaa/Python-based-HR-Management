import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys
from PIL import Image, ImageTk  
class ModernLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        # --- AYARLAR ---
        self.db_yolu = r"C:\Users\stajyer\Desktop\database"
        # Logonun adı neyse buraya onu yaz 
        self.logo_adi = "yenilogo.png"    
        self.title("ARTI IK - Toolkits")
        self.geometry("850x650")
        self.configure(bg="#C3C4D6")
        # RENK PALETİ
        self.ozel_kirmizi = "#06173B"  # Senin istediğin yeni renk kodu
        self.koyu_mavi = "#06173B"     # Yan menü arka planı
        self.acik_gri = "#C3C4D6"      # Buton arka planı
        self.araclar = [
            ("Aday Kayıt Sistemi", "Aday_Kayit.py"),
            ("Mazeret İzni Takibi", "Mazeret_Izin.py"),
            ("Yıllık İzin Takibi", "Yillik_Izin.py"),
            ("Kısaltma Çözümleme", "Cozumleyici.py"),
            ("Isim Düzenleme", "proisim.py")
        ]
        self.arayuz_olustur()
    def arayuz_olustur(self):
        # (Sidebar)
        sidebar = tk.Frame(self, bg= self.koyu_mavi, width=280, height=650)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        # --- LOGO YÜKLEME ---
        logo_tam_yol = os.path.normpath(os.path.join(self.db_yolu, self.logo_adi))
        
        if os.path.exists(logo_tam_yol):
            try:
                img = Image.open(logo_tam_yol)
                # Logoyu alana sığacak şekilde boyutlandırır (150x150 idealdir)
                img = img.resize((250, 250), Image.Resampling.LANCZOS)
                self.logo_image = ImageTk.PhotoImage(img)
                
                logo_label = tk.Label(sidebar, image=self.logo_image, bg=self.koyu_mavi)
                logo_label.pack(pady=(40, 10))
            except Exception as e:
                tk.Label(sidebar, text="ARTI İK", fg="white", bg=self.ozel_kirmizi, font=("Helvetica", 20, "bold")).pack(pady=40)
        else:
            tk.Label(sidebar, text="ARTI İK", fg="white", bg=self.ozel_kirmizi, font=("Helvetica", 20, "bold")).pack(pady=40)

        tk.Label(sidebar, text="Maşallah", fg="white", 
                 bg=self.koyu_mavi, font=("Helvetica", 14 , "bold")).pack(side="bottom", pady=20)

        # 2. SAĞ İÇERİK ALANI
        ana_ekran = tk.Frame(self, bg="#C3C4D6")
        ana_ekran.pack(side="right", expand=True, fill="both", padx=40, pady=20)

        tk.Label(ana_ekran, text="Hızlı Erişim Paneli", fg="#06173B", bg="#C3C4D6",
                 font=("Helvetica", 22, "bold")).pack(anchor="w", pady=(0, 80))

        # Butonları oluştururken yeni kırmızı rengini kullanıyoruz
        for metin, dosya in self.araclar:
            self.modern_buton_ekle(ana_ekran, metin, dosya)

    def modern_buton_ekle(self, parent, metin, dosya):
        btn_frame = tk.Frame(parent, bg="#C3C4D6")
        btn_frame.pack(fill="x", pady=6)

        btn = tk.Button(btn_frame, text=f"  ▶  {metin}", 
                       bg=self.acik_gri, fg=self.koyu_mavi,
                       activebackground=self.ozel_kirmizi, activeforeground="#C3C4D6",
                       font=("Helvetica", 11), anchor="w",
                       relief="flat", bd=0, cursor="hand2",
                       command=lambda d=dosya: self.dosyayi_calistir(d))
        
        # Sol taraftaki şerit rengi senin verdiğin #913619 oldu
        sol_serit = tk.Frame(btn, bg=self.ozel_kirmizi, width=5)
        sol_serit.pack(side="left", fill="y")
        
        btn.pack(fill="x", ipady=12)

    def dosyayi_calistir(self, dosya_adi):
        tam_yol = os.path.normpath(os.path.join(self.db_yolu, dosya_adi))
        if os.path.exists(tam_yol):
            try:
                subprocess.Popen(["pythonw", tam_yol], cwd=self.db_yolu, shell=False, creationflags=0x08000000)
            except Exception as e:
                messagebox.showerror("Hata", f"Sistem hatası: {e}")
        else:
            messagebox.showwarning("Dosya Bulunamadı", f"Yol bulunamadı:\n{tam_yol}")

if __name__ == "__main__":
    app = ModernLauncher()
    app.mainloop()