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


def add_search_params(connect, user_id, from_age, to_age, sex, city):
    """Добавляем/обновляем критерии поиска пары"""
    with connect.cursor as cur:
        cur.execute("""
                    SELECT user_id
                    FROM search_params
                    WHERE user_id = %s;
                        """, (user_id,)
                    )
        if cur.fetchone():
            cur.execute("""
                            UPDATE search_params
                            SET from_age = %s, to_age = %s, sex = %s, city = %s
                            WHERE user_id = %s;
                                    """, (from_age, to_age, sex, city, user_id)
                        )
        else:
            cur.execute("""
                            INSERT INTO search_params
                            VALUES (%s, %s, %s, %s, %s);
                            """, (user_id, from_age, to_age, sex, city)
                        )


def add_to_favorites(connect, finder_id, partner_id):
    """Добавляем пользователя в избранное"""
    with connect.cursor as cur:
        cur.execute("""
                        INSERT INTO favorites_users(finder_id, partner_id)
                        VALUES (%s, %s);
                        """, (finder_id, partner_id)
                    )


def del_from_favorites(connect, finder_id, partner_id):
    """Удаляем пользователя из избранного"""
    with connect.cursor as cur:
        cur.execute("""
                        DELETE FROM favorites_users
                        WHERE finder_id = %s AND partner_id = %s;
                        """, (finder_id, partner_id)
                    )


def show_favorites_users(connect, finder_id):
    """Показать избранное"""
    with connect.cursor as cur:
        cur.execute("""
                        SELECT name, surname
                        FROM users
                        WHERE user_id IN (
                                          SELECT partner_id
                                          FROM favorites_users
                                          WHERE finder_id = %s
                        );
                        """, (finder_id,)
                    )
        res = cur.fetchall()
    return res


conn = psycopg2.connect(database='vkinder', user=USER, password=PASSWORD)

with conn:
    pass
