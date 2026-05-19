import subprocess


class Context:
    def __init__(self):
        self.modules_to_install = []
        self.scripts_to_run = []
        self.installed = set()
        self.ran_scripts = set()
        self.selected_profile = None

    def run(self, command: str):
        # print(f"▶ {command}")
        subprocess.run(command, shell=True, check=True)

    def mark_installed(self, name):
        self.installed.add(name)

    def is_installed(self, name):
        return name in self.installed

    def mark_ran_script(self, name):
        self.ran_scripts.add(name)

    def is_script_ran(self, name):
        return name in self.ran_scripts
