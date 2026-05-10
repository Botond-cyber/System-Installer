import platform as py_platform
import distro


class LinuxPlatform:
    def resolve(self, actions):
        return actions.get("linux", {}).get(distro.id(), [])


class WindowsPlatform:
    def resolve(self, actions):
        return actions.get("windows", [])


def get_platform():
    system = py_platform.system().lower()

    if system == "linux":
        return LinuxPlatform()
    elif system == "windows":
        return WindowsPlatform()
    else:
        raise Exception("Unsupported OS")
