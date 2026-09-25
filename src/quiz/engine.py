import random

from database import (
    get_races,
    get_classes,
    get_subclasses,
    get_backgrounds
)

from .fantasy import FANTASY_QUESTIONS, FANTASY_CLASS_TAGS
from .cyberpunk import CYBERPUNK_QUESTIONS, CYBERPUNK_CLASS_TAGS


QUIZ_TYPES = {
    "Pathfinder": "fantasy",
    "Dungeons & Dragons": "fantasy",
    "Divinity: Original Sin 2": "fantasy",
    "Warhammer Fantasy Roleplay": "fantasy",
    "Baldur's Gate 3": "fantasy",
    "Pathfinder: Wrath of the Righteous": "fantasy",
    "Cyberpunk RED": "cyberpunk"
}


def ask_question(question):
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
    tags = class_tags.get(class_name)

    if tags is None:
        return 0

    score = 0

    for tag, importance in tags.items():
        score += player_scores.get(tag, 0) * importance

    return score


def find_best_class(game_id, player_scores, class_tags):
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
def create_quiz_character_from_scores(game, scores):
    """Создаёт персонажа по результатам теста из GUI."""

    quiz_type = QUIZ_TYPES.get(game["name"], "fantasy")

    if quiz_type == "cyberpunk":
        class_tags = CYBERPUNK_CLASS_TAGS
    else:
        class_tags = FANTASY_CLASS_TAGS

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