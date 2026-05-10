import subprocess


class Context:
    def __init__(self):
        self.state = {}

    def run(self, command: str):
        print(f"▶ {command}")
        subprocess.run(command, shell=True, check=True)
