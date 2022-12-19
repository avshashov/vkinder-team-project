# import psycopg2
# from db_auth import USER, PASSWORD
#
#
# def add_new_user(connect, user_id, name, surname, sex, age, city, url, photos):
#     '''Добавить/обновить пользователя в БД.'''
#     with connect.cursor() as cur:
#         cur.execute("""
#                     SELECT user_id
#                     FROM users
#                     WHERE user_id = %s;
#                         """, (user_id,)
#                     )
#         if cur.fetchone():
#             cur.execute("""
#                             UPDATE users
#                             SET name = %s, surname = %s, sex = %s, age = %s, city = %s, url = %s
#                             WHERE user_id = %s;
#                                     """, (name, surname, sex, age, city, url, user_id)
#                         )
#
#             cur.execute("""
#                             UPDATE user_photos
#                             SET photo_ids = %s
#                             WHERE user_id = %s;
#                                     """, (photos, user_id)
#                         )
#
#         else:
#             cur.execute("""
#                         INSERT INTO users
#                         VALUES (%s, %s, %s, %s, %s, %s, %s);
#                         """, (user_id, name, surname, sex, age, city, url)
#                         )
#
#             cur.execute("""
#                             INSERT INTO user_photos(user_id, photo_ids)
#                             VALUES (%s, %s);
#                                     """, (user_id, photos)
#                         )
#
#
# def add_search_params(connect, user_id, from_age, to_age, sex, city):
#     """Добавить/обновить критерии поиска пары."""
#     with connect.cursor() as cur:
#         cur.execute("""
#                     SELECT user_id
#                     FROM search_params
#                     WHERE user_id = %s;
#                         """, (user_id,)
#                     )
#         if cur.fetchone():
#             cur.execute("""
#                             UPDATE search_params
#                             SET from_age = %s, to_age = %s, sex = %s, city = %s
#                             WHERE user_id = %s;
#                                     """, (from_age, to_age, sex, city, user_id)
#                         )
#         else:
#             cur.execute("""
#                             INSERT INTO search_params
#                             VALUES (%s, %s, %s, %s, %s);
#                             """, (user_id, from_age, to_age, sex, city)
#                         )
#
#
# def add_to_favorites(connect, finder_id, partner_id):
#     """Добавить пользователя в избранное."""
#     with connect.cursor() as cur:
#         cur.execute("""
#                         INSERT INTO favorites_users(finder_id, partner_id)
#                         VALUES (%s, %s);
#                         """, (finder_id, partner_id)
#                     )
#
#
# def del_from_favorites(connect, finder_id, partner_id):
#     """Удалить пользователя из избранного."""
#     with connect.cursor() as cur:
#         cur.execute("""
#                         DELETE FROM favorites_users
#                         WHERE finder_id = %s AND partner_id = %s;
#                         """, (finder_id, partner_id)
#                     )
#
#
# def show_favorites_users(connect, finder_id):
#     """Показать избранное."""
#     with connect.cursor() as cur:
#         cur.execute("""
#                         SELECT name, surname, url
#                         FROM users
#                         WHERE user_id IN (
#                                           SELECT partner_id
#                                           FROM favorites_users
#                                           WHERE finder_id = %s
#                         );
#                         """, (finder_id,)
#                     )
#         res = cur.fetchall()
#     return res
#
#
# def find_a_couple(connect, user_id):
#     '''Найти пару'''
#     with connect.cursor() as cur:
#         cur.execute("""
#                         SELECT from_age, to_age, sex, city
#                         FROM search_params
#                         WHERE user_id = %s;
#                     """, (user_id,)
#                     )
#         search_params = cur.fetchone()
#
#         cur.execute("""
#                         SELECT name, surname, age, url, photo_ids
#                         FROM users
#                             JOIN user_photos USING(user_id)
#                         WHERE user_id != %s
#                             AND (age BETWEEN %s AND %s)
#                               AND sex = %s
#                               AND city = %s;
#                     """, (user_id, *search_params)
#                     )
#         res = cur.fetchall()
#     return res
#
#
# conn = psycopg2.connect(database='vkinder', user=USER, password=PASSWORD)
#
# with conn:
#     pass