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

    @staticmethod
    def delete_installed_packages_file():
        Path(path.join(path.expanduser("~"), ".system-installer")).unlink(missing_ok=True)

    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx
        self.log_file_path = None
        self._is_setup = False

    def _setup_log_file(self):
        """Creates the log directory and initial file only when needed."""
        if not self._is_setup:
            makedirs("logs", exist_ok=True)
            self.log_file_path = path.join("logs", f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
            with open(self.log_file_path, "w", encoding="utf-8") as f:
                f.write(f"[{datetime.now().isoformat()}] Logger initialized\n")
            self._is_setup = True

    def log_to_file(self, message: str):
        if self.ctx.settings.enable_logging:
            self._setup_log_file()

            if self.log_file_path is not None:
                with open(self.log_file_path, "a", encoding="utf-8") as f:
                    f.write(f"[{datetime.now().isoformat()}] {message}\n")
