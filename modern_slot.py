import tkinter as tk
from tkinter import messagebox
import random
import time

class VegasSlot:
    def __init__(self, root):
        self.root = root
        self.root.title("🎰 VEGAS SLOTS")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1E0836')
        self.root.resizable(False, False)
        
        self.bakiye = 10000
        self.bahis = 50
        self.spinning = False
        
        # Klasik slot sembolleri ve değerleri
        self.semboller = {
            '7': {'sembol': '7', 'renk': '#FF0000', 'deger': 1000},
            'BAR': {'sembol': 'BAR', 'renk': '#FFD700', 'deger': 500},
            '⭐': {'sembol': '⭐', 'renk': '#FFFF00', 'deger': 250},
            '💎': {'sembol': '💎', 'renk': '#00FFFF', 'deger': 200},
            '🔔': {'sembol': '🔔', 'renk': '#FFA500', 'deger': 150},
            '🍇': {'sembol': '🍇', 'renk': '#9400D3', 'deger': 100},
            '🍊': {'sembol': '🍊', 'renk': '#FF8C00', 'deger': 75},
            '🍋': {'sembol': '🍋', 'renk': '#FFD700', 'deger': 50},
            '🍒': {'sembol': '🍒', 'renk': '#FF0000', 'deger': 25}
        }
        
        self.create_ui()
        
        # Klavye kontrolleri
        self.root.bind('<space>', lambda e: self.spin())
        self.root.bind('<Return>', lambda e: self.set_bet(1000))
        self.root.bind('<Left>', lambda e: self.change_bet(-50))
        self.root.bind('<Right>', lambda e: self.change_bet(50))

    def create_ui(self):
        # Mac OS tarzı stil tanımlamaları
        self.styles = {
            'bg_dark': '#1E0836',  # Ana arka plan
            'bg_light': '#2A0F47', # Panel arka planı
            'accent': '#FF1493',   # Vurgu rengi
            'text_light': '#FFFFFF'
        }
        
        # Ana container frame (gölgeli)
        main_container = tk.Frame(self.root, bg=self.styles['bg_dark'])
        main_container.pack(padx=20, pady=20, fill='both', expand=True)
        
        self.create_header()
        self.create_slot_display()
        self.create_info_panel()
        self.create_controls()

    def create_header(self):
        header_frame = tk.Frame(self.root, bg='#1E0836', height=100)
        header_frame.pack(fill='x', pady=20)
        
        # Vegas tarzı başlık
        title = tk.Label(header_frame,
                        text="★ VEGAS LUXURY SLOTS ★",
                        font=('Arial Black', 36, 'bold'),
                        bg='#1E0836',
                        fg='#FFD700')
        title.pack(pady=10)
        
        # Animasyonlu ışıklar için üst frame
        top_lights = tk.Frame(header_frame, bg='#1E0836')
        top_lights.pack(fill='x', padx=20)
        
        # Animasyonlu ışıklar için alt frame
        bottom_lights = tk.Frame(header_frame, bg='#1E0836')
        bottom_lights.pack(fill='x', padx=20)
        
        # Neon renkler
        neon_colors = ['#FF0000', '#00FF00', '#0000FF', '#FFD700', 
                       '#FF1493', '#00FFFF', '#FF4500', '#9400D3']
        
        # Üst sıra ışıklar
        for i in range(30):
            light = tk.Label(top_lights,
                            text="●",
                            font=('Arial', 20),
                            bg='#1E0836',
                            fg=random.choice(neon_colors))
            light.pack(side='left', padx=2)
            self.blink_light(light, neon_colors)
        
        # Alt sıra ışıklar
        for i in range(30):
            light = tk.Label(bottom_lights,
                            text="●",
                            font=('Arial', 20),
                            bg='#1E0836',
                            fg=random.choice(neon_colors))
            light.pack(side='left', padx=2)
            self.blink_light(light, neon_colors)
        
        # Başlık animasyonu
        def animate_title():
            current_color = title.cget('fg')
            next_color = random.choice([c for c in neon_colors if c != current_color])
            title.config(fg=next_color)
            self.root.after(1000, animate_title)
        
        animate_title()
        
    def create_slot_display(self):
        # Ana slot çerçevesi
        slot_frame = tk.Frame(self.root, bg=self.styles['bg_light'])
        slot_frame.pack(pady=20, padx=20)
        
        # Slot grid container
        grid_frame = tk.Frame(slot_frame, bg='black', padx=20, pady=20)
        grid_frame.pack()
        
        # Slot grid
        self.slot_grid = []
        for i in range(5):  # 5 sütun
            column = []
            col_frame = tk.Frame(grid_frame, bg='black', padx=5)
            col_frame.pack(side='left')
            
            # Neon border
            tk.Frame(col_frame, bg='#FF1493', width=2).pack(side='left', fill='y')
            tk.Frame(col_frame, bg='#FF1493', width=2).pack(side='right', fill='y')
            
            for j in range(3):  # 3 satır
                symbol_frame = tk.Frame(col_frame, 
                                      bg='black',
                                      width=120,
                                      height=100)
                symbol_frame.pack(pady=2)
                symbol_frame.pack_propagate(False)
                
                label = tk.Label(symbol_frame,
                               text="7",
                               font=('Arial Black', 40, 'bold'),
                               bg='black',
                               fg='#FF0000')
                label.pack(expand=True)
                column.append(label)
            
            self.slot_grid.append(column)

    def create_info_panel(self):
        # Bilgi paneli
        info_frame = tk.Frame(self.root, bg=self.styles['bg_light'])
        info_frame.pack(fill='x', padx=20, pady=20)
        
        for title, value, color in [
            ("BALANCE", f"${self.bakiye:,}", '#FFD700'),
            ("BET", f"${self.bahis}", '#00FF00'),
            ("WIN", "$0", '#FF1493')
        ]:
            display = tk.Frame(info_frame, bg='black', padx=20, pady=10)
            display.pack(side='left', expand=True, padx=10)
            
            tk.Label(display,
                    text=title,
                    font=('Arial Black', 14),
                    bg='black',
                    fg=color).pack(pady=(5,0))
            
            label = tk.Label(display,
                            text=value,
                            font=('Arial Black', 24),
                            bg='black',
                            fg='white')
            label.pack()
            
            setattr(self, f"{title.lower()}_label", label)
        
    def create_controls(self):
        # Kontrol butonları
        control_frame = tk.Frame(self.root, bg=self.styles['bg_light'])
        control_frame.pack(pady=20)
        
        # Spin butonu
        self.spin_button = tk.Button(control_frame,
                                    text="SPIN",
                                    font=('Arial Black', 24, 'bold'),
                                    bg='#FF0000',
                                    fg='white',
                                    relief='raised',
                                    borderwidth=5,
                                    command=self.spin,
                                    width=12,
                                    height=1)
        self.spin_button.pack(pady=10)
        
        # Alt butonlar
        button_frame = tk.Frame(control_frame, bg=self.styles['bg_light'])
        button_frame.pack()
        
        button_configs = [
            ("MAX BET", '#FFD700', lambda: self.set_bet(1000)),
            ("AUTO PLAY", '#00FF00', self.auto_play),
            ("BET +", '#FF1493', lambda: self.change_bet(50)),
            ("BET -", '#FF1493', lambda: self.change_bet(-50))
        ]
        
        for text, color, cmd in button_configs:
            btn = tk.Button(button_frame,
                           text=text,
                           font=('Arial Black', 12, 'bold'),
                           bg=color,
                           fg='black' if color != '#FF1493' else 'white',
                           relief='raised',
                           borderwidth=3,
                           command=cmd,
                           width=10)
            btn.pack(side='left', padx=5)
            
            # Hover efekti
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg='#FF1493'))
            btn.bind('<Leave>', lambda e, b=btn, c=color: b.config(bg=c))
        
    def blink_light(self, light, colors):
        """Işıkları yanıp söndür"""
        current_color = light.cget('fg')
        new_color = random.choice([c for c in colors if c != current_color])
        light.config(fg=new_color)
        self.root.after(500, lambda: self.blink_light(light, colors))
        
    def spin(self):
        if self.spinning or self.bakiye < self.bahis:
            return
            
        self.spinning = True
        self.bakiye -= self.bahis
        self.update_balance_display()
        self.win_label.config(text="$0")
        
        # Hızlı spin animasyonu
        for _ in range(10):
            for col in self.slot_grid:
                for label in col:
                    symbol = random.choice(list(self.semboller.keys()))
                    label.config(text=self.semboller[symbol]['sembol'],
                               fg=self.semboller[symbol]['renk'])
            self.root.update()
            time.sleep(0.05)
        
        # Son sonuçları göster
        sonuc = []
        for col in self.slot_grid:
            column_symbols = []
            for label in col:
                symbol = random.choice(list(self.semboller.keys()))
                label.config(text=self.semboller[symbol]['sembol'],
                           fg=self.semboller[symbol]['renk'])
                column_symbols.append(symbol)
            sonuc.append(column_symbols)
        
        # Kazancı hesapla
        kazanc = self.calculate_win(sonuc)
        if kazanc > 0:
            self.bakiye += kazanc
            self.win_label.config(text=f"${kazanc:,}")
            self.highlight_winning_combinations(sonuc)
            
        self.update_balance_display()
        self.spinning = False

    def calculate_win(self, sonuc):
        toplam_kazanc = 0
        
        # Yatay çizgileri kontrol et
        for row in range(3):
            for col in range(3):
                symbols = [sonuc[col+i][row] for i in range(3)]
                if len(set(symbols)) == 1:  # 3 aynı sembol
                    symbol = symbols[0]
                    toplam_kazanc += self.bahis * self.semboller[symbol]['deger']
                elif len(set(symbols)) == 2:  # 2 aynı sembol
                    toplam_kazanc += self.bahis * 2
        
        return toplam_kazanc

    def highlight_winning_combinations(self, sonuc):
        # Kazanan kombinasyonları vurgula
        for row in range(3):
            for col in range(3):
                symbols = [sonuc[col+i][row] for i in range(3)]
                if len(set(symbols)) <= 2:
                    for i in range(3):
                        label = self.slot_grid[col+i][row]
                        original_color = label.cget('fg')
                        # Yanıp sönme efekti
                        for _ in range(3):
                            label.config(fg='#FFFFFF')
                            self.root.update()
                            time.sleep(0.1)
                            label.config(fg=original_color)
                            self.root.update()
                            time.sleep(0.1)

    def update_balance_display(self):
        self.balance_label.config(text=f"${self.bakiye:,}")
        self.bet_label.config(text=f"${self.bahis}")

    def set_bet(self, amount):
        if not self.spinning:
            self.bahis = amount
            self.update_balance_display()

    def change_bet(self, delta):
        if not self.spinning:
            new_bet = self.bahis + delta
            if 50 <= new_bet <= 1000:
                self.bahis = new_bet
                self.update_balance_display()

    def auto_play(self):
        if not self.spinning and self.bakiye >= self.bahis:
            self.spin()
            self.root.after(2000, self.auto_play)

def main():
    root = tk.Tk()
    app = VegasSlot(root)
    root.mainloop()

if __name__ == "__main__":
    main() 