import subprocess

from lib.core.context import Context
from lib.core.dependency_resolver import DependencyResolver
from lib.core.loader import Loader
from lib.core.logger import Logger
from lib.models.package import Package


class Engine:
    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx
        pass

    # main method for running the installer
    def run(self):
        print(self.ctx.packages_to_install)
        for i in Loader.load_installation_history(self.ctx):  # loads already installed packages form file
            print(i)
            self.ctx.mark_installed(i)

        resolved_packages: list[str] = []  # resolves dependencies
        for package_id in self.ctx.packages_to_install:
            for resolved_package in DependencyResolver.resolve(self.ctx, package_id):
                if resolved_package not in resolved_packages:
                    resolved_packages.append(resolved_package)

        for package_id in resolved_packages:  # runs install and configure functions on all the packages
            if self.check_if_installed(package_id):
                continue
            try:
                self.install(package_id)
            except Exception as e:
                print(f"failed to install: {package_id}\n{e} ")
            else:
                self.ctx.mark_installed(package_id)
                self.configure(package_id)
        Logger.generate_installed_packages_file(self.ctx)

    # package installer method
    def install(self, package_id: str):
        package: Package = self.ctx.available_packages[package_id]
        for i in package.install[self.ctx.os]:
            print(i)

    # package configure method
    def configure(self, package_id: str):
        package: Package = self.ctx.available_packages[package_id]
        for i in package.configure[self.ctx.os]:
            print(i)

    # checks if package is already installed
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
