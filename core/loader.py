import yaml


def load_module(name: str):
    path = f"modules/{name}.yaml"

    with open(path, "r") as f:
        return yaml.safe_load(f)
