import sys

from core.engine import Engine
from core.context import Context
from ui.installer_app import InstallerApp


def main():
    ctx = Context()
    engine = Engine(ctx)

    if len(sys.argv) < 2:
        app = InstallerApp(ctx, engine)
        app.run()

    modules = sys.argv[1:]

    for m in modules:
        engine.install(m)


if __name__ == "__main__":
    main()
