import yaml
from os import listdir, path


def load_module(name: str) -> dict:
    path = f"modules/{name}.yaml"

    with open(path, "r") as f:
        return yaml.safe_load(f)


def getModules(directory) -> tuple:
    modules = []
    for f in listdir(directory):
        if path.isfile(path.join(directory, f)):
            modules.append(
                {
                    "filename": f.removesuffix(".yaml"),
                    "content": load_module(f.removesuffix(".yaml")),
                }
            )
    return tuple(modules)


def getModulesFromProfile(profile) -> tuple:
    if profile == "Custom":
        return ()
    else:
        path = f"profiles/{profile.lower()}.yaml"
        with open(path, "r") as f:
            return tuple(yaml.safe_load(f)["modules"])
