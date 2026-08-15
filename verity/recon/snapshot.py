from pydantic import BaseModel, Field


class EnvironmentInfo(BaseModel):
    operating_system: str
    architecture: str
    python_version: str


class ProcessInfo(BaseModel):
    pid: int
    name: str

class NetworkInterfaceInfo(BaseModel):
    name: str
    addresses: list[str] = Field(default_factory=list)


class ReconSnapshot(BaseModel):
    environment: EnvironmentInfo
    tools: list[str] = Field(default_factory=list)
    filesystem: list[str] = Field(default_factory=list)
    processes: list[ProcessInfo] = Field(default_factory=list)
    network_interfaces: list[NetworkInterfaceInfo] = Field(default_factory=list)