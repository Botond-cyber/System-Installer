import subprocess

from lib.core.context import Context
from lib.core.loader import Loader
from lib.models.package import Package


class Engine:
    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx
        pass

    def run(self):
        print(self.ctx.packages_to_install)
        for i in Loader.load_installation_history(self.ctx):
            self.ctx.mark_installed(i)

        for p in self.ctx.packages_to_install:
            print(p)
            if self.check_if_installed(p):
                continue

    def install(self):
        pass

    def configure(self):
        pass

    def check_if_installed(self, package_id: str):
        package: Package = self.ctx.available_packages[package_id]
        try:
            res = subprocess.run(
                str(package.check[self.ctx.os]),
                shell=True,
                capture_output=True,
                text=True,
            )
            output = res.stdout.strip()
            print(output)
            return True if output == "true" else False
        except:
            return False
