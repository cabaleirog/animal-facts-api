"""
This module is meant to collect config files and return them as dictionaries.
"""
import json
import os
from dataclasses import dataclass
from typing import Any


@dataclass
class Collector:
    """
    Collects config files and returns the json files as dictionaries.
    """

    BASE_CONFIG_LOCATION = "src/config"
    _CONFIG_FILES = {DATABASE_CONFIG := "database-config.json"}

    config_path: str = BASE_CONFIG_LOCATION

    def load_config(self, file_name: str) -> dict[str, Any]:
        """
        Loads a config based on the given config file.
        """
        assert file_name in Collector._CONFIG_FILES

        config: dict[str, Any] = {}
        for config_file in os.listdir(self.config_path):
            if config_file == file_name:
                path_to_file = os.path.join(self.config_path, config_file)
                with open(path_to_file, "r", encoding="utf-8") as f_conf:
                    config.update(json.load(f_conf))
        return config

    @property
    def database_config(self) -> dict[str, Any]:
        """
        Returns the Database Configuration
        """
        return self.load_config(file_name=Collector.DATABASE_CONFIG)
