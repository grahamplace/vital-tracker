#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Chrome.
curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

# Update our system
apt-get -y update

# Install Chrome
apt-get -y install google-chrome-stable

echo "$GOOGLE_CREDENTIAL" >> "credentials.json"

poetry lock --no-update
poetry env use $PYTHON_VERSION
poetry install

