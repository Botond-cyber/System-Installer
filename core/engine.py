from core.loader import load_module_or_script
from core.platform import get_platform_instructions


class Engine:
    def __init__(self, ctx):
        self.ctx = ctx
        self.platform_instructions = get_platform_instructions()

    def _resolve_dependencies(self, depends):
        if not depends:
            return []
        if isinstance(depends, dict):
            return self.platform_instructions.resolve(depends)
        if isinstance(depends, str):
            return [depends]
        if isinstance(depends, list):
            return depends
        return []

    def install(self, module_name: str):
        if self.ctx.is_installed(module_name):
            return
        try:
            module = load_module_or_script(module_name)
        except:
            print(f"❌ Module {module_name} not found")
            return
        print(f"📦 Installing {module_name}...")
        for dep in self._resolve_dependencies(module.get("depends")):
            self.install(dep)
            if not self.ctx.is_installed(dep):
                print(
                    f"❌ Failed to install {module_name} because it failed to install dependency: {dep}"
                )
                return
        actions = module["actions"]["install"]
        steps = self.platform_instructions.resolve(actions)
        for step in steps:
            try:
                self.ctx.run(step)
            except Exception as e:
                print(f"❌ Failed to install {module_name}")
        self.ctx.mark_installed(module_name)

    
    def run(self, script_name: str):
        try:
            script = load_module_or_script(script_name, "scripts/")
        except:
            print(f"❌ script {script_name} not found")
            return
        print(f"📦 Running {script_name}...")
        for dep in self._resolve_dependencies(script.get("depends")):
            self.install(dep)
            if not self.ctx.is_installed(dep):
                print(
                    f"❌ Failed to run {script_name} because it failed to install dependency: {dep}"
                )
                return
        actions = script["actions"]
        steps = self.platform_instructions.resolve(actions)
        for step in steps:
            try:
                self.ctx.run(step)
            except Exception as e:
                print(f"❌ Failed to run {script_name}")