from textual import on
from textual.events import Mount
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import (
    SelectionList,
    Footer,
    Button,
    Static,
    TabbedContent,
    TabPane,
    Markdown,
)
from textual.containers import Vertical

from core.loader import get_modules_or_scripts, get_modules_or_scrips_from_profile


class MainScreen(Screen):
    CSS_PATH = "assets/main.tcss"
    modules_directory = "modules/"
    scripts_directory = "scripts/"

    def __init__(
        self, name: str | None = None, id: str | None = None, classes: str | None = None
    ) -> None:
        self.modules = ()
        self.scripts = ()
        self.preSelectedModules = ()
        self.dependencies = []
        self.selected_modules = []
        self.selected_scripts = []
        super().__init__(name, id, classes)

    @property
    def ctx(self):
        return getattr(self.app, "ctx")

    @property
    def engine(self):
        return getattr(self.app, "engine")

    def compose(self) -> ComposeResult:
        self.modules = get_modules_or_scripts(self.modules_directory)
        self.scripts = get_modules_or_scripts(self.scripts_directory)
        self.pre_selected_modules = get_modules_or_scrips_from_profile(
            self.ctx.selected_profile, "modules/"
        )
        self.pre_selected_scripts = get_modules_or_scrips_from_profile(
            self.ctx.selected_profile, "scripts"
        )
        with TabbedContent():
            with TabPane(title="Modules"):
                with Static(id="grid-container"):
                    with Static(classes="modules-pane"):
                        modules = self._construct_widgets("modules")
                        yield SelectionList[int](*modules, id="modules-select")

                    with Vertical(id="actions-pane"):
                        yield Button("Select all")
                        yield Button("Deselect all")
                        yield Button("Reset")
                        yield Button("Next->", id="next-btn-modules")

            with TabPane(title="Scripts", id="scripts"):
                with Static(id="grid-container"):
                    with Static(classes="modules-pane"):
                        modules = self._construct_widgets("scripts")
                        yield SelectionList[int](*modules, id="scripts-select")

                    with Vertical(id="actions-pane"):
                        yield Button("Select all")
                        yield Button("Deselect all")
                        yield Button("Reset")
                        yield Button("Next->", id="next-btn-scripts")
                        yield Button("<-Back", id="back-btn-scripts")

            with TabPane(title="Overview", id="install"):
                with Static(id="grid-container"):
                    with Static(classes="modules-pane"):
                        yield Markdown(id="overviewMarkdown")

                    with Vertical(id="actions-pane"):
                        yield Button("Install", id="install-btn")
                        yield Button("<-Back", id="back-btn-install")

        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#modules-select").border_title = "Choose modules to install:"
        self.query_one("#scripts-select").border_title = "Choose scripts to install:"
        self.query_one(Markdown).border_title = "Selected modules and scripts:"

    @on(Mount)
    @on(SelectionList.SelectedChanged)
    def update_selected_view(self, event) -> None:
        modules_select = self.query_one("#modules-select", SelectionList)
        scripts_select = self.query_one("#scripts-select", SelectionList)

        def _values_from_selection(sel: SelectionList) -> list:
            vals = getattr(sel, "selected", None)
            if not vals:
                return []
            out = []
            for v in vals:
                # Prefer an explicit value attribute when available
                candidate = None
                if hasattr(v, "value"):
                    candidate = v.value
                elif isinstance(v, (tuple, list)) and len(v) > 1:
                    candidate = v[1]
                else:
                    candidate = v

                s = str(candidate)
                # normalize whitespace and non-breaking spaces
                s = s.replace("\u00a0", " ").strip()
                out.append(s)
            return out

        def _sanitize_name(name: str) -> str:
            n = name.strip()
            if n.endswith(".yaml"):
                n = n[: -len(".yaml")]
            return n

        self.selected_modules = [
            _sanitize_name(s) for s in _values_from_selection(modules_select)
        ]
        self.selected_scripts = [
            _sanitize_name(s) for s in _values_from_selection(scripts_select)
        ]
        self._get_dependencies("modules")
        self._get_dependencies("scripts")
        self.query_one(Markdown).update(self._construct_markdown())
        # self.query_one(Markdown).update([self.modules, self.scripts])

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "next-btn-modules":
                self.query_one("#next-btn-scripts").focus()
            case "next-btn-scripts":
                self.query_one("#install-btn").focus()
            case "back-btn-scripts":
                self.query_one("#next-btn-modules").focus()
            case "back-btn-install":
                self.query_one("#next-btn-scripts").focus()

        # if event.button.id == "install":
        #     self.app.exit(str(event.button))
        #     subprocess.run("cls" if name == "nt" else "clear", shell=True)
        #     self.engine.install("powertoys")

    def _construct_widgets(self, widget_type) -> tuple:
        widgets = []
        for m in self.modules if widget_type == "modules" else self.scripts:
            widgets.append(
                (
                    m["content"]["name"].capitalize(),
                    m["filename"],
                    (
                        True
                        if m["filename"].removesuffix(".yaml")
                        in (
                            self.pre_selected_modules
                            if widget_type == "modules"
                            else self.pre_selected_scripts
                        )
                        else False
                    ),
                )
            )
        return tuple(widgets)

    def _construct_markdown(self) -> str:
        modules_md = "\n".join(f"- {m}" for m in self.selected_modules) or "None"
        scripts_md = "\n".join(f"- {s}" for s in self.selected_scripts) or "None"
        deps_md = "\n".join(f"- {d}" for d in self.dependencies) or "None"

        return "\n".join(
            [
                "## Modules:",
                modules_md,
                "",
                "## Scripts:",
                scripts_md,
                "",
                "## Dependencies:",
                deps_md,
            ]
        )

    def _get_dependencies(self, dependency_type):
        for m in self.modules if dependency_type == "modules" else self.scripts:
            depends = m.get("content", {}).get("depends")
            if not depends:
                continue
            dependencies = [depends] if isinstance(depends, str) else depends
            for d in dependencies:
                if d not in self.dependencies:
                    self.dependencies.append(d)
