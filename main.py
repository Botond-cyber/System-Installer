import subprocess
import sys
from os import name
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.core.context import Context
from lib.core.engine import Engine
from lib.core.loader import Loader
from lib.core.logger import Logger
from lib.core.settings import Settings
from lib.ui.installer_app import InstallerApp

PACKAGE_DIRECTORY = "../packages/"
PROFILE_DIRECTORY = "../profiles/"


def main():
    ctx = Context()
    logger = Logger(ctx)
    Settings.load_settings(ctx, logger)
    engine = Engine(ctx, logger)

    ctx.available_packages = {package.id: package for package in Loader.load_packages(PACKAGE_DIRECTORY)}
    ctx.available_profiles = Loader.loadProfiles(PROFILE_DIRECTORY)
    app = InstallerApp(logger, ctx, engine)
    app.run()
    subprocess.run("cls" if name == "nt" else "clear", shell=True)
    engine.run()


if __name__ == "__main__":
    main()
