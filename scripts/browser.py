#!/usr/bin/env python3
"""KSI Chromium session helper.

This script standardizes visible Chromium sessions for login handoff and
post-login Playwright/browser verification.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_PORT = 9222
PROFILE_ROOT = Path.home() / ".cache" / "ksi-browser"


def find_chromium() -> str | None:
    for binary in ["chromium", "chromium-browser", "google-chrome", "google-chrome-stable"]:
        path = shutil.which(binary)
        if path:
            return path
    return None


def sanitize_profile(name: str) -> str:
    value = re.sub(r"[^A-Za-z0-9_.-]+", "-", name.strip())
    value = value.strip(".-")
    if not value:
        raise SystemExit("profile name must contain at least one safe character")
    return value


def run_quiet(command: list[str], *, timeout: int = 20) -> tuple[int, str]:
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
        return 127, ""
    except subprocess.TimeoutExpired:
        return 124, ""
    return result.returncode, result.stdout.strip()


def check_command(label: str, commands: list[str]) -> bool:
    for command in commands:
        path = shutil.which(command)
        if path:
            print(f"PASS {label}: {command} -> {path}")
            return True
    print(f"WARN {label}: missing ({', '.join(commands)})")
    return False


def check_playwright() -> bool:
    code, output = run_quiet(["npx", "playwright", "--version"])
    if code == 0:
        print(f"PASS playwright: {output}")
        return True
    print("WARN playwright: npx playwright --version failed")
    return False


def check_cached_chromium() -> bool:
    root = Path.home() / ".cache" / "ms-playwright"
    if not root.exists():
        print(f"WARN playwright chromium cache: missing {root}")
        return False
    matches = sorted(path.name for path in root.iterdir() if path.name.startswith("chromium-"))
    if matches:
        print(f"PASS playwright chromium cache: {', '.join(matches[:3])}")
        return True
    print(f"WARN playwright chromium cache: no chromium-* directory under {root}")
    return False


def command_check(_args: argparse.Namespace) -> int:
    checks = [
        check_command("chromium", ["chromium", "chromium-browser", "google-chrome", "google-chrome-stable"]),
        check_playwright(),
        check_cached_chromium(),
        check_command("xdotool", ["xdotool"]),
        check_command("wmctrl", ["wmctrl"]),
        check_command("imagemagick import", ["import"]),
        check_command("imagemagick convert", ["convert"]),
        check_command("xclip", ["xclip"]),
    ]
    return 0 if all(checks) else 1


def command_open(args: argparse.Namespace) -> int:
    chromium = find_chromium()
    if not chromium:
        print("ERROR chromium binary not found", file=sys.stderr)
        return 1

    profile_name = sanitize_profile(args.profile)
    profile_dir = PROFILE_ROOT / profile_name
    profile_dir.mkdir(parents=True, exist_ok=True)

    command = [
        chromium,
        f"--remote-debugging-address={args.host}",
        f"--remote-debugging-port={args.port}",
        f"--user-data-dir={profile_dir}",
        "--new-window",
    ]
    if args.url:
        command.append(args.url)

    print(f"Chromium: {chromium}")
    print(f"Profile: {profile_dir}")
    print(f"Remote debugging: http://{args.host}:{args.port}")
    print("URL: provided" if args.url else "URL: about:blank/default")

    if args.dry_run:
        print("Dry run complete. Chromium was not launched.")
        return 0

    subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    print("Launched visible Chromium session.")
    return 0


def command_profiles(_args: argparse.Namespace) -> int:
    if not PROFILE_ROOT.exists():
        print(f"No profiles found under {PROFILE_ROOT}")
        return 0
    for path in sorted(item for item in PROFILE_ROOT.iterdir() if item.is_dir()):
        print(path)
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="KSI Chromium browser helper.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    check = subparsers.add_parser("check", help="Check browser automation dependencies.")
    check.set_defaults(func=command_check)

    open_parser = subparsers.add_parser("open", help="Open a visible persistent Chromium session.")
    open_parser.add_argument("--profile", default="default", help="Persistent profile name.")
    open_parser.add_argument("--url", default="about:blank", help="URL to open.")
    open_parser.add_argument("--host", default="127.0.0.1", help="Remote debugging host.")
    open_parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Remote debugging port.")
    open_parser.add_argument("--dry-run", action="store_true", help="Print session details without launching.")
    open_parser.set_defaults(func=command_open)

    profiles = subparsers.add_parser("profiles", help="List known KSI Chromium profiles.")
    profiles.set_defaults(func=command_profiles)

    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
