import secrets
import string
import tkinter as tk
from tkinter import messagebox, ttk


class PasswordGeneratorApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Генератор паролей")
        self.root.geometry("460x480")
        self.root.resizable(False, False)

        # Настройка стилей
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Переменные настроек
        self.length_var = tk.IntVar(value=14)
        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)

        self._create_widgets()
        # Генерируем пароль сразу при запуске
        self.generate_password()

    def _create_widgets(self):
        # 1. Поле вывода пароля и кнопка копирования
        output_frame = ttk.LabelFrame(self.root, text="Сгенерированный пароль", padding=10)
        output_frame.pack(fill="x", padx=15, pady=10)

        self.password_entry = ttk.Entry(
            output_frame, font=("Consolas", 14), justify="center"
        )
        self.password_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        copy_btn = ttk.Button(
            output_frame, text="Копировать", command=self.copy_to_clipboard
        )
        copy_btn.pack(side="right")

        # 2. Индикатор надёжности пароля
        strength_frame = ttk.Frame(self.root, padding=(15, 0))
        strength_frame.pack(fill="x")

        self.strength_label = ttk.Label(
            strength_frame, text="Надёжность: —", font=("Arial", 10, "bold")
        )
        self.strength_label.pack(anchor="w", pady=(0, 3))

        self.strength_bar = ttk.Progressbar(
            strength_frame, maximum=100, mode="determinate"
        )
        self.strength_bar.pack(fill="x", pady=(0, 10))

        # 3. Настройка длины
        length_frame = ttk.LabelFrame(self.root, text="Длина пароля", padding=10)
        length_frame.pack(fill="x", padx=15, pady=5)

        self.length_slider = ttk.Scale(
            length_frame,
            from_=4,
            to=36,
            variable=self.length_var,
            command=self._update_length_label,
        )
        self.length_slider.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.length_display = ttk.Label(
            length_frame,
            text=str(self.length_var.get()),
            font=("Arial", 11, "bold"),
            width=3,
        )
        self.length_display.pack(side="right")

        # 4. Набор символов (Флажки)
        chars_frame = ttk.LabelFrame(self.root, text="Используемые символы", padding=10)
        chars_frame.pack(fill="x", padx=15, pady=10)

        ttk.Checkbutton(
            chars_frame, text="Заглавные буквы (A-Z)", variable=self.use_upper
        ).pack(anchor="w", pady=2)
        ttk.Checkbutton(
            chars_frame, text="Строчные буквы (a-z)", variable=self.use_lower
        ).pack(anchor="w", pady=2)
        ttk.Checkbutton(
            chars_frame, text="Цифры (0-9)", variable=self.use_digits
        ).pack(anchor="w", pady=2)
        ttk.Checkbutton(
            chars_frame,
            text="Специальные символы (!@#$%^&*)",
            variable=self.use_symbols,
        ).pack(anchor="w", pady=2)

        # 5. Кнопка генерации
        generate_btn = tk.Button(
            self.root,
            text="Сгенерировать пароль",
            font=("Arial", 11, "bold"),
            bg="#2ecc71",
            fg="white",
            activebackground="#27ae60",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.generate_password,
        )
        generate_btn.pack(fill="x", padx=15, pady=10, ipady=6)

    def _update_length_label(self, *args):
        # Округляем до целого числа при движении слайдера
        val = int(self.length_slider.get())
        self.length_var.set(val)
        self.length_display.config(text=str(val))

    def generate_password(self):
        length = self.length_var.get()

        # Формирование пула символов
        pool = ""
        guaranteed_chars = []

        if self.use_upper.get():
            pool += string.ascii_uppercase
            guaranteed_chars.append(secrets.choice(string.ascii_uppercase))
        if self.use_lower.get():
            pool += string.ascii_lowercase
            guaranteed_chars.append(secrets.choice(string.ascii_lowercase))
        if self.use_digits.get():
            pool += string.digits
            guaranteed_chars.append(secrets.choice(string.digits))
        if self.use_symbols.get():
            # Набор частых спецсимволов (можно использовать и string.punctuation)
            symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
            pool += symbols
            guaranteed_chars.append(secrets.choice(symbols))

        # Валидация: выбран ли хотя бы один набор
        if not pool:
            messagebox.showwarning(
                "Ошибка", "Выберите хотя бы один набор символов для генерации!"
            )
            return

        # Гарантируем наличие хотя бы одного символа из каждого выбранного набора
        if length < len(guaranteed_chars):
            password_list = [secrets.choice(pool) for _ in range(length)]
        else:
            remaining = length - len(guaranteed_chars)
            password_list = guaranteed_chars + [
                secrets.choice(pool) for _ in range(remaining)
            ]
            secrets.SystemRandom().shuffle(password_list)

        password = "".join(password_list)

        # Вставка в поле
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

        # Оценка
        self.evaluate_strength(password)

    def evaluate_strength(self, password):
        """Оценка стойкости пароля (длина + разнообразие)."""
        length = len(password)
        has_upper = any(c in string.ascii_uppercase for c in password)
        has_lower = any(c in string.ascii_lowercase for c in password)
        has_digit = any(c in string.digits for c in password)
        has_symbol = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

        types_count = sum([has_upper, has_lower, has_digit, has_symbol])

        # Подсчет очков
        score = 0
        if length >= 8:
            score += 1
        if length >= 12:
            score += 1
        if length >= 16:
            score += 1
        if types_count >= 3:
            score += 1
        if types_count == 4 and length >= 12:
            score += 1

        # Формирование вывода
        if score <= 1:
            text = "Очень слабый"
            color = "#e74c3c"  # Красный
            percent = 20
        elif score == 2:
            text = "Слабый"
            color = "#e67e22"  # Оранжевый
            percent = 40
        elif score == 3:
            text = "Средний"
            color = "#f1c40f"  # Желтый
            percent = 60
        elif score == 4:
            text = "Надёжный"
            color = "#2ecc71"  # Зеленый
            percent = 80
        else:
            text = "Очень надёжный"
            color = "#27ae60"  # Темно-зеленый
            percent = 100

        self.strength_label.config(text=f"Надёжность: {text}", foreground=color)
        self.strength_bar["value"] = percent

    def copy_to_clipboard(self):
        pwd = self.password_entry.get()
        if pwd:
            self.root.clipboard_clear()
            self.root.clipboard_append(pwd)
            messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена!")
        else:
            messagebox.showwarning("Внимание", "Нечего копировать!")


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()