from typing import Any


class Package:
    def __init__(self, package: dict[str, Any]) -> None:
        # Required fields
        self.package_schema_version: int = package["package_schema_version"]
        self.name: str = package["name"]
        self.id: str = package["id"]
        self.version: int = package["version"]
        self.type: str = package["type"]
        self.supported_os: list[str] = package["supported_os"]

        # Optional fields
        self.author: str | None = package.get("author")
        self.tags: list[str] = package.get("tags", [])
        self.description: str | None = package.get("description")

        self.dependencies: dict[str, list[str]] = package.get("dependencies", {})

        self.check: dict[str, Any] = package.get("check", {})

        self.install: dict[str, Any] = package.get("install", {})

        self.configure: dict[str, Any] = package.get("configure", {})
