from core.engine import Engine
from core.context import Context

def main():
    ctx = Context()
    engine = Engine(ctx)

    # for now: hardcoded test module
    engine.install("flutter")

if __name__ == "__main__":
    main()