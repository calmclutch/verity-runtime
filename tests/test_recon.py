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

