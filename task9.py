import psycopg2
from prettytable import PrettyTable

# Параметри підключення до бази даних
db_config = {
    "dbname": "cinema_db",
    "user": "admin",
    "password": "admin123",
    "host": "localhost",
    "port": 5432
}


def print_table_structure(cursor, table_name):
    """Отримує та виводить структуру таблиці"""
    query = f"""
    SELECT column_name, data_type, character_maximum_length
    FROM information_schema.columns
    WHERE table_name = '{table_name}';
    """
    cursor.execute(query)
    columns = cursor.fetchall()

    print(f"\n--- Структура таблиці '{table_name}' ---")
    structure_table = PrettyTable(["Стовпець", "Тип даних", "Довжина"])
    for column in columns:
        structure_table.add_row(column)
    print(structure_table)


def print_table_data(cursor, table_name):
    """Отримує та виводить дані з таблиці"""
    query = f"SELECT * FROM {table_name};"
    cursor.execute(query)
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    print(f"\n--- Дані таблиці '{table_name}' ---")
    data_table = PrettyTable(column_names)
    for row in rows:
        data_table.add_row(row)
    print(data_table)


def execute_custom_query(cursor, query, description):
    """Виконує запит та виводить результати"""
    cursor.execute(query)
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    print(f"\n--- {description} ---")
    result_table = PrettyTable(column_names)
    for row in rows:
        result_table.add_row(row)
    print(result_table)


def main():
    try:
        # Підключення до бази даних
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Отримання списку таблиць
        cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public';
        """)
        tables = cursor.fetchall()

        print("=== Таблиці у базі даних ===")
        for table in tables:
            print(f"- {table[0]}")

        # Виведення структури та даних для кожної таблиці
        for table in tables:
            table_name = table[0]
            print_table_structure(cursor, table_name)
            print_table_data(cursor, table_name)

        # Виконання запитів
        queries = [
            ("Відобразити всі комедії, відсортовані за рейтингом",
             "SELECT * FROM Films WHERE genre = 'комедія' ORDER BY rating DESC;"),
            ("Порахувати останню дату показу фільму для кожного транслювання",
             """
             SELECT f.title AS Назва_фільму, c.name AS Назва_кінотеатру, 
                    s.start_date AS Дата_початку, s.duration AS Тривалість_днів,
                    (s.start_date + s.duration * interval '1 day') AS Кінцева_дата
             FROM Showings s
             JOIN Films f ON s.film_id = f.film_id
             JOIN Cinemas c ON s.cinema_id = c.cinema_id;
             """),
            ("Порахувати максимальний прибуток для кожного кінотеатру від одного показу",
             """
             SELECT c.name AS Назва_кінотеатру, 
                    MAX(c.ticket_price * c.seats) AS Максимальний_прибуток
             FROM Cinemas c
             JOIN Showings s ON c.cinema_id = s.cinema_id
             GROUP BY c.name;
             """)
        ]

        for description, query in queries:
            execute_custom_query(cursor, query, description)

        # Закриття з'єднання
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Помилка: {e}")


if __name__ == "__main__":
    main()
