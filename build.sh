#!/bin/bash

set -e

echo "=== Building TTS Rust Backend ==="

cd "$(dirname "$0")/rust"

# Build for macOS
echo "Building for macOS..."
cargo build --target=x86_64-apple-darwin --release
cargo build --target=aarch64-apple-darwin --release

# Create universal binary
lipo -create \
    target/x86_64-apple-darwin/release/libtts.dylib \
    target/aarch64-apple-darwin/release/libtts.dylib \
    -output libtts-universal.dylib

echo "Universal binary created: libtts-universal.dylib"

# Build for iOS
echo "Building for iOS..."
cargo build --target=aarch64-apple-ios --release

echo "iOS binary created: target/aarch64-apple-ios/release/libtts.a"

# Copy to Swift project
cp libtts-universal.dylib ../swift/iOSApp/libtts.dylib

echo "=== Build Complete ==="
