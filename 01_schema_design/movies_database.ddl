-- Создание схемы content
CREATE SCHEMA IF NOT EXISTS content;

-- Создание таблицы film_work в схеме content
CREATE TABLE IF NOT EXISTS content.film_work (id            uuid PRIMARY KEY,
                                              title         text NOT NULL,
                                              description   text,
                                              creation_date date,
                                              rating        float,
                                              type          text NOT NULL,
                                              created       timestamp with time zone,
                                              modified      timestamp with time zone);

COMMENT ON TABLE film_work IS 'Основная информация о кинопроизведении';

-- Создание таблицы person в схеме content
CREATE TABLE IF NOT EXISTS content.person (id        uuid PRIMARY KEY,
                                           full_name text NOT NULL,
                                           created   timestamp with time zone,
                                           modified  timestamp with time zone);

COMMENT ON TABLE person IS 'Участник произведения';

-- Создание таблицы person_film_work в схеме content
CREATE TABLE IF NOT EXISTS content.person_film_work (id           uuid PRIMARY KEY,
                                                     film_work_id uuid NOT NULL,
                                                     person_id    uuid NOT NULL,
                                                     role         text NOT NULL,
                                                     created      timestamp with time zone);

COMMENT ON TABLE person_film_work IS 'Связи кинопроизведений и участников';

-- Создание таблицы genre в схеме content
CREATE TABLE IF NOT EXISTS content.genre (id          uuid PRIMARY KEY,
                                          name        text NOT NULL,
                                          description text,
                                          created     timestamp with time zone,
                                          modified    timestamp with time zone);
COMMENT ON TABLE genre IS 'Жанры кинопроизведений';

-- Создание таблицы genre_film_work в схеме content
CREATE TABLE IF NOT EXISTS  content.genre_film_work (id           uuid PRIMARY KEY,
                                                     genre_id     uuid NOT NULL,
                                                     film_work_id uuid NOT NULL,
                                                     created      timestamp with time zone);

COMMENT ON TABLE genre_film_work IS 'Связи жанров и кинопроизведений';

-- Создание индексов для таблицы film_work
CREATE INDEX IF NOT EXISTS film_work_creation_date_rating_idx ON content.film_work(creation_date, rating);
CREATE INDEX IF NOT EXISTS film_work_title_idx ON content.film_work(title);

-- Создание индексов для таблицы person
CREATE INDEX IF NOT EXISTS person_full_name_idx ON content.person(full_name);

-- Создание индексов для таблицы person_film_work
CREATE UNIQUE INDEX IF NOT EXISTS film_work_person_idx ON content.person_film_work (film_work_id, person_id, role);

-- Создание индексов для таблицы genre_film_work
CREATE UNIQUE INDEX IF NOT EXISTS genre_film_work_idx ON content.genre_film_work(film_work_id,genre_id);