import random

from database import (
    get_races,
    get_classes,
    get_subclasses,
    get_backgrounds
)


def choose_item(items, title):
    """Позволяет пользователю выбрать элемент из списка."""

    if not items:
        return None

    print()
    print(title)

    for number, item in enumerate(items, start=1):
        print(f"{number}. {item['name']}")

    while True:
        try:
            choice = int(input("\nВаш выбор: "))

            if 1 <= choice <= len(items):
                return items[choice - 1]

            print("Выберите номер из списка.")

        except ValueError:
            print("Введите число.")


def create_manual_character(game):
    """Создаёт персонажа вручную."""

    race = choose_item(
        get_races(game["id"]),
        "Выберите расу:"
    )

    character_class = choose_item(
        get_classes(game["id"]),
        "Выберите класс:"
    )

    subclass = None

    if character_class:
        subclasses = get_subclasses(character_class["id"])

        if subclasses:
            subclass = choose_item(
                subclasses,
                "Выберите подкласс:"
            )

    background = choose_item(
        get_backgrounds(game["id"]),
        "Выберите предысторию:"
    )

    return {
        "race": race,
        "class": character_class,
        "subclass": subclass,
        "background": background
    }


def create_random_character(game):
    """Создаёт случайного персонажа."""

    races = get_races(game["id"])
    classes = get_classes(game["id"])
    backgrounds = get_backgrounds(game["id"])

    race = random.choice(races) if races else None
    character_class = random.choice(classes) if classes else None
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
        "background": background
    }


def print_character(game_type, game, character):
    """Выводит готового персонажа."""

    print()
    print("==============================")
    print("       ВАШ ПЕРСОНАЖ")
    print("==============================")

    print(f"Тип игры: {game_type['name']}")
    print(f"Игра: {game['name']}")

    if character["race"]:
        print(f"Раса: {character['race']['name']}")
    else:
        print("Раса: отсутствует")

    if character["class"]:
        print(f"Класс: {character['class']['name']}")
    else:
        print("Класс: отсутствует")

    if character["subclass"]:
        print(f"Подкласс: {character['subclass']['name']}")
    else:
        print("Подкласс: отсутствует")

    if character["background"]:
        print(f"Предыстория: {character['background']['name']}")
    else:
        print("Предыстория: отсутствует")

    print("==============================")