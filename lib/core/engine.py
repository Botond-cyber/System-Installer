import subprocess

from lib.core.context import Context
from lib.core.loader import Loader
from lib.core.logger import Logger
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
            if self.check_if_installed(p):
                continue
            self.install(p)
        Logger.generate_installed_packages_file(self.ctx)

    def install(self, package_id: str):
        package: Package = self.ctx.available_packages[package_id]
        for i in package.install[self.ctx.os]:
            print(i)

    def configure(self, package_id: str):
        package: Package = self.ctx.available_packages[package_id]
        for i in package.configure[self.ctx.os]:
            print(i)

    def check_if_installed(self, package_id: str):
        if self.ctx.is_installed(package_id):
            return True

        package: Package = self.ctx.available_packages[package_id]

        try:
            res = subprocess.run(
                str(package.check[self.ctx.os]),
                shell=True,
                capture_output=True,
                text=True,
            )
            output = res.stdout.strip()

            if output == "true":
                self.ctx.mark_installed(package_id)
                return True
            else:
                return False

        except:
            return False
