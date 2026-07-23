from dataclasses import dataclass

from lib.core.platform import Platform
from lib.models.package import Package
from lib.models.profile import Profile


@dataclass(slots=True)
class InstallerSettings:
    enable_dry_run: bool = False
    enable_logging: bool = True
    use_installer_file: bool = True
    use_central_repo: bool = False


class Context:
    def __init__(self) -> None:
        self.packages_to_install: list[str] = []
        self.packages_from_profile: set[str] = set()
        self.available_packages: dict[str, Package] = {}
        self.available_profiles: list[Profile] = []
        self.os: str = Platform.get_os()

        self.installed_packages: set[str] = set()

        self.selected_profile: Profile | None = None

        self.settings = InstallerSettings()

    def mark_installed(self, package_id: str) -> None:
        self.installed_packages.add(package_id)

    def is_installed(self, package_id: str) -> bool:
        return package_id in self.installed_packages
