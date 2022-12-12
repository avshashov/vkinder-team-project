import psycopg2
from db_auth import USER, PASSWORD


def add_new_user(connect, user_id, name, surname, sex, age, city):
    """Добавляем нового пользователя в БД.
     Если пользователь есть в базе, то обновляем по нему информацию"""
    with connect.cursor() as cur:
        cur.execute("""
                    SELECT user_id
                    FROM users
                    WHERE user_id = %s;
                        """, (user_id,)
                    )
        if cur.fetchone():
            cur.execute("""
                            UPDATE users
                            SET name = %s, surname = %s, sex = %s, age = %s, city = %s
                            WHERE user_id = %s;
                                    """, (name, surname, sex, age, city, user_id)
                        )
        else:
            cur.execute("""
                        INSERT INTO users
                        VALUES (%s, %s, %s, %s, %s, %s);
                        """, (user_id, name, surname, sex, age, city)
                        )


conn = psycopg2.connect(database='vkinder', user=USER, password=PASSWORD)

with conn:
    pass