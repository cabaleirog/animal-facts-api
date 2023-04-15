# """
# This module is meant to collect config files and return them as dictionaries.
# """
# import json
# import os
# from dataclasses import dataclass
# from typing import Any
#
#
# # DEPRECATED... NO LONGER NEEDED BECAUSE WE USE
# # ENVIRONMENTAL VARIABLES INSTEAD... DOCKER <3
#
#
# @dataclass
# class Collector:
#     """
#     Collects config files and returns the json files as dictionaries.
#     """
#
#     BASE_CONFIG_LOCATION = "src/config"
#     _CONFIG_FILES = {
#         DATABASE_CONFIG := "database-config.json",
#     }
#
#     def load_config(self, config_file: str) -> dict[str, Any]:
#         """
#         Loads a config based on the given config file.
#         """
#         assert config_file in Collector._CONFIG_FILES
#
#         config: dict[str, Any] = {}
#
#         # Find the correct config file
#         for file in os.listdir(self.BASE_CONFIG_LOCATION):
#             if file == config_file:
#                 path_to_file = os.path.join(self.BASE_CONFIG_LOCATION, config_file)
#                 with open(path_to_file, "r", encoding="utf-8") as f_conf:
#                     config.update(json.load(fp=f_conf))
#         return config
#
#     @property
#     def database_config(self) -> dict[str, Any]:
#         """
#         Returns the Database Configuration
#         """
#         return self.load_config(config_file=Collector.DATABASE_CONFIG)
#
