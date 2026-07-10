import platform as py_platform
import distro


class LinuxPlatform:
    def resolve(self, actions):
        actions = actions or {}
        linux_actions = actions.get("linux")
        if isinstance(linux_actions, dict):
            return linux_actions.get(distro.id(), []) or []
        if isinstance(linux_actions, list):
            return linux_actions
        if isinstance(linux_actions, str):
            return [linux_actions]
        return []


class WindowsPlatform:
    def resolve(self, actions):
        actions = actions or {}
        windows_actions = actions.get("windows")
        if isinstance(windows_actions, list):
            return windows_actions
        if isinstance(windows_actions, str):
            return [windows_actions]
        return []


def get_platform_instructions():
    system = py_platform.system().lower()

    if system == "linux":
        return LinuxPlatform()
    elif system == "windows":
        return WindowsPlatform()
    else:
        raise Exception("Unsupported OS")