"""
Модуль 5: Трекер задач
Простой список задач на сессию концентрации
"""

import customtkinter as ctk
import json
from pathlib import Path
from datetime import datetime

class TaskTracker(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("✅ Трекер задач")
        self.geometry("500x550")
        self.resizable(False, False)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Файл для сохранения задач
        self.tasks_file = Path(__file__).parent / "tasks.json"
        self.tasks = []
        
        self.create_ui()
        self.load_tasks()
        
    def create_ui(self):
        # Заголовок
        title_label = ctk.CTkLabel(
            self,
            text="✅ Трекер Задач",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=15)
        
        # Статистика
        stats_frame = ctk.CTkFrame(self)
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        self.total_label = ctk.CTkLabel(stats_frame, text="Всего: 0")
        self.total_label.pack(side="left", padx=20, pady=10)
        
        self.completed_label = ctk.CTkLabel(stats_frame, text="Выполнено: 0", text_color="green")
        self.completed_label.pack(side="left", padx=20, pady=10)
        
        self.progress_label = ctk.CTkLabel(stats_frame, text="0%")
        self.progress_label.pack(side="right", padx=20, pady=10)
        
        # Поле ввода новой задачи
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(fill="x", padx=20, pady=10)
        
        self.task_entry = ctk.CTkEntry(input_frame, placeholder_text="Новая задача...", height=40)
        self.task_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.task_entry.bind("<Return>", lambda e: self.add_task())
        
        add_btn = ctk.CTkButton(
            input_frame,
            text="➕ Добавить",
            command=self.add_task,
            width=120,
            height=40
        )
        add_btn.pack(side="left")
        
        # Список задач
        list_frame = ctk.CTkFrame(self)
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(list_frame, text="Задачи на сессию:", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        
        self.tasks_scroll = ctk.CTkScrollableFrame(list_frame)
        self.tasks_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Кнопки управления
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        clear_btn = ctk.CTkButton(
            btn_frame,
            text="🗑 Очистить выполненные",
            command=self.clear_completed,
            fg_color="#FF6B6B",
            width=180
        )
        clear_btn.pack(side="left")
        
        save_btn = ctk.CTkButton(
            btn_frame,
            text="💾 Сохранить",
            command=self.save_tasks,
            width=120
        )
        save_btn.pack(side="right")
        
    def add_task(self):
        task_text = self.task_entry.get().strip()
        if not task_text:
            return
            
        task = {
            "id": len(self.tasks) + 1,
            "text": task_text,
            "completed": False,
            "created": datetime.now().strftime("%H:%M")
        }
        
        self.tasks.append(task)
        self.task_entry.delete(0, "end")
        self.refresh_list()
        self.update_stats()
        
    def toggle_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = not task["completed"]
                break
        self.refresh_list()
        self.update_stats()
        
    def delete_task(self, task_id):
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        # Переназначаем ID
        for i, task in enumerate(self.tasks):
            task["id"] = i + 1
        self.refresh_list()
        self.update_stats()
        
    def refresh_list(self):
        # Очистка списка
        for widget in self.tasks_scroll.winfo_children():
            widget.destroy()
            
        # Добавление задач
        for task in self.tasks:
            task_frame = ctk.CTkFrame(self.tasks_scroll)
            task_frame.pack(fill="x", pady=3, padx=5)
            
            # Чекбокс
            cb_var = ctk.BooleanVar(value=task["completed"])
            cb = ctk.CTkCheckBox(
                task_frame,
                text="",
                variable=cb_var,
                command=lambda tid=task["id"]: self.toggle_task(tid),
                width=20
            )
            cb.pack(side="left", padx=5, pady=10)
            
            # Текст задачи
            text_color = "gray" if task["completed"] else "white"
            text_label = ctk.CTkLabel(
                task_frame,
                text=task["text"],
                text_color=text_color,
                anchor="w"
            )
            text_label.pack(side="left", fill="x", expand=True, padx=5)
            
            # Время создания
            time_label = ctk.CTkLabel(
                task_frame,
                text=task["created"],
                text_color="gray",
                width=50
            )
            time_label.pack(side="left", padx=5)
            
            # Кнопка удаления
            del_btn = ctk.CTkButton(
                task_frame,
                text="✕",
                width=30,
                fg_color="#FF6B6B",
                command=lambda tid=task["id"]: self.delete_task(tid)
            )
            del_btn.pack(side="left", padx=5)
            
    def update_stats(self):
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t["completed"])
        percentage = int((completed / total * 100) if total > 0 else 0)
        
        self.total_label.configure(text=f"Всего: {total}")
        self.completed_label.configure(text=f"Выполнено: {completed}")
        self.progress_label.configure(text=f"{percentage}%")
        
    def clear_completed(self):
        self.tasks = [t for t in self.tasks if not t["completed"]]
        # Переназначаем ID
        for i, task in enumerate(self.tasks):
            task["id"] = i + 1
        self.refresh_list()
        self.update_stats()
        
    def save_tasks(self):
        try:
            with open(self.tasks_file, 'w', encoding='utf-8') as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
            
    def load_tasks(self):
        try:
            if self.tasks_file.exists():
                with open(self.tasks_file, 'r', encoding='utf-8') as f:
                    self.tasks = json.load(f)
                self.refresh_list()
                self.update_stats()
        except Exception as e:
            print(f"Ошибка загрузки: {e}")


if __name__ == "__main__":
    app = TaskTracker()
    app.mainloop()
