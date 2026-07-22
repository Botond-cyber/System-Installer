import subprocess

from lib.core.context import Context
from lib.core.dependency_resolver import DependencyResolver
from lib.core.loader import Loader
from lib.core.logger import Logger
from lib.models.package import Package


class Engine:
    def __init__(self, ctx: Context, logger: Logger) -> None:
        self.ctx = ctx
        self.logger = logger
        pass

    # main method for running the installer
    def run(self):
        print(self.ctx.packages_to_install)
        self.logger.write_to_log_file(f"Packages selected: {self.ctx.packages_to_install}")
        for i in Loader.load_installation_history(self.ctx):  # loads already installed packages form file
            print(i)
            self.ctx.mark_installed(i)

        resolved_packages: list[str] = []  # resolves dependencies
        for package_id in self.ctx.packages_to_install:
            for resolved_package in DependencyResolver.resolve(self.ctx, package_id):
                if resolved_package not in resolved_packages:
                    resolved_packages.append(resolved_package)

        self.logger.write_to_log_file(f"Packages to install: {resolved_packages}")

        for package_id in resolved_packages:  # runs install and configure functions on all the packages
            self.install(package_id)
            self.configure(package_id)

        Logger.generate_installed_packages_file(self.ctx)
        input("PRESS ANY KEY TO EXIT...")

    # package installer method
    def install(self, package_id: str):
        package: Package = self.ctx.available_packages[package_id]
        if package.install.get(self.ctx.os):
            self.logger.write_to_log_file(f"Installing: {package_id} ...")

            if self.check_if_installed(package_id):
                self.logger.write_to_log_file(f"Already installed: {package_id} ✅")
                return
            try:
                for i in package.install[self.ctx.os]:
                    if self.ctx.dry_run == True:
                        print(i)
                    else:
                        subprocess.run(
                            str(i),
                            shell=True,
                            capture_output=True,
                            text=True,
                        )
            except Exception as e:
                print(f"failed to install: {package_id}\n{e} ")
                self.logger.write_to_log_file(f"Failed to install: {package_id} ❌\n\tReason: {e}")
                return

            else:
                self.ctx.mark_installed(package_id)
                self.logger.write_to_log_file(f"Successfully installed: {package_id} ✅")
                return
        return

    # package configure method
    def configure(self, package_id: str):
        package: Package = self.ctx.available_packages[package_id]
        if package.configure.get(self.ctx.os):
            self.logger.write_to_log_file(f"Configuring: {package_id} ...")
            try:
                for i in package.configure[self.ctx.os]:
                    if self.ctx.dry_run == True:
                        print(i)
                    else:
                        subprocess.run(
                            str(i),
                            shell=True,
                            capture_output=True,
                            text=True,
                        )

            except Exception as e:
                print(f"Failed to configure: {package_id}\n{e}")
                self.logger.write_to_log_file(f"Failed to configure: {package_id} ❌\n\tReason: {e}")
            else:
                self.logger.write_to_log_file(f"Successfully configured: {package_id} ✅")

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
