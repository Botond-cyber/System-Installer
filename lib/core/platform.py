import platform as py_platform
import distro


class Platform:
    @staticmethod
    def get_os() -> str:
        system = py_platform.system().lower()
        if system == "linux":
            return distro.id()
        elif system == "windows":
            return "windows"
        else:
            raise Exception("Unsupported OS")
