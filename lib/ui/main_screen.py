from typing import Any

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

from lib.core.context import Context
from lib.core.engine import Engine
from lib.core.resources import resource_path
from lib.models.package import Package


class MainScreen(Screen[Any]):
    CSS_PATH = resource_path("ui/assets/main.tcss")

    def __init__(
        self, name: str | None = None, id: str | None = None, classes: str | None = None
    ) -> None:
        self.selected_packages = []
        super().__init__(name, id, classes)

    @property
    def app(self) -> Any:
        return super().app  # type: ignore

    @property
    def ctx(self) -> Context:
        return self.app.ctx  # type: ignore[attr-defined]

    @property
    def engine(self) -> Engine:
        return self.app.engine  # type: ignore[attr-defined]

    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane(title="Packages"):
                with Static(id="grid-container"):
                    with Static(classes="package-pane"):
                        packages = self._construct_widgets()
                        yield SelectionList[int](*packages, id="package-select")

                    with Vertical(id="actions-pane"):
                        yield Button("Select all")
                        yield Button("Deselect all")
                        yield Button("Reset")
                        yield Button("Next->", id="next-btn-packages")

            with TabPane(title="Overview", id="install"):
                with Static(id="grid-container"):
                    with Static(classes="package-pane"):
                        yield Markdown(id="overviewMarkdown")

                    with Vertical(id="actions-pane"):
                        yield Button("Install", id="install-btn")
                        yield Button("<-Back", id="back-btn-install")

        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#package-select").border_title = "Choose modules to install:"
        self.query_one(Markdown).border_title = "Selected modules and scripts:"

    @on(Mount)
    @on(SelectionList.SelectedChanged)
    def update_selected_view(
        self, event: Mount | SelectionList.SelectedChanged[Any]
    ) -> None:
        package_select = self.query_one("#package-select", SelectionList)  # type: ignore

        def _selected_names(sel: SelectionList[int]) -> list[str]:
            return [str(v) for v in (sel.selected or [])]

        self.selected_packages = _selected_names(package_select)  # type: ignore
        self.query_one(Markdown).update(self._construct_markdown())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "next-btn-packages":
                self.query_one("#install-btn").focus()
            case "next-btn-scripts":
                self.query_one("#install-btn").focus()
            case "back-btn-install":
                self.query_one("#next-btn-packages").focus()
            case "install-btn":
                self.app.exit(str(event.button))
            case _:
                pass

    def _construct_widgets(
        self,
    ) -> tuple[tuple[str, int, bool], ...]:
        widgets: list[tuple[str, int, bool]] = []
        selected_profile = self.ctx.selected_profile
        selected_packages: list[Package] = (
            selected_profile.packages[self.ctx.os] if selected_profile else []
        )
        for idx, p in enumerate(self.ctx.available_packages.values()):
            if self.ctx.os not in p.supported_os:
                continue
            else:
                widgets.append((p.name, idx, p in selected_packages))
        return tuple(widgets)

    def _construct_markdown(self) -> str:
        # packages_md = "\n".join(f"- {m}" for  in self.selected_modules) or "None"
        # scripts_md = "\n".join(f"- {s}" for s in self.selected_scripts) or "None"
        # deps_md = "\n".join(f"- {d}" for d in self.dependencies) or "None"

        # return "\n".join(
        #     [
        #         "## Modules:",
        #         modules_md,
        #         "",
        #         "## Scripts:",
        #         scripts_md,
        #         "",
        #         "## Dependencies:",
        #         deps_md,
        #     ]
        # )
        return str(self.ctx.selected_profile.id) if self.ctx.selected_profile else ""
