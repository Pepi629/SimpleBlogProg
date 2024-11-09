import psycopg2

def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="corn_hub",
            user="postgres",
            password="111111",
            host="192.168.56.101",  # Укажи IP-адрес сервера с базой данных
            port="5432"  # По умолчанию используется порт 5432, но можно указать другой, если он отличается
        )
        print("Подключение к базе данных успешно")
        return conn
    except Exception as e:
        print(f"Ошибка подключения к БД: {e}")
        return None