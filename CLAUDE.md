# CLAUDE.md

## Language & Runtime

- Python `>=3.11, <4.0` (target: 3.12)
- Package manager: **Poetry** (`poetry-core>=2.0.0`)

## Code Style

- Formatter and linter: **Ruff** (`v0.15.5`)
- Line length: **120** characters
- Indent width: **4 spaces**
- Quote style: **double quotes**
- Line endings: **auto**
- Docstring convention: **Google style**

### Enabled Ruff rule sets

`ANN`, `E`, `D`, `F`, `B`, `B9`, `C4`, `SIM`, `I`, `UP`, `PIE`, `PGH`, `PYI`, `RUF`

### Ignored rules

- `B011` — assert False is not used
- `E501` — line length is handled by the formatter, not enforced as an error

## Commit Messages

- Convention: **Conventional Commits** (`cz_conventional_commits`)
- Enforced via commitizen pre-commit hook on every commit and pre-push
- Common prefixes: `fix:`, `feat:`, `bump:`, `docs:`, `ci:`, `refactor:`
- Do **not** start commit messages with `bump:` manually — that prefix is reserved for the automated version bump CI job

## Versioning & Changelog

- Version scheme: **PEP 440**
- Version source: `pyproject.toml` (`[project].version`)
- Changelog is updated automatically by commitizen on every merge to `main`
- Tag format: `$version` (e.g. `0.5.3`)

## CI/CD

- Merges to `main` trigger an automatic version bump and changelog update via the `Bump version` GitHub Actions workflow
- The workflow uses a GitHub App token (app ID: `MERMAID_APP_ID`, key: `MERMAID_APP_TOKEN`) for authentication

## Pre-commit Hooks

Run `pre-commit install` after cloning. The following hooks run automatically:

| Hook | When |
|---|---|
| `check-yaml` | commit |
| `end-of-file-fixer` | commit |
| `trailing-whitespace` | commit |
| `ruff-check` | commit |
| `ruff-format` | commit |
| `commitizen` | commit |
| `commitizen-branch` | pre-push |

## File Encoding

Always open files with `encoding="utf-8"` explicitly.
