from verity.recon.engine import ReconEngine


def test_recon_detects_environment():
    snapshot = ReconEngine().inspect()

    assert snapshot.environment.operating_system
    assert snapshot.environment.architecture
    assert snapshot.environment.python_version
    