"""
Модуль 8: Напоминания о перерывах
Регулярные уведомления для отдыха во время работы
"""

import customtkinter as ctk
import threading
import time
from datetime import datetime, timedelta

try:
    import winsound
    SOUND_AVAILABLE = True
except:
    SOUND_AVAILABLE = False

class BreakReminder(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("☕ Напоминания о перерывах")
        self.geometry("450x400")
        self.resizable(False, False)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.is_running = False
        self.work_interval = 25 * 60  # 25 минут
        self.break_duration = 5 * 60  # 5 минут
        self.timer_thread = None
        self.stop_flag = False
        
        self.create_ui()
        
    def create_ui(self):
        # Заголовок
        title_label = ctk.CTkLabel(
            self,
            text="☕ Напоминания о Перерывах",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=15)
        
        # Статус
        self.status_frame = ctk.CTkFrame(self, fg_color="#2D2D2D")
        self.status_frame.pack(fill="x", padx=20, pady=10)
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="● Ожидание запуска",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        self.status_label.pack(pady=10)
        
        # Таймер до следующего перерыва
        self.timer_display = ctk.CTkLabel(
            self,
            text="00:00",
            font=ctk.CTkFont(size=48, weight="bold"),
            text_color="#4ECDC4"
        )
        self.timer_display.pack(pady=20)
        
        # Настройки интервалов
        settings_frame = ctk.CTkFrame(self)
        settings_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(settings_frame, text="Работа (мин):").grid(row=0, column=0, padx=10, pady=5)
        self.work_entry = ctk.CTkEntry(settings_frame, width=60)
        self.work_entry.insert(0, "25")
        self.work_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(settings_frame, text="Перерыв (мин):").grid(row=0, column=2, padx=10, pady=5)
        self.break_entry = ctk.CTkEntry(settings_frame, width=60)
        self.break_entry.insert(0, "5")
        self.break_entry.grid(row=0, column=3, padx=5, pady=5)
        
        apply_btn = ctk.CTkButton(
            settings_frame,
            text="Применить",
            command=self.apply_settings,
            height=30
        )
        apply_btn.grid(row=1, column=0, columnspan=4, pady=10)
        
        # Типы уведомлений
        notify_frame = ctk.CTkFrame(self)
        notify_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(notify_frame, text="Тип уведомления:", 
                    font=ctk.CTkFont(size=14)).pack(pady=5)
        
        self.notify_var = ctk.StringVar(value="sound")
        notify_types = [
            ("🔊 Звук + окно", "sound"),
            ("🪟 Только окно", "window"),
            ("💻 Только в трее", "tray")
        ]
        
        for text, value in notify_types:
            radio = ctk.CTkRadioButton(
                notify_frame,
                text=text,
                variable=self.notify_var,
                value=value
            )
            radio.pack(anchor="w", padx=20, pady=2)
        
        # Кнопки управления
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=15)
        
        self.start_btn = ctk.CTkButton(
            btn_frame,
            text="▶ Запустить напоминания",
            command=self.toggle_reminder,
            height=45,
            width=220,
            font=ctk.CTkFont(size=16)
        )
        self.start_btn.pack(pady=10)
        
        # Информация
        info_label = ctk.CTkLabel(
            self,
            text="Регулярные перерывы повышают продуктивность\nи снижают утомляемость",
            text_color="gray",
            justify="center"
        )
        info_label.pack(pady=10)
        
    def apply_settings(self):
        try:
            work_min = int(self.work_entry.get())
            break_min = int(self.break_entry.get())
            
            if work_min > 0 and break_min > 0:
                self.work_interval = work_min * 60
                self.break_duration = break_min * 60
        except ValueError:
            pass
            
    def toggle_reminder(self):
        if self.is_running:
            self.stop_reminder()
        else:
            self.start_reminder()
            
    def start_reminder(self):
        self.is_running = True
        self.stop_flag = False
        self.start_btn.configure(text="⏹ Остановить", fg_color="#FF6B6B")
        self.status_label.configure(text="● Отсчёт времени...", text_color="#4ECDC4")
        
        self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
        self.timer_thread.start()
        
    def stop_reminder(self):
        self.is_running = False
        self.stop_flag = True
        self.start_btn.configure(text="▶ Запустить напоминания", fg_color="#2E86DE")
        self.status_label.configure(text="● Остановлено", text_color="gray")
        self.timer_display.configure(text="00:00")
        
    def run_timer(self):
        """Основной цикл таймера"""
        remaining = self.work_interval
        is_work_time = True
        
        while not self.stop_flag:
            # Обновление отображения
            mins = remaining // 60
            secs = remaining % 60
            time_str = f"{mins:02d}:{secs:02d}"
            
            self.after(0, lambda t=time_str, w=is_work_time: self.update_timer_display(t, w))
            
            if remaining <= 0:
                # Время перерыва или работы
                if is_work_time:
                    self.show_break_notification()
                    remaining = self.break_duration
                    is_work_time = False
                else:
                    self.show_work_notification()
                    remaining = self.work_interval
                    is_work_time = True
            else:
                remaining -= 1
                time.sleep(1)
                
    def update_timer_display(self, time_str, is_work_time):
        self.timer_display.configure(text=time_str)
        if is_work_time:
            self.timer_display.configure(text_color="#4ECDC4")
        else:
            self.timer_display.configure(text_color="#FF6B6B")
            
    def show_break_notification(self):
        """Показ уведомления о перерыве"""
        notify_type = self.notify_var.get()
        
        if notify_type in ["sound", "window"]:
            self.play_sound()
            
        if notify_type != "tray":
            self.show_notification_window("☕ Пора на перерыв!", 
                                         "Отойдите от компьютера на 5 минут.\n"
                                         "Разомнитесь, выпейте воды.")
                                         
    def show_work_notification(self):
        """Показ уведомления о начале работы"""
        notify_type = self.notify_var.get()
        
        if notify_type in ["sound", "window"]:
            self.play_sound()
            
        if notify_type != "tray":
            self.show_notification_window("🎯 Время работать!",
                                         "Перерыв окончен.\n"
                                         "Настройтесь на продуктивную работу.")
                                         
    def play_sound(self):
        """Воспроизведение звука уведомления"""
        if SOUND_AVAILABLE:
            try:
                winsound.Beep(1000, 300)
                time.sleep(0.1)
                winsound.Beep(1200, 300)
            except:
                pass
                
    def show_notification_window(self, title, message):
        """Показ всплывающего окна"""
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("350x150")
        dialog.attributes("-topmost", True)
        
        label = ctk.CTkLabel(
            dialog,
            text=message,
            font=ctk.CTkFont(size=16),
            justify="center"
        )
        label.pack(pady=20, padx=20)
        
        ok_btn = ctk.CTkButton(
            dialog,
            text="Понятно",
            command=dialog.destroy,
            width=100
        )
        ok_btn.pack(pady=10)


if __name__ == "__main__":
    app = BreakReminder()
    app.mainloop()
