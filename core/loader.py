import yaml
from os import listdir, path



def load_module(name: str):
    path = f"modules/{name}.yaml"

    with open(path, "r") as f:
        return yaml.safe_load(f)

def getModules(directory):
        modules = []
        for idx, f in enumerate(listdir(directory)):
            if path.isfile(path.join(directory, f)):
                modules.append((f.removesuffix(".yaml").capitalize(), idx))
        return tuple(modules)