from datetime import datetime
from os import makedirs, path
from pathlib import Path

import yaml

from lib.core.context import Context


class Logger:
    @staticmethod
    def generate_installed_packages_file(ctx: Context):
        with open(path.join(path.expanduser("~"), ".system-installer"), "w") as f:
            yaml.dump({"Packages": list(ctx.installed_packages)}, f, default_flow_style=False)

    @staticmethod
    def clear_logs():
        log_path = Path("logs")
        for log in log_path.iterdir():
            if log.is_file():
                log.unlink()

    def __init__(self) -> None:
        makedirs("logs", exist_ok=True)
        self.log_file_path = path.join("logs", f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
        with open(self.log_file_path, "w", encoding="utf-8") as f:
            f.write(f"[{datetime.now().isoformat()}] Logger initialized\n")

    def write_to_log_file(self, message: str):
        with open(self.log_file_path, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().isoformat()}] {message}\n")
