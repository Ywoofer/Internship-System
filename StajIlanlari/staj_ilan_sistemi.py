import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

# Veritabanı oluşturma
def veritabani_olustur():
    con = sqlite3.connect("staj.db")
    cursor = con.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS staj_ilanlari (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        baslik TEXT NOT NULL,
        kategori TEXT NOT NULL,
        aciklama TEXT,
        konum TEXT,
        tarih TEXT,
        son_tarih TEXT,
        iletisim           
    )
    """)
    con.commit()
    con.close()

veritabani_olustur()

# Otomatik son tarih kontrolü
def son_tarih_kontrol():
    con = sqlite3.connect("staj.db")
    cursor = con.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("DELETE FROM staj_ilanlari WHERE son_tarih < ?", (today,))
    con.commit()
    con.close()

# Geri dön fonksiyonu
def geri_don():
    ana_menu()

# Yönetici girişi
def yonetici_giris_ekrani():
    temizle()
    tk.Label(frame, text="Yönetici Girişi", font=("Arial", 16)).pack()

    tk.Label(frame, text="Şifre:").pack()
    entry_sifre = tk.Entry(frame, show="*")
    entry_sifre.pack()

    def sifre_kontrol():
        if entry_sifre.get() == "admin123":  # Yönetici şifresi
            ilanlari_silme_ekrani()
        else:
            messagebox.showerror("Hata", "Yanlış şifre!")

    tk.Button(frame, text="Giriş", command=sifre_kontrol).pack()
    tk.Button(frame, text="Geri Dön", command=geri_don).pack()

# İlan ekleme ekranı
# İlan ekleme ekranı
def ilan_ekle_ekrani():
    temizle()
    tk.Label(frame, text="Staj İlanı Ekle", font=("Arial", 16)).pack()

    tk.Label(frame, text="Başlık:").pack()
    entry_baslik = tk.Entry(frame)
    entry_baslik.pack()

    tk.Label(frame, text="Kategori:").pack()
    entry_kategori = tk.Entry(frame)
    entry_kategori.pack()

    tk.Label(frame, text="Açıklama:").pack()
    entry_aciklama = tk.Entry(frame)
    entry_aciklama.pack()

    tk.Label(frame, text="Konum:").pack()
    entry_konum = tk.Entry(frame)
    entry_konum.pack()

    tk.Label(frame, text="Tarih (YYYY-MM-DD):").pack()
    entry_tarih = tk.Entry(frame)
    entry_tarih.pack()

    tk.Label(frame, text="Son Tarih (YYYY-MM-DD):").pack()
    entry_son_tarih = tk.Entry(frame)
    entry_son_tarih.pack()

    tk.Label(frame, text="İletişim Bilgisi:").pack()  # Yeni alan
    entry_iletisim = tk.Entry(frame)
    entry_iletisim.pack()

    def ilan_ekle():
        baslik = entry_baslik.get()
        kategori = entry_kategori.get()
        aciklama = entry_aciklama.get()
        konum = entry_konum.get()
        tarih = entry_tarih.get()
        son_tarih = entry_son_tarih.get()
        iletisim = entry_iletisim.get()  # Yeni iletişim bilgisi

        if not baslik or not kategori or not son_tarih or not iletisim:
            messagebox.showwarning("Uyarı", "Tüm zorunlu alanları doldurunuz!")
            return

        con = sqlite3.connect("staj.db")
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO staj_ilanlari (baslik, kategori, aciklama, konum, tarih, son_tarih, iletisim)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (baslik, kategori, aciklama, konum, tarih, son_tarih, iletisim))  # İletişimi de ekle
        con.commit()
        con.close()
        messagebox.showinfo("Başarılı", "Staj ilanı başarıyla eklendi!")
        ilan_ekle_ekrani()

    tk.Button(frame, text="Ekle", command=ilan_ekle).pack()
    tk.Button(frame, text="Geri Dön", command=geri_don).pack()
def ilan_detaylarini_goster(ilan_id):
    con = sqlite3.connect("staj.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM staj_ilanlari WHERE id=?", (ilan_id,))
    ilan = cursor.fetchone()
    con.close()

    if ilan:
        detay_ekrani = tk.Toplevel(root)  # Yeni bir pencere oluşturuyoruz
        detay_ekrani.title("İlan Detayı")
        detay_ekrani.geometry("400x300")

        tk.Label(detay_ekrani, text=f"Başlık: {ilan[1]}", font=("Arial", 14)).pack(pady=5)
        tk.Label(detay_ekrani, text=f"Kategori: {ilan[2]}", font=("Arial", 12)).pack(pady=5)
        tk.Label(detay_ekrani, text=f"Açıklama: {ilan[3]}", font=("Arial", 12)).pack(pady=5)
        tk.Label(detay_ekrani, text=f"Konum: {ilan[4]}", font=("Arial", 12)).pack(pady=5)
        tk.Label(detay_ekrani, text=f"Tarih: {ilan[5]}", font=("Arial", 12)).pack(pady=5)
        tk.Label(detay_ekrani, text=f"Son Tarih: {ilan[6]}", font=("Arial", 12)).pack(pady=5)
        tk.Label(detay_ekrani, text=f"İletişim: {ilan[7]}", font=("Arial", 12)).pack(pady=5)

        tk.Button(detay_ekrani, text="Kapat", command=detay_ekrani.destroy).pack(pady=10)


# İlanları görüntüleme ekranı
def ilanlari_goruntule_ekrani():
    temizle()
    tk.Label(frame, text="Staj İlanlarını Görüntüle", font=("Arial", 16)).pack()

    tk.Label(frame, text="Kategori Seçin:").pack()
    con = sqlite3.connect("staj.db")
    cursor = con.cursor()
    cursor.execute("SELECT DISTINCT kategori FROM staj_ilanlari")
    kategoriler = [row[0] for row in cursor.fetchall()]
    con.close()

    kategori_combobox = ttk.Combobox(frame, values=kategoriler)
    kategori_combobox.pack()

    listbox = tk.Listbox(frame, width=50)
    listbox.pack()

    def ilanlari_listele():
        con = sqlite3.connect("staj.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM staj_ilanlari WHERE kategori=?", (kategori_combobox.get(),))
        ilanlar = cursor.fetchall()
        con.close()

        listbox.delete(0, tk.END)
        for ilan in ilanlar:
            listbox.insert(tk.END, f"{ilan[0]} - {ilan[1]} - {ilan[7]}")  # İletişimi de ekle

    def ilan_secilince_detaylari_goster(event):
        secilen = listbox.curselection()
        if secilen:
            ilan_id = listbox.get(secilen).split(" - ")[0]  # İlan ID'sini alıyoruz
            ilan_detaylarini_goster(ilan_id)

    listbox.bind("<Double-1>", ilan_secilince_detaylari_goster)

    tk.Button(frame, text="Listele", command=ilanlari_listele).pack()
    tk.Button(frame, text="Geri Dön", command=geri_don).pack()
# İlan silme ekranı (Yönetici)
def ilanlari_silme_ekrani():
    temizle()
    tk.Label(frame, text="Staj İlanlarını Sil (Yönetici)", font=("Arial", 16)).pack()

    listbox = tk.Listbox(frame, width=50)
    listbox.pack()

    def ilanlari_listele():
        con = sqlite3.connect("staj.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM staj_ilanlari")
        ilanlar = cursor.fetchall()
        con.close()

        listbox.delete(0, tk.END)
        for ilan in ilanlar:
            listbox.insert(tk.END, f"{ilan[0]} - {ilan[1]}")

    def ilan_sil():
        secilen = listbox.curselection()
        if secilen:
            ilan_id = listbox.get(secilen).split(" - ")[0]
            con = sqlite3.connect("staj.db")
            cursor = con.cursor()
            cursor.execute("DELETE FROM staj_ilanlari WHERE id=?", (ilan_id,))
            con.commit()
            con.close()
            messagebox.showinfo("Başarılı", "İlan başarıyla silindi!")
            ilanlari_listele()

    tk.Button(frame, text="Listele", command=ilanlari_listele).pack()
    tk.Button(frame, text="Sil", command=ilan_sil).pack()
    tk.Button(frame, text="Geri Dön", command=geri_don).pack()

# Ana menü
def ana_menu():
    temizle()
    son_tarih_kontrol()  # Süresi dolan ilanları siler
    tk.Label(frame, text="Staj İlan Sistemi", font=("Arial", 20)).pack()

    tk.Button(frame, text="İş Veren (Staj İlanı Ekle)", width=30, command=ilan_ekle_ekrani).pack(pady=10)
    tk.Button(frame, text="Öğrenci (İlanları Görüntüle)", width=30, command=ilanlari_goruntule_ekrani).pack(pady=10)
    tk.Button(frame, text="Yönetici Girişi", width=30, command=yonetici_giris_ekrani).pack(pady=10)

# Frame'i temizleme
def temizle():
    for widget in frame.winfo_children():
        widget.destroy()

# Ana pencere
root = tk.Tk()
root.title("Staj İlan Sistemi")
root.geometry("800x400")
root.resizable(True, True)

frame = tk.Frame(root)
frame.pack(expand=True, fill="both")

ana_menu()

root.mainloop()
