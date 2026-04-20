"""Tests for CLI commands."""

import pytest
from click.testing import CliRunner

from neurobits.cli import main


@pytest.fixture
def runner():
    return CliRunner()


def test_version(runner):
    """--version shows version."""
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "neurobits" in result.output
    assert "0.1.0" in result.output


def test_doctor_hugo_not_found(runner, monkeypatch):
    """doctor reports when hugo not found."""
    monkeypatch.setattr(
        "shutil.which", lambda cmd: None if cmd == "hugo" else "/usr/bin/git"
    )
    monkeypatch.delenv("NEUROBITS_SITE_PATH", raising=False)
    monkeypatch.setenv("XDG_CONFIG_HOME", "/nonexistent")

    result = runner.invoke(main, ["doctor"])
    assert result.exit_code == 1
    assert "hugo: NOT FOUND" in result.output


def test_doctor_all_ok(runner, monkeypatch, tmp_path):
    """doctor passes when everything configured."""
    site_path = tmp_path / "site"
    site_path.mkdir()
    (site_path / "hugo.toml").touch()

    monkeypatch.setenv("NEUROBITS_SITE_PATH", str(site_path))
    monkeypatch.setenv("EDITOR", "vim")

    def mock_which(cmd):
        return f"/usr/bin/{cmd}"

    def mock_run(args, **kwargs):
        class Result:
            returncode = 0
            stdout = f"{args[0]} version 1.0"

        return Result()

    monkeypatch.setattr("shutil.which", mock_which)
    monkeypatch.setattr("subprocess.run", mock_run)

    result = runner.invoke(main, ["doctor"])
    assert result.exit_code == 0
    assert "All checks passed" in result.output


def test_build_calls_hugo(runner, monkeypatch, tmp_path):
    """build invokes hugo with correct args."""
    site_path = tmp_path / "site"
    site_path.mkdir()

    monkeypatch.setenv("NEUROBITS_SITE_PATH", str(site_path))
    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/hugo")

    called_with = []

    def mock_run(args, **kwargs):
        called_with.append(args)

        class Result:
            returncode = 0

        return Result()

    monkeypatch.setattr("subprocess.run", mock_run)

    result = runner.invoke(main, ["build"])
    assert result.exit_code == 0
    assert any(
        "--minify" in args and "--cleanDestinationDir" in args for args in called_with
    )


def test_preview_starts_server(runner, monkeypatch, tmp_path):
    """preview starts hugo server."""
    site_path = tmp_path / "site"
    site_path.mkdir()

    monkeypatch.setenv("NEUROBITS_SITE_PATH", str(site_path))
    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/hugo")

    called_with = []

    def mock_run(args, **kwargs):
        called_with.append(args)

        class Result:
            returncode = 0

        return Result()

    monkeypatch.setattr("subprocess.run", mock_run)

    result = runner.invoke(main, ["preview"])
    assert result.exit_code == 0
    assert any("server" in args for args in called_with)


def test_new_post_default_type(runner, monkeypatch, tmp_path):
    """new post creates note type by default."""
    site_path = tmp_path / "site"
    content_path = site_path / "content" / "posts"
    content_path.mkdir(parents=True)

    monkeypatch.setenv("NEUROBITS_SITE_PATH", str(site_path))
    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/hugo")

    def mock_run(args, **kwargs):
        # Simulate hugo new creating the file
        if "new" in args:
            filepath = content_path / args[-1].split("/")[-1]
            filepath.write_text("---\npostType: note\ndraft: true\n---\n")

        class Result:
            returncode = 0

        return Result()

    monkeypatch.setattr("subprocess.run", mock_run)
    # Prevent execlp from replacing the process
    monkeypatch.setattr("os.execlp", lambda *args: None)

    result = runner.invoke(main, ["new", "post", "-t", "Test Post"])
    assert result.exit_code == 0
    assert "Created:" in result.output
    assert "posts" in result.output


def test_new_post_blog_type(runner, monkeypatch, tmp_path):
    """new post --type blog sets postType to blog."""
    site_path = tmp_path / "site"
    content_path = site_path / "content" / "posts"
    content_path.mkdir(parents=True)

    monkeypatch.setenv("NEUROBITS_SITE_PATH", str(site_path))
    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/hugo")

    created_file = None

    def mock_run(args, **kwargs):
        nonlocal created_file
        if "new" in args:
            filepath = content_path / args[-1].split("/")[-1]
            filepath.write_text("---\npostType: note\ndraft: true\n---\n")
            created_file = filepath

        class Result:
            returncode = 0

        return Result()

    monkeypatch.setattr("subprocess.run", mock_run)
    monkeypatch.setattr("os.execlp", lambda *args: None)

    result = runner.invoke(main, ["new", "post", "-t", "Blog Post", "--type", "blog"])
    assert result.exit_code == 0

    # Verify postType was updated to blog
    content = created_file.read_text()
    assert "postType: blog" in content


def test_new_rejects_old_sections(runner):
    """new rejects old blog/note section names."""
    result = runner.invoke(main, ["new", "blog", "-t", "Test"])
    assert result.exit_code != 0
    assert "Invalid value" in result.output or "blog" in result.output

    result = runner.invoke(main, ["new", "note", "-t", "Test"])
    assert result.exit_code != 0
    assert "Invalid value" in result.output or "note" in result.output
