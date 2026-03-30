#!/usr/bin/env python3
"""
Test Apple's built-in System TTS for baseline benchmarking.
"""

import subprocess
import time
import os

# Test Apple System TTS
text = "Hello world, this is a test of the system text to speech engine."

# Get available voices
result = subprocess.run(
    ["say", "-v", "?"],
    capture_output=True,
    text=True
)
print("=== Available Voices ===")
for line in result.stdout.split('\n')[:10]:
    if line.strip():
        print(f"  {line}")

# Test with different voices
print("\n=== Latency Test (Apple System TTS) ===")

voices = ["Alex", "Ava", "Samantha", "Victoria"]

for voice in voices:
    try:
        # Time the command
        start = time.time()
        subprocess.run(
            ["say", "-v", voice, text],
            capture_output=True,
            timeout=10
        )
        elapsed = time.time() - start
        
        # Check if audio was created
        print(f"Voice '{voice}': {elapsed:.3f}s")
    except subprocess.TimeoutExpired:
        print(f"Voice '{voice}': Timed out")
    except Exception as e:
        print(f"Voice '{voice}': Error - {e}")

# Test with audio output to file for timing
print("\n=== File Output Test ===")
output_file = "/tmp/test_speech.wav"

start = time.time()
subprocess.run(
    ["say", "-v", "Alex", "-o", output_file, text],
    capture_output=True,
    timeout=10
)
elapsed = time.time() - start

# Check if file exists
if os.path.exists(output_file):
    file_size = os.path.getsize(output_file)
    print(f"File: {output_file}")
    print(f"Size: {file_size} bytes")
else:
    print("⚠️ File not created (may need different macOS version)")
print(f"Time: {elapsed:.3f}s")
