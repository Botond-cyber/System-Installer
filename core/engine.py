from core.loader import load_module
from core.platform import get_platform


class Engine:
    def __init__(self, ctx):
        self.ctx = ctx
        self.platform = get_platform()

    def install(self, module_name: str):

        if self.ctx.is_installed(module_name):
            return

        try:
            module = load_module(module_name)
        except:
            print(f"❌ Module {module_name} not found")
            return
        print(f"📦 Installing {module_name}...")

        for dep in module.get("depends", []):
            self.install(dep)
            if not self.ctx.is_installed(dep):
                print(
                    f"❌ Failed to install {module_name} because it failed to install dependency: {dep}"
                )
                return

        actions = module["actions"]["install"]

        # pick OS-specific steps
        steps = self.platform.resolve(actions)

        for step in steps:
            try:
                self.ctx.run(step)
            except Exception as e:
                print(f"❌ Failed to install {module_name}")

        self.ctx.mark_installed(module_name)
