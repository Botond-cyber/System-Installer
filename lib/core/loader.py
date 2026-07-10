from ast import List
from warnings import deprecated

import yaml
from os import listdir, path

from lib.core.resources import resource_path
from lib.models.package import Module


class Loader:
    @staticmethod
    @deprecated("Use Loader.load_module(file_path:str) instead")
    
    def load_module_or_script(name: str, directory: str = "modules/") -> dict:
        dir_clean = directory.rstrip("/")
        file_path = f"{dir_clean}/{name}.yaml"

        with open(resource_path(file_path), "r") as f:
            return yaml.safe_load(f)

    @staticmethod
    @deprecated("Use Loader.load_modules(directory: str) instead")
    def get_modules_or_scripts(directory) -> tuple:
        arr = []
        dir_path = resource_path(directory)
        for f in listdir(dir_path):
            if path.isfile(path.join(dir_path, f)):
                name = f.removesuffix(".yaml")
                arr.append(
                    {
                        "filename": name,
                        "content": Loader.load_module_or_script(name, directory),
                    }
                )
        return tuple(arr)

    @staticmethod
    def get_modules_or_scrips_from_profile(profile, directory) -> tuple:
        if profile == "Custom":
            return ()
        else:
            profile_path = f"profiles/{profile.lower()}.yaml"
            key = directory.rstrip("/")
            with open(resource_path(profile_path), "r") as f:
                return tuple(yaml.safe_load(f)[key])

    @staticmethod
    def getProfiles(directory):
        dir_path = resource_path(directory)
        profiles = [f for f in listdir(dir_path) if path.isfile(path.join(dir_path, f))]
        return profiles

    @staticmethod
    def load_modules(directory: str) -> list[Module]:
        modules: list[Module] = []
        dir_path = resource_path(directory)
        for f in listdir(dir_path):
            if path.isfile(path.join(dir_path, f)):
                modules.append(Loader.load_module(f"{dir_path}/{f}"))
        return modules
        

    @staticmethod
    def load_module(file_path:str) -> Module:
        print(file_path)
        with open(resource_path(file_path), "r") as f:
            return Module(yaml.safe_load(f))
