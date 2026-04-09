import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import fitz  
from PIL import Image, ImageTk

class PDFMasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF İşleme Merkezi")
        self.root.geometry("1100x850")
        self.root.withdraw()  # Ana pencereyi seçim yapılana kadar gizle

        # 1. ADIM: DOSYA SEÇİMİ
        self.selected_file = filedialog.askopenfilename(
            title="İşlemek istediğiniz PDF dosyasını seçin",
            filetypes=[("PDF Dosyaları", "*.pdf")]
        )

        if not self.selected_file:
            messagebox.showinfo("İptal", "Dosya seçilmediği için çıkılıyor.")
            self.root.destroy()
            return

        # Dosya yolları kurulumu
        self.base_dir = os.path.dirname(self.selected_file)
        self.input_folder = os.path.join(self.base_dir, "islem_bekleyen_sayfalar")
        self.output_folder = os.path.join(self.base_dir, "isimlendirilmis_pdfler")

        if not os.path.exists(self.input_folder): os.makedirs(self.input_folder)
        if not os.path.exists(self.output_folder): os.makedirs(self.output_folder)

        # 2. ADIM: OTOMATİK BÖLME
        self.split_selected_pdf()

        # İşlenecek sayfaları listele
        self.pdf_list = [f for f in os.listdir(self.input_folder) if f.lower().endswith('.pdf')]
        self.current_index = 0

        if not self.pdf_list:
            messagebox.showwarning("Hata", "İşlenecek sayfa bulunamadı!")
            self.root.destroy()
            return

        self.root.deiconify() 
        self.setup_ui()
        self.load_pdf()

    def split_selected_pdf(self):
        """Seçilen tekil PDF'i sayfalara bölüp geçici klasöre atar."""
        try:
            doc = fitz.open(self.selected_file)
            base_name = os.path.splitext(os.path.basename(self.selected_file))[0]
            
            for i in range(len(doc)):
                yeni_pdf = fitz.open()
                yeni_pdf.insert_pdf(doc, from_page=i, to_page=i)
                out_name = f"SAYFA_{i+1}_{base_name}.pdf"
                yeni_pdf.save(os.path.join(self.input_folder, out_name))
                yeni_pdf.close()
            doc.close()
        except Exception as e:
            messagebox.showerror("Bölme Hatası", f"PDF bölünürken hata oluştu: {e}")

    def setup_ui(self):
        # --- STİL TANIMLAMALARI ---
        style = ttk.Style()
        style.theme_use('clam') 
        
        # Readonly (sadece okunur) modundaki renkleri zorlamak için MAP kullanıyoruz
        style.map("Custom.TCombobox",
                  fieldbackground=[('readonly', "#C3C4D6")],
                  background=[('readonly', "#C3C4D6")],
                  foreground=[('readonly', "black")])

        style.configure("Custom.TCombobox",
                        fieldbackground="#C3C4D6",
                        background="#C3C4D6",
                        foreground="black",
                        arrowcolor="black",
                        borderwidth=1,
                        relief="flat")

        # Açılır liste menüsü ayarları (Tıklandığında açılan liste)
        self.root.option_add("*TCombobox*Listbox.background", "#C3C4D6")
        self.root.option_add("*TCombobox*Listbox.foreground", "black")
        self.root.option_add("*TCombobox*Listbox.selectBackground", "#06173B")
        self.root.option_add("*TCombobox*Listbox.selectForeground", "white")

        # --- ARAYÜZ PANELLERİ ---
        # Sol Panel: Önizleme
        self.preview_frame = tk.Frame(self.root, bg="#C3C4D6")
        self.preview_frame.pack(side="left", fill="both", expand=True)
        self.canvas = tk.Canvas(self.preview_frame, bg="#C3C4D6", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=70, pady=50)

        # Sağ Panel: Kontroller
        self.control_frame = tk.Frame(self.root, width=350, padx=100, pady=100, bg="#06173B")
        self.control_frame.pack(side="right", fill="both")

        # 1. Form Türü
        tk.Label(self.control_frame, text="1. Form Türü", font=("Helvetica", 10, "bold"), fg="white", bg="#06173B").pack(anchor="w")
        self.prefixes = {
            "Yıllık İzin": "FRM-34_yillik_ucretli_izin_formu",
            "Mazeret İzni": "FRM-37_mazeret_izin_formu",
            "Şehir Dışı Görev": "FRM-30_sehirdisi_yurtdisi_gorevlendirme_formu",
            "Görevlendirme": "FRM-76_gorevlendirme_formu",
            "Diğer (Özel İsim)": "DIGER"
        }
        self.form_var = tk.StringVar()
        self.form_combo = ttk.Combobox(self.control_frame, 
                                       textvariable=self.form_var, 
                                       values=list(self.prefixes.keys()), 
                                       state="readonly", 
                                       font=("Helvetica", 11),
                                       style="Custom.TCombobox")
        self.form_combo.pack(fill="x", pady=(5, 15))
        self.form_combo.current(0)

        # 2. Çalışan Kodu
        tk.Label(self.control_frame, text="Çalışan Kodu", font=("Helvetica", 10, "bold"), fg="white", bg="#06173B").pack(anchor="w")
        self.name_var = tk.StringVar()
        self.name_var.trace_add("write", lambda *args: self.name_var.set(self.name_var.get().upper()))
        self.entry_name = tk.Entry(self.control_frame, 
                                   textvariable=self.name_var, 
                                   font=("Helvetica", 12),
                                   bg="#C3C4D6",
                                   fg="black",
                                   insertbackground="black",
                                   relief="flat")
        self.entry_name.pack(fill="x", pady=(5, 15))

        # 3. Tarih
        tk.Label(self.control_frame, text="Tarih", font=("Helvetica", 10, "bold"), fg="white", bg="#06173B").pack(anchor="w")
        self.entry_date = tk.Entry(self.control_frame, 
                                   font=("Helvetica", 12),
                                   bg="#C3C4D6",
                                   fg="black",
                                   insertbackground="black",
                                   relief="flat")
        self.entry_date.pack(fill="x", pady=(5, 15))

        # Kaydet Butonu
        self.btn_save = tk.Button(self.control_frame, text="Kaydet", bg="#C3C4D6", fg="#06173B", 
                                  font=("Helvetica", 15, "bold"), height=3, command=self.rename_and_next,
                                  activebackground="#A8A9B8")
        self.btn_save.pack(fill="x", pady=20)

        self.lbl_status = tk.Label(self.control_frame, text="", font=("Helvetica", 9), fg="#C3C4D6", bg="#06173B")
        self.lbl_status.pack(side="bottom", pady=10)

        self.root.bind('<Return>', lambda event: self.rename_and_next())

    def load_pdf(self):
        if self.current_index < len(self.pdf_list):
            pdf_path = os.path.join(self.input_folder, self.pdf_list[self.current_index])
            try:
                doc = fitz.open(pdf_path)
                page = doc.load_page(0)
                pix = page.get_pixmap(matrix=fitz.Matrix(1.1, 1.1))
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img.thumbnail((700, 850))
                self.photo = ImageTk.PhotoImage(img)
                self.canvas.delete("all")
                self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
                self.lbl_status.config(text=f"Dosya: {self.current_index + 1} / {len(self.pdf_list)}")
                doc.close()
                self.entry_name.focus_set()
            except:
                self.current_index += 1
                self.load_pdf()
        else:
            messagebox.showinfo("Bitti", "Tüm sayfalar başarıyla isimlendirildi!")
            self.root.destroy()

    def rename_and_next(self):
        user_input = self.name_var.get().strip()
        date_val = self.entry_date.get().strip()
        if not user_input or not date_val: return

        prefix = self.prefixes[self.form_var.get()]
        new_name = f"{user_input}_{date_val}.pdf" if prefix == "DIGER" else f"{prefix}_{user_input}_{date_val}.pdf"
        
        try:
            os.rename(os.path.join(self.input_folder, self.pdf_list[self.current_index]), 
                      os.path.join(self.output_folder, new_name))
            self.name_var.set("")
            self.entry_date.delete(0, tk.END)
            self.current_index += 1
            self.load_pdf()
        except Exception as e:
            messagebox.showerror("Hata", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMasterApp(root)
    root.mainloop()