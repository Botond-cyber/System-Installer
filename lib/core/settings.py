from typing import Any

import yaml

from lib.core.context import Context
from lib.core.logger import Logger


class Settings:
    @staticmethod
    def load_settings(ctx: Context, logger: Logger):
        try:
            with open("settings/settings.yaml", "r", encoding="utf-8") as f:
                file = yaml.safe_load(f)
                Settings.save_settings_to_context(ctx, file)

        except Exception as e:
            logger.write_to_log_file(f"Failed to load settings from file\n\tException:{e}")

    @staticmethod
    def save_settings_to_file():
        pass

    @staticmethod
    def save_settings_to_context(ctx: Context, settings: dict[str, Any]):
        pass
