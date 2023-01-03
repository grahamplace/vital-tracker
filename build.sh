#!/usr/bin/env bash
# exit on error
set -o errexit

echo "$GOOGLE_CREDENTIAL" >> "credentials.json"

poetry lock --no-update
poetry env use $PYTHON_VERSION
poetry install

