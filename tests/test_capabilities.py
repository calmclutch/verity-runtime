from pathlib import Path

from verity.capabilities.filesystem import FilesystemCapability


def test_filesystem_capability():
    capability = FilesystemCapability(
        action="read",
        scope=Path("workspace"),
    )

    assert capability.action == "read"
    assert capability.scope == Path("workspace")