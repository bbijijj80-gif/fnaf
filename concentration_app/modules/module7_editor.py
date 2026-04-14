"""
Модуль 7: Минималистичный редактор
Текстовый редактор без отвлечений для записи мыслей
"""

import customtkinter as ctk
from pathlib import Path
from datetime import datetime

class MinimalEditor(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("📝 Минималистичный редактор")
        self.geometry("700x550")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.current_file = None
        
        self.create_ui()
        
    def create_ui(self):
        # Верхняя панель
        top_frame = ctk.CTkFrame(self, height=50)
        top_frame.pack(fill="x", padx=10, pady=10)
        
        # Кнопки
        new_btn = ctk.CTkButton(
            top_frame,
            text="📄 Новый",
            command=self.new_file,
            width=80
        )
        new_btn.pack(side="left", padx=5)
        
        open_btn = ctk.CTkButton(
            top_frame,
            text="📂 Открыть",
            command=self.open_file,
            width=80
        )
        open_btn.pack(side="left", padx=5)
        
        save_btn = ctk.CTkButton(
            top_frame,
            text="💾 Сохранить",
            command=self.save_file,
            width=80
        )
        save_btn.pack(side="left", padx=5)
        
        # Статус справа
        self.status_label = ctk.CTkLabel(
            top_frame,
            text="Готов",
            text_color="gray"
        )
        self.status_label.pack(side="right", padx=20)
        
        # Счётчик слов
        self.words_label = ctk.CTkLabel(
            top_frame,
            text="Слов: 0",
            text_color="gray"
        )
        self.words_label.pack(side="right", padx=20)
        
        # Текстовое поле
        self.text_area = ctk.CTkTextbox(
            self,
            font=ctk.CTkFont(family="Consolas", size=16),
            wrap="word"
        )
        self.text_area.pack(fill="both", expand=True, padx=10, pady=10)
        self.text_area.bind("<KeyRelease>", self.update_word_count)
        
        # Нижняя панель с цитатой
        bottom_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        bottom_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        quotes = [
            "Пишите так, как будто никто не читает.",
            "Простота — высшая форма утончённости.",
            "Лучший способ начать — перестать говорить и начать делать."
        ]
        
        quote_label = ctk.CTkLabel(
            bottom_frame,
            text=quotes[0],
            text_color="gray",
            font=ctk.CTkFont(size=14, style="italic")
        )
        quote_label.pack(pady=10)
        
    def update_word_count(self, event=None):
        text = self.text_area.get("1.0", "end-1c")
        words = len(text.split())
        chars = len(text)
        self.words_label.configure(text=f"Слов: {words} | Символов: {chars}")
        
    def new_file(self):
        self.text_area.delete("1.0", "end")
        self.current_file = None
        self.status_label.configure(text="Новый файл")
        
    def open_file(self):
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(
            title="Открыть файл",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.text_area.delete("1.0", "end")
                self.text_area.insert("1.0", content)
                self.current_file = file_path
                self.status_label.configure(text=f"Открыт: {Path(file_path).name}")
                self.update_word_count()
            except Exception as e:
                print(f"Ошибка: {e}")
                
    def save_file(self):
        if self.current_file:
            self._save_to_file(self.current_file)
        else:
            from tkinter import filedialog
            file_path = filedialog.asksaveasfilename(
                title="Сохранить как",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if file_path:
                self.current_file = file_path
                self._save_to_file(file_path)
                
    def _save_to_file(self, file_path):
        try:
            content = self.text_area.get("1.0", "end-1c")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.status_label.configure(text=f"Сохранён: {Path(file_path).name}")
        except Exception as e:
            print(f"Ошибка сохранения: {e}")


if __name__ == "__main__":
    app = MinimalEditor()
    app.mainloop()
