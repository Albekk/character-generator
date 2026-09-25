import tkinter as tk
from tkinter import ttk
from quiz.engine import (
    QUIZ_TYPES,
    create_quiz_character_from_scores
)

from quiz.fantasy import FANTASY_QUESTIONS
from quiz.cyberpunk import CYBERPUNK_QUESTIONS
from database import (
    get_game_types,
    get_games_by_type,
    get_races,
    get_classes,
    get_subclasses,
    get_backgrounds,
    save_character,
    get_saved_characters
)
from generator import create_random_character


class CharacterGeneratorApp:
    def __init__(self, root):
        self.root = root

        self.root.title("Character Generator")
        self.root.geometry("900x600")
        self.root.minsize(700, 500)

        self.game_types = []
        self.games = []

        self.selected_game_type = None
        self.selected_game = None

        self.create_main_menu()

    def clear_window(self):
        """Удаляет все элементы текущего экрана."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_main_menu(self):
        """Создаёт главное меню."""
        self.clear_window()

        container = ttk.Frame(
            self.root,
            padding=40
        )
        container.pack(
            expand=True,
            fill="both"
        )

        title = ttk.Label(
            container,
            text="CHARACTER GENERATOR",
            font=("Arial", 26, "bold")
        )
        title.pack(pady=(80, 10))

        subtitle = ttk.Label(
            container,
            text="Генератор персонажей для ролевых игр",
            font=("Arial", 12)
        )
        subtitle.pack(pady=(0, 50))

        create_button = ttk.Button(
            container,
            text="Создать персонажа",
            command=self.open_create_character
        )
        create_button.pack(
            ipadx=30,
            ipady=10,
            pady=10
        )

        saved_button = ttk.Button(
            container,
            text="Мои персонажи",
            command=self.open_saved_characters
        )
        saved_button.pack(
            ipadx=38,
            ipady=10,
            pady=10
        )

        exit_button = ttk.Button(
            container,
            text="Выход",
            command=self.root.destroy
        )
        exit_button.pack(
            ipadx=67,
            ipady=10,
            pady=10
        )

    def open_create_character(self):
        """Экран выбора игры."""

        self.clear_window()

        container = ttk.Frame(
            self.root,
            padding=40
        )
        container.pack(
            expand=True,
            fill="both"
        )

        title = ttk.Label(
            container,
            text="Создание персонажа",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=(15, 20))

        # Получаем типы игр из БД
        self.game_types = get_game_types()

        ttk.Label(
            container,
            text="Тип игры:",
            font=("Arial", 11)
        ).pack(pady=(5, 5))

        self.game_type_combobox = ttk.Combobox(
            container,
            state="readonly",
            width=35
        )

        self.game_type_combobox["values"] = [
            game_type["name"]
            for game_type in self.game_types
        ]

        self.game_type_combobox.pack(ipady=5)

        # При изменении типа обновляем игры
        self.game_type_combobox.bind(
            "<<ComboboxSelected>>",
            self.on_game_type_selected
        )

        ttk.Label(
            container,
            text="Игра:",
            font=("Arial", 11)
        ).pack(pady=(5, 5))

        self.game_combobox = ttk.Combobox(
            container,
            state="readonly",
            width=35
        )

        self.game_combobox.pack(ipady=5)

        self.game_combobox.bind(
            "<<ComboboxSelected>>",
            self.on_game_selected
        )

        # Автоматически выбираем первый тип
        if self.game_types:
            self.game_type_combobox.current(0)
            self.on_game_type_selected()

        button_frame = ttk.Frame(container)
        button_frame.pack(pady=40)

        manual_button = ttk.Button(
            button_frame,
            text="Составить вручную",
            command=self.open_manual_mode
        )
        manual_button.pack(
            fill="x",
            ipadx=30,
            ipady=7,
            pady=6
        )

        quiz_button = ttk.Button(
            button_frame,
            text="Пройти тест",
            command=self.open_quiz_mode
        )
        quiz_button.pack(
            fill="x",
            ipadx=30,
            ipady=7,
            pady=6
        )

        random_button = ttk.Button(
            button_frame,
            text="Случайный персонаж",
            command=self.open_random_mode
        )
        random_button.pack(
            fill="x",
            ipadx=30,
            ipady=7,
            pady=6
        )

        ttk.Button(
            container,
            text="Назад",
            command=self.create_main_menu
        ).pack(
            ipadx=30,
            ipady=6,
            pady=(15, 5)
        )

    def open_saved_characters(self):
        """Показывает сохранённых персонажей."""

        self.clear_window()

        container = ttk.Frame(
            self.root,
            padding=30
        )
        container.pack(
            expand=True,
            fill="both"
        )

        title = ttk.Label(
            container,
            text="Мои персонажи",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=(10, 20))

        characters = get_saved_characters()

        if not characters:
            ttk.Label(
                container,
                text="Сохранённых персонажей пока нет.",
                font=("Arial", 12)
            ).pack(pady=30)

        else:
            columns = (
                "name",
                "game",
                "race",
                "class",
                "subclass",
                "background"
            )

            table = ttk.Treeview(
                container,
                columns=columns,
                show="headings",
                height=12
            )

            table.heading("name", text="Имя")
            table.heading("game", text="Игра")
            table.heading("race", text="Раса")
            table.heading("class", text="Класс")
            table.heading("subclass", text="Подкласс")
            table.heading("background", text="Предыстория")

            table.column("name", width=100)
            table.column("game", width=170)
            table.column("race", width=100)
            table.column("class", width=100)
            table.column("subclass", width=150)
            table.column("background", width=140)

            for character in characters:
                table.insert(
                    "",
                    "end",
                    values=(
                        character["character_name"],
                        character["game"],
                        character["race"],
                        character["class"],
                        character["subclass"] or "—",
                        character["background"] or "—"
                    )
                )

            table.pack(
                expand=True,
                fill="both",
                pady=10
            )

        ttk.Button(
            container,
            text="Назад",
            command=self.create_main_menu
        ).pack(
            ipadx=30,
            ipady=6,
            pady=10
        )

    def on_game_type_selected(self, event=None):
        """Обновляет список игр после выбора типа."""

        index = self.game_type_combobox.current()

        if index < 0:
            return

        self.selected_game_type = self.game_types[index]

        self.games = get_games_by_type(
            self.selected_game_type["id"]
        )

        self.game_combobox["values"] = [
            game["name"]
            for game in self.games
        ]

        if self.games:
            self.game_combobox.current(0)
            self.selected_game = self.games[0]

        else:
            self.game_combobox.set("")
            self.selected_game = None

    def open_manual_mode(self):
        """Экран ручного создания персонажа."""

        if not self.selected_game:
            return

        self.clear_window()

        container = ttk.Frame(
            self.root,
            padding=30
        )
        container.pack(
            expand=True,
            fill="both"
        )

        ttk.Label(
            container,
            text="Создание персонажа вручную",
            font=("Arial", 22, "bold")
        ).pack(pady=(10, 10))

        ttk.Label(
            container,
            text=f"Игра: {self.selected_game['name']}",
            font=("Arial", 12)
        ).pack(pady=(0, 20))

        # Получаем данные из БД
        self.manual_races = get_races(self.selected_game["id"])
        self.manual_classes = get_classes(self.selected_game["id"])
        self.manual_backgrounds = get_backgrounds(self.selected_game["id"])

        # ---------- РАСА ----------

        ttk.Label(
            container,
            text="Раса:"
        ).pack(pady=(5, 3))

        self.race_combobox = ttk.Combobox(
            container,
            state="readonly",
            width=35
        )

        self.race_combobox["values"] = [
            race["name"] for race in self.manual_races
        ]

        self.race_combobox.pack(ipady=4)

        if self.manual_races:
            self.race_combobox.current(0)

        # ---------- КЛАСС ----------

        ttk.Label(
            container,
            text="Класс:"
        ).pack(pady=(12, 3))

        self.class_combobox = ttk.Combobox(
            container,
            state="readonly",
            width=35
        )

        self.class_combobox["values"] = [
            character_class["name"]
            for character_class in self.manual_classes
        ]

        self.class_combobox.pack(ipady=4)

        self.class_combobox.bind(
            "<<ComboboxSelected>>",
            self.on_manual_class_selected
        )

        # ---------- ПОДКЛАСС ----------

        ttk.Label(
            container,
            text="Подкласс:"
        ).pack(pady=(12, 3))

        self.subclass_combobox = ttk.Combobox(
            container,
            state="readonly",
            width=35
        )

        self.subclass_combobox.pack(ipady=4)

        # ---------- ПРЕДЫСТОРИЯ ----------

        ttk.Label(
            container,
            text="Предыстория:"
        ).pack(pady=(12, 3))

        self.background_combobox = ttk.Combobox(
            container,
            state="readonly",
            width=35
        )

        self.background_combobox["values"] = [
            background["name"]
            for background in self.manual_backgrounds
        ]

        self.background_combobox.pack(ipady=4)

        if self.manual_backgrounds:
            self.background_combobox.current(0)

        # Автоматически выбираем первый класс
        if self.manual_classes:
            self.class_combobox.current(0)
            self.on_manual_class_selected()

        ttk.Button(
            container,
            text="Создать персонажа",
            command=self.create_manual_character_gui
        ).pack(
            ipadx=35,
            ipady=7,
            pady=(25, 7)
        )

        ttk.Button(
            container,
            text="Назад",
            command=self.open_create_character
        ).pack(
            ipadx=35,
            ipady=7,
            pady=5
        )

    def open_quiz_mode(self):
        """Запускает тест для выбранной игры."""

        if not self.selected_game:
            return

        quiz_type = QUIZ_TYPES.get(
            self.selected_game["name"],
            "fantasy"
        )

        if quiz_type == "cyberpunk":
            self.quiz_questions = CYBERPUNK_QUESTIONS
        else:
            self.quiz_questions = FANTASY_QUESTIONS

        self.quiz_question_index = 0
        self.quiz_scores = {}

        self.show_quiz_question()

    def show_quiz_question(self):
        """Показывает текущий вопрос теста."""

        self.clear_window()

        question = self.quiz_questions[self.quiz_question_index]

        container = ttk.Frame(
            self.root,
            padding=30
        )
        container.pack(
            expand=True,
            fill="both"
        )

        ttk.Label(
            container,
            text="Тест персонажа",
            font=("Arial", 22, "bold")
        ).pack(pady=(20, 10))

        ttk.Label(
            container,
            text=f"Игра: {self.selected_game['name']}",
            font=("Arial", 11)
        ).pack(pady=(0, 10))

        ttk.Label(
            container,
            text=(
                f"Вопрос {self.quiz_question_index + 1} "
                f"из {len(self.quiz_questions)}"
            ),
            font=("Arial", 10)
        ).pack(pady=5)

        ttk.Label(
            container,
            text=question["text"],
            font=("Arial", 14, "bold"),
            wraplength=700,
            justify="center"
        ).pack(pady=(20, 20))

        self.quiz_answer_var = tk.IntVar(value=-1)

        for index, answer in enumerate(question["answers"]):
            ttk.Radiobutton(
                container,
                text=answer[0],
                variable=self.quiz_answer_var,
                value=index
            ).pack(
                anchor="center",
                pady=7
            )

        self.quiz_error_label = ttk.Label(
            container,
            text=""
        )
        self.quiz_error_label.pack(pady=5)

        ttk.Button(
            container,
            text="Далее",
            command=self.next_quiz_question
        ).pack(
            ipadx=40,
            ipady=7,
            pady=(15, 5)
        )

        ttk.Button(
            container,
            text="Отменить тест",
            command=self.open_create_character
        ).pack(
            ipadx=30,
            ipady=5,
            pady=5
        )

    def next_quiz_question(self):
        """Сохраняет ответ и переходит к следующему вопросу."""

        answer_index = self.quiz_answer_var.get()

        if answer_index == -1:
            self.quiz_error_label.config(
                text="Выберите один из вариантов ответа."
            )
            return

        question = self.quiz_questions[self.quiz_question_index]

        answer_scores = question["answers"][answer_index][1]

        for tag, points in answer_scores.items():
            self.quiz_scores[tag] = (
                    self.quiz_scores.get(tag, 0) + points
            )

        self.quiz_question_index += 1

        if self.quiz_question_index < len(self.quiz_questions):
            self.show_quiz_question()
        else:
            character = create_quiz_character_from_scores(
                self.selected_game,
                self.quiz_scores
            )

            self.show_character_result(character)

    def on_manual_class_selected(self, event=None):
        """Обновляет подклассы при выборе класса."""

        class_index = self.class_combobox.current()

        if class_index < 0:
            return

        selected_class = self.manual_classes[class_index]

        self.manual_subclasses = get_subclasses(
            selected_class["id"]
        )

        if self.manual_subclasses:
            self.subclass_combobox["values"] = [
                subclass["name"]
                for subclass in self.manual_subclasses
            ]

            self.subclass_combobox.current(0)

        else:
            self.subclass_combobox["values"] = [
                "Подклассы отсутствуют"
            ]

            self.subclass_combobox.current(0)

    def create_manual_character_gui(self):
        """Создаёт персонажа из выбранных пользователем параметров."""

        race_index = self.race_combobox.current()
        class_index = self.class_combobox.current()
        background_index = self.background_combobox.current()

        if race_index < 0 or class_index < 0:
            return

        race = self.manual_races[race_index]
        character_class = self.manual_classes[class_index]

        # Подкласс
        if self.manual_subclasses:
            subclass_index = self.subclass_combobox.current()

            if subclass_index >= 0:
                subclass = self.manual_subclasses[subclass_index]
            else:
                subclass = None
        else:
            subclass = None

        # Предыстория
        if self.manual_backgrounds and background_index >= 0:
            background = self.manual_backgrounds[background_index]
        else:
            background = None

        character = {
            "race": race,
            "class": character_class,
            "subclass": subclass,
            "background": background
        }

        self.show_character_result(character)

    def open_random_mode(self):
        """Создаёт случайного персонажа и показывает результат."""

        if not self.selected_game:
            return

        character = create_random_character(self.selected_game)

        self.show_character_result(character)

    def show_character_result(self, character):
        """Показывает готового персонажа в GUI."""

        self.clear_window()
        self.current_character = character

        container = ttk.Frame(
            self.root,
            padding=40
        )
        container.pack(
            expand=True,
            fill="both"
        )

        title = ttk.Label(
            container,
            text="Ваш персонаж",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=(15, 15))

        game_name = self.selected_game["name"]

        ttk.Label(
            container,
            text=f"Игра: {game_name}",
            font=("Arial", 12)
        ).pack(pady=5)

        race = character["race"]["name"] if character["race"] else "Отсутствует"
        character_class = (
            character["class"]["name"]
            if character["class"]
            else "Отсутствует"
        )
        subclass = (
            character["subclass"]["name"]
            if character["subclass"]
            else "Отсутствует"
        )
        background = (
            character["background"]["name"]
            if character["background"]
            else "Отсутствует"
        )

        ttk.Label(
            container,
            text=f"Раса: {race}",
            font=("Arial", 14)
        ).pack(pady=4)

        ttk.Label(
            container,
            text=f"Класс: {character_class}",
            font=("Arial", 14)
        ).pack(pady=4)

        ttk.Label(
            container,
            text=f"Подкласс: {subclass}",
            font=("Arial", 14)
        ).pack(pady=4)

        ttk.Label(
            container,
            text=f"Предыстория: {background}",
            font=("Arial", 14)
        ).pack(pady=4)

        ttk.Label(
            container,
            text="Имя персонажа:",
            font=("Arial", 11)
        ).pack(pady=(15, 5))

        self.character_name_entry = ttk.Entry(
            container,
            width=30
        )
        self.character_name_entry.pack(ipady=5)

        self.save_status_label = ttk.Label(
            container,
            text=""
        )
        self.save_status_label.pack(pady=5)

        self.save_button = ttk.Button(
            container,
            text="Сохранить персонажа",
            command=self.save_current_character
        )

        self.save_button.pack(
            ipadx=30,
            ipady=6,
            pady=5
        )

        ttk.Button(
            container,
            text="Назад",
            command=self.open_create_character
        ).pack(
            ipadx=30,
            ipady=6,
            pady=5
        )

    def on_game_selected(self, event=None):
        """Сохраняет выбранную игру."""

        index = self.game_combobox.current()

        if index >= 0:
            self.selected_game = self.games[index]

    def save_current_character(self):
        """Сохраняет текущего персонажа в БД."""

        name = self.character_name_entry.get().strip()

        if not name:
            self.save_status_label.config(
                text="Введите имя персонажа."
            )
            return

        character = self.current_character

        race_id = (
            character["race"]["id"]
            if character["race"]
            else None
        )

        class_id = (
            character["class"]["id"]
            if character["class"]
            else None
        )

        subclass_id = (
            character["subclass"]["id"]
            if character["subclass"]
            else None
        )

        background_id = (
            character["background"]["id"]
            if character["background"]
            else None
        )

        character_id = save_character(
            self.selected_game["id"],
            race_id,
            class_id,
            subclass_id,
            background_id,
            name
        )

        if character_id:
            self.save_status_label.config(
                text=f"Персонаж «{name}» сохранён! ID: {character_id}"
            )
            self.save_button.config(state="disabled")
            self.character_name_entry.config(state="disabled")
        else:
            self.save_status_label.config(
                text="Не удалось сохранить персонажа."
            )

def run_gui():
    root = tk.Tk()

    app = CharacterGeneratorApp(root)

    root.mainloop()

if __name__ == "__main__":
    run_gui()