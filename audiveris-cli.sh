#!/bin/bash

# Resolve the location of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$SCRIPT_DIR/audiveris/app/build/distributions/app-5.6.0"

# Run Audiveris with the correct classpath
java -cp "$APP_DIR/audiveris.jar:$APP_DIR/lib/*" org.audiveris.omr.Main "$@"

