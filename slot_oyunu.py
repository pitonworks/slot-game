import random
import tkinter as tk
from tkinter import messagebox, ttk
import time
import math

# Font ayarları için yeni bir değişken ekleyelim
MAC_FONT = ("SF Pro Display", "Helvetica Neue", "Arial")  # Mac OS tarzı fontlar

class ModernSlotMakinesi:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Luxury Vegas Slots ✨")
        self.root.geometry("1400x900")
        self.root.configure(bg='#0D1117')
        
        self.bakiye = 10000
        self.bahis = 50
        self.semboller = {
            '👑': 1000,    # Kral tacı - Jackpot
            '🌟': 500,     # Parlayan yıldız
            '🎯': 250,     # Hedef
            '🎪': 200,     # Sirk çadırı
            '🎨': 150,     # Sanat paleti
            '🌈': 100,     # Gökkuşağı
            '🎭': 75,      # Tiyatro maskeleri
            '🎪': 50,      # Sirk
            '🎰': 30,      # Slot makinesi
            '💫': 20       # Yıldız
        }
        
        self.efekt_sembolleri = ['✨', '💫', '⭐', '🌟', '💥', '🌈']
        
        # Klavye kontrolleri için bind işlemleri
        self.root.bind('<space>', lambda e: self.slot_cevir())  # Boşluk tuşu ile çevir
        self.root.bind('<Left>', lambda e: self.bahis_degistir(-50))  # Sol ok ile bahis azalt
        self.root.bind('<Right>', lambda e: self.bahis_degistir(50))  # Sağ ok ile bahis artır
        self.root.bind('<Return>', lambda e: self.bahis_degistir(1000))  # Enter ile max bahis
        self.root.bind('a', lambda e: self.auto_spin())  # 'a' tuşu ile auto spin
        
        # Animasyon durumları
        self.animating = False
        self.explosion_particles = []
        
        # Animasyon hızı için yeni değişkenler
        self.animation_speed = 0.01  # Daha hızlı animasyon
        self.spin_duration = 5  # Daha kısa spin süresi
        
        # Ana container frame
        self.main_container = tk.Frame(self.root, bg='#0D1117')
        self.main_container.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Canvas ve Scrollbar oluştur
        self.canvas = tk.Canvas(self.main_container, bg='#0D1117', highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.main_container, orient="vertical", command=self.canvas.yview)
        
        # Scroll edilecek frame
        self.scrollable_frame = tk.Frame(self.canvas, bg='#0D1117')
        
        # Canvas'a frame'i yerleştir
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Scrollbar ayarları
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Mouse wheel binding
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.scrollable_frame.bind("<Configure>", self._configure_scroll_region)
        self.canvas.bind("<Configure>", self._configure_canvas_window)
        
        # Layout
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.create_widgets()
        self.neon_effect()
        
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def _configure_scroll_region(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def _configure_canvas_window(self, event):
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def create_widgets(self):
        # Vegas tarzı başlık
        title_frame = tk.Frame(self.scrollable_frame, bg='#0D1117')
        title_frame.pack(pady=20)
        
        # Lüks görünümlü logo/başlık
        self.baslik = tk.Label(title_frame, 
                             text="🎰 LUXURY VEGAS SLOTS 🎰",
                             font=(MAC_FONT[0], 48, 'bold'),
                             bg='#0D1117',
                             fg='#FFD700')
        self.baslik.pack()
        
        # Alt başlık
        self.alt_baslik = tk.Label(title_frame,
                                 text="♦ PREMIUM EDITION ♦",
                                 font=(MAC_FONT[0], 18),
                                 bg='#0D1117',
                                 fg='#E5E4E2')
        self.alt_baslik.pack()
        
        # Ana oyun çerçevesi
        self.game_frame = tk.Frame(self.scrollable_frame, bg='#1F2937', 
                                 relief='raised', borderwidth=5)
        self.game_frame.pack(padx=20, pady=10)
        
        # Slot makinesi ekranı (10x4 matrix)
        self.slot_frame = tk.Frame(self.game_frame, bg='#111827', 
                                 padx=30, pady=30)
        self.slot_frame.pack()
        
        # Slot çarkları (10 sütun, 4 satır)
        self.slot_labels = []
        for i in range(10):  # 10 sütun
            frame = tk.Frame(self.slot_frame, 
                           bg='#111827', 
                           width=80, 
                           height=320,
                           relief='sunken',
                           borderwidth=3)
            frame.pack_propagate(False)
            frame.pack(side=tk.LEFT, padx=5)
            
            # Her sütun için 4 sembol göster
            column_labels = []
            for j in range(4):  # 4 satır
                label = tk.Label(frame, 
                               text="?",
                               font=('Arial', 32),
                               bg='#111827',
                               fg='white')
                label.pack(expand=True)
                column_labels.append(label)
            self.slot_labels.append(column_labels)
        
        # Modern bilgi paneli
        self.create_info_panel()
        
        # Kontrol butonları
        self.create_control_buttons()
        
        # Ödeme tablosu
        self.create_modern_paytable()
        
        # Klavye kısayolları bilgisi ekle
        shortcuts_frame = tk.Frame(self.scrollable_frame, bg='#1F2937', 
                                 relief='sunken', borderwidth=2)
        shortcuts_frame.pack(pady=5, padx=20, fill='x')
        
        shortcuts_text = """
        🎮 KLAVYE KONTROLLERI:
        SPACE: Çevir | ← →: Bahis Ayarla | ENTER: Max Bahis | A: Auto Spin
        """
        tk.Label(shortcuts_frame, text=shortcuts_text, font=('Arial', 12), 
                bg='#1F2937', fg='#FFD700').pack(pady=5)
        
        # Modern buton stilleri için yeni bir stil oluştur
        self.create_modern_button_style()
    
    def create_modern_button_style(self):
        # Modern buton stili
        style = ttk.Style()
        style.configure('Modern.TButton',
                       font=(MAC_FONT[0], 14, 'bold'),
                       padding=10,
                       background='#2E3440',
                       foreground='white')
        
        style.map('Modern.TButton',
                 background=[('active', '#4C566A')],
                 foreground=[('active', 'white')])
    
    def create_info_panel(self):
        info_frame = tk.Frame(self.scrollable_frame, bg='#0D1117')
        info_frame.pack(pady=20)
        
        styles = {
            'bakiye': {'bg': '#B8860B', 'text': 'BAKİYE', 'icon': '💰'},
            'bahis': {'bg': '#4169E1', 'text': 'BAHİS', 'icon': '🎲'},
            'kazanc': {'bg': '#228B22', 'text': 'KAZANÇ', 'icon': '💎'}
        }
        
        for key, style in styles.items():
            frame = tk.Frame(info_frame, bg=style['bg'], 
                           relief='raised', borderwidth=2)
            frame.pack(side=tk.LEFT, padx=20, ipadx=15, ipady=8)
            
            header_frame = tk.Frame(frame, bg=style['bg'])
            header_frame.pack()
            
            tk.Label(header_frame, text=style['icon'],
                    font=('Segoe UI Emoji', 16),
                    bg=style['bg']).pack(side=tk.LEFT, padx=2)
            
            tk.Label(header_frame, text=style['text'],
                    font=('Arial', 14, 'bold'),
                    bg=style['bg'],
                    fg='white').pack(side=tk.LEFT)
            
            value = self.bakiye if key == 'bakiye' else (self.bahis if key == 'bahis' else 0)
            label = tk.Label(frame,
                           text=f"${value:,}",
                           font=('Arial', 22, 'bold'),
                           bg=style['bg'],
                           fg='white')
            label.pack()
            setattr(self, f"{key}_label", label)
    
    def create_control_buttons(self):
        control_frame = tk.Frame(self.scrollable_frame, bg='#0D1117')
        control_frame.pack(pady=20)
        
        button_styles = {
            'bahis_azalt': {
                'text': '◀ BAHİS',
                'gradient': ['#E74C3C', '#C0392B'],
                'cmd': lambda: self.bahis_degistir(-50),
                'icon': '➖'
            },
            'max_bet': {
                'text': 'MAX BAHİS',
                'gradient': ['#9B59B6', '#8E44AD'],
                'cmd': lambda: self.bahis_degistir(1000),
                'icon': '⭐'
            },
            'spin': {
                'text': 'ÇEVİR',
                'gradient': ['#2ECC71', '#27AE60'],
                'cmd': self.slot_cevir,
                'icon': '🎰'
            },
            'auto_spin': {
                'text': 'AUTO',
                'gradient': ['#E67E22', '#D35400'],
                'cmd': self.auto_spin,
                'icon': '🔄'
            },
            'bahis_arttir': {
                'text': 'BAHİS ▶',
                'gradient': ['#3498DB', '#2980B9'],
                'cmd': lambda: self.bahis_degistir(50),
                'icon': '➕'
            }
        }
        
        for key, style in button_styles.items():
            # Modern görünümlü buton çerçevesi
            btn_frame = tk.Frame(control_frame, bg=style['gradient'][0],
                               relief='flat', borderwidth=0)
            btn_frame.pack(side=tk.LEFT, padx=10)
            
            # Gradient efektli modern buton
            btn = tk.Button(btn_frame,
                          text=f"{style['icon']} {style['text']}",
                          command=style['cmd'],
                          font=(MAC_FONT[0], 16, 'bold'),
                          bg=style['gradient'][0],
                          fg='white',
                          activebackground=style['gradient'][1],
                          activeforeground='white',
                          relief='flat',
                          bd=0,
                          padx=20,
                          pady=10,
                          width=12 if key == 'spin' else 10,
                          cursor='hand2')  # El işaretçisi
            
            # Hover efekti
            btn.bind('<Enter>', lambda e, b=btn, g=style['gradient']: 
                    b.configure(bg=g[1]))
            btn.bind('<Leave>', lambda e, b=btn, g=style['gradient']: 
                    b.configure(bg=g[0]))
            
            btn.pack(padx=1, pady=1)
            
            if key == 'spin':
                self.spin_button = btn

    def create_modern_paytable(self):
        paytable_frame = tk.Frame(self.scrollable_frame, bg='#1F2937', 
                                relief='sunken', borderwidth=2)
        paytable_frame.pack(pady=10, padx=20, fill='x')
        
        header = tk.Label(paytable_frame,
                         text="✨ ÖDEME TABLOSU ✨",
                         font=('Arial', 16, 'bold'),
                         bg='#1F2937',
                         fg='#FFD700')
        header.pack(pady=5)
        
        grid_frame = tk.Frame(paytable_frame, bg='#1F2937')
        grid_frame.pack(pady=5)
        
        row = 0
        col = 0
        for sembol, carpan in self.semboller.items():
            frame = tk.Frame(grid_frame, bg='#1F2937', padx=10)
            frame.grid(row=row, column=col, pady=2)
            
            tk.Label(frame, text=sembol,
                    font=('Segoe UI Emoji', 28),
                    bg='#1F2937').pack(side=tk.LEFT, padx=5)
            
            tk.Label(frame,
                    text=f"x{carpan}",
                    font=('Arial', 14, 'bold'),
                    bg='#1F2937',
                    fg=self.get_random_color()).pack(side=tk.LEFT)
            
            col += 1
            if col > 4:
                col = 0
                row += 1
    
    def neon_effect(self):
        colors = ['#FFD700', '#FFA500', '#FF4500', '#FF0000', '#FF1493']
        current_color = getattr(self, 'current_color', 0)
        
        self.baslik.config(fg=colors[current_color])
        self.alt_baslik.config(fg=colors[(current_color + 2) % len(colors)])
        
        current_color = (current_color + 1) % len(colors)
        setattr(self, 'current_color', current_color)
        
        self.root.after(300, self.neon_effect)
    
    def create_particle(self, x, y, color):
        """Patlama efekti için parçacık oluştur"""
        return {
            'x': x,
            'y': y,
            'dx': random.uniform(-5, 5),
            'dy': random.uniform(-5, 5),
            'life': 1.0,
            'color': color,
            'size': random.randint(2, 6)
        }

    def animate_particles(self):
        """Parçacık animasyonunu güncelle"""
        if not self.explosion_particles:
            return
        
        canvas = self.slot_frame
        
        for particle in self.explosion_particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['dy'] += 0.2  # Yerçekimi efekti
            particle['life'] -= 0.02
            
            if particle['life'] <= 0:
                self.explosion_particles.remove(particle)
            else:
                size = int(particle['size'] * particle['life'])
                x, y = particle['x'], particle['y']
                
                label = tk.Label(canvas, text='✨', font=('Arial', size),
                               fg=particle['color'], bg='#111827')
                label.place(x=x, y=y)
                self.root.after(50, label.destroy)
        
        if self.explosion_particles:
            self.root.after(20, self.animate_particles)

    def create_explosion(self, x, y):
        """Patlama efekti oluştur"""
        colors = ['#FFD700', '#FF4500', '#FF1493', '#00FFFF', '#FF0000']
        for _ in range(30):
            self.explosion_particles.append(
                self.create_particle(x, y, random.choice(colors))
            )
        self.animate_particles()

    def symbol_fall_animation(self, col_idx, label_idx, symbol):
        """Sembollerin düşme animasyonu"""
        label = self.slot_labels[col_idx][label_idx]
        start_y = -50
        end_y = label.winfo_y()
        steps = 20
        
        for step in range(steps):
            progress = step / steps
            # Easing function for bounce effect
            y = start_y + (end_y - start_y) * (1 - math.cos(progress * math.pi / 2))
            
            label.place(y=y)
            label.config(text=symbol)
            self.root.update()
            time.sleep(0.02)
        
        label.place(y=end_y)

    def shatter_animation(self, label):
        """Kırılma efekti animasyonu"""
        original_text = label.cget('text')
        pieces = ['💥', '✨', '💫', '⚡']
        
        for _ in range(5):
            label.config(text=random.choice(pieces))
            self.root.update()
            time.sleep(0.05)
        
        label.config(text=original_text)

    def slot_cevir(self, event=None):
        if self.animating:
            return
            
        if self.bakiye < self.bahis:
            messagebox.showwarning("⚠️ Uyarı", "Yetersiz bakiye!")
            return
        
        self.animating = True
        self.spin_button.config(state='disabled')
        self.bakiye -= self.bahis
        self.bakiye_label.config(text=f"${self.bakiye:,}")
        self.kazanc_label.config(text="$0")
        
        # Hızlandırılmış spin animasyonu
        for t in range(self.spin_duration):
            for col_idx, col in enumerate(self.slot_labels):
                for label_idx, label in enumerate(col):
                    if t < self.spin_duration - 5:
                        delay = (col_idx * 0.05) * math.sin(t * math.pi / 10)
                        time.sleep(max(0.005, self.animation_speed * delay))
                        
                        if random.random() < 0.2:  # Efekt görünme şansını azalttık
                            label.config(text=random.choice(self.efekt_sembolleri),
                                       fg=self.get_random_color())
                        else:
                            label.config(text=random.choice(list(self.semboller.keys())),
                                       fg='white')
                        
                        # Kırılma efektini daha nadir yap
                        if random.random() < 0.05:
                            self.shatter_animation(label)
                    
            self.root.update()
        
        # Hızlı düşme animasyonu
        sonuc = [[random.choice(list(self.semboller.keys())) for _ in range(4)] for _ in range(10)]
        for i, col in enumerate(self.slot_labels):
            for j, label in enumerate(col):
                label.config(text=sonuc[i][j], font=(MAC_FONT[0], 32, 'bold'))
                self.root.update()
                time.sleep(0.01)  # Çok kısa bekleme
        
        # Kazanç hesapla
        kazanc = self.kazanc_hesapla(sonuc)
        if kazanc > 0:
            if kazanc >= self.bahis * 50:
                self.jackpot_animasyonu()
                # Hızlı patlama efekti
                for i in range(3):  # Patlama sayısını azalttık
                    x = random.randint(0, self.slot_frame.winfo_width())
                    y = random.randint(0, self.slot_frame.winfo_height())
                    self.create_explosion(x, y)
            else:
                self.kazanc_animasyonu(kazanc)
            
            self.bakiye += kazanc
            self.kazanc_label.config(text=f"${kazanc:,}")
            self.bakiye_label.config(text=f"${self.bakiye:,}")
        
        self.spin_button.config(state='normal')
        self.animating = False

    def kazanc_hesapla(self, sonuc):
        toplam_kazanc = 0
        
        # Yatay satırları kontrol et
        for j in range(4):
            row = [col[j] for col in sonuc]
            for i in range(len(row)-2):
                segment = row[i:i+3]
                if len(set(segment)) == 1:
                    toplam_kazanc += self.bahis * self.semboller[segment[0]]
                elif len(set(segment)) == 2:
                    toplam_kazanc += self.bahis * 2
        
        return toplam_kazanc

    def jackpot_animasyonu(self):
        # Geliştirilmiş jackpot animasyonu
        colors = ['#FF0000', '#FFD700', '#00FF00', '#0000FF', '#FF1493', '#9400D3']
        effects = ['🎉', '💫', '✨', '🌟', '💥', '🎊']
        
        # Başlık animasyonu
        for _ in range(10):
            color = random.choice(colors)
            effect = random.choice(effects)
            self.baslik.config(text=f"{effect} MEGA JACKPOT {effect}",
                             fg=color,
                             font=('Arial', random.randint(48, 56), 'bold'))
            
            # Tüm sembolleri de yanıp söndür
            for col in self.slot_labels:
                for label in col:
                    label.config(fg=random.choice(colors))
            
            self.root.update()
            time.sleep(0.1)
        
        # Başlığı normale döndür
        self.baslik.config(text="🎰 LUXURY VEGAS SLOTS 🎰",
                          fg='#FFD700',
                          font=('Arial', 48, 'bold'))

    def bahis_degistir(self, miktar):
        yeni_bahis = self.bahis + miktar
        if 50 <= yeni_bahis <= 1000:
            self.bahis = yeni_bahis
            self.bahis_label.config(text=f"${self.bahis:,}")
        else:
            messagebox.showwarning("Uyarı", "Bahis 50 ile 1000 arasında olmalıdır!")
            
    def auto_spin(self):
        # Auto spin özelliği için ileride eklenecek
        messagebox.showinfo("Bilgi", "Bu özellik yakında eklenecek!")

    def get_random_color(self):
        # Parlak renkler için
        colors = ['#FF0000', '#00FF00', '#0000FF', '#FFD700', 
                 '#FF1493', '#00FFFF', '#FF4500', '#9400D3']
        return random.choice(colors)

    def kazanc_animasyonu(self, kazanc):
        # Kazanan sembolleri vurgula
        flash_colors = ['#FFD700', '#FFA500', '#FF4500']
        for _ in range(5):
            for color in flash_colors:
                self.kazanc_label.config(fg=color, font=('Arial', 26, 'bold'))
                self.root.update()
                time.sleep(0.1)
        self.kazanc_label.config(fg='white', font=('Arial', 22, 'bold'))

def main():
    root = tk.Tk()
    app = ModernSlotMakinesi(root)
    root.mainloop()

if __name__ == "__main__":
    main() 