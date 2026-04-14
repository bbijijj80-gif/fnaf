"""
Модуль 1: Таймер Помодоро
Классический таймер 25 минут работы / 5 минут отдыха
"""

import customtkinter as ctk
from datetime import datetime, timedelta

class PomodoroTimer(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("🍅 Таймер Помодоро")
        self.geometry("400x350")
        self.resizable(False, False)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Переменные
        self.work_time = 25 * 60  # 25 минут в секундах
        self.break_time = 5 * 60  # 5 минут в секундах
        self.current_time = self.work_time
        self.is_work_session = True
        self.is_running = False
        self.timer_id = None
        
        self.create_ui()
        
    def create_ui(self):
        # Заголовок
        title_label = ctk.CTkLabel(
            self,
            text="🍅 Помодоро Таймер",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Статус сессии
        self.status_label = ctk.CTkLabel(
            self,
            text="Время работать!",
            font=ctk.CTkFont(size=18),
            text_color="#FF6B6B"
        )
        self.status_label.pack(pady=10)
        
        # Отображение времени
        self.time_label = ctk.CTkLabel(
            self,
            text="25:00",
            font=ctk.CTkFont(size=64, weight="bold")
        )
        self.time_label.pack(pady=20)
        
        # Кнопки управления
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        self.start_btn = ctk.CTkButton(
            btn_frame,
            text="▶ Старт",
            command=self.start_timer,
            width=100,
            height=40
        )
        self.start_btn.grid(row=0, column=0, padx=5)
        
        pause_btn = ctk.CTkButton(
            btn_frame,
            text="⏸ Пауза",
            command=self.pause_timer,
            width=100,
            height=40
        )
        pause_btn.grid(row=0, column=1, padx=5)
        
        reset_btn = ctk.CTkButton(
            btn_frame,
            text="🔄 Сброс",
            command=self.reset_timer,
            width=100,
            height=40
        )
        reset_btn.grid(row=0, column=2, padx=5)
        
        # Настройки
        settings_frame = ctk.CTkFrame(self)
        settings_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(settings_frame, text="Работа (мин):").pack(side="left", padx=10)
        self.work_entry = ctk.CTkEntry(settings_frame, width=60)
        self.work_entry.insert(0, "25")
        self.work_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(settings_frame, text="Отдых (мин):").pack(side="left", padx=10)
        self.break_entry = ctk.CTkEntry(settings_frame, width=60)
        self.break_entry.insert(0, "5")
        self.break_entry.pack(side="left", padx=5)
        
        apply_btn = ctk.CTkButton(
            settings_frame,
            text="Применить",
            command=self.apply_settings,
            width=80,
            height=30
        )
        apply_btn.pack(side="right", padx=10, pady=10)
        
        # Счётчик циклов
        self.cycle_label = ctk.CTkLabel(
            self,
            text="Цикл: 1",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.cycle_label.pack(pady=10)
        
        self.cycle_count = 1
        
    def update_timer(self):
        if self.is_running and self.current_time > 0:
            self.current_time -= 1
            
            # Форматирование времени
            minutes = self.current_time // 60
            seconds = self.current_time % 60
            time_str = f"{minutes:02d}:{seconds:02d}"
            self.time_label.configure(text=time_str)
            
            # Планируем следующее обновление
            self.timer_id = self.after(1000, self.update_timer)
            
        elif self.current_time == 0:
            # Переключение между работой и отдыхом
            self.switch_session()
            
    def switch_session(self):
        if self.is_work_session:
            # Переход к перерыву
            self.is_work_session = False
            self.current_time = self.break_time
            self.status_label.configure(text="☕ Время отдохнуть!", text_color="#4ECDC4")
            self.play_notification("break")
        else:
            # Переход к работе
            self.is_work_session = True
            self.current_time = self.work_time
            self.cycle_count += 1
            self.cycle_label.configure(text=f"Цикл: {self.cycle_count}")
            self.status_label.configure(text="🎯 Время работать!", text_color="#FF6B6B")
            self.play_notification("work")
            
        self.update_display()
        if self.is_running:
            self.update_timer()
            
    def update_display(self):
        minutes = self.current_time // 60
        seconds = self.current_time % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        self.time_label.configure(text=time_str)
        
    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.start_btn.configure(text="⏳ Идёт...", state="disabled")
            self.update_timer()
            
    def pause_timer(self):
        if self.is_running:
            self.is_running = False
            self.start_btn.configure(text="▶ Продолжить", state="normal")
            if self.timer_id:
                self.after_cancel(self.timer_id)
                
    def reset_timer(self):
        self.is_running = False
        self.is_work_session = True
        self.current_time = self.work_time
        self.cycle_count = 1
        self.start_btn.configure(text="▶ Старт", state="normal")
        self.status_label.configure(text="Время работать!", text_color="#FF6B6B")
        self.cycle_label.configure(text="Цикл: 1")
        self.update_display()
        
    def apply_settings(self):
        try:
            work_min = int(self.work_entry.get())
            break_min = int(self.break_entry.get())
            
            if work_min > 0 and break_min > 0:
                self.work_time = work_min * 60
                self.break_time = break_min * 60
                
                if not self.is_running:
                    self.current_time = self.work_time
                    self.update_display()
        except ValueError:
            pass
            
    def play_notification(self, session_type):
        """Воспроизведение звукового уведомления"""
        try:
            import winsound
            if session_type == "break":
                winsound.Beep(800, 500)
            else:
                winsound.Beep(1000, 500)
                winsound.Beep(1200, 500)
        except:
            pass  # Для кроссплатформенности


if __name__ == "__main__":
    app = PomodoroTimer()
    app.mainloop()
