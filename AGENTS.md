# Project conventions

## English-first publishing

- Use English for commit messages, pull request titles and descriptions, issue templates,
  default documentation, UI defaults, CLI messages, and new code comments.
- Keep Simplified Chinese as an explicit localization (`?lang=zh`, language switch,
  `README.zh-CN.md`, and translated reports). Preserve original source material verbatim.
- A new visitor sees English regardless of browser locale. Honor an explicit language
  choice from the URL or a previously saved preference.
- Conversation language can follow the user's preference.

## Public identity

- Before committing, configure a repository-local GitHub username and the account's
  GitHub-provided `users.noreply.github.com` address for both author and committer.
- Never inherit a workstation's personal or company identity without checking it.
  Never publish personal email addresses, machine paths, credentials, or local backups.
- For this repository, use `The-T800` and `65542540+The-T800@users.noreply.github.com`.
- Enable the supplied hooks with `git config --local core.hooksPath .githooks`.
- Run `uv run python scripts/check_public_metadata.py` before pushing. Never push
  backup refs or old history containing a private identity.

## Publication

- The public repository is `The-T800/agi-atlas`; the live site is
  `https://the-t800.github.io/agi-atlas/`.
- GitHub renders README Markdown but does not execute the HTML app inside it.
  Link the README title/preview to the deployed GitHub Pages site.
- Configure Pages to use GitHub Actions, deploy `docs/`, and verify a successful
  deployment and HTTP response before reporting the live site as ready.
- Keep source provenance and both translations. Regenerate outputs through the
  documented scripts; do not edit generated datasets or `docs/index.html` by hand.
- Run lint, formatting, tests, and the generated-output checks before publishing.

## Subject reference set

- Use the pinned Nature public subject directory for the academic reference set.
- Preserve original subject IDs and cross-listings; count each subject once overall.
- Do not treat a national curriculum or an arbitrary library shelf scheme as a complete
  human knowledge taxonomy. Do not infer a hierarchy from links labelled "Related Subjects".
- Keep benchmark mappings separate from source taxonomy, with evidence and partial-coverage
  qualifications. Document denominator changes and recompute all reports and public copy.
