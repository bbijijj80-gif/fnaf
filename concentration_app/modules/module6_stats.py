"""
Модуль 6: Статистика фокуса
Отслеживание времени концентрации и продуктивности
"""

import customtkinter as ctk
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

class FocusStats(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("📊 Статистика фокуса")
        self.geometry("600x500")
        self.resizable(False, False)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Файл для хранения статистики
        self.stats_file = Path(__file__).parent / "focus_stats.json"
        self.stats = self.load_stats()
        
        self.create_ui()
        self.update_display()
        
    def create_ui(self):
        # Заголовок
        title_label = ctk.CTkLabel(
            self,
            text="📊 Статистика Фокуса",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=15)
        
        # Общая статистика
        overview_frame = ctk.CTkFrame(self)
        overview_frame.pack(fill="x", padx=20, pady=10)
        
        self.total_time_label = ctk.CTkLabel(
            overview_frame,
            text="Всего времени: 0ч 0м",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.total_time_label.grid(row=0, column=0, padx=20, pady=10)
        
        self.sessions_label = ctk.CTkLabel(
            overview_frame,
            text="Сессий: 0",
            font=ctk.CTkFont(size=18)
        )
        self.sessions_label.grid(row=0, column=1, padx=20, pady=10)
        
        self.streak_label = ctk.CTkLabel(
            overview_frame,
            text="Серия дней: 0",
            font=ctk.CTkFont(size=18),
            text_color="#FF6B6B"
        )
        self.streak_label.grid(row=0, column=2, padx=20, pady=10)
        
        # Статистика по дням недели
        week_frame = ctk.CTkFrame(self)
        week_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(week_frame, text="По дням недели:", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        
        self.week_chart = ctk.CTkFrame(week_frame, fg_color="#1a1a1a")
        self.week_chart.pack(fill="x", padx=10, pady=10)
        
        days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        self.day_bars = {}
        
        for i, day in enumerate(days):
            day_frame = ctk.CTkFrame(self.week_chart, fg_color="transparent")
            day_frame.grid(row=0, column=i, padx=5, pady=5, sticky="ns")
            
            bar = ctk.CTkProgressBar(day_frame, width=40, height=100, orientation="vertical")
            bar.pack(pady=5)
            bar.set(0)
            self.day_bars[day] = bar
            
            label = ctk.CTkLabel(day_frame, text=day, font=ctk.CTkFont(size=12))
            label.pack()
            
        self.week_chart.grid_columnconfigure((0,1,2,3,4,5,6), weight=1)
        
        # Последние сессии
        sessions_frame = ctk.CTkFrame(self)
        sessions_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(sessions_frame, text="Последние сессии:", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        
        self.sessions_scroll = ctk.CTkScrollableFrame(sessions_frame)
        self.sessions_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Кнопки управления
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        add_btn = ctk.CTkButton(
            btn_frame,
            text="➕ Добавить сессию",
            command=self.add_session_dialog,
            width=180
        )
        add_btn.pack(side="left")
        
        reset_btn = ctk.CTkButton(
            btn_frame,
            text="🗑 Сбросить статистику",
            command=self.reset_stats,
            fg_color="#FF6B6B",
            width=180
        )
        reset_btn.pack(side="right")
        
    def load_stats(self):
        try:
            if self.stats_file.exists():
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return {"sessions": [], "daily": {}}
        
    def save_stats(self):
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
            
    def update_display(self):
        sessions = self.stats.get("sessions", [])
        
        # Общее время
        total_minutes = sum(s.get("duration", 0) for s in sessions)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        self.total_time_label.configure(text=f"Всего времени: {hours}ч {minutes}м")
        
        # Количество сессий
        self.sessions_label.configure(text=f"Сессий: {len(sessions)}")
        
        # Серия дней
        streak = self.calculate_streak()
        self.streak_label.configure(text=f"Серия дней: {streak}")
        
        # Статистика по дням недели
        day_totals = defaultdict(int)
        for session in sessions:
            date_str = session.get("date", "")
            if date_str:
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                    day_name = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"][date.weekday()]
                    day_totals[day_name] += session.get("duration", 0)
                except:
                    pass
        
        # Нормализация и отображение
        max_minutes = max(day_totals.values()) if day_totals else 1
        for day, bar in self.day_bars.items():
            minutes = day_totals.get(day, 0)
            bar.set(minutes / max_minutes if max_minutes > 0 else 0)
            
        # Последние сессии
        self.update_sessions_list()
        
    def calculate_streak(self):
        """Вычисление текущей серии дней"""
        sessions = self.stats.get("sessions", [])
        if not sessions:
            return 0
            
        dates = set()
        for s in sessions:
            date_str = s.get("date", "")
            if date_str:
                dates.add(date_str)
                
        if not dates:
            return 0
            
        # Сортировка дат
        sorted_dates = sorted(list(dates), reverse=True)
        today = datetime.now().strftime("%Y-%m-%d")
        
        streak = 0
        current_date = datetime.now()
        
        while True:
            date_str = current_date.strftime("%Y-%m-%d")
            if date_str in dates:
                streak += 1
                current_date -= timedelta(days=1)
            else:
                break
                
        return streak
        
    def update_sessions_list(self):
        # Очистка
        for widget in self.sessions_scroll.winfo_children():
            widget.destroy()
            
        # Последние 10 сессий
        sessions = self.stats.get("sessions", [])[-10:][::-1]
        
        for session in sessions:
            session_frame = ctk.CTkFrame(self.sessions_scroll)
            session_frame.pack(fill="x", pady=3, padx=5)
            
            date = session.get("date", "N/A")
            duration = session.get("duration", 0)
            focus_type = session.get("type", "Работа")
            
            ctk.CTkLabel(
                session_frame,
                text=f"{date} • {focus_type}",
                anchor="w"
            ).pack(side="left", padx=10, pady=5)
            
            ctk.CTkLabel(
                session_frame,
                text=f"{duration} мин",
                text_color="#4ECDC4"
            ).pack(side="right", padx=10, pady=5)
            
    def add_session_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Добавить сессию")
        dialog.geometry("350x250")
        dialog.transient(self)
        
        ctk.CTkLabel(dialog, text="Длительность (мин):").pack(pady=10)
        duration_entry = ctk.CTkEntry(dialog, width=200)
        duration_entry.pack()
        duration_entry.insert(0, "25")
        
        ctk.CTkLabel(dialog, text="Тип активности:").pack(pady=10)
        type_var = ctk.StringVar(value="Работа")
        type_menu = ctk.CTkOptionMenu(dialog, values=["Работа", "Учёба", "Чтение", "Другое"])
        type_menu.pack()
        
        def save():
            try:
                duration = int(duration_entry.get())
                session = {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "time": datetime.now().strftime("%H:%M"),
                    "duration": duration,
                    "type": type_var.get()
                }
                self.stats["sessions"].append(session)
                self.save_stats()
                self.update_display()
                dialog.destroy()
            except:
                pass
                
        ctk.CTkButton(dialog, text="Сохранить", command=save).pack(pady=20)
        
    def reset_stats(self):
        confirm = ctk.CTkToplevel(self)
        confirm.title("Подтверждение")
        confirm.geometry("300x150")
        
        ctk.CTkLabel(confirm, text="Вы уверены?\nВсе данные будут удалены.").pack(pady=20)
        
        def do_reset():
            self.stats = {"sessions": [], "daily": {}}
            self.save_stats()
            self.update_display()
            confirm.destroy()
            
        ctk.CTkButton(confirm, text="Да, сбросить", command=do_reset, 
                     fg_color="#FF6B6B").pack(side="left", padx=20, pady=10)
        ctk.CTkButton(confirm, text="Отмена", command=confirm.destroy).pack(side="right", padx=20, pady=10)


if __name__ == "__main__":
    app = FocusStats()
    app.mainloop()
