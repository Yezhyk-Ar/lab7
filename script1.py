import psycopg2

# Параметри підключення
db_config = {
    "dbname": "cinema_db",
    "user": "admin",
    "password": "admin123",
    "host": "localhost",
    "port": 5432,
}

# Підключення до бази даних
conn = psycopg2.connect(**db_config)
cursor = conn.cursor()

# Створення таблиць
queries = [
    """
    CREATE TABLE IF NOT EXISTS Films (
        film_id SERIAL PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        genre VARCHAR(50) NOT NULL CHECK (genre IN ('мелодрама', 'комедія', 'бойовик')),
        duration INTEGER NOT NULL CHECK (duration > 0),
        rating NUMERIC(3, 1) CHECK (rating BETWEEN 0 AND 10)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Cinemas (
        cinema_id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        ticket_price NUMERIC(5, 2) NOT NULL CHECK (ticket_price >= 0),
        seat_count INTEGER NOT NULL CHECK (seat_count > 0),
        address VARCHAR(200),
        phone VARCHAR(15) CHECK (phone ~ '^\+\d{1,3}-\d{9,12}$')
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Screenings (
        screening_id SERIAL PRIMARY KEY,
        film_id INTEGER REFERENCES Films(film_id) ON DELETE CASCADE,
        cinema_id INTEGER REFERENCES Cinemas(cinema_id) ON DELETE CASCADE,
        start_date DATE NOT NULL,
        duration_days INTEGER NOT NULL CHECK (duration_days > 0)
    );
    """,
]

# Виконання запитів
for query in queries:
    cursor.execute(query)

conn.commit()
cursor.close()
conn.close()

print("Таблиці створено успішно!")
