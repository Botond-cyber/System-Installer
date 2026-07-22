from os import path

import yaml

from lib.core.context import Context


class Logger:
    @staticmethod
    def generate_installed_packages_file(ctx: Context):
        with open(path.join(path.expanduser("~"), ".system-installer"), "w") as f:
            yaml.dump(
                {"Packages": list(ctx.installed_packages)}, f, default_flow_style=False
            )

    @staticmethod
    def generate_log_file():
        pass
