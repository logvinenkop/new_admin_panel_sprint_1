from asyncio import exceptions
import sqlite3
from black import err
import pytest
import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extras import DictCursor

load_dotenv()


@pytest.fixture
def sqlite_connection():
    try:
        conn = sqlite3.connect(os.environ.get("SQLITE_DB_PATH"))
        cursor = conn.cursor()
        print("SQLIte connection fixed")
        yield cursor
        print("SQLite connection closed")
    except Exception as e:
        print("Возникла ошибка: {er}".format(er=e))
    finally:
        conn.close()
        print("SQLite connection closed")


@pytest.fixture
def pg_connection():
    try:
        dsl = {
            "dbname": os.environ.get("DB_NAME"),
            "user": os.environ.get("DB_USER"),
            "password": os.environ.get("DB_PASSWORD"),
            "host": "127.0.0.1",
            "port": 5432,
        }
        conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)
        cursor = conn.cursor()
        print("Postgres connection fixed")
        yield cursor
    except Exception as e:
        print("Возникла ошибка: {er}".format(er=e))
    finally:
        conn.close()
        print("Postgres connection closed")


@pytest.fixture
def tables_info():
    tables = [
        {
            "name": "genre",
            "fields": ["id", "name", "description"],
        },
        {
            "name": "genre_film_work",
            "fields": ["id", "film_work_id", "genre_id"],
        },
        {
            "name": "person_film_work",
            "fields": ["id", "film_work_id", "person_id", "role"],
        },
        {
            "name": "person",
            "fields": ["id", "full_name"],
        },
        {
            "name": "film_work",
            "fields": [
                "id",
                "title",
                "description",
                "creation_date",
                "file_path",
                "rating",
                "type",
            ],
        },
    ]
    return tables


def test_rowcount(sqlite_connection, pg_connection, tables_info):
    errors = []
    for table in tables_info:
        t_name = table.get("name")
        select_rowcount_sql = "SELECT count(*) as rowcount FROM {tn};".format(tn=t_name)
        sqlite_rowcount = list(
            sqlite_connection.execute(select_rowcount_sql).fetchone()
        )
        pg_connection.execute(select_rowcount_sql)
        pg_rowcount = pg_connection.fetchone()
        if not sqlite_rowcount == pg_rowcount:
            errors.append(
                "Таблица '{tn}' имеет разное количество строк в SQLite и Postgres".format(
                    tn=t_name
                )
            )
    assert not errors, "Возникли ошибки:\n{}".format("\n".join(errors))


def test_rows_consistency(sqlite_connection, pg_connection, tables_info):
    errors = []
    for table in tables_info:
        t_name = table.get("name")
        t_fields = ", ".join(table.get("fields"))
        select_table_fields_sql = "SELECT {tf} FROM {tn};".format(
            tf=t_fields, tn=t_name
        )
        sqlite_table = list(
            sqlite_connection.execute(select_table_fields_sql).fetchall()
        )
        pg_connection.execute(select_table_fields_sql)
        pg_table = pg_connection.fetchall()
        for i in range(len(sqlite_table)):
            if not sqlite_table[i] == tuple(pg_table[i]):
                errors.append(
                    "Разница строк: {sq} и {pg}".format(
                        sq=sqlite_table[i], pg=pg_table[i]
                    )
                )
    assert not errors
