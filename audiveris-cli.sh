#!/bin/bash

# Resolve the location of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIST_DIR="$SCRIPT_DIR/audiveris/app/build/distributions"
APP_DIR="$DIST_DIR/app-5.6.0"

# If app-5.6.0 directory doesn't exist, unzip or untar it
if [ ! -d "$APP_DIR" ]; then
  echo "Extracting Audiveris app-5.6.0 distribution..."

  if [ -f "$DIST_DIR/app-5.6.0.zip" ]; then
    unzip "$DIST_DIR/app-5.6.0.zip" -d "$DIST_DIR"
  elif [ -f "$DIST_DIR/app-5.6.0.tar" ]; then
    mkdir -p "$APP_DIR"
    tar -xf "$DIST_DIR/app-5.6.0.tar" -C "$APP_DIR"
  else
    echo "ERROR: Neither app-5.6.0.zip nor app-5.6.0.tar found!"
    exit 1
  fi
fi

# Run Audiveris with the correct classpath
java -cp "$APP_DIR/audiveris.jar:$APP_DIR/lib/*" org.audiveris.omr.Main "$@"
