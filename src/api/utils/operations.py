"""
Holds basic Animal commands.
"""
import dataclasses
import re
from typing import Any


from src.api.models.http.body import RequestBody

# from src.config.collector import Collector
from src.database.postgres import DatabaseHandle, temporary_connection
from src.api.models.animal import FactModel


@dataclasses.dataclass(frozen=True)
class Operator:
    """
    Abstract Operator class to perform DB actions.
    Allows the api to make CRUD operations to the postgresDB.
    """

    __AVAILABLE_TABLES = {
        ANIMAL_TABLE := "animals"
        # BIRDS_TABLE := "birds",
        # CATS_TABLE := "cats",
        # DOGS_TABLE := "dogs",
        # FOXES_TABLE := "foxes",
        # KANGAROOS_TABLE := "kangaroos",
    }
    __VALID_PROPERTIES = {
        ID := "id",
        FACT := "fact",
        ANIMAL := "animal",
    }

    @classmethod
    def count_for_animal(cls, animal: str) -> int | None:
        """
        Returns the count of a table.
        """
        with temporary_connection(
            database_handle=DatabaseHandle.from_collector()
        ) as cursor:
            sql = f"SELECT COUNT(*) FROM {cls.ANIMAL_TABLE} WHERE animal='{animal}'"
            cursor.execute(sql)
            row = cursor.fetchone()
        return row[0]

    @classmethod
    def count_all(cls) -> int | None:
        """
        Returns the count of a table.
        """
        with temporary_connection(
            database_handle=DatabaseHandle.from_collector()
        ) as cursor:
            sql = f"SELECT COUNT(*) FROM {cls.ANIMAL_TABLE}"
            cursor.execute(sql)
            row = cursor.fetchone()
        return row[0]

    @classmethod
    def get_all_for_animal(cls, animal: str) -> list[dict[str, Any]]:
        """
        Returns a list of all entries in a specific table.
        """
        with temporary_connection(
            database_handle=DatabaseHandle.from_collector()
        ) as cursor:
            sql = f"SELECT id,fact,animal FROM {cls.ANIMAL_TABLE} WHERE animal={animal}"
            cursor.execute(sql)
            rows = cursor.fetchall()
        if len(rows) == 0:
            return [{"ERROR": "Current query returned an empty row."}]
        return [{cls.ID: row[0], cls.FACT: row[1], cls.ANIMAL: row[2]} for row in rows]

    @classmethod
    def get_one(cls, _id: int) -> dict[str, Any] | None:
        """
        Return the row that belongs to the correct ID key.
        """
        with temporary_connection(
            database_handle=DatabaseHandle.from_collector()
        ) as cursor:
            sql = f"SELECT id,fact,animal FROM {cls.ANIMAL_TABLE} WHERE id={_id};"
            cursor.execute(sql)
            row = cursor.fetchone()
        if len(row) == 0:
            return {"ERROR": "Current query returned an empty row."}
        return {cls.ID: row[0], cls.FACT: row[1], cls.ANIMAL: row[2]}

    @classmethod
    def get_random_by_animal(cls, animal: str) -> dict[str, Any] | None:
        """
        Return the row that belongs to the correct ID key.
        """
        with temporary_connection(
            database_handle=DatabaseHandle.from_collector()
        ) as cursor:
            sql = f"SELECT id,fact,animal FROM {cls.ANIMAL_TABLE} WHERE animal='{animal}' ORDER BY random() LIMIT 1;"
            cursor.execute(sql)
            row = cursor.fetchone()
        if len(row) == 0:
            return {"ERROR": "Current query returned an empty row."}
        return {cls.ID: row[0], cls.FACT: row[1], cls.ANIMAL: row[2]}

    @classmethod
    def get_random(cls) -> dict[str, Any]:
        """
        Return the row that belongs to the correct ID key.
        """
        with temporary_connection(
            database_handle=DatabaseHandle.from_collector()
        ) as cursor:
            sql = f"SELECT id,fact,animal FROM {cls.ANIMAL_TABLE} ORDER BY random() LIMIT 1;"
            cursor.execute(sql)
            row = cursor.fetchone()
        if len(row) == 0:
            return {"ERROR": "Current query returned an empty row."}

        return {cls.ID: row[0], cls.FACT: row[1], cls.ANIMAL: row[2]}

    @classmethod
    def create(cls, animal: str, request_body: RequestBody) -> dict[str, Any] | None:
        """
        Create a new resource to the database.
        """

        # Sanity Check...
        if re.match("^[0-9]+$", request_body.fact):
            # Checks if the fact is all numerical or if it's actually text.
            # Does almost the same check as "".isdigit()
            return None

        with temporary_connection(
            database_handle=DatabaseHandle.from_collector()
        ) as cursor:
            query = "INSERT INTO {table} (fact, animal) VALUES (%s, %s) RETURNING id, fact, animal;".format_map(
                {"table": cls.ANIMAL_TABLE}
            )
            cursor.execute(query, (request_body.fact, animal))
            row = cursor.fetchone()
        return {cls.ID: row[0], cls.FACT: row[1], cls.ANIMAL: row[2]}

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
