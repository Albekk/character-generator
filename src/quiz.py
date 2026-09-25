import random

from database import (
    get_races,
    get_classes,
    get_subclasses,
    get_backgrounds
)


# Какой тест используется для каждой игры
QUIZ_TYPES = {
    "Pathfinder": "fantasy",
    "Dungeons & Dragons": "fantasy",
    "Divinity: Original Sin 2": "fantasy",
    "Warhammer Fantasy Roleplay": "fantasy",
    "Baldur's Gate 3": "fantasy",
    "Pathfinder: Wrath of the Righteous": "fantasy",
    "Cyberpunk RED": "cyberpunk"
}


# ============================================================
# ФЭНТЕЗИ-КВИЗ
# ============================================================

FANTASY_QUESTIONS = [
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
            ("Встану впереди и приму удар на себя",
             {"warrior": 2, "support": 1}),

            ("Попытаюсь найти магическое решение",
             {"magic": 2}),

            ("Попытаюсь незаметно обойти противника",
             {"stealth": 2}),

            ("Помогу группе и продумаю общий план",
             {"support": 2})
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


FANTASY_CLASS_TAGS = {
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

    # BG3
    "Колдун": {"magic": 3},
    "Клирик": {"magic": 1, "support": 3}
}


# ============================================================
# CYBERPUNK RED
# ============================================================

CYBERPUNK_QUESTIONS = [
    {
        "text": "Началась перестрелка. Что вы сделаете?",
        "answers": [
            ("Вступлю в бой", {"combat": 3}),
            ("Взломаю систему безопасности", {"hacking": 3}),
            ("Использую технику или гаджеты", {"tech": 3}),
            ("Найду способ решить проблему через связи", {"social": 3})
        ]
    },
    {
        "text": "Что для вас ценнее всего в Найт-Сити?",
        "answers": [
            ("Боевая репутация", {"combat": 2}),
            ("Информация", {"hacking": 1, "investigation": 2}),
            ("Деньги и полезные знакомства", {"social": 3}),
            ("Свобода и возможность быть в дороге", {"mobility": 3})
        ]
    },
    {
        "text": "Ваш напарник тяжело ранен. Что будете делать?",
        "answers": [
            ("Прикрою его и устраню угрозу", {"combat": 2}),
            ("Окажу медицинскую помощь", {"medical": 3}),
            ("Организую помощь через своих людей", {"leadership": 2, "social": 1}),
            ("Быстро вывезу команду из опасной зоны", {"mobility": 3})
        ]
    },
    {
        "text": "Какую работу вы бы выбрали?",
        "answers": [
            ("Наёмник и телохранитель", {"combat": 3}),
            ("Взлом защищённой сети", {"hacking": 3}),
            ("Ремонт и создание оборудования", {"tech": 3}),
            ("Поиск компромата и расследование", {"investigation": 3})
        ]
    },
    {
        "text": "Как вы хотите влиять на Найт-Сити?",
        "answers": [
            ("Стать известным и вести людей за собой",
             {"performance": 3}),

            ("Получить власть внутри корпорации",
             {"leadership": 3}),

            ("Контролировать сделки и связи",
             {"social": 3}),

            ("Раскрывать правду",
             {"investigation": 3})
        ]
    },
    {
        "text": "Ваш главный инструмент?",
        "answers": [
            ("Оружие", {"combat": 2}),
            ("Кибердека", {"hacking": 2}),
            ("Инструменты и оборудование", {"tech": 2}),
            ("Слова, репутация и связи", {"social": 2, "performance": 1})
        ]
    }
]


CYBERPUNK_CLASS_TAGS = {
    "Рокер": {"performance": 3, "social": 1},
    "Rockerboy": {"performance": 3, "social": 1},

    "Соло": {"combat": 3},
    "Solo": {"combat": 3},

    "Нетраннер": {"hacking": 3},
    "Netrunner": {"hacking": 3},

    "Техник": {"tech": 3},
    "Tech": {"tech": 3},

    "Медтех": {"medical": 3, "tech": 1},
    "Medtech": {"medical": 3, "tech": 1},

    "Медиа": {"investigation": 3, "social": 1},
    "Media": {"investigation": 3, "social": 1},

    "Корпорат": {"leadership": 3, "social": 1},
    "Exec": {"leadership": 3, "social": 1},

    "Законник": {"combat": 1, "leadership": 2},
    "Lawman": {"combat": 1, "leadership": 2},

    "Фиксер": {"social": 3},
    "Fixer": {"social": 3},

    "Кочевник": {"mobility": 3},
    "Nomad": {"mobility": 3}
}


# ============================================================
# ОБЩИЕ ФУНКЦИИ
# ============================================================

def ask_question(question):
    """Задаёт один вопрос."""

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


def calculate_scores(questions):
    """Проводит тест и суммирует полученные баллы."""

    scores = {}

    print()
    print("==============================")
    print("       ТЕСТ ПЕРСОНАЖА")
    print("==============================")

    for question in questions:
        answer_scores = ask_question(question)

        for tag, points in answer_scores.items():
            scores[tag] = scores.get(tag, 0) + points

    return scores


def calculate_class_score(class_name, player_scores, class_tags):
    """Определяет соответствие класса результатам теста."""

    tags = class_tags.get(class_name)

    if tags is None:
        return 0

    score = 0

    for tag, importance in tags.items():
        score += player_scores.get(tag, 0) * importance

    return score


def find_best_class(game_id, player_scores, class_tags):
    """Выбирает наиболее подходящий класс из выбранной игры."""

    classes = get_classes(game_id)

    if not classes:
        return None

    best_classes = []
    best_score = -1

    for character_class in classes:
        score = calculate_class_score(
            character_class["name"],
            player_scores,
            class_tags
        )

        if score > best_score:
            best_score = score
            best_classes = [character_class]

        elif score == best_score:
            best_classes.append(character_class)

    return random.choice(best_classes)


def create_quiz_character(game):
    """Создаёт персонажа на основании теста."""

    quiz_type = QUIZ_TYPES.get(game["name"], "fantasy")

    if quiz_type == "cyberpunk":
        questions = CYBERPUNK_QUESTIONS
        class_tags = CYBERPUNK_CLASS_TAGS
    else:
        questions = FANTASY_QUESTIONS
        class_tags = FANTASY_CLASS_TAGS

    scores = calculate_scores(questions)

    character_class = find_best_class(
        game["id"],
        scores,
        class_tags
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