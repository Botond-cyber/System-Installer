from lib.core.loader import Loader
from lib.core.platform import get_platform_instructions


class Engine:
    def __init__(self, ctx):
        self.ctx = ctx
        self.platform_instructions = get_platform_instructions()

    def _resolve_dependencies(self, depends, dep_type="modules"):
        """Resolve dependencies for a given type (modules or scripts).
        Returns a list of dependency names."""
        if not depends:
            return []
        if isinstance(depends, dict):
            # Extract the specific dependency type (modules or scripts)
            dep_list = depends.get(dep_type, {})
            if isinstance(dep_list, dict):
                # It's platform-specific, resolve it
                return self.platform_instructions.resolve(dep_list)
            elif isinstance(dep_list, list):
                return dep_list
        return []

    def install(self, module_name: str):
        if self.ctx.is_installed(module_name):
            return
        try:
            module = Loader.load_module_or_script(module_name)
        except:
            print(f"❌ Module {module_name} not found")
            return
        print(f"📦 Installing {module_name}...")
        # Install module dependencies
        for dep in self._resolve_dependencies(module.get("depends"), "modules"):
            self.install(dep)
            if not self.ctx.is_installed(dep):
                print(
                    f"❌ Failed to install {module_name} because it failed to install dependency: {dep}"
                )
                return
        # Run script dependencies
        for dep in self._resolve_dependencies(module.get("depends"), "scripts"):
            self.run(dep)
            if not self.ctx.is_script_ran(dep):
                print(
                    f"❌ Failed to install {module_name} because it failed to run script dependency: {dep}"
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
        if self.ctx.is_script_ran(script_name):
            return
        try:
            script = Loader.load_module_or_script(script_name, "scripts/")
        except:
            print(f"❌ script {script_name} not found")
            return
        print(f"📦 Running {script_name}...")
        # Install module dependencies
        for dep in self._resolve_dependencies(script.get("depends"), "modules"):
            self.install(dep)
            if not self.ctx.is_installed(dep):
                print(
                    f"❌ Failed to run {script_name} because it failed to install dependency: {dep}"
                )
                return
        # Run script dependencies
        for dep in self._resolve_dependencies(script.get("depends"), "scripts"):
            self.run(dep)
            if not self.ctx.is_script_ran(dep):
                print(
                    f"❌ Failed to run {script_name} because it failed to run script dependency: {dep}"
                )
                return
        actions = script["actions"]
        steps = self.platform_instructions.resolve(actions)
        for step in steps:
            try:
                self.ctx.run(step)
            except Exception as e:
                print(f"❌ Failed to run {script_name}")
        self.ctx.mark_ran_script(script_name)