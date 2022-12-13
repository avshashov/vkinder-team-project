import psycopg2
from db_auth import USER, PASSWORD


class VkinderDB:
    conn = psycopg2.connect(database='vkinder', user=USER, password=PASSWORD)

    def add_new_user(self, user_data):
        '''Добавить/обновить пользователя в БД.'''
        with VkinderDB.conn:
            with VkinderDB.conn.cursor() as cur:
                cur.execute("""
                            SELECT user_id
                            FROM users
                            WHERE user_id = %s;
                                """, (user_data['user_id'],)
                            )
                if cur.fetchone():
                    cur.execute("""
                                    UPDATE users
                                    SET name = %s, surname = %s, sex = %s, 
                                        age = %s, city = %s, url = %s
                                    WHERE user_id = %s;
                                            """, (user_data['name'], user_data['surname'], user_data['sex'],
                                                  user_data['age'], user_data['city'], user_data['url'],
                                                  user_data['user_id'])
                                )

                    cur.execute("""
                                    UPDATE user_photos
                                    SET photo_ids = %s
                                    WHERE user_id = %s;
                                            """, (user_data['photos'], user_data['user_id'])
                                )

                else:
                    cur.execute("""
                                INSERT INTO users
                                VALUES (%s, %s, %s, %s, %s, %s, %s);
                                """, (user_data['user_id'], user_data['name'], user_data['surname'],
                                      user_data['sex'], user_data['age'], user_data['city'],
                                      user_data['url'])
                                )

                    cur.execute("""
                                    INSERT INTO user_photos(user_id, photo_ids) 
                                    VALUES (%s, %s);
                                            """, (user_data['user_id'], user_data['photos'])
                                )

    def add_search_params(self, params):
        '''Добавить/обновить критерии поиска пары.'''
        with VkinderDB.conn:
            with VkinderDB.conn.cursor() as cur:
                cur.execute("""
                                SELECT user_id
                                FROM search_params
                                WHERE user_id = %s;
                                    """, (params['user_id'],)
                            )
                if cur.fetchone():
                    cur.execute("""
                                        UPDATE search_params
                                        SET from_age = %s, to_age = %s, sex = %s, city = %s
                                        WHERE user_id = %s;
                                                """, (params['from_age'], params['to_age'],
                                                      params['sex'], params['city'],
                                                      params['user_id'])
                                )
                else:
                    cur.execute("""
                                        INSERT INTO search_params
                                        VALUES (%s, %s, %s, %s, %s);
                                        """, (params['user_id'], params['from_age'],
                                              params['to_age'], params['sex'],
                                              params['city'])
                                )

    def add_to_favorites(self, finder_id, partner_id):
        '''Добавить пользователя в избранное.'''
        with VkinderDB.conn:
            with VkinderDB.conn.cursor() as cur:
                cur.execute("""
                                INSERT INTO favorites_users(finder_id, partner_id)
                                VALUES (%s, %s);
                                """, (finder_id, partner_id)
                            )

    def del_from_favorites(self, finder_id, partner_id):
        '''Удалить пользователя из избранного.'''
        with VkinderDB.conn:
            with VkinderDB.conn.cursor() as cur:
                cur.execute("""
                                DELETE FROM favorites_users
                                WHERE finder_id = %s AND partner_id = %s;
                                """, (finder_id, partner_id)
                            )

    def show_favorites_users(self, finder_id):
        '''Показать избранное.'''
        with VkinderDB.conn:
            with VkinderDB.conn.cursor() as cur:
                cur.execute("""
                                SELECT name, surname, url
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

    def find_a_couple(connect, user_id):
        '''Найти пару'''
        with VkinderDB.conn:
            with VkinderDB.conn.cursor() as cur:
                cur.execute("""
                                SELECT from_age, to_age, sex, city
                                FROM search_params
                                WHERE user_id = %s;
                            """, (user_id,)
                            )
                search_params = cur.fetchone()

                cur.execute("""
                                SELECT name, surname, age, url, photo_ids
                                FROM users 
                                    JOIN user_photos USING(user_id)
                                WHERE user_id != %s 
                                    AND (age BETWEEN %s AND %s)
                                      AND sex = %s 
                                      AND city = %s;
                            """, (user_id, *search_params)
                            )
                res = cur.fetchall()
        return res


# add_new_user(conn, 11111, 'Иван', 'Иванов', 'мужской', 26, 'Москва', 'ссылка', 'ссылка1,ссылка2,ссылка3')

data = {'user_id': 77772, 'name': 'Лупа', 'surname': 'Пупа',
        'sex': 'мужской', 'age': 59, 'city': 'Tomsk', 'url': 'ссылка 51',
        'photos': 'photo1,photo2,photo3'}

params = {'user_id': 77772, 'from_age': 28, 'to_age': '35',
          'sex': 'женский', 'city': 'Tomsk'}
db = VkinderDB()
# db.add_new_user(data)
# db.add_search_params(params)
print(db.find_a_couple(11111))
print(db.find_a_couple(22222))