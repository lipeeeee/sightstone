# Base config class 

from __future__ import annotations
from typing import Callable
import os
from pathlib import Path

class Config:
    """Base class 

    Attributes
        - CONFIG_FOLDER(str): the path to the home directory config folder
        - name(str): the specific name of the config
        - config_file(str): the path to the specific config json

    Has features such as:
        - `json_dict()` to create a json dict of the current config
        - `load()` to load the specific config from disk
        - `save()` to save the contents of the config into disk
        - `defaults()` load defaults for specific config

    And Utility functions such as:
        - `config_folder_exists()`
        - `create_config_folder()`
        - `config_file_exists()`
        - `fix_files()`
        - `execute_and_save()`
    """

    CONFIG_FOLDER: str = str(Path.home()) + "/sightstone/"

    name: str
    config_file: str

    def __init__(self, name: str) -> None:
        assert name

        self.name = name
        self.config_file = self.CONFIG_FOLDER + name + ".json"

        self.fix_files()
        self.load()

    @property
    def json_dict(self) -> str:
        """Generates json dict of current configuration"""
        raise NotImplementedError("Config.json_dict not implemented")

    def load(self) -> bool:
        """Loads config from disk"""
        raise NotImplementedError("Config.load not implemented")

    def defaults(self) -> None:
        """Sets atributes to their default values"""
        raise NotImplementedError("Config.defaults not implemented")

    def save(self) -> None:
        """Saves config to disk"""
        with open(self.config_file, "w") as file:
            file.write(self.json_dict)

    def fix_files(self) -> None:
        if not self.config_folder_exists():
            self.create_config_folder()
            self.create_config_file()
        elif not self.config_file_exists():
            self.create_config_file()

    def config_folder_exists(self) -> bool:
        return os.path.exists(self.CONFIG_FOLDER)

    def config_file_exists(self) -> bool:
        return os.path.exists(self.config_file)

    def create_config_folder(self) -> None:
        assert self.CONFIG_FOLDER and not self.config_folder_exists()
        os.mkdir(self.CONFIG_FOLDER)

    def create_config_file(self) -> None:
        assert (
            self.config_file and
            not self.config_file_exists() and
            self.config_folder_exists()
        )
        self.defaults()
        self.save()

    def execute_and_save(self, fn: Callable) -> object:
        fn_res = fn()
        self.save()
        return fn_res
