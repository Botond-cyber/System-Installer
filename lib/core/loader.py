import yaml
from os import listdir, path

from lib.core.context import Context
from lib.core.resources import resource_path
from lib.models.package import Package
from lib.models.profile import Profile

# INSTALLFILEPATHWINODWS = path.join(path.expanduser("~"), ".system-installer")
# INSTALLFILEPATHLINUX = path.join(path.expanduser("~"), ".system-installer")


class Loader:
    @staticmethod
    def loadProfiles(directory: str) -> list[Profile]:
        dir_path = resource_path(directory)
        profiles: list[Profile] = []
        for f in listdir(dir_path):
            if path.isfile(path.join(dir_path, f)):
                profiles.append(Loader.loadProfile(f"{dir_path}/{f}"))
        return profiles

    @staticmethod
    def loadProfile(file_path: str) -> Profile:
        with open(resource_path(file_path), "r") as f:
            return Profile(yaml.safe_load(f))

    @staticmethod
    def load_packages(directory: str) -> list[Package]:
        packages: list[Package] = []
        dir_path = resource_path(directory)
        for f in listdir(dir_path):
            if path.isfile(path.join(dir_path, f)):
                packages.append(Loader.load_package(f"{dir_path}/{f}"))
        return packages

    @staticmethod
    def load_package(file_path: str) -> Package:
        with open(resource_path(file_path), "r") as f:
            return Package(yaml.safe_load(f))

    @staticmethod
    def load_installation_history(ctx: Context) -> list[str]:
        try:
            with open(path.join(path.expanduser("~"), ".system-installer"), "r") as f:
                file = yaml.safe_load(f)
            print(f"loader: {file['Packages']}")
            return file["Packages"]
        except:
            print("error")
            return []
