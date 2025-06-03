#!/bin/bash
set -e

git submodule update --init --recursive

cd audiveris
git checkout tags/5.6.0
./gradlew build

cd ..
echo "Setup complete! You can now run ./audiveris-cli.sh"
