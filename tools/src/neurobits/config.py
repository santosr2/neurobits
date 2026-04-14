"""Configuration handling for Neurobits CLI."""

import os
import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


def get_config_path() -> Path:
    """Return the config file path (~/.config/neurobits/config.toml)."""
    xdg_config = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
    return Path(xdg_config) / "neurobits" / "config.toml"


def load_config() -> dict:
    """Load config from file. Returns empty dict if not found."""
    config_path = get_config_path()
    if not config_path.exists():
        return {}
    with open(config_path, "rb") as f:
        return tomllib.load(f)


def get_site_path() -> Path:
    """
    Resolve the site path from env or config.

    Priority:
    1. NEUROBITS_SITE_PATH env var
    2. site_path in config file
    3. Error if neither set
    """
    env_path = os.environ.get("NEUROBITS_SITE_PATH")
    if env_path:
        return Path(env_path).expanduser().resolve()

    config = load_config()
    config_path = config.get("site_path")
    if config_path:
        return Path(config_path).expanduser().resolve()

    raise RuntimeError(
        "Site path not configured. Set NEUROBITS_SITE_PATH env var or "
        f"add site_path to {get_config_path()}"
    )


def get_editor() -> str:
    """Return the editor command from $EDITOR, defaulting to 'vi'."""
    return os.environ.get("EDITOR", "vi")
