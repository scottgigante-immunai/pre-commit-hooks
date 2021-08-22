[![Build Status](https://asottile.visualstudio.com/asottile/_apis/build/status/pre-commit.pre-commit-hooks?branchName=master)](https://asottile.visualstudio.com/asottile/_build/latest?definitionId=17&branchName=master)
[![Azure DevOps coverage](https://img.shields.io/azure-devops/coverage/asottile/asottile/17/master.svg)](https://dev.azure.com/asottile/asottile/_build/latest?definitionId=17&branchName=master)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/pre-commit/pre-commit-hooks/master.svg)](https://results.pre-commit.ci/latest/github/pre-commit/pre-commit-hooks/master)

pre-commit-hooks
================

Custom pre-commit hooks. Repo copied from https://github.com/pre-commit/pre-commit-hooks

See also: https://github.com/pre-commit/pre-commit


### Using pre-commit-hooks with pre-commit

Add this to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/scottgigante-immunai/pre-commit-hooks
    rev: v0.0
    hooks:
    -   id: check-makefile
    #   args: ['--target=all', '--target=help']
```

### Hooks available

#### `check-makefile`
Check makefile syntax
  - Replaces spaces with tabs
  - Runs `make --dry-run` to check syntax

### As a standalone package

If you'd like to use these hooks, they're also available as a standalone package.

Simply `pip install git+https://github.com/scottgigante-immunai/pre-commit-hooks`
