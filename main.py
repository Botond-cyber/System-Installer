import sys
import subprocess
from os import name

from core.engine import Engine
from core.context import Context
from ui.installer_app import InstallerApp


def main():
    ctx = Context()
    engine = Engine(ctx)

    if len(sys.argv) < 2:
        app = InstallerApp(ctx, engine)
        app.run()
        subprocess.run("cls" if name == "nt" else "clear", shell=True)
        print(ctx.modules_to_install)
        print(ctx.scripts_to_run)
        for m in ctx.modules_to_install:
            engine.install(m)

    modules = sys.argv[1:]

    for m in modules:
        engine.install(m)


if __name__ == "__main__":
    main()
