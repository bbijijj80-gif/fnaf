"""
Модуль 2: Генератор белого шума
Создаёт фоновый шум для улучшения концентрации
"""

import customtkinter as ctk
import numpy as np
import threading
import time

try:
    import sounddevice as sd
    SOUND_AVAILABLE = True
except:
    SOUND_AVAILABLE = False

class WhiteNoiseGenerator(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("🔊 Белый шум")
        self.geometry("450x400")
        self.resizable(False, False)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Переменные
        self.is_playing = False
        self.volume = 0.3
        self.noise_type = "white"
        self.audio_thread = None
        self.stop_flag = False
        
        self.create_ui()
        
    def create_ui(self):
        # Заголовок
        title_label = ctk.CTkLabel(
            self,
            text="🔊 Генератор Белого Шума",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=15)
        
        # Индикатор статуса
        self.status_frame = ctk.CTkFrame(self, fg_color="#2D2D2D")
        self.status_frame.pack(fill="x", padx=20, pady=10)
        
        self.status_indicator = ctk.CTkLabel(
            self.status_frame,
            text="● Остановлено",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        self.status_indicator.pack(pady=10)
        
        # Выбор типа шума
        noise_frame = ctk.CTkFrame(self)
        noise_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(noise_frame, text="Тип шума:", font=ctk.CTkFont(size=16)).pack(pady=5)
        
        self.noise_var = ctk.StringVar(value="white")
        noise_types = [
            ("⚪ Белый шум", "white"),
            ("🟤 Розовый шум", "pink"),
            ("🔵 Коричневый шум", "brown"),
            ("🌧️ Дождь", "rain")
        ]
        
        for text, value in noise_types:
            radio = ctk.CTkRadioButton(
                noise_frame,
                text=text,
                variable=self.noise_var,
                value=value,
                command=self.change_noise_type
            )
            radio.pack(anchor="w", padx=20, pady=5)
        
        # Контроль громкости
        volume_frame = ctk.CTkFrame(self)
        volume_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(volume_frame, text="Громкость:", font=ctk.CTkFont(size=16)).pack(pady=5)
        
        self.volume_slider = ctk.CTkSlider(
            volume_frame,
            from_=0,
            to=1,
            number_of_steps=100,
            command=self.change_volume,
            width=300
        )
        self.volume_slider.set(self.volume)
        self.volume_slider.pack(pady=10)
        
        self.volume_label = ctk.CTkLabel(volume_frame, text=f"{int(self.volume * 100)}%")
        self.volume_label.pack()
        
        # Кнопка воспроизведения
        self.play_btn = ctk.CTkButton(
            self,
            text="▶ Воспроизвести",
            command=self.toggle_play,
            height=50,
            width=200,
            font=ctk.CTkFont(size=18)
        )
        self.play_btn.pack(pady=20)
        
        # Информация
        info_label = ctk.CTkLabel(
            self,
            text="Белый шум помогает сконцентрироваться\nи блокировать отвлекающие звуки",
            text_color="gray",
            justify="center"
        )
        info_label.pack(pady=10)
        
        if not SOUND_AVAILABLE:
            warning_label = ctk.CTkLabel(
                self,
                text="⚠ Установите: pip install sounddevice numpy",
                text_color="orange"
            )
            warning_label.pack(pady=5)
            
    def change_noise_type(self):
        self.noise_type = self.noise_var.get()
        if self.is_playing:
            self.stop_audio()
            self.start_audio()
            
    def change_volume(self, value):
        self.volume = value
        self.volume_label.configure(text=f"{int(value * 100)}%")
        
    def toggle_play(self):
        if self.is_playing:
            self.stop_audio()
        else:
            self.start_audio()
            
    def start_audio(self):
        if not SOUND_AVAILABLE:
            return
            
        self.is_playing = True
        self.stop_flag = False
        self.play_btn.configure(text="⏹ Стоп", fg_color="#FF6B6B")
        self.status_indicator.configure(text="● Воспроизведение...", text_color="#4ECDC4")
        
        self.audio_thread = threading.Thread(target=self.generate_noise, daemon=True)
        self.audio_thread.start()
        
    def stop_audio(self):
        self.is_playing = False
        self.stop_flag = True
        self.play_btn.configure(text="▶ Воспроизвести", fg_color="#2E86DE")
        self.status_indicator.configure(text="● Остановлено", text_color="gray")
        
    def generate_noise(self):
        """Генерация различных типов шума"""
        if not SOUND_AVAILABLE:
            return
            
        sample_rate = 44100
        buffer_size = 4096
        
        while not self.stop_flag:
            # Генерация шума в зависимости от типа
            if self.noise_type == "white":
                noise = np.random.uniform(-1, 1, buffer_size)
            elif self.noise_type == "pink":
                white = np.random.uniform(-1, 1, buffer_size)
                noise = np.cumsum(white) / buffer_size
                noise = noise * 5  # Усиление
            elif self.noise_type == "brown":
                white = np.random.uniform(-1, 1, buffer_size)
                noise = np.cumsum(white) / buffer_size
                noise = noise * 10  # Усиление
            elif self.noise_type == "rain":
                # Имитация дождя
                noise = np.random.uniform(-1, 1, buffer_size)
                noise = np.convolve(noise, np.ones(10)/10, mode='same')
            
            # Применение громкости
            noise = noise * self.volume
            
            # Ограничение амплитуды
            noise = np.clip(noise, -1, 1)
            
            try:
                sd.play(noise, sample_rate, blocking=False)
                time.sleep(buffer_size / sample_rate)
            except:
                break


if __name__ == "__main__":
    app = WhiteNoiseGenerator()
    app.mainloop()
