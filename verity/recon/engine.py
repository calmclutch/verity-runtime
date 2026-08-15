import platform
import shutil
import sys
from pathlib import Path

from .snapshot import EnvironmentInfo, ReconSnapshot


class ReconEngine:
    def __init__(self, workspace: Path | None = None):
        self.workspace = workspace or Path.cwd()

    def inspect(self) -> ReconSnapshot:
        environment = EnvironmentInfo(
            operating_system=platform.system(),
            architecture=platform.machine(),
            python_version=sys.version.split()[0],
        )

        tools = self._discover_tools()
        filesystem = self._discover_filesystem()

        return ReconSnapshot(
            environment=environment,
            tools=tools,
            filesystem=filesystem,
        )

    def _discover_tools(self) -> list[str]:
        candidates = [
            "python",
            "git",
            "pytest",
            "docker",
        ]

        return [
            tool
            for tool in candidates
            if shutil.which(tool) is not None
        ]

    def _discover_filesystem(self) -> list[str]:
        if not self.workspace.exists():
            return []

        return sorted(
            path.relative_to(self.workspace).as_posix()
            for path in self.workspace.rglob("*")
             if path.is_file()
        )