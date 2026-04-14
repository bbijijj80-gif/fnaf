"""
Главный лаунчер приложения для концентрации
Запускает интерфейс и управляет 10 модулями
"""

import customtkinter as ctk
import subprocess
import os
import sys
from pathlib import Path

class ConcentrationApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Настройка окна
        self.title("Concentration Hub - Центр Концентрации")
        self.geometry("900x700")
        self.minsize(800, 600)
        
        # Тема
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Путь к модулям
        self.modules_dir = Path(__file__).parent / "modules"
        
        # Список модулей с описанием
        self.modules = [
            {
                "name": "Таймер Помодоро",
                "file": "module1_pomodoro.exe",
                "desc": "Классический таймер 25/5 для работы",
                "icon": "⏱️"
            },
            {
                "name": "Белый шум",
                "file": "module2_white_noise.exe",
                "desc": "Генератор белого шума для фокусировки",
                "icon": "🔊"
            },
            {
                "name": "Блокировщик сайтов",
                "file": "module3_site_blocker.exe",
                "desc": "Временная блокировка отвлекающих сайтов",
                "icon": "🚫"
            },
            {
                "name": "Дыхательные упражнения",
                "file": "module4_breathing.exe",
                "desc": "Упражнения для снятия стресса",
                "icon": "🧘"
            },
            {
                "name": "Трекер задач",
                "file": "module5_task_tracker.exe",
                "desc": "Простой список задач на сессию",
                "icon": "✅"
            },
            {
                "name": "Статистика фокуса",
                "file": "module6_stats.exe",
                "desc": "Отслеживание времени концентрации",
                "icon": "📊"
            },
            {
                "name": "Минималистичный редактор",
                "file": "module7_editor.exe",
                "desc": "Текстовый редактор без отвлечений",
                "icon": "📝"
            },
            {
                "name": "Напоминания о перерывах",
                "file": "module8_break_reminder.exe",
                "desc": "Регулярные напоминания отдохнуть",
                "icon": "☕"
            },
            {
                "name": "Цитаты для мотивации",
                "file": "module9_quotes.exe",
                "desc": "Случайные мотивирующие цитаты",
                "icon": "💡"
            },
            {
                "name": "Тёмная тема экрана",
                "file": "module10_dark_screen.exe",
                "desc": "Затемнение экрана для снижения нагрузки",
                "icon": "🌙"
            }
        ]
        
        self.create_ui()
        
    def create_ui(self):
        # Заголовок
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(pady=20, padx=20, fill="x")
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="🎯 Центр Концентрации",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack()
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="10 инструментов для максимальной продуктивности",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        subtitle_label.pack(pady=5)
        
        # Сетка модулей
        modules_frame = ctk.CTkScrollableFrame(self)
        modules_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Создаём кнопки для каждого модуля
        row = 0
        col = 0
        max_cols = 2
        
        for module in self.modules:
            module_card = self.create_module_card(modules_frame, module)
            module_card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # Настройка сетки
        for i in range(max_cols):
            modules_frame.grid_columnconfigure(i, weight=1)
        
        # Нижняя панель
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.pack(pady=10, padx=20, fill="x")
        
        refresh_btn = ctk.CTkButton(
            footer_frame,
            text="🔄 Обновить статус",
            command=self.refresh_status,
            width=150
        )
        refresh_btn.pack(side="left")
        
        status_label = ctk.CTkLabel(
            footer_frame,
            text="✓ Все модули готовы",
            text_color="green"
        )
        status_label.pack(side="right")
        
    def create_module_card(self, parent, module):
        card = ctk.CTkFrame(parent, corner_radius=10, border_width=2, border_color="gray")
        
        # Иконка и название
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(pady=10, padx=15, fill="x")
        
        icon_label = ctk.CTkLabel(
            header_frame,
            text=module["icon"],
            font=ctk.CTkFont(size=30)
        )
        icon_label.pack(side="left")
        
        name_label = ctk.CTkLabel(
            header_frame,
            text=module["name"],
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        name_label.pack(side="left", padx=10, pady=10)
        
        # Описание
        desc_label = ctk.CTkLabel(
            card,
            text=module["desc"],
            font=ctk.CTkFont(size=14),
            text_color="gray",
            wraplength=350,
            justify="left"
        )
        desc_label.pack(padx=15, pady=(0, 10), anchor="w")
        
        # Кнопка запуска
        launch_btn = ctk.CTkButton(
            card,
            text="▶ Запустить",
            command=lambda m=module: self.launch_module(m),
            width=200,
            height=35
        )
        launch_btn.pack(pady=10, padx=15)
        
        # Статус
        status_label = ctk.CTkLabel(
            card,
            text="● Готов",
            text_color="green",
            font=ctk.CTkFont(size=12)
        )
        status_label.pack(pady=(0, 10))
        
        return card
    
    def launch_module(self, module):
        """Запуск выбранного модуля"""
        module_path = self.modules_dir / module["file"]
        
        if module_path.exists():
            try:
                subprocess.Popen([str(module_path)])
                print(f"Запущен модуль: {module['name']}")
            except Exception as e:
                print(f"Ошибка запуска: {e}")
        else:
            print(f"Модуль не найден: {module_path}")
            # Для тестирования - сообщение
            ctk.CTkMessagebox(
                title="Информация",
                message=f"Модуль '{module['name']}' будет доступен после компиляции всех файлов.",
                icon="info"
            )
    
    def refresh_status(self):
        """Проверка доступности модулей"""
        available = 0
        for module in self.modules:
            module_path = self.modules_dir / module["file"]
            if module_path.exists():
                available += 1
        
        status_text = f"✓ Доступно {available}/10 модулей"
        print(status_text)


if __name__ == "__main__":
    app = ConcentrationApp()
    app.mainloop()
