import mysql.connector
from mysql.connector import Error


def get_connection():

    return mysql.connector.connect(
        host="127.127.126.30",
        port=3306,
        user="root",
        password="",
        database="character_generator",
        charset="utf8mb4",
        use_pure = True
    )


def execute_select(query, params=None):

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(query, params or ())
        return cursor.fetchall()

    except Error as error:
        print(f"Ошибка базы данных: {error}")
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def get_game_types():

    return execute_select(
        "SELECT id, name FROM game_types ORDER BY id"
    )


def get_games_by_type(game_type_id):
    """Возвращает игры выбранного типа."""
    return execute_select(
        """
        SELECT id, name
        FROM games
        WHERE game_type_id = %s
        ORDER BY name
        """,
        (game_type_id,)
    )


def get_races(game_id):

    return execute_select(
        """
        SELECT id, name
        FROM races
        WHERE game_id = %s
        ORDER BY name
        """,
        (game_id,)
    )


def get_classes(game_id):

    return execute_select(
        """
        SELECT id, name
        FROM classes
        WHERE game_id = %s
        ORDER BY name
        """,
        (game_id,)
    )


def get_subclasses(class_id):

    return execute_select(
        """
        SELECT id, name
        FROM subclasses
        WHERE class_id = %s
        ORDER BY name
        """,
        (class_id,)
    )


def get_backgrounds(game_id):

    return execute_select(
        """
        SELECT id, name
        FROM backgrounds
        WHERE game_id = %s
        ORDER BY name
        """,
        (game_id,)
    )

def save_character(game_id, race_id, class_id,
                   subclass_id, background_id, name):
    """Сохраняет созданного персонажа в базу данных."""

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO characters
            (game_id, race_id, class_id, subclass_id, background_id, name)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                game_id,
                race_id,
                class_id,
                subclass_id,
                background_id,
                name
            )
        )

        connection.commit()

        return cursor.lastrowid

    except Error as error:
        print(f"Ошибка сохранения персонажа: {error}")
        return None

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def get_saved_characters():
    """Возвращает всех сохранённых персонажей."""

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                characters.id,
                characters.name AS character_name,
                games.name AS game,
                races.name AS race,
                classes.name AS class,
                subclasses.name AS subclass,
                backgrounds.name AS background,
                characters.created_at
            FROM characters
            JOIN games
                ON characters.game_id = games.id
            JOIN races
                ON characters.race_id = races.id
            JOIN classes
                ON characters.class_id = classes.id
            LEFT JOIN subclasses
                ON characters.subclass_id = subclasses.id
            LEFT JOIN backgrounds
                ON characters.background_id = backgrounds.id
            ORDER BY characters.created_at DESC
        """

        cursor.execute(query)

        return cursor.fetchall()

    except Error as error:
        print(f"Ошибка получения персонажей: {error}")
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()