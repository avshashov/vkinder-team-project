CREATE TABLE users
(
    user_id INT PRIMARY KEY,
    name    VARCHAR(20) NOT NULL,
    surname VARCHAR(20) NOT NULL,
    sex     CHAR(7)     NOT NULL,
    age     INT,
    city    VARCHAR(20) NOT NULL,
    url     TEXT NOT NULL
);

CREATE TABLE user_photos
(
    id       SERIAL PRIMARY KEY,
    user_id  INT REFERENCES users (user_id),
    photo_ids TEXT
);

CREATE TABLE search_params
(
    user_id  INT PRIMARY KEY,
    from_age INT         NOT NULL,
    to_age   INT         NOT NULL,
    sex      VARCHAR(7)  NOT NULL,
    city     VARCHAR(20) NOT NULL
);

CREATE TABLE favorites_users
(
    id         SERIAL PRIMARY KEY,
    finder_id  INT REFERENCES users (user_id),
    partner_id INT REFERENCES users (user_id)
);