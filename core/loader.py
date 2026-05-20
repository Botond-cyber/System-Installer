import yaml
from os import listdir, path

from core.resources import resource_path


def load_module_or_script(name: str, directory: str = "modules/") -> dict:
    dir_clean = directory.rstrip("/")
    file_path = f"{dir_clean}/{name}.yaml"

    with open(resource_path(file_path), "r") as f:
        return yaml.safe_load(f)


def get_modules_or_scripts(directory) -> tuple:
    arr = []
    dir_path = resource_path(directory)
    for f in listdir(dir_path):
        if path.isfile(path.join(dir_path, f)):
            name = f.removesuffix(".yaml")
            arr.append(
                {
                    "filename": name,
                    "content": load_module_or_script(name, directory),
                }
            )
    return tuple(arr)


def get_modules_or_scrips_from_profile(profile, directory) -> tuple:
    if profile == "Custom":
        return ()
    else:
        profile_path = f"profiles/{profile.lower()}.yaml"
        key = directory.rstrip("/")
        with open(resource_path(profile_path), "r") as f:
            return tuple(yaml.safe_load(f)[key])
