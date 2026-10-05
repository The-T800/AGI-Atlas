"""Guard against leaking a local identity in public commit metadata."""

import importlib

import pytest
from conftest import REPO


@pytest.fixture
def checks(monkeypatch):
    monkeypatch.syspath_prepend(str(REPO / "scripts"))
    return importlib.import_module("check_public_metadata")


@pytest.mark.parametrize(
    "name,email,committer,valid",
    [
        ("example-user", "123+example-user@users.noreply.github.com", False, True),
        ("example-user", "example-user@users.noreply.github.com", False, True),
        ("example-user", "person@example.org", False, False),
        ("Private Name", "123+example-user@users.noreply.github.com", False, False),
        ("other-user", "123+example-user@users.noreply.github.com", False, False),
        ("example-user", "example-user@users.noreply.github.com.example.org", False, False),
        ("GitHub", "noreply@github.com", True, True),
        ("GitHub", "noreply@github.com", False, False),
        (
            "github-actions[bot]",
            "41898282+github-actions[bot]@users.noreply.github.com",
            True,
            True,
        ),
    ],
)
def test_only_matching_public_github_identities_are_allowed(checks, name, email, committer, valid):
    assert (checks.identity_error(name, email, committer=committer) is None) == valid


@pytest.mark.parametrize(
    "message,valid", [("Publish AGI Atlas\n", True), ("更新页面", False), ("", False)]
)
def test_commit_message_language_policy(checks, message, valid):
    assert (checks.message_error(message) is None) == valid
