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

- Use the official OpenAlex four-level research taxonomy, preserving source IDs and lineage.
- Pin complete releases with source timestamps and SHA-256 hashes. Rebuild offline in CI.
- Refresh from the live API with an optional OPENALEX_API_KEY, or use the latest official
  public snapshot. Never describe a bulk release as current live API data.
- Keep release date, retrieval date, evaluation date and publication date separate.
- Classify benchmark task content, not the research subject of the benchmark paper.
- Link only at the supported level. Broad benchmark totals never become child-topic scores.
- Unmeasured subjects remain unknown. Do not compute AGI completion from topic counts.
- Capability annotations are independently curated project data; O*NET remains the work axis.
- Keep API keys in environment variables or ignored local files. Never store keys in source URLs.
