import subprocess


class Context:
    def __init__(self):
        self.state = {}
        self.installed = set()
        self.selected_profile = None

    def run(self, command: str):
        print(f"▶ {command}")
        subprocess.run(command, shell=True, check=True)

    def mark_installed(self, name):
        self.installed.add(name)

    def is_installed(self, name):
        return name in self.installed
