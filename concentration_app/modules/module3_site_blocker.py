"""
Модуль 3: Блокировщик сайтов
Временно блокирует отвлекающие сайты на Windows
"""

import customtkinter as ctk
import subprocess
import os
import sys
from datetime import datetime, timedelta

class SiteBlocker(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("🚫 Блокировщик сайтов")
        self.geometry("500x450")
        self.resizable(False, False)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Путь к hosts файлу (Windows)
        self.hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
        self.redirect_ip = "127.0.0.1"
        
        # Сайты для блокировки по умолчанию
        self.default_sites = [
            "facebook.com", "www.facebook.com",
            "twitter.com", "www.twitter.com",
            "instagram.com", "www.instagram.com",
            "youtube.com", "www.youtube.com",
            "tiktok.com", "www.tiktok.com",
            "reddit.com", "www.reddit.com"
        ]
        
        self.blocked_sites = []
        self.is_blocking = False
        
        self.create_ui()
        
    def create_ui(self):
        # Заголовок
        title_label = ctk.CTkLabel(
            self,
            text="🚫 Блокировщик Сайтов",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=15)
        
        # Статус
        self.status_frame = ctk.CTkFrame(self, fg_color="#2D2D2D")
        self.status_frame.pack(fill="x", padx=20, pady=10)
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="● Блокировка не активна",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        self.status_label.pack(pady=10)
        
        # Выбор времени блокировки
        time_frame = ctk.CTkFrame(self)
        time_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(time_frame, text="Длительность блокировки:", 
                    font=ctk.CTkFont(size=16)).pack(pady=5)
        
        self.duration_var = ctk.StringVar(value="30")
        durations = [
            ("15 минут", "15"),
            ("30 минут", "30"),
            ("1 час", "60"),
            ("2 часа", "120"),
            ("4 часа", "240")
        ]
        
        duration_container = ctk.CTkFrame(time_frame, fg_color="transparent")
        duration_container.pack(pady=5)
        
        for text, value in durations:
            radio = ctk.CTkRadioButton(
                duration_container,
                text=text,
                variable=self.duration_var,
                value=value,
                width=100
            )
            radio.pack(side="left", padx=10)
        
        # Список сайтов
        sites_frame = ctk.CTkFrame(self)
        sites_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(sites_frame, text="Сайты для блокировки:", 
                    font=ctk.CTkFont(size=16)).pack(pady=5)
        
        # Прокручиваемый список
        self.sites_scroll = ctk.CTkScrollableFrame(sites_frame, height=150)
        self.sites_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.site_checkboxes = {}
        for site in self.default_sites[::2]:  # Берём только основные домены
            display_name = site.replace("www.", "")
            var = ctk.BooleanVar(value=True)
            cb = ctk.CTkCheckBox(self.sites_scroll, text=display_name, variable=var)
            cb.pack(anchor="w", pady=3)
            self.site_checkboxes[site] = var
        
        # Кнопки управления
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=15)
        
        self.toggle_btn = ctk.CTkButton(
            btn_frame,
            text="▶ Начать блокировку",
            command=self.toggle_blocking,
            height=45,
            width=200,
            font=ctk.CTkFont(size=16)
        )
        self.toggle_btn.pack(pady=10)
        
        # Инструкции
        info_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        info_frame.pack(fill="x", padx=20, pady=10)
        
        info_label = ctk.CTkLabel(
            info_frame,
            text="⚠ Требуется запуск от имени администратора\n"
                 "Блокировка работает через файл hosts",
            text_color="orange",
            justify="center",
            font=ctk.CTkFont(size=12)
        )
        info_label.pack(pady=10)
        
        # Таймер обратного отсчёта
        self.timer_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FF6B6B"
        )
        self.timer_label.pack(pady=5)
        
    def toggle_blocking(self):
        if not self.is_blocking:
            self.start_blocking()
        else:
            self.stop_blocking()
            
    def start_blocking(self):
        """Начало блокировки сайтов"""
        selected_sites = [
            site for site, var in self.site_checkboxes.items() 
            if var.get()
        ]
        
        if not selected_sites:
            return
            
        try:
            # Добавление записей в hosts файл
            with open(self.hosts_path, 'r') as f:
                content = f.read()
            
            # Проверка, не заблокированы ли уже сайты
            already_blocked = True
            for site in selected_sites:
                if f"{self.redirect_ip} {site}" not in content:
                    already_blocked = False
                    break
            
            if not already_blocked:
                with open(self.hosts_path, 'a') as f:
                    f.write("\n# Concentration App - Blocked Sites\n")
                    for site in selected_sites:
                        f.write(f"{self.redirect_ip} {site}\n")
            
            self.is_blocking = True
            self.toggle_btn.configure(text="⏹ Снять блокировку", fg_color="#FF6B6B")
            self.status_label.configure(
                text="● Блокировка активна", 
                text_color="#FF6B6B"
            )
            
            # Запуск таймера
            duration_minutes = int(self.duration_var.get())
            self.start_countdown(duration_minutes * 60)
            
        except PermissionError:
            self.show_admin_warning()
        except Exception as e:
            print(f"Ошибка: {e}")
            
    def stop_blocking(self):
        """Снятие блокировки"""
        try:
            with open(self.hosts_path, 'r') as f:
                lines = f.readlines()
            
            # Удаление наших записей
            new_lines = []
            skip_until_marker = False
            
            for line in lines:
                if "# Concentration App - Blocked Sites" in line:
                    skip_until_marker = True
                    continue
                if skip_until_marker and line.startswith('#'):
                    continue
                if skip_until_marker and line.strip() == '':
                    skip_until_marker = False
                    continue
                if not skip_until_marker:
                    new_lines.append(line)
            
            with open(self.hosts_path, 'w') as f:
                f.writelines(new_lines)
            
            self.is_blocking = False
            self.toggle_btn.configure(text="▶ Начать блокировку", fg_color="#2E86DE")
            self.status_label.configure(
                text="● Блокировка не активна", 
                text_color="gray"
            )
            self.timer_label.configure(text="")
            
        except PermissionError:
            self.show_admin_warning()
            
    def start_countdown(self, seconds):
        """Обратный отсчёт до снятия блокировки"""
        def countdown():
            while seconds > 0 and self.is_blocking:
                mins, secs = divmod(seconds, 60)
                time_str = f"{mins:02d}:{secs:02d}"
                self.timer_label.configure(text=f"До разблокировки: {time_str}")
                self.after(1000)
                seconds -= 1
                
            if seconds <= 0 and self.is_blocking:
                self.stop_blocking()
                
        # Запуск в отдельном потоке
        import threading
        thread = threading.Thread(target=countdown, daemon=True)
        thread.start()
        
    def show_admin_warning(self):
        """Показ предупреждения о правах администратора"""
        warning_window = ctk.CTkToplevel(self)
        warning_window.title("Требуется доступ администратора")
        warning_window.geometry("400x200")
        
        label = ctk.CTkLabel(
            warning_window,
            text="Для работы блокировщика необходимо\nзапустить программу от имени администратора.\n\n"
                 "Щёлкните правой кнопкой мыши на exe-файле\nи выберите 'Запуск от имени администратора'",
            justify="center"
        )
        label.pack(pady=20, padx=20)
        
        ok_btn = ctk.CTkButton(
            warning_window,
            text="Понятно",
            command=warning_window.destroy
        )
        ok_btn.pack(pady=10)


if __name__ == "__main__":
    app = SiteBlocker()
    app.mainloop()
