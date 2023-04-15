"""
Holds basic Animal commands.
"""
import dataclasses
import re
from typing import Any


from src.api.models.http.body import RequestBody

# from src.config.collector import Collector
from src.database.postgres import DatabaseHandle, temporary_connection


@dataclasses.dataclass(frozen=True)
class Operator:
    """
    Abstract Operator class to perform DB actions.
    Allows the api to make CRUD operations to the postgresDB.
    """

    __AVAILABLE_TABLES = {
        BIRDS_TABLE := "birds",
        CATS_TABLE := "cats",
        DOGS_TABLE := "dogs",
        FOXES_TABLE := "foxes",
        KANGAROOS_TABLE := "kangaroos",
    }

    @staticmethod
    def get_count(table: str) -> tuple | None:
        """
        Returns the count of a table.
        """
        assert table in Operator.__AVAILABLE_TABLES
        with temporary_connection(
            database_handle=DatabaseHandle.from_collector()
        ) as cursor:
            sql = f"SELECT COUNT(*) FROM {table}"
            cursor.execute(sql)
            row = cursor.fetchone()
        return row

    @staticmethod
    def get_all(table: str) -> list[tuple]:
        """
        Returns a list of all entries in a specific table.
        """
        assert table in Operator.__AVAILABLE_TABLES
        with temporary_connection(
            database_handle=DatabaseHandle.from_collector()
        ) as cursor:
            sql = f"SELECT * FROM {table}"
            cursor.execute(sql)
            rows = cursor.fetchall()
        return rows

    @staticmethod
    def get_one(table: str, _id: int) -> tuple[int, str] | None:
        """
        Return the row that belongs to the correct ID key.
        """
        assert table in Operator.__AVAILABLE_TABLES
        with temporary_connection(
            database_handle=DatabaseHandle.from_collector()
        ) as cursor:
            sql = f"SELECT * FROM {table} WHERE id={_id};"
            cursor.execute(sql)
            row = cursor.fetchone()
        return row

    @staticmethod
    def create(table: str, request_body: RequestBody) -> tuple | None:
        """
        Create a new resource to the database.
        """
        assert table in Operator.__AVAILABLE_TABLES

        # Sanity Check...
        if re.match("^[0-9]+$", request_body.fact):
            # Checks if the fact is all numerical or if it's actually text.
            # Does almost the same check as "".isdigit()
            return None

        with temporary_connection(
            database_handle=DatabaseHandle.from_collector()
        ) as cursor:
            query = (
                "INSERT INTO {table} (fact) VALUES (%s) RETURNING id, fact;".format_map(
                    {"table": table}
                )
            )
            cursor.execute(query, (request_body.fact,))
            row = cursor.fetchone()
        return row

    # @staticmethod
    # def add(file_name: str, request_body: RequestBody):
    #     """
    #     Append a fact to the animal list
    #     """
    #     all_facts = Animal.all_facts(fact_file_name=file_name)
    #     max_number = max(all_facts, key=lambda x: x["id"])
    #     dict_to_add = {
    #         "id": int(max_number["id"]) + 1,
    #         "fact": request_body.fact,
    #     }
    #     all_facts.append(dict_to_add)
    #     with open(
    #         f"{os.path.dirname(__file__)}/{file_name}.json", "w", encoding="UTF-8"
    #     ) as fact_file:
    #         json.dump(all_facts, fact_file, indent=4)
    #     return dict_to_add

    # @staticmethod
    # def delete(file_name: str, animal_id: int):
    #     """
    #     Delete a fact from an animal
    #     """

    #     all_facts = Animal.all_facts(fact_file_name=file_name)

    #     for fact in all_facts:
    #         if fact.get("id") == animal_id:
    #             all_facts.remove(fact)
    #             with open(
    #                 f"{os.path.dirname(__file__)}/{file_name}.json",
    #                 "w",
    #                 encoding="UTF-8",
    #             ) as fact_file:
    #                 json.dump(all_facts, fact_file, indent=4)
    #             return "204"
    #     return "404"

    # @staticmethod
    # def update(file_name: str, animal_id: int, request_body: RequestBody):
    #     """
    #     Update a fact
    #     """
    #     all_facts = Animal.all_facts(fact_file_name=file_name)

    #     for index, fact in enumerate(all_facts):
    #         if fact.get("id") == animal_id:
    #             the_fact_to_update = all_facts.pop(index)
    #             the_fact_to_update["fact"] = request_body.fact
    #             all_facts.insert(index, the_fact_to_update)
    #             with open(
    #                 f"{os.path.dirname(__file__)}/{file_name}.json",
    #                 "w",
    #                 encoding="UTF-8",
    #             ) as fact_file:
    #                 json.dump(all_facts, fact_file, indent=4)
    #             return "204"
    #     return "404"


# Animal.convert_all(file="kangaroos")
