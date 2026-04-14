"""
Модуль 10: Тёмная тема экрана
Затемнение экрана для снижения нагрузки на глаза
"""

import customtkinter as ctk

class DarkScreenFilter(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("🌙 Тёмная тема экрана")
        self.geometry("400x350")
        self.resizable(False, False)
        
        # Убираем декорации окна для полноэкранного режима
        self.overrideredirect(False)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Создаём прозрачный overlay
        self.overlay = None
        self.is_active = False
        
        self.create_ui()
        
    def create_ui(self):
        # Заголовок
        title_label = ctk.CTkLabel(
            self,
            text="🌙 Фильтр Синего Света",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=15)
        
        # Описание
        desc_label = ctk.CTkLabel(
            self,
            text="Снижает нагрузку на глаза\nи улучшает качество сна",
            text_color="gray",
            justify="center"
        )
        desc_label.pack(pady=10)
        
        # Контроль интенсивности
        intensity_frame = ctk.CTkFrame(self)
        intensity_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(intensity_frame, text="Интенсивность:", 
                    font=ctk.CTkFont(size=16)).pack(pady=5)
        
        self.intensity_slider = ctk.CTkSlider(
            intensity_frame,
            from_=0,
            to=0.8,
            number_of_steps=8,
            command=self.change_intensity,
            width=280
        )
        self.intensity_slider.set(0.3)
        self.intensity_slider.pack(pady=10)
        
        self.intensity_label = ctk.CTkLabel(
            intensity_frame,
            text="30%",
            font=ctk.CTkFont(size=14)
        )
        self.intensity_label.pack()
        
        # Цветовая температура
        temp_frame = ctk.CTkFrame(self)
        temp_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(temp_frame, text="Температура цвета:", 
                    font=ctk.CTkFont(size=14)).pack(pady=5)
        
        self.temp_var = ctk.StringVar(value="warm")
        temp_options = [
            ("🔵 Обычный", "normal"),
            ("🟡 Тёплый", "warm"),
            ("🟠 Очень тёплый", "very_warm")
        ]
        
        for text, value in temp_options:
            radio = ctk.CTkRadioButton(
                temp_frame,
                text=text,
                variable=self.temp_var,
                value=value,
                command=self.change_temperature
            )
            radio.pack(anchor="w", padx=20, pady=2)
        
        # Кнопка включения/выключения
        self.toggle_btn = ctk.CTkButton(
            self,
            text="▶ Включить фильтр",
            command=self.toggle_filter,
            height=45,
            width=200,
            font=ctk.CTkFont(size=16)
        )
        self.toggle_btn.pack(pady=20)
        
        # Горячие клавиши
        shortcut_label = ctk.CTkLabel(
            self,
            text="Горячая клавиша: F12",
            text_color="gray",
            font=ctk.CTkFont(size=12)
        )
        shortcut_label.pack(pady=5)
        
        # Привязка клавиши F12
        self.bind("<F12>", lambda e: self.toggle_filter())
        
    def change_intensity(self, value):
        percentage = int(value / 0.8 * 100)
        self.intensity_label.configure(text=f"{percentage}%")
        if self.overlay and self.is_active:
            self.update_overlay()
            
    def change_temperature(self):
        if self.overlay and self.is_active:
            self.update_overlay()
            
    def toggle_filter(self):
        if self.is_active:
            self.disable_filter()
        else:
            self.enable_filter()
            
    def enable_filter(self):
        """Включение фильтра"""
        self.is_active = True
        self.toggle_btn.configure(text="⏹ Выключить фильтр", fg_color="#FF6B6B")
        
        # Создание полноэкранного overlay
        self.overlay = ctk.CTkToplevel(self)
        self.overlay.title("")
        self.overlay.attributes("-fullscreen", True)
        self.overlay.attributes("-topmost", True)
        self.overlay.attributes("-alpha", 0.3 + self.intensity_slider.get() * 0.5)
        
        # Установка цвета в зависимости от температуры
        self.update_overlay()
        
        # Клик по overlay не должен его закрывать
        self.overlay.bind("<Button-1>", lambda e: "break")
        
    def disable_filter(self):
        """Выключение фильтра"""
        self.is_active = False
        self.toggle_btn.configure(text="▶ Включить фильтр", fg_color="#2E86DE")
        
        if self.overlay:
            self.overlay.destroy()
            self.overlay = None
            
    def update_overlay(self):
        """Обновление параметров overlay"""
        if not self.overlay:
            return
            
        intensity = self.intensity_slider.get()
        temp = self.temp_var.get()
        
        # Цвет в зависимости от температуры
        if temp == "normal":
            color = "#0000FF"  # Синий
        elif temp == "warm":
            color = "#FF8800"  # Оранжевый
        else:  # very_warm
            color = "#FF4400"  # Красновато-оранжевый
            
        self.overlay.configure(bg=color)
        alpha = 0.2 + intensity * 0.6
        self.overlay.attributes("-alpha", alpha)


if __name__ == "__main__":
    app = DarkScreenFilter()
    app.mainloop()
