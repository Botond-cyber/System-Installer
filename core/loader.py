import yaml
from os import listdir, path


def load_module_or_script(name: str, directory: str = "modules/") -> dict:
    dir_clean = directory.rstrip("/")
    file_path = f"{dir_clean}/{name}.yaml"

    with open(file_path, "r") as f:
        return yaml.safe_load(f)


def get_modules_or_scripts(directory) -> tuple:
    arr = []
    for f in listdir(directory):
        if path.isfile(path.join(directory, f)):
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
        with open(profile_path, "r") as f:
            return tuple(yaml.safe_load(f)[key])
