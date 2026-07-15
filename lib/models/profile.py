from typing import Any


class Profile:
    def __init__(self, profile: dict[str, Any]) -> None:
        # Required fields
        self.profile_schema_version: int = profile["profile_schema_version"]
        self.name: str = profile["name"]
        self.id: str = profile["id"]
        self.version: int = profile["version"]
        self.supported_os: list[str] = profile["supported_os"]
        self.packages: dict[str, Any] = profile["packages"]

        # Optional fields
        self.author: str | None = profile.get("author")
        self.tags: list[str] = profile.get("tags", [])
        self.description: str | None = profile.get("description")

    def get_packages(self, os: str) -> list[str]:
        packages: set[str] = set()
        if self.packages.get("all"):
            for p in self.packages["all"]:
                packages.add(p)
        if self.packages.get(os):
            for p in self.packages[os]:
                packages.add(p)
        return list(packages)
