import psycopg2


class VkinderDB:

    def __init__(self, user, password):
        self.connect = psycopg2.connect(database='vkinder', user=user, password=password)

    def add_new_user(self, user_data, photos):
        '''Добавить/обновить пользователя в БД.'''
        with self.connect as conn:
            with conn.cursor() as cur:
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
                                            """, (photos, user_data['user_id'])
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
                                            """, (user_data['user_id'], photos)
                                )

    def search_params_exists(self, user_id):
        '''Проверить, заданы ли критерии поиска для пользователя.'''
        with self.connect as conn:
            with conn.cursor() as cur:
                cur.execute("""
                                SELECT user_id
                                FROM search_params
                                WHERE user_id = %s;
                            """, (user_id,)
                            )
                res = cur.fetchone()
        return bool(res)

    def add_search_params(self, params):
        '''Добавить/обновить критерии поиска пары.'''
        with self.connect as conn:
            with conn.cursor() as cur:
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

    def get_search_params(self, user_id):
        '''Получить критерии поиска пары'''
        with self.connect as conn:
            with conn.cursor() as cur:
                cur.execute("""
                                SELECT from_age, to_age, sex, city
                                FROM search_params
                                WHERE user_id = %s;
                                """, (user_id,)
                            )
                res = cur.fetchone()
        return res

    def add_to_favorites(self, finder_id, partner_id):
        '''Добавить пользователя в избранное.'''
        with self.connect as conn:
            with conn.cursor() as cur:
                cur.execute("""
                                SELECT partner_id
                                FROM favorites_users
                                WHERE finder_id = %s AND partner_id = %s;
                                """, (finder_id, partner_id)
                            )
                res = cur.fetchone()

                if not res:
                    cur.execute("""
                                    INSERT INTO favorites_users(finder_id, partner_id)
                                    VALUES (%s, %s);
                                    """, (finder_id, partner_id)
                                )

    def del_from_favorites(self, finder_id, partner_id):
        '''Удалить пользователя из избранного.'''
        with self.connect as conn:
            with conn.cursor() as cur:
                cur.execute("""
                                DELETE FROM favorites_users
                                WHERE finder_id = %s AND partner_id = %s;
                                """, (finder_id, partner_id)
                            )

    def show_favorites_users(self, finder_id):
        '''Показать избранное.'''
        with self.connect as conn:
            with conn.cursor() as cur:
                cur.execute("""
                                SELECT user_id, name, surname, url
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

    def find_a_couple(self, user_id):
        '''Найти пару'''
        with self.connect as conn:
            with conn.cursor() as cur:
                cur.execute("""
                                SELECT from_age, to_age, sex, city
                                FROM search_params
                                WHERE user_id = %s;
                            """, (user_id,)
                            )
                search_params = cur.fetchone()

                cur.execute("""
                                SELECT user_id, name, surname, age, url, photo_ids
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
