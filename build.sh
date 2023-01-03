#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Chrome.
sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
sudo echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

# Update our system
sudo apt-get -y update

# Install Chrome
sudo apt-get -y install google-chrome-stable

echo "$GOOGLE_CREDENTIAL" >> "credentials.json"

poetry lock --no-update
poetry env use $PYTHON_VERSION
poetry install

