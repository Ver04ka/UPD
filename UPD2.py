import tkinter as tk
from tkinter import messagebox, ttk

# --- СЛОВАРИ ДЛЯ ПРЕОБРАЗОВАНИЯ В СЛОВА ---
UNITS_M = [
    "",
    "один",
    "два",
    "три",
    "четыре",
    "пять",
    "шесть",
    "семь",
    "восемь",
    "девять",
]
UNITS_F = [
    "",
    "одна",
    "две",
    "три",
    "четыре",
    "пять",
    "шесть",
    "семь",
    "восемь",
    "девять",
]
TEENS = [
    "десять",
    "одиннадцать",
    "двенадцать",
    "тринадцать",
    "четырнадцать",
    "пятнадцать",
    "шестнадцать",
    "семнадцать",
    "восемнадцать",
    "девятнадцать",
]
TENS = [
    "",
    "",
    "двадцать",
    "тридцать",
    "сорок",
    "пятьдесят",
    "шестьдесят",
    "семьдесят",
    "восемьдесят",
    "девяносто",
]
HUNDREDS = [
    "",
    "сто",
    "двести",
    "триста",
    "четыреста",
    "пятьсот",
    "шестьсот",
    "семьсот",
    "восемьсот",
    "девятьсот",
]

# Классы разрядов: (форма для 1, форма для 2-4, форма для 5+, род: 'm'/'f')
CLASSES = [
    ("", "", "", "m"),  # единицы
    ("тысяча", "тысячи", "тысяч", "f"),  # тысячи (женский род)
    ("миллион", "миллиона", "миллионов", "m"),  # миллионы
    ("миллиард", "миллиарда", "миллиардов", "m"),  # миллиарды
    ("триллион", "триллиона", "триллионов", "m"),  # триллионы
]


def plural_form(n: int, form1: str, form2: str, form5: str) -> str:
    """Выбирает правильное грамматическое окончание слова."""
    n_abs = abs(n) % 100
    n1 = n_abs % 10
    if 11 <= n_abs <= 19:
        return form5
    if n1 == 1:
        return form1
    if 2 <= n1 <= 4:
        return form2
    return form5


def number_to_words(n: int) -> str:
    """Преобразует целое число в строку словами."""
    if n == 0:
        return "ноль"

    is_negative = n < 0
    n = abs(n)

    triplets = []
    while n > 0:
        triplets.append(n % 1000)
        n //= 1000

    if len(triplets) > len(CLASSES):
        raise ValueError("Слишком большое число (поддерживается до 999 триллионов)")

    words = []

    for i in range(len(triplets) - 1, -1, -1):
        triplet = triplets[i]
        if triplet == 0:
            continue

        h = triplet // 100
        t = (triplet % 100) // 10
        u = triplet % 10
        gender = CLASSES[i][3]

        # 1. Сотни
        if h > 0:
            words.append(HUNDREDS[h])

        # 2. Десятки и единицы
        if t == 1:
            words.append(TEENS[u])
        else:
            if t > 1:
                words.append(TENS[t])
            if u > 0:
                words.append(UNITS_F[u] if gender == "f" else UNITS_M[u])

        # 3. Название разряда (тысячи, миллионы и т.д.)
        class_name = CLASSES[i][0]
        if class_name:
            form = plural_form(
                triplet, CLASSES[i][0], CLASSES[i][1], CLASSES[i][2]
            )
            words.append(form)

    result = " ".join(words)
    if is_negative:
        result = "минус " + result

    return result


# --- ГРАФИЧЕСКИЙ ИНТЕРФЕЙС (TKINTER) ---
class NumberToWordsApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Числа прописью")
        self.root.geometry("520x420")
        self.root.resizable(False, False)

        # Стилизация
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.capitalize_var = tk.BooleanVar(value=True)

        self._create_widgets()

    def _create_widgets(self):
        # 1. Поле ввода числа
        input_frame = ttk.LabelFrame(self.root, text=" Ввод числа ", padding=15)
        input_frame.pack(fill="x", padx=15, pady=10)

        ttk.Label(
            input_frame,
            text="Введите целое число:",
            font=("Arial", 10),
        ).pack(anchor="w", pady=(0, 5))

        self.entry_input = ttk.Entry(
            input_frame, font=("Consolas", 14), justify="center"
        )
        self.entry_input.pack(fill="x", pady=5)
        self.entry_input.focus()
        # Преобразование на лету при нажатии Enter
        self.entry_input.bind("<Return>", lambda event: self.convert())

        # Опции
        opts_frame = ttk.Frame(input_frame)
        opts_frame.pack(fill="x", pady=(5, 0))
        ttk.Checkbutton(
            opts_frame,
            text="С заглавной буквы",
            variable=self.capitalize_var,
            command=self.convert,
        ).pack(side="left")

        # Кнопка перевода
        btn_convert = tk.Button(
            self.root,
            text="Перевести в слова",
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.convert,
        )
        btn_convert.pack(fill="x", padx=15, pady=5, ipady=6)

        # 2. Поле вывода результата
        output_frame = ttk.LabelFrame(
            self.root, text=" Результат прописью ", padding=15
        )
        output_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # Текстовое поле для длинных описаний
        self.text_result = tk.Text(
            output_frame,
            wrap="word",
            font=("Arial", 11),
            height=4,
            relief="solid",
            bd=1,
            padx=5,
            pady=5,
        )
        self.text_result.pack(fill="both", expand=True, pady=(0, 10))

        # Кнопка копирования
        self.btn_copy = ttk.Button(
            output_frame,
            text="Скопировать результат",
            command=self.copy_to_clipboard,
        )
        self.btn_copy.pack(anchor="e")

    def convert(self):
        raw_text = self.entry_input.get().strip().replace(" ", "")

        if not raw_text:
            return

        try:
            number = int(raw_text)
            result = number_to_words(number)

            if self.capitalize_var.get():
                result = result.capitalize()

            self.text_result.delete("1.0", tk.END)
            self.text_result.insert(tk.END, result)
        except ValueError as e:
            if "Слишком большое число" in str(e):
                messagebox.showwarning("Ошибка", str(e))
            else:
                messagebox.showerror(
                    "Ошибка ввода",
                    "Пожалуйста, введите корректное целое число (цифры без букв).",
                )

    def copy_to_clipboard(self):
        text = self.text_result.get("1.0", tk.END).strip()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            messagebox.showinfo("Успех", "Текст скопирован в буфер обмена!")
        else:
            messagebox.showwarning("Внимание", "Нет текста для копирования!")


if __name__ == "__main__":
    root = tk.Tk()
    app = NumberToWordsApp(root)
    root.mainloop()
