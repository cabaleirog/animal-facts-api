"""
This module is meant to represent the Database handle to PostgreSQL
"""

from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Iterator

import psycopg2

from src.config.collector import Collector


@dataclass
class DatabaseHandle:
    """
    This is the Postgres database handle
    Used to connect to the database where all Animal facts are located.
    """

    _VALID_KEYS = {
        HOST_KEY := "host",
        DATABASE_KEY := "database",
        USER_KEY := "user",
        PASSWORD_KEY := "password",
    }
    host: str
    database: str
    user: str
    password: str

    @classmethod
    def from_collector(cls, config_obj: dict[str, Any]) -> "DatabaseHandle":
        """
        Converts the database config into a DatabaseHandle and returns the class.
        """
        return cls(
            host=config_obj[cls.HOST_KEY],
            database=config_obj[cls.DATABASE_KEY],
            user=config_obj[cls.USER_KEY],
            password=config_obj[cls.PASSWORD_KEY],
        )

    @staticmethod
    def connect(host: str, database: str, user: str, password: str):
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
