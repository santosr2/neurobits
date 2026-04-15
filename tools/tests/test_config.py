"""Tests for config module."""

import pytest

from neurobits.config import get_config_path, get_editor, get_site_path


def test_get_config_path_default():
    """Config path uses ~/.config by default."""
    path = get_config_path()
    assert path.name == "config.toml"
    assert "neurobits" in str(path)


def test_get_config_path_xdg(monkeypatch, tmp_path):
    """Config path respects XDG_CONFIG_HOME."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    path = get_config_path()
    assert path == tmp_path / "neurobits" / "config.toml"


def test_get_editor_from_env(monkeypatch):
    """Editor comes from $EDITOR."""
    monkeypatch.setenv("EDITOR", "nvim")
    assert get_editor() == "nvim"


def test_get_editor_default(monkeypatch):
    """Editor defaults to vi when $EDITOR not set."""
    monkeypatch.delenv("EDITOR", raising=False)
    assert get_editor() == "vi"


def test_get_site_path_from_env(monkeypatch, tmp_path):
    """Site path from NEUROBITS_SITE_PATH env var."""
    monkeypatch.setenv("NEUROBITS_SITE_PATH", str(tmp_path))
    assert get_site_path() == tmp_path


def test_get_site_path_not_configured(monkeypatch, tmp_path):
    """Error when site path not configured."""
    monkeypatch.delenv("NEUROBITS_SITE_PATH", raising=False)
    # Point config to non-existent file
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "noconfig"))

    with pytest.raises(RuntimeError, match="Site path not configured"):
        get_site_path()
