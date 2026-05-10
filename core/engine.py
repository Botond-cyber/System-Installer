from core.loader import load_module
from core.platform import get_platform


class Engine:
    def __init__(self, ctx):
        self.ctx = ctx
        self.platform = get_platform()

    def install(self, module_name: str):
        module = load_module(module_name)

        print(f"\n📦 Installing {module_name}...\n")

        actions = module["actions"]["install"]

        # pick OS-specific steps
        steps = self.platform.resolve(actions)

        for step in steps:
            self.ctx.run(step)
