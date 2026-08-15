from pathlib import Path

from verity.recon.engine import ReconEngine


def test_recon_detects_environment():
    snapshot = ReconEngine().inspect()

    assert snapshot.environment.operating_system
    assert snapshot.environment.architecture
    assert snapshot.environment.python_version


def test_recon_discovers_available_tools():
    snapshot = ReconEngine().inspect()

    assert "python" in snapshot.tools
    assert "git" in snapshot.tools


def test_recon_discovers_workspace_files(tmp_path: Path):
    (tmp_path / "app.py").write_text("print('hello')")
    (tmp_path / "README.md").write_text("# Test")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_app.py").write_text("def test_example(): pass")

    snapshot = ReconEngine(workspace=tmp_path).inspect()

    assert "app.py" in snapshot.filesystem
    assert "README.md" in snapshot.filesystem
    assert "tests/test_app.py" in snapshot.filesystem


def test_recon_discovers_processes():
    snapshot = ReconEngine().inspect()

    assert len(snapshot.processes) > 0

    for process in snapshot.processes:
        assert process.pid > 0
        assert process.name


def test_recon_discovers_network_interfaces():
    snapshot = ReconEngine().inspect()

    assert len(snapshot.network_interfaces) > 0

    for interface in snapshot.network_interfaces:
        assert interface.name