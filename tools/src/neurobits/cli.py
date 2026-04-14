"""Main CLI entrypoint for Neurobits."""

import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import click

from neurobits import __version__
from neurobits.config import get_editor, get_site_path


def require_hugo() -> str:
    """Check that hugo is available. Returns the path to hugo."""
    hugo = shutil.which("hugo")
    if not hugo:
        click.echo("Error: hugo not found in PATH", err=True)
        sys.exit(1)
    return hugo


def run_hugo(args: list[str], site_path: Path) -> subprocess.CompletedProcess:
    """Run hugo with the given arguments from the site directory."""
    hugo = require_hugo()
    return subprocess.run([hugo, *args], cwd=site_path, check=False)


@click.group()
@click.version_option(__version__, prog_name="neurobits")
def main():
    """Neurobits CLI - thin wrapper around Hugo for content authoring."""
    pass


@main.command()
@click.argument("section", type=click.Choice(["blog", "note", "project"]))
@click.option("--title", "-t", required=True, help="Title for the new content")
@click.option("--draft/--no-draft", default=True, help="Create as draft (default: true)")
def new(section: str, title: str, draft: bool):
    """Create new content (blog, note, or project)."""
    site_path = get_site_path()

    # Map section to content path
    section_map = {
        "blog": "blog",
        "note": "notes",
        "project": "projects",
    }
    content_section = section_map[section]

    # Generate filename from title
    date_prefix = datetime.now().strftime("%Y-%m")
    slug = title.lower().replace(" ", "-").replace("_", "-")
    # Remove non-alphanumeric chars except hyphens
    slug = "".join(c for c in slug if c.isalnum() or c == "-")
    filename = f"{date_prefix}-{slug}.md"

    content_path = f"{content_section}/{filename}"

    # Run hugo new
    result = run_hugo(["new", "content", content_path], site_path)
    if result.returncode != 0:
        click.echo(f"Error: hugo new failed with code {result.returncode}", err=True)
        sys.exit(result.returncode)

    full_path = site_path / "content" / content_path
    click.echo(f"Created: {full_path}")

    # If not draft, update the frontmatter
    if not draft and full_path.exists():
        content = full_path.read_text()
        content = content.replace("draft: true", "draft: false", 1)
        full_path.write_text(content)

    # Open in editor
    editor = get_editor()
    click.echo(f"Opening in {editor}...")
    os.execlp(editor, editor, str(full_path))


@main.command()
@click.argument("path", type=click.Path(exists=True))
def open(path: str):
    """Open an existing content file in $EDITOR."""
    editor = get_editor()
    os.execlp(editor, editor, path)


@main.command()
@click.option("--drafts/--no-drafts", "-D", default=True, help="Include drafts")
@click.option("--port", "-p", default=1313, help="Port for dev server")
def preview(drafts: bool, port: int):
    """Start Hugo dev server for local preview."""
    site_path = get_site_path()
    args = ["server", "--port", str(port)]
    if drafts:
        args.append("--buildDrafts")

    click.echo(f"Starting preview server at http://localhost:{port}")
    result = run_hugo(args, site_path)
    sys.exit(result.returncode)


@main.command()
@click.option("--minify/--no-minify", default=True, help="Minify output")
@click.option("--clean/--no-clean", default=True, help="Clean destination before build")
def build(minify: bool, clean: bool):
    """Build the site for production."""
    site_path = get_site_path()
    args = []
    if minify:
        args.append("--minify")
    if clean:
        args.append("--cleanDestinationDir")

    click.echo("Building site...")
    result = run_hugo(args, site_path)
    if result.returncode == 0:
        click.echo("Build complete.")
    sys.exit(result.returncode)


@main.command()
@click.option("--push", is_flag=True, help="Actually push changes (default: dry run)")
def publish(push: bool):
    """Validate, build, and optionally push changes."""
    site_path = get_site_path()

    # Check for uncommitted changes
    git_status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=site_path,
        capture_output=True,
        text=True,
    )
    if git_status.returncode != 0:
        click.echo("Error: git status failed", err=True)
        sys.exit(1)

    # Build first
    click.echo("Building site...")
    result = run_hugo(["--minify", "--cleanDestinationDir"], site_path)
    if result.returncode != 0:
        click.echo("Error: build failed", err=True)
        sys.exit(result.returncode)

    click.echo("Build successful.")

    if not push:
        click.echo("Dry run complete. Use --push to actually push changes.")
        return

    # Push changes
    click.echo("Pushing changes...")
    push_result = subprocess.run(["git", "push"], cwd=site_path)
    sys.exit(push_result.returncode)


@main.command()
def doctor():
    """Check dependencies and configuration."""
    issues = []

    # Check hugo
    hugo = shutil.which("hugo")
    if hugo:
        result = subprocess.run([hugo, "version"], capture_output=True, text=True)
        version = result.stdout.strip().split("\n")[0] if result.returncode == 0 else "unknown"
        click.echo(f"hugo: {version}")
    else:
        click.echo("hugo: NOT FOUND", err=True)
        issues.append("hugo not found in PATH")

    # Check git
    git = shutil.which("git")
    if git:
        result = subprocess.run([git, "--version"], capture_output=True, text=True)
        version = result.stdout.strip() if result.returncode == 0 else "unknown"
        click.echo(f"git: {version}")
    else:
        click.echo("git: NOT FOUND", err=True)
        issues.append("git not found in PATH")

    # Check editor
    editor = os.environ.get("EDITOR")
    if editor:
        click.echo(f"$EDITOR: {editor}")
    else:
        click.echo("$EDITOR: not set (will use 'vi')")

    # Check site path
    try:
        site_path = get_site_path()
        if site_path.exists():
            click.echo(f"site_path: {site_path}")
            hugo_toml = site_path / "hugo.toml"
            if hugo_toml.exists():
                click.echo("  hugo.toml: found")
            else:
                click.echo("  hugo.toml: NOT FOUND", err=True)
                issues.append(f"hugo.toml not found in {site_path}")
        else:
            click.echo(f"site_path: {site_path} (NOT FOUND)", err=True)
            issues.append(f"site_path does not exist: {site_path}")
    except RuntimeError as e:
        click.echo(f"site_path: NOT CONFIGURED", err=True)
        issues.append(str(e))

    # Summary
    click.echo()
    if issues:
        click.echo(f"Found {len(issues)} issue(s):", err=True)
        for issue in issues:
            click.echo(f"  - {issue}", err=True)
        sys.exit(1)
    else:
        click.echo("All checks passed.")


if __name__ == "__main__":
    main()
