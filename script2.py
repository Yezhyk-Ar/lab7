import psycopg2
from datetime import date

from script1 import db_config

data_queries = [
    """
    INSERT INTO Films (title, genre, duration, rating)
    VALUES
        ('Фільм 1', 'комедія', 90, 8.5),
        ('Фільм 2', 'мелодрама', 120, 7.0),
        ('Фільм 3', 'бойовик', 105, 9.0);
    """,
    """
    INSERT INTO Cinemas (name, ticket_price, seat_count, address, phone)
    VALUES
        ('Кінотеатр 1', 150.00, 100, 'Вул. Перемоги, 10', '+380-123456789'),
        ('Кінотеатр 2', 200.00, 80, 'Вул. Шевченка, 15', '+380-987654321'),
        ('Кінотеатр 3', 180.00, 120, 'Проспект Миру, 5', '+380-567891234');
    """,
    """
    INSERT INTO Screenings (film_id, cinema_id, start_date, duration_days)
    VALUES
        (1, 1, '2024-11-20', 7),
        (2, 2, '2024-11-22', 5),
        (3, 3, '2024-11-23', 10);
    """
]

conn = psycopg2.connect(**db_config)
cursor = conn.cursor()

for query in data_queries:
    cursor.execute(query)

conn.commit()
cursor.close()
conn.close()

print("Дані додано успішно!")
