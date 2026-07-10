import sys
import subprocess
from os import name

from lib.core.engine import Engine
from lib.core.context import Context
from lib.ui.installer_app import InstallerApp


def main():
    ctx = Context()
    engine = Engine(ctx)

    if len(sys.argv) < 2:
        app = InstallerApp(ctx, engine)
        app.run()
        subprocess.run("cls" if name == "nt" else "clear", shell=True)
        if ctx.packages_to_install:
            print(ctx.packages_to_install)
            for m in ctx.packages_to_install:
                engine.install(m)
        if ctx.scripts_to_run:
            print(ctx.scripts_to_run)
            for s in ctx.scripts_to_run:
                engine.run(s)
    modules = sys.argv[1:]

    for m in modules:
        engine.install(m)


if __name__ == "__main__":
    main()
