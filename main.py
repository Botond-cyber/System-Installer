import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


import subprocess
from os import name


from lib.core.engine import Engine
from lib.core.context import Context
from lib.core.loader import Loader
from lib.ui.installer_app import InstallerApp

PACKAGE_DIRECTORY = "../packages/"
PROFILE_DIRECTORY = "../profiles/"


def main():
    ctx = Context()
    engine = Engine(ctx)

    ctx.available_packages = {
        package.id: package for package in Loader.load_packages(PACKAGE_DIRECTORY)
    }
    ctx.available_profiles = Loader.loadProfiles(PROFILE_DIRECTORY)
    app = InstallerApp(ctx, engine)
    app.run()
    subprocess.run("cls" if name == "nt" else "clear", shell=True)


if __name__ == "__main__":
    main()
