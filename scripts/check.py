#!/usr/bin/env python3
"""Validate the KSI Codex harness source and installed state."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_NAMES: list[str] = []
CUSTOM_AGENTS = {
    "explorer.toml": {
        "name": "explorer",
        "model": "gpt-5.4-mini",
        "model_reasoning_effort": "low",
    },
}
EXCLUDED_DEFAULT_PLUGINS = {
    "gmail@openai-curated",
    "google-calendar@openai-curated",
    "canva@openai-curated",
    "figma@openai-curated",
    "notion@openai-curated",
    "linear@openai-curated",
}
EXPECTED_ENABLED_PLUGINS = {
    "github@openai-curated",
}
REQUIRED_AGENTS_FRAGMENTS = [
    "# KSI Codex Global Routing",
    "Use `/goal` and `/plan` before non-trivial",
    "Use `explorer` only for bounded, read-only codebase discovery",
    "Use the built-in `worker` for one clearly scoped implementation or testing task",
    "Do not add standing specialized agents by default",
    "Use Context7 for version-specific framework, library, or API behavior",
    "Use Local Codex only for an explicitly requested design workflow",
]


class Reporter:
    def __init__(self) -> None:
        self.passed = 0
        self.warnings: list[str] = []
        self.failures: list[str] = []
        self.infos: list[str] = []

    def pass_(self, label: str) -> None:
        self.passed += 1
        print(f"PASS {label}")

    def warn(self, label: str) -> None:
        self.warnings.append(label)
        print(f"WARN {label}")

    def fail(self, label: str) -> None:
        self.failures.append(label)
        print(f"FAIL {label}")

    def info(self, label: str) -> None:
        self.infos.append(label)
        print(f"INFO {label}")

    def expect(self, condition: bool, label: str) -> None:
        if condition:
            self.pass_(label)
        else:
            self.fail(label)

    def summary(self) -> int:
        print()
        print(
            f"Summary: {self.passed} passed, "
            f"{len(self.warnings)} warnings, {len(self.failures)} failures"
        )
        if self.warnings:
            print("Warnings:")
            for warning in self.warnings:
                print(f"- {warning}")
        if self.failures:
            print("Failures:")
            for failure in self.failures:
                print(f"- {failure}")
            return 1
        return 0


def frontmatter_fields(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields


def check_source(reporter: Reporter) -> None:
    reporter.expect((REPO_ROOT / "README.md").exists(), "README.md exists")
    reporter.expect((REPO_ROOT / "LICENSE").exists(), "LICENSE exists")
    reporter.expect((REPO_ROOT / "install.sh").exists(), "install.sh exists")
    reporter.expect((REPO_ROOT / "scripts" / "apply.py").exists(), "apply.py exists")
    reporter.expect((REPO_ROOT / "scripts" / "check.py").exists(), "check.py exists")
    reporter.expect((REPO_ROOT / "scripts" / "browser.py").exists(), "browser.py exists")

    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    reporter.expect("MIT License" in license_text, "MIT license text")

    source_files = [path for path in REPO_ROOT.rglob("*") if path.is_file() and ".git" not in path.parts]
    forbidden_names = {"auth.json", "credentials.json", ".env", "cookies.json"}
    forbidden_files = [path for path in source_files if path.name in forbidden_names]
    reporter.expect(not forbidden_files, "repository excludes known credential files")
    token_patterns = [
        re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
        re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
        re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
        re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    ]
    suspected_secret_files: list[Path] = []
    for path in source_files:
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if any(pattern.search(text) for pattern in token_patterns):
            suspected_secret_files.append(path)
    reporter.expect(not suspected_secret_files, "repository contains no recognized secret material")

    agents = (REPO_ROOT / "codex" / "AGENTS.md").read_text(encoding="utf-8")
    for fragment in REQUIRED_AGENTS_FRAGMENTS:
        reporter.expect(fragment in agents, f"global AGENTS.md contains {fragment!r}")
    if len(agents.encode("utf-8")) > 12_000:
        reporter.warn("global AGENTS.md is larger than 12KB; keep it lean")
    else:
        reporter.pass_("global AGENTS.md size is lean")

    portable_config = REPO_ROOT / "codex" / "config.portable.toml"
    reporter.expect(portable_config.exists(), "portable config exists")
    if portable_config.exists():
        config_text = portable_config.read_text(encoding="utf-8")
        config = read_toml(portable_config, reporter)
        reporter.expect(config.get("model") == "gpt-5.6-sol", "portable config model")
        reporter.expect(
            config.get("sandbox_mode") == "danger-full-access",
            "portable config sandbox mode",
        )
        reporter.expect(
            config.get("approval_policy") == "never",
            "portable config approval policy",
        )
        reporter.expect("/home/" not in config_text, "portable config has no Linux home path")
        reporter.expect("C:\\\\Users\\\\" not in config_text, "portable config has no Windows home path")
        for excluded in ["projects", "desktop", "apps"]:
            reporter.expect(excluded not in config, f"portable config excludes [{excluded}]")
        mcp_servers = config.get("mcp_servers", {})
        reporter.expect(
            isinstance(mcp_servers, dict) and set(mcp_servers) == {"context7"},
            "portable config includes only Context7 MCP",
        )

    for name in SKILL_NAMES:
        path = REPO_ROOT / "skills" / name / "SKILL.md"
        reporter.expect(path.exists(), f"{name} SKILL.md exists")
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        fields = frontmatter_fields(text)
        reporter.expect(fields.get("name") == name, f"{name} frontmatter name")
        reporter.expect(bool(fields.get("description")), f"{name} frontmatter description")
        if len(text.splitlines()) > 220:
            reporter.warn(f"{name} SKILL.md is long; consider references/")
        else:
            reporter.pass_(f"{name} SKILL.md length is reasonable")

    for filename, expected in CUSTOM_AGENTS.items():
        path = REPO_ROOT / "codex" / "agents" / filename
        reporter.expect(path.exists(), f"custom agent source {filename} exists")
        if not path.exists():
            continue
        data = read_toml(path, reporter)
        reporter.expect(data.get("name") == expected["name"], f"{filename} agent name")
        reporter.expect(data.get("model") == expected["model"], f"{filename} model")
        reporter.expect(
            data.get("model_reasoning_effort") == expected["model_reasoning_effort"],
            f"{filename} reasoning effort",
        )
        reporter.expect(
            data.get("sandbox_mode") == "read-only",
            f"{filename} sandbox is read-only",
        )

    for doc in [
        "autonomy.md",
        "browser-automation.md",
        "philosophy.md",
        "workflow.md",
        "mcp.md",
        "plugins.md",
        "lsp.md",
        "vibe-intake.md",
        "memory.md",
        "model-tiering.md",
        "external-integrations.md",
        "install.md",
        "decisions.md",
    ]:
        reporter.expect((REPO_ROOT / "docs" / doc).exists(), f"docs/{doc} exists")

    reporter.expect(
        (REPO_ROOT / "presets" / "strict" / "AGENTS.append.md").exists(),
        "strict preset append exists",
    )
    reporter.expect(
        (REPO_ROOT / "presets" / "power-user" / "AGENTS.append.md").exists(),
        "power-user preset append exists",
    )


def check_installed(reporter: Reporter, home: Path) -> None:
    codex_agents = home / ".codex" / "AGENTS.md"
    if codex_agents.exists():
        text = codex_agents.read_text(encoding="utf-8", errors="replace")
        source_text = (REPO_ROOT / "codex" / "AGENTS.md").read_text(encoding="utf-8")
        if text == source_text:
            reporter.pass_("installed ~/.codex/AGENTS.md matches portable source")
        else:
            reporter.warn("~/.codex/AGENTS.md differs from portable source")
    else:
        reporter.warn("~/.codex/AGENTS.md is not installed")

    skills_root = home / ".agents" / "skills"
    for name in SKILL_NAMES:
        path = skills_root / name / "SKILL.md"
        if path.exists():
            reporter.pass_(f"installed skill {name}")
        else:
            reporter.warn(f"skill {name} is not installed under ~/.agents/skills")

    rules = home / ".codex" / "rules" / "ksi-default.rules"
    if rules.exists():
        source_rules = REPO_ROOT / "codex" / "rules" / "ksi-default.rules"
        if rules.read_bytes() == source_rules.read_bytes():
            reporter.pass_("installed ksi-default.rules matches portable source")
        else:
            reporter.warn("installed ksi-default.rules differs from portable source")
    else:
        reporter.warn("ksi-default.rules is not installed")

    for filename, expected in CUSTOM_AGENTS.items():
        agent = home / ".codex" / "agents" / filename
        if not agent.exists():
            reporter.warn(f"{expected['name']} custom agent is not installed")
            continue
        reporter.pass_(f"installed {expected['name']} custom agent")
        data = read_toml(agent, reporter)
        source_agent = REPO_ROOT / "codex" / "agents" / filename
        if agent.read_bytes() == source_agent.read_bytes():
            reporter.pass_(f"installed {expected['name']} matches portable source")
        else:
            reporter.warn(f"installed {expected['name']} differs from portable source")
        if data.get("sandbox_mode") == "read-only":
            reporter.pass_(f"installed {expected['name']} remains read-only")
        else:
            reporter.warn(f"installed {expected['name']} is not read-only")

    portable_path = REPO_ROOT / "codex" / "config.portable.toml"
    expected_config = read_toml(portable_path, reporter)
    profile_path = home / ".codex" / "ksi.config.toml"
    default_path = home / ".codex" / "config.toml"
    if profile_path.exists() and profile_path.read_bytes() == portable_path.read_bytes():
        reporter.pass_("installed ksi config profile matches portable source")
    elif default_path.exists():
        actual_config = read_toml(default_path, reporter)
        if portable_config_matches(actual_config, expected_config):
            reporter.pass_("default config contains the portable KSI baseline")
        else:
            reporter.warn("default config does not fully match the portable KSI baseline")
    else:
        reporter.warn("no installed portable config profile or default config found")


def check_plugins(reporter: Reporter, home: Path) -> None:
    config_path = home / ".codex" / "config.toml"
    if not config_path.exists():
        reporter.warn("~/.codex/config.toml not found; skipped plugin check")
        return

    data = read_toml(config_path, reporter)
    plugins = data.get("plugins", {})
    if not isinstance(plugins, dict):
        reporter.info("no Codex plugins configured")
        return

    enabled = sorted(
        name
        for name, config in plugins.items()
        if isinstance(config, dict) and config.get("enabled") is True
    )
    disabled = sorted(
        name
        for name, config in plugins.items()
        if isinstance(config, dict) and config.get("enabled") is False
    )

    if enabled:
        reporter.info(f"enabled Codex plugins: {', '.join(enabled)}")
    else:
        reporter.info("no enabled Codex plugins")
    if disabled:
        reporter.info(f"disabled Codex plugins: {', '.join(disabled)}")

    for name in enabled:
        if name in EXPECTED_ENABLED_PLUGINS:
            reporter.pass_(f"recommended plugin enabled: {name}")
        if name in EXCLUDED_DEFAULT_PLUGINS:
            reporter.warn(f"v1-excluded plugin is enabled: {name}")

    for name in EXCLUDED_DEFAULT_PLUGINS:
        if name in plugins and name not in enabled:
            reporter.pass_(f"v1-excluded plugin disabled: {name}")


def check_memory(reporter: Reporter, home: Path) -> None:
    config_path = home / ".codex" / "config.toml"
    memories_dir = home / ".codex" / "memories"
    memory_db = home / ".codex" / "memories_1.sqlite"

    if not config_path.exists():
        reporter.warn("~/.codex/config.toml not found; skipped memory check")
        return

    data = read_toml(config_path, reporter)
    features = data.get("features", {})
    memories = data.get("memories", {})
    enabled = isinstance(features, dict) and features.get("memories") is True

    if enabled:
        reporter.info("Codex memories feature enabled")
    else:
        reporter.info("Codex memories feature disabled")
        if memories_dir.exists() or memory_db.exists():
            reporter.warn("memory state exists but memories feature is disabled")
        return

    if not isinstance(memories, dict):
        reporter.warn("memories feature enabled but [memories] config is missing")
        return

    use_memories = memories.get("use_memories")
    generate_memories = memories.get("generate_memories")
    disable_external = memories.get("disable_on_external_context")
    min_rate = memories.get("min_rate_limit_remaining_percent")

    reporter.info(f"memories.use_memories={use_memories!r}")
    reporter.info(f"memories.generate_memories={generate_memories!r}")
    reporter.info(f"memories.disable_on_external_context={disable_external!r}")
    reporter.info(f"memories.min_rate_limit_remaining_percent={min_rate!r}")

    if use_memories is True:
        reporter.pass_("memories.use_memories enabled")
    else:
        reporter.warn("memories.use_memories is not explicitly true")

    if generate_memories is True:
        reporter.pass_("memories.generate_memories enabled")
    else:
        reporter.warn("memories.generate_memories is not explicitly true")

    if disable_external is True:
        reporter.pass_("memories.disable_on_external_context enabled")
    else:
        reporter.warn("memories.disable_on_external_context should be true for KSI")

    if isinstance(min_rate, int) and min_rate >= 10:
        reporter.pass_("memories.min_rate_limit_remaining_percent set")
    else:
        reporter.warn("memories.min_rate_limit_remaining_percent should be an integer >= 10")


def check_browser_tools(reporter: Reporter, home: Path) -> None:
    chromium = first_available(
        ["chromium", "chromium-browser", "google-chrome", "google-chrome-stable"]
    )
    if chromium:
        reporter.pass_(f"Chromium browser found: {chromium}")
    else:
        reporter.warn("Chromium browser not found on PATH")

    playwright_ok, playwright_version = run_command(["npx", "playwright", "--version"])
    if playwright_ok:
        reporter.pass_(f"Playwright CLI available: {playwright_version}")
    else:
        reporter.warn("npx playwright --version failed")

    chromium_cache = home / ".cache" / "ms-playwright"
    if chromium_cache.exists() and any(
        path.name.startswith("chromium-") for path in chromium_cache.iterdir()
    ):
        reporter.pass_("Playwright Chromium cache found")
    else:
        reporter.warn("Playwright Chromium cache not found")

    for binary, label in [
        ("xdotool", "xdotool visible-window automation"),
        ("wmctrl", "wmctrl window discovery"),
        ("import", "ImageMagick import screenshot tool"),
        ("convert", "ImageMagick convert tool"),
        ("xclip", "xclip clipboard handoff"),
    ]:
        path = shutil.which(binary)
        if path:
            reporter.pass_(f"{label} found: {path}")
        else:
            reporter.warn(f"{label} not found on PATH")

    helper = REPO_ROOT / "scripts" / "browser.py"
    helper_ok, helper_output = run_command([sys.executable, str(helper), "check"])
    if helper_ok:
        reporter.pass_("browser.py check passed")
    else:
        reporter.warn(f"browser.py check failed: {first_line(helper_output)}")


def check_mcp(reporter: Reporter) -> None:
    try:
        result = subprocess.run(
            ["codex", "mcp", "list"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=20,
            check=False,
        )
    except FileNotFoundError:
        reporter.warn("codex CLI not found; skipped MCP check")
        return
    except subprocess.TimeoutExpired:
        reporter.warn("codex mcp list timed out")
        return

    output = result.stdout.strip()
    if result.returncode != 0:
        reporter.warn(f"codex mcp list failed: {first_line(output)}")
        return
    if "No MCP servers configured" in output or not output:
        reporter.info("no MCP servers configured")
        return

    reporter.pass_("codex mcp list succeeded")
    lowered = output.lower()
    if "supabase" in lowered:
        if "read_only=true" in output or "read-only" in lowered:
            reporter.pass_("Supabase MCP appears read-only")
        else:
            reporter.warn("Supabase MCP found; verify read_only=true for normal use")
        if "project_ref=" in output or "project-ref" in lowered:
            reporter.pass_("Supabase MCP appears project-scoped")
        else:
            reporter.warn("Supabase MCP found; verify project_ref scoping")
    if re.search(r"\bprod(uction)?\b", lowered):
        reporter.warn("MCP config mentions production; treat as strict-mode work")


def first_line(text: str) -> str:
    return text.splitlines()[0] if text.splitlines() else ""


def first_available(commands: Iterable[str]) -> str | None:
    for command in commands:
        path = shutil.which(command)
        if path:
            return path
    return None


def run_command(command: list[str], *, timeout: int = 20) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            command,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError:
        return False, ""
    except subprocess.TimeoutExpired:
        return False, "timed out"
    return result.returncode == 0, result.stdout.strip()


def read_toml(path: Path, reporter: Reporter) -> dict:
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        reporter.fail(f"TOML parse failed for {path}: {exc}")
        return {}


def portable_config_matches(actual: dict, expected: dict) -> bool:
    scalar_keys = [
        "model",
        "model_reasoning_effort",
        "personality",
        "plan_mode_reasoning_effort",
        "approvals_reviewer",
        "approval_policy",
        "sandbox_mode",
        "web_search",
    ]
    if any(actual.get(key) != expected.get(key) for key in scalar_keys):
        return False

    for section in ["agents", "plugins", "features", "memories"]:
        if actual.get(section) != expected.get(section):
            return False

    actual_context7 = actual.get("mcp_servers", {}).get("context7", {})
    expected_context7 = expected.get("mcp_servers", {}).get("context7", {})
    if Path(str(actual_context7.get("command", ""))).name != "npx":
        return False
    return all(
        actual_context7.get(key) == expected_context7.get(key)
        for key in ["args", "startup_timeout_ms"]
    )


def check_project_tooling(reporter: Reporter, project: Path) -> None:
    project = project.expanduser().resolve()
    if not project.exists():
        reporter.warn(f"project path does not exist: {project}")
        return
    if not project.is_dir():
        reporter.warn(f"project path is not a directory: {project}")
        return

    reporter.info(f"checking project tooling: {project}")

    package_json = project / "package.json"
    if package_json.exists():
        reporter.info("Node/JavaScript project signal: package.json")
        scripts = read_package_scripts(package_json, reporter)
        for name in ["dev", "start", "typecheck", "lint", "test", "test:e2e", "e2e"]:
            if name in scripts:
                reporter.info(f"package.json script found: {name} -> {scripts[name]}")
        if (project / "tsconfig.json").exists() and "typecheck" not in scripts:
            reporter.warn("tsconfig.json detected but package.json has no typecheck script")
        if not any(name in scripts for name in ["lint", "test", "typecheck"]):
            reporter.warn("package.json detected but no lint/test/typecheck scripts found")

    file_signals = {
        "tsconfig.json": "TypeScript config",
        "eslint.config.js": "ESLint flat config",
        ".eslintrc": "ESLint config",
        ".eslintrc.json": "ESLint config",
        "vitest.config.ts": "Vitest config",
        "vitest.config.js": "Vitest config",
        "playwright.config.ts": "Playwright config",
        "playwright.config.js": "Playwright config",
        "cypress.config.ts": "Cypress config",
        "cypress.config.js": "Cypress config",
        "pyproject.toml": "Python project config",
        "pyrightconfig.json": "Pyright config",
        "mypy.ini": "mypy config",
        "ruff.toml": "Ruff config",
        "Cargo.toml": "Rust project config",
        "go.mod": "Go module config",
        "compile_commands.json": "C/C++ compile commands",
    }
    for filename, label in file_signals.items():
        if (project / filename).exists():
            reporter.info(f"{label} detected: {filename}")

    binaries = {
        "typescript-language-server": "TypeScript language server",
        "tsserver": "TypeScript server",
        "vscode-eslint-language-server": "ESLint language server",
        "pyright-langserver": "Pyright language server",
        "pyright": "Pyright",
        "ruff": "Ruff",
        "ruff-lsp": "Ruff LSP",
        "mypy": "mypy",
        "rust-analyzer": "rust-analyzer",
        "gopls": "gopls",
        "clangd": "clangd",
        "jdtls": "Java language server",
    }
    found_any_binary = False
    for binary, label in binaries.items():
        if shutil.which(binary):
            found_any_binary = True
            reporter.info(f"{label} binary found on PATH: {binary}")
    if not found_any_binary:
        reporter.info("no common language-server/typecheck binaries found on PATH")


def read_package_scripts(package_json: Path, reporter: Reporter) -> dict[str, str]:
    try:
        data = json.loads(package_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        reporter.warn(f"package.json parse failed: {exc}")
        return {}
    scripts = data.get("scripts", {})
    if not isinstance(scripts, dict):
        reporter.warn("package.json scripts field is not an object")
        return {}
    return {str(key): str(value) for key, value in scripts.items()}


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check KSI Codex harness.")
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--source-only", action="store_true")
    parser.add_argument("--skip-mcp", action="store_true")
    parser.add_argument("--skip-browser", action="store_true")
    parser.add_argument(
        "--project",
        type=Path,
        help="Optional project path to inspect for existing typecheck/lint/test/LSP tooling.",
    )
    return parser.parse_args(list(argv))


def main(argv: Iterable[str]) -> int:
    args = parse_args(argv)
    reporter = Reporter()
    check_source(reporter)
    if not args.source_only:
        home = args.home.expanduser()
        check_installed(reporter, home)
        check_plugins(reporter, home)
        check_memory(reporter, home)
        if not args.skip_browser:
            check_browser_tools(reporter, home)
    if not args.skip_mcp:
        check_mcp(reporter)
    if args.project:
        check_project_tooling(reporter, args.project)
    return reporter.summary()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
