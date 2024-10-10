# Poetry Azure Artifacts Plugin

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![GitHub license](https://img.shields.io/github/license/NathanVaughn/poetry-azure-artifacts-plugin)](https://github.com/NathanVaughn/poetry-azure-artifacts-plugin/blob/main/LICENSE)
[![PyPi versions](https://img.shields.io/pypi/pyversions/poetry-azure-artifacts-plugin)](https://pypi.org/project/poetry-azure-artifacts-plugin)
[![PyPi downloads](https://img.shields.io/pypi/dm/poetry-azure-artifacts-plugin)](https://pypi.org/project/poetry-azure-artifacts-plugin)

---

This is a [Poetry](https://python-poetry.org/) plugin that transparently takes
care of authentication with Azure Artifacts feeds. This is heavily based on
[semgrep/poetry-codeartifact-plugin](https://github.com/semgrep/poetry-codeartifact-plugin).

## Usage

This plugin requires Python 3.9+ which is a bit less lenient than Poetry itself.

Install this plugin with

```bash
poetry self add poetry-azure-artifacts-plugin
```

or

```bash
pipx inject poetry poetry-azure-artifacts-plugin
```

In your `pyproject.toml` file, add your Azure Artifacts feed URL as a source.

```toml
[[tool.poetry.source]]
name = "ado"
url  = "https://pkgs.dev.azure.com/{organization}/_packaging/{feed}/pypi/simple/"
priority = "primary"
```

Now, when running `poetry install`, or `poetry lock`, Poetry will automatically
fetch credentials for your Azure Artifacts feed, utilizing
[artifacts-keyring](https://github.com/microsoft/artifacts-keyring).
Note: `artifacts-keyring` requires `dotnet` to be installed and available
in your PATH.

This works by recognizing authentication failures to URLs containing
`pkgs.dev.azure.com` or `pkgs.visualstudio.com`. If you have an on-premises
Azure DevOps server that works with `artifacts-keyring`, instead make the
source name include the text `azure-artifacts`:

```toml
[[tool.poetry.source]]
name = "azure-artifacts-feed"
url  = "https://devops.mydomain.com/{organization}/_packaging/{feed}/pypi/simple/"
priority = "primary"
```

## Development

Use the provided [devcontainer](https://containers.dev/)
or run the following for local development:

```bash
# Install uv
# https://docs.astral.sh/uv/getting-started/installation/
uv tool install vscode-task-runner
vtr install
```
