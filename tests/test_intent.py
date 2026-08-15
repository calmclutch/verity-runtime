from verity.intent.contract import IntentContract


def test_intent_contract():
    intent = IntentContract(
        objective="Run project tests",
        capabilities=[
            "filesystem.read",
            "process.execute",
        ],
    )

    assert intent.objective == "Run project tests"
    assert "filesystem.read" in intent.capabilities
    assert "process.execute" in intent.capabilities