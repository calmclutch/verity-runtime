from pathlib import Path

from pydantic import BaseModel


class FilesystemCapability(BaseModel):
    action: str
    scope: Path