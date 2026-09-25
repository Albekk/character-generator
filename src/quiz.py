import random

from database import (
    get_races,
    get_classes,
    get_subclasses,
    get_backgrounds
)


QUESTIONS = [
    {
        "text": "Как вы предпочитаете решать проблемы?",
        "answers": [
            ("Силой", {"warrior": 2}),
            ("Магией или знаниями", {"magic": 2}),
            ("Хитростью", {"stealth": 2}),
            ("Переговорами и помощью другим", {"support": 2})
        ]
    },
    {
        "text": "Какой стиль боя вам ближе?",
        "answers": [
            ("Ближний бой", {"warrior": 2}),
            ("Заклинания и необычные способности", {"magic": 2}),
            ("Скрытность и точные атаки", {"stealth": 2}),
            ("Поддержка союзников", {"support": 2})
        ]
    },
    {
        "text": "Что для вас важнее всего?",
        "answers": [
            ("Сила и выносливость", {"warrior": 2}),
            ("Интеллект и знания", {"magic": 2}),
            ("Ловкость и осторожность", {"stealth": 2}),
            ("Харизма и взаимодействие с людьми", {"support": 2})
        ]
    },
    {
        "text": "Группа попала в опасную ситуацию. Что вы сделаете?",
        "answers": [
            ("Встану впереди и приму удар на себя", {"warrior": 2, "support": 1}),
            ("Попытаюсь найти магическое или техническое решение", {"magic": 2}),
            ("Попытаюсь незаметно обойти противника", {"stealth": 2}),
            ("Помогу группе и попробую придумать общий план", {"support": 2})
        ]
    },
    {
        "text": "Какой герой вам интереснее?",
        "answers": [
            ("Могучий воин", {"warrior": 2}),
            ("Таинственный маг или учёный", {"magic": 2}),
            ("Ловкий авантюрист", {"stealth": 2}),
            ("Лидер или защитник команды", {"support": 2})
        ]
    }
]


CLASS_TAGS = {
    # Общие названия
    "Воин": {"warrior": 3},
    "Варвар": {"warrior": 3},
    "Паладин": {"warrior": 2, "support": 2},
    "Монах": {"warrior": 2, "stealth": 1},
    "Следопыт": {"warrior": 1, "stealth": 2},
    "Плут": {"stealth": 3},
    "Убийца": {"stealth": 3},
    "Истребитель": {"warrior": 2, "stealth": 1},

    "Волшебник": {"magic": 3},
    "Чародей": {"magic": 3},
    "Ведьма": {"magic": 3},
    "Магус": {"warrior": 2, "magic": 2},
    "Арканист": {"magic": 3},
    "Кинетик": {"magic": 2, "warrior": 1},

    "Жрец": {"magic": 1, "support": 3},
    "Друид": {"magic": 2, "support": 1},
    "Бард": {"magic": 1, "support": 3},
    "Шаман": {"magic": 2, "support": 2},
    "Оракул": {"magic": 2, "support": 2},
    "Воин-жрец": {"warrior": 2, "support": 2},
}


def ask_question(question):
    """Задаёт один вопрос и возвращает баллы ответа."""

    print()
    print(question["text"])

    for number, answer in enumerate(question["answers"], start=1):
        print(f"{number}. {answer[0]}")

    while True:
        try:
            choice = int(input("\nВаш выбор: "))

            if 1 <= choice <= len(question["answers"]):
                return question["answers"][choice - 1][1]

            print("Выберите номер из списка.")

        except ValueError:
            print("Введите число.")


def calculate_scores():
    """Проводит тест и подсчитывает баллы."""

    scores = {
        "warrior": 0,
        "magic": 0,
        "stealth": 0,
        "support": 0
    }

    print()
    print("==============================")
    print("       ТЕСТ ПЕРСОНАЖА")
    print("==============================")

    for question in QUESTIONS:
        answer_scores = ask_question(question)

        for tag, points in answer_scores.items():
            scores[tag] += points

    return scores


def calculate_class_score(class_name, player_scores):
    """Считает, насколько класс подходит ответам игрока."""

    tags = CLASS_TAGS.get(class_name)

    if tags is None:
        return 0

    score = 0

    for tag, importance in tags.items():
        score += player_scores[tag] * importance

    return score


def find_best_class(game_id, player_scores):
    """Находит наиболее подходящий класс выбранной игры."""

    classes = get_classes(game_id)

    if not classes:
        return None

    best_classes = []
    best_score = -1

    for character_class in classes:
        score = calculate_class_score(
            character_class["name"],
            player_scores
        )

        if score > best_score:
            best_score = score
            best_classes = [character_class]

        elif score == best_score:
            best_classes.append(character_class)

    return random.choice(best_classes)


def create_quiz_character(game):
    """Создаёт персонажа по результатам теста."""

    scores = calculate_scores()

    character_class = find_best_class(
        game["id"],
        scores
    )

    races = get_races(game["id"])
    backgrounds = get_backgrounds(game["id"])

    race = random.choice(races) if races else None
    background = random.choice(backgrounds) if backgrounds else None

    subclass = None

    if character_class:
        subclasses = get_subclasses(character_class["id"])

        if subclasses:
            subclass = random.choice(subclasses)

    return {
        "race": race,
        "class": character_class,
        "subclass": subclass,
        "background": background,
        "scores": scores
    }