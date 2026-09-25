from database import get_game_types, get_games_by_type

from generator import (
    choose_item,
    create_manual_character,
    create_random_character,
    print_character,
    ask_to_save_character,
    show_saved_characters
)

from quiz import create_quiz_character


def choose_creation_mode():
    print()
    print("Выберите способ создания персонажа:")
    print("1. Составить вручную")
    print("2. Пройти тест")
    print("3. Случайный персонаж")

    while True:
        choice = input("\nВаш выбор: ")

        if choice in ("1", "2", "3"):
            return choice

        print("Введите 1, 2 или 3.")


def create_character():
    """Создание нового персонажа."""

    game_type = choose_item(
        get_game_types(),
        "Выберите тип игры:"
    )

    if game_type is None:
        print("Типы игр не найдены.")
        return

    game = choose_item(
        get_games_by_type(game_type["id"]),
        "Выберите игру:"
    )

    if game is None:
        print("Игры этого типа не найдены.")
        return

    mode = choose_creation_mode()

    if mode == "1":
        character = create_manual_character(game)

    elif mode == "2":
        character = create_quiz_character(game)

    else:
        character = create_random_character(game)

    print_character(game_type, game, character)

    ask_to_save_character(game, character)


def main():
    while True:
        print()
        print("==============================")
        print("     CHARACTER GENERATOR")
        print("==============================")
        print("1. Создать персонажа")
        print("2. Мои персонажи")
        print("3. Выход")

        choice = input("\nВаш выбор: ")

        if choice == "1":
            create_character()

        elif choice == "2":
            show_saved_characters()

        elif choice == "3":
            print()
            print("До свидания!")
            break

        else:
            print("Введите 1, 2 или 3.")


if __name__ == "__main__":
    main()