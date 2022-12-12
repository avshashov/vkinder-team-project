CREATE TABLE users
(
    user_id int PRIMARY KEY,
    name    varchar(20) NOT NULL,
    surname varchar(20) NOT NULL,
    sex     varchar(7)  NOT NULL,
    age     int,
    city    varchar(20) NOT NULL
);

CREATE TABLE search_params
(
    user_id  int PRIMARY KEY,
    from_age int         NOT NULL,
    to_age   int         NOT NULL,
    sex      varchar(7)  NOT NULL,
    city     varchar(20) NOT NULL
);

CREATE TABLE favorites_users
(
    id         serial PRIMARY KEY,
    finder_id  int REFERENCES users (user_id),
    partner_id int REFERENCES users (user_id)
);