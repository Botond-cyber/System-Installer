from typing import Any


class Module:
    def __init__(self, module: dict[str, Any]) -> None:
        self.id: str = module["id"]
        self.name: str = module["name"]
        self.dependencies: list[Any] = module["dependencies"]
        self.check:dict[str, Any] = module["check"]
        self.install:dict[str, Any] = module["install"]
