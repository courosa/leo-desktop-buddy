#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
BUILD_DIR="$SCRIPT_DIR/build"
APP_DIR="$BUILD_DIR/Leo Desktop Buddy.app"

mkdir -p "$APP_DIR/Contents/MacOS" "$APP_DIR/Contents/Resources"

xcrun swiftc -O -target x86_64-apple-macos12.0 -framework AppKit \
  "$SCRIPT_DIR/LeoDesktopBuddy.swift" -o "$BUILD_DIR/LeoDesktopBuddy-x86_64"
xcrun swiftc -O -target arm64-apple-macos12.0 -framework AppKit \
  "$SCRIPT_DIR/LeoDesktopBuddy.swift" -o "$BUILD_DIR/LeoDesktopBuddy-arm64"
lipo -create "$BUILD_DIR/LeoDesktopBuddy-x86_64" "$BUILD_DIR/LeoDesktopBuddy-arm64" \
  -output "$APP_DIR/Contents/MacOS/LeoDesktopBuddy"

cp "$SCRIPT_DIR/Info.plist" "$APP_DIR/Contents/Info.plist"
cp "$PROJECT_DIR/assets/sprites/leo-walk-v2.png" "$APP_DIR/Contents/Resources/"
cp "$PROJECT_DIR/assets/sprites/leo-fight.png" "$APP_DIR/Contents/Resources/"

codesign --force --deep --sign - "$APP_DIR"
ditto -c -k --sequesterRsrc --keepParent "$APP_DIR" "$BUILD_DIR/LeoDesktopBuddy-macOS.zip"
echo "$BUILD_DIR/LeoDesktopBuddy-macOS.zip"
