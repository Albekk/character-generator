from database import (
    get_game_types,
    get_games_by_type,
    get_races,
    get_classes,
    get_subclasses,
    get_backgrounds
)


def choose_item(items, title):
    """Показывает список и возвращает выбранный элемент."""

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


def main():
    print("==============================")
    print("     CHARACTER GENERATOR")
    print("==============================")

    # Тип игры
    game_type = choose_item(
        get_game_types(),
        "Выберите тип игры:"
    )

    if game_type is None:
        print("Типы игр не найдены.")
        return

    # Игра
    game = choose_item(
        get_games_by_type(game_type["id"]),
        "Выберите игру:"
    )

    if game is None:
        print("Игры этого типа не найдены.")
        return

    # Раса
    race = choose_item(
        get_races(game["id"]),
        "Выберите расу:"
    )

    # Класс
    character_class = choose_item(
        get_classes(game["id"]),
        "Выберите класс:"
    )

    # Подкласс
    subclass = None

    if character_class is not None:
        subclasses = get_subclasses(character_class["id"])

        if subclasses:
            subclass = choose_item(
                subclasses,
                "Выберите подкласс:"
            )

    # Предыстория
    background = choose_item(
        get_backgrounds(game["id"]),
        "Выберите предысторию:"
    )

    # Результат
    print()
    print("==============================")
    print("       ВАШ ПЕРСОНАЖ")
    print("==============================")

    print(f"Тип игры: {game_type['name']}")
    print(f"Игра: {game['name']}")

    if race:
        print(f"Раса: {race['name']}")
    else:
        print("Раса: отсутствует")

    if character_class:
        print(f"Класс: {character_class['name']}")
    else:
        print("Класс: отсутствует")

    if subclass:
        print(f"Подкласс: {subclass['name']}")
    else:
        print("Подкласс: отсутствует")

    if background:
        print(f"Предыстория: {background['name']}")
    else:
        print("Предыстория: отсутствует")

    print("==============================")


if __name__ == "__main__":
    main()