from dataclasses import asdict
from typing import Any, cast
from pathlib import Path

import yaml

from lib.core.context import Context, InstallerSettings
from lib.core.logger import Logger


class Settings:
    SETTINGS_PATH = Path("settings/settings.yaml")

    @staticmethod
    def load_settings(ctx: Context, logger: Logger):
        try:
            if not Settings.SETTINGS_PATH.exists():
                logger.log_to_file("Settings file not found; using defaults")
                return

            with Settings.SETTINGS_PATH.open("r", encoding="utf-8") as f:
                raw_settings: Any = yaml.safe_load(f)

            if isinstance(raw_settings, dict):
                settings = cast(dict[str, Any], raw_settings)
            else:
                settings = {}

            ctx.settings = Settings.load_settings_from_mapping(settings)

        except Exception as e:
            logger.log_to_file(f"Failed to load settings from file\n\tException:{e}")
        else:
            logger.log_to_file(f"Settings loaded successfully")

    @staticmethod
    def save_settings_to_file(ctx: Context, logger: Logger):
        try:
            Settings.SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
            with Settings.SETTINGS_PATH.open("w", encoding="utf-8") as f:
                yaml.safe_dump(asdict(ctx.settings), f, default_flow_style=False, sort_keys=False)
        except Exception as e:
            logger.log_to_file(f"Failed to save settings\n\rException:{e}")
            raise Exception(e)
        else:
            logger.log_to_file(f"Successfully saved settings")

    @staticmethod
    def load_settings_from_mapping(settings: dict[str, Any]) -> InstallerSettings:
        defaults = InstallerSettings()

        return InstallerSettings(
            enable_dry_run=bool(settings.get("enable_dry_run", defaults.enable_dry_run)),
            enable_logging=bool(settings.get("enable_logging", defaults.enable_logging)),
            use_installer_file=bool(settings.get("use_installer_file", defaults.use_installer_file)),
            use_central_repo=bool(settings.get("use_central_repo", defaults.use_central_repo)),
        )
