from lib.models.package import Package
from lib.models.profile import Profile


class Context:
    def __init__(self) -> None:
        self.packages_to_install: list[Package] = []
        self.packages_from_profile: list[Package] = []
        self.available_packages: list[Package] = []
        self.available_profiles: list[Profile] = []

        self.installed_packages: set[str] = set()

        self.selected_profile: Profile | None = None

    def mark_installed(self, package_id: str) -> None:
        self.installed_packages.add(package_id)

    def is_installed(self, package_id: str) -> bool:
        return package_id in self.installed_packages
