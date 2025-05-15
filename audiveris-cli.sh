#!/bin/bash

APP_DIR="$(pwd)/audiveris/app/build/distributions/app-5.6.0"

java -cp "$APP_DIR/audiveris.jar:$APP_DIR/lib/*" org.audiveris.omr.Main "$@"

