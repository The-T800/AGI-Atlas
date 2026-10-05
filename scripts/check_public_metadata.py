"""Reject public commits with personal identities or non-English commit messages."""

import argparse
import re
import subprocess
from pathlib import Path


def identity_error(name: str, email: str, *, committer: bool = False) -> str | None:
    if committer and (name, email) == ("GitHub", "noreply@github.com"):
        return None
    match = re.fullmatch(
        r"(?:\d+\+)?([A-Za-z0-9-]+(?:\[bot\])?)@users\.noreply\.github\.com", email
    )
    if not match or name.casefold() != match[1].casefold():
        return "Use a GitHub username with its matching GitHub noreply email."
    return None


def message_error(message: str) -> str | None:
    if not message.strip() or not message.isascii():
        return "Write the commit message in English using ASCII characters."
    return None


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True, encoding="utf-8").strip()


def check_current_identity() -> list[str]:
    errors = []
    for kind in ("AUTHOR", "COMMITTER"):
        value = git("var", f"GIT_{kind}_IDENT")
        match = re.fullmatch(r"(.+) <([^>]+)> \d+ [+-]\d+", value)
        error = (
            identity_error(match[1], match[2], committer=kind == "COMMITTER")
            if match
            else "Cannot read the effective Git identity."
        )
        if error:
            errors.append(f"{kind}: {error}")
    return errors


def check_history() -> list[str]:
    errors = []
    for sha in git("rev-list", "HEAD").splitlines():
        fields = git("show", "-s", "--format=%an%x00%ae%x00%cn%x00%ce%x00%B", sha).split("\0", 4)
        for kind, name, email in (
            ("author", fields[0], fields[1]),
            ("committer", fields[2], fields[3]),
        ):
            error = identity_error(name, email, committer=kind == "committer")
            if error:
                errors.append(f"{sha[:12]} {kind}: {error}")
        if error := message_error(fields[4]):
            errors.append(f"{sha[:12]}: {error}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--identity-only", action="store_true")
    parser.add_argument("--message", type=Path)
    args = parser.parse_args()
    if args.message:
        error = message_error(args.message.read_text(encoding="utf-8"))
        errors = [error] if error else []
    elif args.identity_only:
        errors = check_current_identity()
    else:
        errors = check_history()
    if errors:
        raise SystemExit("\n".join(errors))
    print("Public commit metadata checks passed.")


if __name__ == "__main__":
    main()
