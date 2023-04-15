"""
This module is meant to represent the Database handle to PostgreSQL
"""

from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Iterator

import psycopg2
from psycopg2._psycopg import connection  # pylint:disable=no-name-in-module

from dotenv import dotenv_values

POSTGRESQL_HOSTNAME = "db"
POSTGRESQL_PORT = "5432"
config: dict[str, Any] = dotenv_values(".env")


@dataclass
class DatabaseHandle:
    """
    This is the Postgres database handle
    Used to connect to the database where all Animal facts are located.
    """

    _VALID_KEYS = {
        DATABASE_KEY := "ANIMAL_DATABASE",
        USER_KEY := "ANIMAL_USER",
        PASSWORD_KEY := "ANIMAL_PASSWORD",
    }
    host: str
    database: str
    user: str
    password: str

    @classmethod
    def from_collector(
        cls,
    ) -> "DatabaseHandle":
        """
        Converts the database config into a DatabaseHandle and returns the class.
        """
        return cls(
            host=POSTGRESQL_HOSTNAME,
            database=config[cls.DATABASE_KEY],
            user=config[cls.USER_KEY],
            password=config[cls.PASSWORD_KEY],
        )

    @staticmethod
    def connect(host: str, database: str, user: str, password: str) -> connection:
        """
        Create and return a connection to the database
        """
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
        )
        return conn


@contextmanager
def temporary_connection(
    database_handle: DatabaseHandle,
) -> Iterator:
    """
    Connects to the database.
    Returns a cursor.
    Commits the action (If successful)
    Closes the connection.

    Use this instead of DatabaseHandle.connect()
    """
    conn = database_handle.connect(
        host=database_handle.host,
        database=database_handle.database,
        user=database_handle.user,
        password=database_handle.password,
    )

    with conn.cursor() as cursor:
        try:
            yield cursor
            conn.commit()
        finally:
            cursor.close()
            conn.close()
