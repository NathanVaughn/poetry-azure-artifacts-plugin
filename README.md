# TODONAME

## Development

Use the provided [devcontainer](https://containers.dev/)
or run the following for local development:

```bash
python -m pip install pipx --upgrade
pipx ensurepath
pipx install poetry
pipx install vscode-task-runner
# (Optionally) Add pre-commit plugin
poetry self add poetry-pre-commit-plugin
```
