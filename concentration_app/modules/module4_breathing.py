"""
Модуль 4: Дыхательные упражнения
Упражнения для снятия стресса и улучшения концентрации
"""

import customtkinter as ctk
import time
import threading

class BreathingExercise(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("🧘 Дыхательные упражнения")
        self.geometry("500x500")
        self.resizable(False, False)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.is_running = False
        self.current_exercise = "box"
        self.phase = 0
        self.cycle_count = 0
        
        # Параметры упражнений
        self.exercises = {
            "box": {"name": "Квадратное дыхание", "phases": [4, 4, 4, 4], 
                   "labels": ["Вдох", "Задержка", "Выдох", "Задержка"]},
            "relax": {"name": "4-7-8 Релаксация", "phases": [4, 7, 8],
                     "labels": ["Вдох", "Задержка", "Выдох"]},
            "energy": {"name": "Энергетическое", "phases": [3, 0, 6],
                      "labels": ["Вдох", "", "Выдох"]}
        }
        
        self.create_ui()
        
    def create_ui(self):
        # Заголовок
        title_label = ctk.CTkLabel(
            self,
            text="🧘 Дыхательные Упражнения",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=15)
        
        # Выбор упражнения
        exercise_frame = ctk.CTkFrame(self)
        exercise_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(exercise_frame, text="Выберите упражнение:", 
                    font=ctk.CTkFont(size=16)).pack(pady=5)
        
        self.exercise_var = ctk.StringVar(value="box")
        exercises_list = [
            ("box", "⬜ Квадратное (4-4-4-4)"),
            ("relax", "😌 Релаксация (4-7-8)"),
            ("energy", "⚡ Энергетическое (3-6)")
        ]
        
        for value, text in exercises_list:
            radio = ctk.CTkRadioButton(
                exercise_frame,
                text=text,
                variable=self.exercise_var,
                value=value,
                command=self.change_exercise
            )
            radio.pack(anchor="w", padx=20, pady=5)
        
        # Визуализация дыхания
        self.visual_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        self.visual_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Круг для анимации
        self.canvas = ctk.CTkCanvas(
            self.visual_frame,
            width=300,
            height=300,
            bg="#1a1a1a",
            highlightthickness=0
        )
        self.canvas.pack(pady=20)
        
        # Центральный круг
        self.circle = self.canvas.create_oval(
            75, 75, 225, 225,
            fill="#2E86DE",
            outline="#4ECDC4",
            width=3
        )
        
        # Текст инструкции
        self.instruction_label = ctk.CTkLabel(
            self.visual_frame,
            text="Нажмите Старт для начала",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        )
        self.instruction_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Счётчик циклов
        self.cycle_label = ctk.CTkLabel(
            self.visual_frame,
            text="Циклы: 0",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        self.cycle_label.place(relx=0.5, rely=0.85, anchor="center")
        
        # Прогресс бар фазы
        self.progress_bar = ctk.CTkProgressBar(self.visual_frame, width=250)
        self.progress_bar.place(relx=0.5, rely=0.92, anchor="center")
        self.progress_bar.set(0)
        
        # Кнопки управления
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=15)
        
        self.start_btn = ctk.CTkButton(
            btn_frame,
            text="▶ Старт",
            command=self.toggle_exercise,
            height=45,
            width=150,
            font=ctk.CTkFont(size=18)
        )
        self.start_btn.pack(side="left", padx=20)
        
        reset_btn = ctk.CTkButton(
            btn_frame,
            text="🔄 Сброс",
            command=self.reset_exercise,
            height=45,
            width=120,
            font=ctk.CTkFont(size=16)
        )
        reset_btn.pack(side="left", padx=10)
        
        # Информация
        info_label = ctk.CTkLabel(
            self,
            text="Дыхательные упражнения помогают снизить стресс\nи улучшить концентрацию внимания",
            text_color="gray",
            justify="center"
        )
        info_label.pack(pady=10)
        
    def change_exercise(self):
        self.current_exercise = self.exercise_var.get()
        if not self.is_running:
            self.reset_exercise()
            
    def toggle_exercise(self):
        if self.is_running:
            self.stop_exercise()
        else:
            self.start_exercise()
            
    def start_exercise(self):
        self.is_running = True
        self.start_btn.configure(text="⏹ Стоп", fg_color="#FF6B6B")
        self.cycle_count = 0
        self.phase = 0
        self.run_exercise_cycle()
        
    def stop_exercise(self):
        self.is_running = False
        self.start_btn.configure(text="▶ Старт", fg_color="#2E86DE")
        self.instruction_label.configure(text="Пауза")
        
    def reset_exercise(self):
        self.is_running = False
        self.start_btn.configure(text="▶ Старт", fg_color="#2E86DE")
        self.phase = 0
        self.cycle_count = 0
        self.cycle_label.configure(text="Циклы: 0")
        self.instruction_label.configure(text="Готов к началу")
        self.progress_bar.set(0)
        
        # Сброс размера круга
        self.canvas.coords(self.circle, 75, 75, 225, 225)
        
    def run_exercise_cycle(self):
        if not self.is_running:
            return
            
        exercise = self.exercises[self.current_exercise]
        phases = exercise["phases"]
        labels = exercise["labels"]
        
        if self.phase >= len(phases):
            self.phase = 0
            self.cycle_count += 1
            self.cycle_label.configure(text=f"Циклы: {self.cycle_count}")
        
        phase_duration = phases[self.phase]
        phase_label = labels[self.phase] if self.phase < len(labels) else ""
        
        if phase_duration == 0:
            # Пропуск фазы (например, без задержки)
            self.phase += 1
            self.after(100, self.run_exercise_cycle)
            return
        
        # Обновление текста
        self.instruction_label.configure(text=phase_label)
        
        # Анимация в зависимости от фазы
        if "Вдох" in phase_label:
            self.animate_circle(75, 75, 225, 225, 150, 150, 250, 250, phase_duration * 1000)
        elif "Выдох" in phase_label:
            self.animate_circle(150, 150, 250, 250, 75, 75, 225, 225, phase_duration * 1000)
        else:
            # Задержка - круг остаётся
            self.animate_progress(phase_duration)
            
    def animate_circle(self, start_x1, start_y1, start_x2, start_y2, 
                       end_x1, end_y1, end_x2, end_y2, duration):
        """Плавная анимация круга"""
        steps = 30
        interval = duration / steps
        
        dx1 = (end_x1 - start_x1) / steps
        dy1 = (end_y1 - start_y1) / steps
        dx2 = (end_x2 - start_x2) / steps
        dy2 = (end_y2 - start_y2) / steps
        
        current_step = [0]
        
        def step():
            if current_step[0] < steps and self.is_running:
                new_x1 = start_x1 + dx1 * current_step[0]
                new_y1 = start_y1 + dy1 * current_step[0]
                new_x2 = start_x2 + dx2 * current_step[0]
                new_y2 = start_y2 + dy2 * current_step[0]
                
                self.canvas.coords(self.circle, new_x1, new_y1, new_x2, new_y2)
                current_step[0] += 1
                self.after(int(interval), step)
            elif self.is_running:
                self.phase += 1
                self.run_exercise_cycle()
                
        step()
        
    def animate_progress(self, duration):
        """Анимация прогресс бара для фазы"""
        steps = 20
        interval = duration / steps
        
        current_step = [0]
        
        def step():
            if current_step[0] <= steps and self.is_running:
                progress = current_step[0] / steps
                self.progress_bar.set(progress)
                current_step[0] += 1
                self.after(int(interval), step)
            elif self.is_running:
                self.progress_bar.set(0)
                self.phase += 1
                self.run_exercise_cycle()
                
        step()


if __name__ == "__main__":
    app = BreathingExercise()
    app.mainloop()
