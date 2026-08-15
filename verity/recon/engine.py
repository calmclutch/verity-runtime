import platform
import socket
import shutil
import sys
from pathlib import Path

import psutil

from .snapshot import (
    EnvironmentInfo,
    NetworkInterfaceInfo,
    ProcessInfo,
    ReconSnapshot,
)


class ReconEngine:
    def __init__(self, workspace=None):
        self.workspace = workspace or Path.cwd()

    def inspect(self) -> ReconSnapshot:
        environment = EnvironmentInfo(
            operating_system=platform.system(),
            architecture=platform.machine(),
            python_version=sys.version.split()[0],
        )

        tools = self._discover_tools()
        filesystem = self._discover_filesystem()
        processes = self._discover_processes()
        network_interfaces = self._discover_network_interfaces()

        return ReconSnapshot(
            environment=environment,
            tools=tools,
            filesystem=filesystem,
            processes=processes,
            network_interfaces=network_interfaces,
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

    def _discover_processes(self) -> list[ProcessInfo]:
        processes = []

        for process in psutil.process_iter(["pid", "name"]):
            try:
                info = process.info

                if info["pid"] > 0 and info["name"]:
                    processes.append(
                        ProcessInfo(
                            pid=info["pid"],
                            name=info["name"],
                        )
                    )
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return sorted(processes, key=lambda process: process.pid)

    def _discover_network_interfaces(self) -> list[NetworkInterfaceInfo]:
        interfaces = []

        for name, addresses in psutil.net_if_addrs().items():
            ip_addresses = [
                address.address
                for address in addresses
                if address.family in (socket.AF_INET, socket.AF_INET6)
            ]

            interfaces.append(
                NetworkInterfaceInfo(
                    name=name,
                    addresses=ip_addresses,
                )
            )

        return sorted(interfaces, key=lambda interface: interface.name)