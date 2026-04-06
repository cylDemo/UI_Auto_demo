import os
import json
import yaml
from pathlib import Path


class ConfigLoader:
    _instance = None
    _config = None
    _users = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.data_dir = Path(__file__).parent
        self._load_config()
        self._load_users()

    def _load_config(self) -> None:
        env = os.getenv("ENV", "staging")
        config_path = self.data_dir / "config.yaml"
        with open(config_path, "r", encoding="utf-8") as f:
            all_configs = yaml.safe_load(f)
            self._config = all_configs.get(env, all_configs.get("staging"))

    def _load_users(self) -> None:
        users_path = self.data_dir / "users.json"
        with open(users_path, "r", encoding="utf-8") as f:
            self._users = json.load(f)

    @property
    def config(self) -> dict:
        return self._config

    @property
    def users(self) -> dict:
        return self._users

    def get_base_url(self) -> str:
        return self._config.get("base_url", "https://staging.example.com")

    def get_api_url(self) -> str:
        return self._config.get("api_url", "https://staging-api.example.com")

    def get_timeout(self) -> int:
        return self._config.get("timeout", 30000)

    def is_headless(self) -> bool:
        return self._config.get("headless", True)

    def get_user(self, key: str) -> dict:
        return self._users.get(key, {})


def get_config() -> ConfigLoader:
    return ConfigLoader()
