set dotenv-load := true

OPENSAFELY_CLI_DIR := "${REPOS_DIR}/opensafely-cli"
EHRQL_DIR := "${REPOS_DIR}/ehrql"

venv:
    test -d .venv/ || uv venv
    uv pip install setuptools
    uv pip install ruff

build-ehrql-dev-image:
    #!/usr/bin/env bash
    cd {{ EHRQL_DIR }} && set -a && source .env && set +a && just build-ehrql-for-os-cli

install-opensafely-cli:
    #!/usr/bin/env bash
    if [ ! -f .venv/.opensafely-installed ] || [ {{ OPENSAFELY_CLI_DIR }}/pyproject.toml -nt .venv/.opensafely-installed ]; then
        uv pip install -e {{ OPENSAFELY_CLI_DIR }} setuptools
        touch .venv/.opensafely-installed
    fi

opensafely *args: venv build-ehrql-dev-image install-opensafely-cli
    #!/usr/bin/env bash
    .venv/bin/opensafely {{ args }}

@nuke:
    rm -rf metadata/ && mkdir metadata
    rm -rf output/ && mkdir output
    touch output/.gitkeep

fix: venv
    .venv/bin/ruff format .
    .venv/bin/ruff check --fix .
