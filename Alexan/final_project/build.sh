#!/bin/bash

# Change to the directory of this, so it will
# work no matter where you call it from.
cd "$(dirname "$0")"

# Create the bin and build directories, if they don't exist.
mkdir -p bin
mkdir -p build
cd build

echo "Running CMake..."
cmake .. 
echo "Building..."
make -j$(nproc)  # Run multiple independent build tasks concurrently.

echo ""
echo "✅ Build complete!"
echo "Executable: bin/finalproject"