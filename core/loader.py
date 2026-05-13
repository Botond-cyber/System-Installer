import yaml
from os import listdir, path



def load_module(name: str):
    path = f"modules/{name}.yaml"

    with open(path, "r") as f:
        return yaml.safe_load(f)

def getModules(directory, profile):
        modules = []
        preSelectedModules = getModulesFromProfile(profile)
        for idx, f in enumerate(listdir(directory)):
            if path.isfile(path.join(directory, f)):
                modules.append((f.removesuffix(".yaml").capitalize(), idx, True if f.removesuffix(".yaml") in preSelectedModules else False))
        return tuple(modules)

def getModulesFromProfile(profile):
    if profile == "Custom":
        return []
    else:
        path = f"profiles/{profile}.yaml"
        with open(path, "r") as f:
            return( yaml.safe_load(f)["modules"])