"""
Модуль 9: Цитаты для мотивации
Случайные мотивирующие цитаты для поддержания продуктивности
"""

import customtkinter as ctk
import random

class MotivationalQuotes(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("💡 Цитаты для мотивации")
        self.geometry("500x400")
        self.resizable(False, False)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Коллекция цитат
        self.quotes = [
            ("Главный способ преуспеть — начать действовать.", "Марк Твен"),
            ("Не ждите. Время никогда не будет идеальным.", "Наполеон Хилл"),
            ("Лучший способ предсказать будущее — создать его.", "Авраам Линкольн"),
            ("Успех — это способность идти от поражения к поражению, не теряя энтузиазма.", "Уинстон Черчилль"),
            ("Через 20 лет вы будете больше жалеть о том, чего не сделали, чем о том, что сделали.", "Марк Твен"),
            ("Единственный способ делать великие дела — любить то, что делаете.", "Стив Джобс"),
            ("Ваше время ограничено, не тратьте его, живя чужой жизнью.", "Стив Джобс"),
            ("Простота — высшая форма утончённости.", "Леонардо да Винчи"),
            ("Начните там, где вы есть. Используйте то, что у вас есть. Делайте всё, что можете.", "Артур Эш"),
            ("Падать — часть жизни, подниматься на ноги — её проживание.", "Хосе Нароски"),
            ("Сложнее всего начать действовать, все остальное зависит только от упорства.", "Амелия Эрхарт"),
            ("Жизнь — это то, что с вами случается, пока вы строите другие планы.", "Джон Леннон"),
            ("Логика приведет вас из пункта А в пункт Б. Воображение приведет вас куда угодно.", "Альберт Эйнштейн"),
            ("Через год вы пожалеете, что не начали сегодня.", "Карен Лэмб"),
            ("Ограничения живут только в нашем разуме. Но если мы используем наше воображение, наши возможности становятся безграничными.", "Джейми Паолинетти"),
            ("Ты не можешь изменить направление ветра, но ты можешь настроить паруса.", "Джимми Дин"),
            ("Чтобы достичь великого, нужно не только действовать, но и мечтать.", "Анатоль Франс"),
            ("Возможности не приходят сами — вы создаете их.", "Крис Гроссер"),
            ("Любите жизнь, которой живете. Живите жизнью, которую любите.", "Боб Марли"),
            ("Мечтайте по-крупному и не бойтесь провала.", "Норман Вон")
        ]
        
        self.current_quote_index = 0
        
        self.create_ui()
        self.show_random_quote()
        
    def create_ui(self):
        # Заголовок
        title_label = ctk.CTkLabel(
            self,
            text="💡 Мотивирующие Цитаты",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=15)
        
        # Область цитаты
        quote_frame = ctk.CTkFrame(self, fg_color="#2D2D2D", corner_radius=15)
        quote_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Текст цитаты
        self.quote_text = ctk.CTkLabel(
            quote_frame,
            text="",
            font=ctk.CTkFont(size=20, style="italic"),
            wraplength=420,
            justify="center"
        )
        self.quote_text.pack(pady=(30, 10), padx=20)
        
        # Автор
        self.quote_author = ctk.CTkLabel(
            quote_frame,
            text="",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#4ECDC4"
        )
        self.quote_author.pack(pady=(0, 30))
        
        # Декоративные кавычки
        open_quote = ctk.CTkLabel(
            quote_frame,
            text='"',
            font=ctk.CTkFont(size=80),
            text_color="#4ECDC4"
        )
        open_quote.place(relx=0.05, rely=0.1)
        
        close_quote = ctk.CTkLabel(
            quote_frame,
            text='"',
            font=ctk.CTkFont(size=80),
            text_color="#4ECDC4"
        )
        close_quote.place(relx=0.95, rely=0.8, anchor="se")
        
        # Кнопки управления
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=15)
        
        prev_btn = ctk.CTkButton(
            btn_frame,
            text="◀ Назад",
            command=self.prev_quote,
            width=120
        )
        prev_btn.pack(side="left", padx=20)
        
        next_btn = ctk.CTkButton(
            btn_frame,
            text="Вперёд ▶",
            command=self.next_quote,
            width=120
        )
        next_btn.pack(side="right", padx=20)
        
        # Кнопка случайной цитаты
        random_btn = ctk.CTkButton(
            self,
            text="🎲 Случайная цитата",
            command=self.show_random_quote,
            height=45,
            width=200
        )
        random_btn.pack(pady=10)
        
        # Автообновление
        self.auto_var = ctk.BooleanVar(value=False)
        auto_cb = ctk.CTkCheckBox(
            self,
            text="Автообновление каждые 30 сек",
            variable=self.auto_var,
            command=self.toggle_auto_update
        )
        auto_cb.pack(pady=5)
        
        # Счётчик
        self.counter_label = ctk.CTkLabel(
            self,
            text=f"Цитата {self.current_quote_index + 1} из {len(self.quotes)}",
            text_color="gray"
        )
        self.counter_label.pack(pady=5)
        
    def show_quote(self, index):
        if 0 <= index < len(self.quotes):
            self.current_quote_index = index
            quote, author = self.quotes[index]
            self.quote_text.configure(text=quote)
            self.quote_author.configure(text=f"— {author}")
            self.counter_label.configure(text=f"Цитата {index + 1} из {len(self.quotes)}")
            
    def show_random_quote(self):
        index = random.randint(0, len(self.quotes) - 1)
        self.show_quote(index)
        
    def next_quote(self):
        next_index = (self.current_quote_index + 1) % len(self.quotes)
        self.show_quote(next_index)
        
    def prev_quote(self):
        prev_index = (self.current_quote_index - 1) % len(self.quotes)
        self.show_quote(prev_index)
        
    def toggle_auto_update(self):
        if self.auto_var.get():
            self.auto_update()
            
    def auto_update(self):
        if self.auto_var.get():
            self.next_quote()
            self.after(30000, self.auto_update)


if __name__ == "__main__":
    app = MotivationalQuotes()
    app.mainloop()
