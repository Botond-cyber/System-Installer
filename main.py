import sys

from core.engine import Engine
from core.context import Context


def main():
    ctx = Context()
    engine = Engine(ctx)

    # for now: hardcoded test module
    if len(sys.argv) < 2:
        print("Usage: installer <module1> <module2> ...")
        return

    modules = sys.argv[1:]

    for m in modules:
        engine.install(m)


if __name__ == "__main__":
    main()
